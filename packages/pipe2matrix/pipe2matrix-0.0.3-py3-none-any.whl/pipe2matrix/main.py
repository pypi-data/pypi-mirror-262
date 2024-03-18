import os
import sys
import argparse
import asyncio
import aiofiles
import aiohttp.client_exceptions
import time
from typing import List, Optional

import nio as matrix
import logging
from logging import Logger

from .matrix_connection import listen_to_room, TextMessageSender, MatrixConnectionError, set_user_id
from .process_connection import run_subprocess, chunckify, stream_from_fd, BackingOffWriter, BackingOffWriterFile, BackingOffWriterStream, ChunkifyEvent, ChunkifyEOF
from .utils import MessageStream


class RoomIntent(object):
    def __init__(self, target: str, create: bool, admin_ids: List[str], wait_join: bool):
        self.target = target
        self.create = create
        self.admin_ids = admin_ids
        self.wait_join = wait_join


class IOIntent(object):
    pass


class RunProgramIntent(IOIntent):
    def __init__(self, prog: str, args: List[str], pseudoterminal: bool):
        self.prog = prog
        self.args = args
        self.pseudoterminal = pseudoterminal


class StdioIntent(IOIntent):
    pass


class IntentAndContext(object):
    def __init__(self, client: matrix.AsyncClient, logger: Logger, room_intent: RoomIntent, io_intent: IOIntent):
        self.client = client
        self.logger = logger
        self.room_intent = room_intent
        self.io_intent = io_intent


class RoomContext(object):
    def __init__(self, base: IntentAndContext, matrix_writer: TextMessageSender, leave_room_when_done: bool):
        self.client = base.client
        self.logger = base.logger
        self.room_intent = base.room_intent
        self.matrix_writer = matrix_writer
        self.leave_room_when_done = leave_room_when_done


async def _state_join_room(context: IntentAndContext):
    client = context.client
    logger = context.logger

    logger.debug("Entering _state_join_room")
    room_id = context.room_intent.target

    leave_room_when_done = False
    response = await client.room_send(room_id, "me.molyboha.anton.marker", {})
    if isinstance(response, matrix.RoomSendError):
        leave_room_when_done = True
        response = await client.join(room_id)
        if isinstance(response, matrix.JoinError):
            logger.error("Error joining room: %s", response)
            return 1
        if not isinstance(response, matrix.JoinResponse):
            raise AssertionError("join() returned neither JoinResponse nor JoinError")

        response = await client.room_send(room_id, "me.molyboha.anton.marker", {})
        if isinstance(response, matrix.RoomSendError):
            logger.error("Error sending a marker event to room: %s", response)
            return await _leave_and_forget_room(client, room_id, logger)
        if not isinstance(response, matrix.RoomSendResponse):
            raise AssertionError("room_send() returned neither RoomSendResponse nor RoomSendError")
    if not isinstance(response, matrix.RoomSendResponse):
        raise AssertionError("room_send() returned neither RoomSendResponse nor RoomSendError")

    stop_event = asyncio.Event()
    matrix_queue = MessageStream(100)
    matrix_reader = asyncio.create_task(listen_to_room(client, room_id, matrix_queue, stop_event, response.event_id))
    if isinstance(context.io_intent, RunProgramIntent):
        return await _state_start_prog(context, room_id, leave_room_when_done, matrix_queue, stop_event, [matrix_reader])
    elif isinstance(context.io_intent, StdioIntent):
        return await _state_pass_stdio(context, room_id, leave_room_when_done, matrix_queue, stop_event, [matrix_reader])
    else:
        raise AssertionError("Unknown IOIntent subtype: {}".format(type(context.io_intent)))


async def _state_create_room(context: IntentAndContext):
    client = context.client
    logger = context.logger

    logger.debug("Entering _state_create_room")
    response = await client.room_create(
        visibility=matrix.RoomVisibility.private,
        name=context.room_intent.target,
        federate=True,
        invite=context.room_intent.admin_ids,
        power_level_override={"users_default": 100}
    )
    if isinstance(response, matrix.RoomCreateError):
        logger.error("Error creating room: %s", response)
        return 1
    if not isinstance(response, matrix.RoomCreateResponse):
        raise AssertionError("room_create() returned neither RoomCreateResponse nor RoomCreateError")
    room_id = response.room_id
    stop_event = asyncio.Event()
    matrix_queue = MessageStream(100)
    logger.debug("Checkpoint 1")
    matrix_reader = asyncio.create_task(listen_to_room(client, room_id, matrix_queue, stop_event))
    if context.room_intent.wait_join:
        logger.info("Waiting for an admin user to join the room.")
        admin_ids = context.room_intent.admin_ids
        goon = True
        wait_for_ids = admin_ids.copy()
        while goon:
            event = await matrix_queue.get()
            if isinstance(event, matrix.RoomMemberEvent):
                if event.membership == "join" and event.state_key in admin_ids:
                    logger.info("%s has joined!", event.state_key)
                    goon = False
                elif event.membership == "leave":
                    if event.state_key == client.user_id:
                        # I have been made to leave
                        logger.info("The bot has left the room. Quitting.")
                        await _forget_room(client, room_id, logger)
                        return await _state_cleanup([matrix_reader], [matrix_queue], stop_event, logger)
                    wait_for_ids.remove(event.state_key)
                    if len(wait_for_ids) == 0:
                        logger.info("None of the admins joined the room. Quitting.")
                        return await _state_leave_room_after_no_subprocess(client, room_id, [matrix_reader],
                                                                           [matrix_queue], stop_event, logger)
                elif event.membership == "ban":
                    if event.state_key == client.user_id:
                        logger.info("The bot has been banned from the room. Quitting.")
                        await _forget_room(client, room_id, logger)
                        return await _state_cleanup([matrix_reader], [matrix_queue], stop_event, logger)
    if isinstance(context.io_intent, RunProgramIntent):
        return await _state_start_prog(context, room_id, True, matrix_queue, stop_event, [matrix_reader])
    elif isinstance(context.io_intent, StdioIntent):
        return await _state_pass_stdio(context, room_id, True, matrix_queue, stop_event, [matrix_reader])
    else:
        raise AssertionError("Unknown IOIntent subtype: {}".format(type(context.io_intent)))


async def _queue_to_matrix(room_context: RoomContext, child_queue: MessageStream, stop_event: asyncio.Event,
                           on_stop_event, on_matrix_error, on_end_of_data, watchdog: Optional[asyncio.Event] = None):
    logger = room_context.logger
    matrix_writer = room_context.matrix_writer
    while True:
        if stop_event.is_set():
            logger.debug("_queue_to_matrix: stop_event set")
            return await on_stop_event()
        # if child_proc.returncode is not None:
        #     logger.debug("%s has finished with exit code %d", context.io_intent.prog, child_proc.returncode)
        #     return await _state_disconnect_after_subprocess_done(context.client, room_id, matrix_writer, matrix_queue,
        #                                                          child_writer, child_queue, child_tasks, stop_event,
        #                                                          logger)
        # Forward child process output to matrix room
        if child_queue.eof():
            logger.debug("_queue_to_matrix: end of data")
            return await on_end_of_data()
        matrix_writer_state = await matrix_writer.ready()
        if not isinstance(matrix_writer_state, bool):
            # We have an unrecoverable problem with the matrix server
            logger.debug("Unrecoverable matrix problem: %s", matrix_writer_state)
            return await on_matrix_error()
            # return await _state_disconnect_after_matrix_problem(matrix_queue, child_writer, child_queue, child_proc,
            #                                                     child_tasks, stop_event, logger)
        if watchdog is not None:
            if not matrix_writer_state or not child_queue.empty():
                watchdog.set()
        if matrix_writer_state and not child_queue.empty():
            msg = await child_queue.get()
            if isinstance(msg, ChunkifyEOF):
                logger.debug("_queue_to_matrix: end of data")
                return await on_end_of_data()
                # return await _state_leave_room_after_normal_run(room_context.client, room_id, matrix_writer, matrix_queue,
                #                                                 child_writer, child_queue, child_tasks, stop_event,
                #                                                 logger)
            if isinstance(msg, ChunkifyEvent):
                # Unknown event
                raise AssertionError("Unexpected ChunkifyEvent in queue: {}".format(msg))
            logger.debug("Passing message to matrix room: %s", msg.decode())
            strmsg = msg.decode()
            if len(strmsg) > 0 and strmsg[-1] == '\n':
                strmsg = strmsg[:-1]
            await matrix_writer.send(strmsg)
        else:
            await asyncio.sleep(0.1)


def stop_on_leave_room(my_user_id: str):
    async def stop_condition(msg):
        if isinstance(msg, matrix.RoomMemberEvent):
            if msg.state_key == my_user_id:
                if msg.membership in ["leave", "ban"]:
                    return True
        return False
    return stop_condition


async def _queue_to_fd(context: IntentAndContext, matrix_queue: MessageStream, child_writer: BackingOffWriter,
                       stop_condition, stop_event: asyncio.Event,
                       on_stop_condition, on_stop_event, on_eof, on_matrix_problem):
    logger = context.logger
    # Forward matrix messages to subprocess
    while True:
        if stop_event.is_set():
            return await on_stop_event()
        if matrix_queue.eof():
            return await on_eof()
        if await child_writer.ready() and not matrix_queue.empty():
            msg = await matrix_queue.get()
            if isinstance(msg, MatrixConnectionError):
                logger.debug("Matrix problem: %s", msg)
                return await on_matrix_problem()
            if await stop_condition(msg):
                return await on_stop_condition()
            if isinstance(msg, matrix.RoomMessageFormatted) or isinstance(msg, matrix.RoomMessageText):
                if msg.sender != context.client.user_id:
                    logger.debug("Passing message to subprocess: %s", msg.body)
                    await child_writer.write((msg.body + '\n').encode())
            else:
                # We ignore all event types we are not specifically handling
                pass
        else:
            await asyncio.sleep(0.1)


async def drain_queue(queue: MessageStream):
    while not queue.eof():
        if queue.empty():
            await asyncio.sleep(3)
        else:
            await queue.get()


async def _state_start_prog(context: IntentAndContext, room_id: str, leave_room_when_done: bool,
                            matrix_queue: MessageStream, stop_event: asyncio.Event, child_tasks: List[asyncio.Task]):
    # client: matrix.AsyncClient, room_id: str, pseudoterminal: bool, prog: str, args: List[str], logger: Logger
    logger = context.logger
    logger.debug("Entering _state_start_prog")
    child_tasks = child_tasks.copy()
    if isinstance(context.io_intent, RunProgramIntent):
        logger.debug("Starting %s", context.io_intent.prog)
        child_stdout, child_stdin, child_proc = await run_subprocess(
            context.io_intent.prog, context.io_intent.args, context.io_intent.pseudoterminal)
    else:
        raise ValueError("IOIntent not supported: {}".format(type(context.io_intent)))
    child_queue = MessageStream(100)
    chunkify_stop_event = asyncio.Event()
    child_reader = asyncio.create_task(chunckify(child_stdout, 5, b'\n', child_queue, chunkify_stop_event))
    child_tasks.append(child_reader)
    matrix_writer = TextMessageSender(context.client, room_id)
    child_writer = BackingOffWriterStream(child_stdin)

    room_context = RoomContext(context, matrix_writer, leave_room_when_done)
    queue_to_matrix_stop_event = asyncio.Event()
    queue_to_fd_stop_event = asyncio.Event()
    watchdog_event = asyncio.Event()
    last_event_id = []

    async def wait_for_subprocess_to_finish():
        await child_proc.wait()
        chunkify_stop_event.set()
        queue_to_fd_stop_event.set()

    async def watchdog_run():
        watch_timeout = 30
        watchdog_event.clear()
        last_timestamp = time.monotonic()
        while True:
            if watchdog_event.is_set():
                watchdog_event.clear()
                last_timestamp = time.monotonic()
            if child_proc.returncode is not None:
                return
            if time.monotonic() > last_timestamp + watch_timeout:
                child_proc.kill()
                try:
                    await asyncio.wait_for(child_proc.wait(), watch_timeout)
                except TimeoutError:
                    child_proc.terminate()
                return
            await asyncio.sleep(5)

    async def on_queue_to_matrix_stop_event():
        # I don't expect these to happen...
        logger.error("Unexpected call to on_queue_to_matrix_stop_event")

    async def on_matrix_write_error():
        # Could be called if, for example, our bot was forced to leave the room.
        # Assume that we are unable to send any messages anymore.
        await drain_queue(child_queue)

    async def send_last_message() -> bool:
        while True:
            status = await matrix_writer.ready()
            if not isinstance(status, bool):
                # Error. Nothing left to wait for.
                return False
            if status:
                # Successfully sent everything.
                return True
            await asyncio.sleep(1)

    async def on_end_of_data():
        status = await send_last_message()
        # if not status:
        #     return await on_matrix_write_error()
        # Wait, what if we are not actually done? What if the subprocess has finished its output, but is still
        # waiting for input?

    async def queue_to_fd_stop_condition(msg):
        if msg.event_id in last_event_id:
            return True
        if isinstance(msg, matrix.RoomMemberEvent):
            if msg.state_key == context.client.user_id:
                if msg.membership in ["leave", "ban"]:
                    return True
        return False

    async def on_queue_to_fd_stop():
        watchdog_task = asyncio.Task(watchdog_run())
        # Stop matrix_reader
        stop_event.set()
        drain_task = asyncio.Task(drain_queue(matrix_queue))
        # Close child_writer.
        while not await child_writer.ready() and child_proc.returncode is None:
            await asyncio.sleep(1)
        await child_writer.close()
        while not await child_writer.ready() and child_proc.returncode is None:
            await asyncio.sleep(1)
        # Drain matrix_queue
        await asyncio.wait_for(watchdog_task, None)
        await asyncio.wait_for(drain_task, None)

    async def on_queue_to_fd_stop_condition():
        return await on_queue_to_fd_stop()

    async def on_queue_to_fd_stop_event():
        return await on_queue_to_fd_stop()

    async def on_queue_to_fd_eof():
        return await on_queue_to_fd_stop()

    async def on_matrix_read_error():
        return await on_queue_to_fd_stop()

    child_tasks.append(asyncio.Task(wait_for_subprocess_to_finish()))
    tasks = [
        asyncio.Task(_queue_to_matrix(
            room_context, child_queue,
            queue_to_matrix_stop_event,
            on_queue_to_matrix_stop_event, on_matrix_write_error, on_end_of_data, watchdog_event)),
        asyncio.Task(_queue_to_fd(
            context, matrix_queue, child_writer,
            queue_to_fd_stop_condition, queue_to_fd_stop_event,
            on_queue_to_fd_stop_condition, on_queue_to_fd_stop_event, on_queue_to_fd_eof, on_matrix_read_error))
    ]
    for task in tasks:
        await asyncio.wait_for(task, None)

    # Clean-up
    if room_context.leave_room_when_done:
        response = await _infinite_retry(context.client.room_leave, room_id)
        if not isinstance(response, matrix.RoomLeaveResponse) and not isinstance(response, matrix.RoomLeaveError):
            raise AssertionError("room_leave() returned neither RoomLeaveResponse nor RoomLeaveError")
        if isinstance(response, matrix.RoomLeaveError):
            logger.warning("Error sending the RoomLeave event to room: %s", response)
        response = await _infinite_retry(context.client.room_forget, room_id)
        if not isinstance(response, matrix.RoomForgetResponse) and not isinstance(response, matrix.RoomForgetError):
            raise AssertionError("room_forget() returned neither RoomForgetResponse nor RoomForgetError")
        if isinstance(response, matrix.RoomForgetError):
            logger.warning("Error sending the RoomForget event to room: %s", response)
    # else:
    #     response = await _infinite_retry(context.client.room_send, room_id, "me.molyboha.anton.marker", {})
    #     if isinstance(response, matrix.RoomSendError):
    #         logger.warning("Error sending a marker event to room: %s", response)
    #     elif not isinstance(response, matrix.RoomSendResponse):
    #         raise AssertionError("room_send() returned neither RoomSendResponse nor RoomSendError")
    #     last_event_id.append(response.event_id)

    for task in child_tasks:
        await asyncio.wait_for(task, None)


async def _state_pass_stdio(context: IntentAndContext, room_id: str, leave_room_when_done: bool,
                            matrix_queue: MessageStream, stop_event: asyncio.Event, child_tasks: List[asyncio.Task]):
    # client: matrix.AsyncClient, room_id: str, pseudoterminal: bool, prog: str, args: List[str], logger: Logger
    logger = context.logger
    logger.debug("Entering _state_start_prog")
    child_tasks = child_tasks.copy()
    if isinstance(context.io_intent, StdioIntent):
        logger.debug("Passing stdin/stdout")
    else:
        raise ValueError("IOIntent not supported: {}".format(type(context.io_intent)))
    child_queue = MessageStream(100)
    chunkify_stop_event = asyncio.Event()
    child_reader = asyncio.create_task(chunckify(aiofiles.stdin_bytes, 5, b'\n', child_queue, chunkify_stop_event))
    child_tasks.append(child_reader)
    matrix_writer = TextMessageSender(context.client, room_id)
    child_writer = BackingOffWriterFile(aiofiles.stdout_bytes)

    room_context = RoomContext(context, matrix_writer, leave_room_when_done)
    queue_to_matrix_stop_event = asyncio.Event()
    queue_to_fd_stop_event = asyncio.Event()
    watchdog_event = asyncio.Event()
    last_event_id = []

    async def on_queue_to_matrix_stop_event():
        # I don't expect these to happen...
        logger.error("Unexpected call to on_queue_to_matrix_stop_event")

    async def on_matrix_write_error():
        logger.debug("matrix write error")
        # Could be called if, for example, our bot was forced to leave the room.
        # Assume that we are unable to send any messages anymore.
        await drain_queue(child_queue)

    async def send_last_message() -> bool:
        while True:
            status = await matrix_writer.ready()
            if not isinstance(status, bool):
                # Error. Nothing left to wait for.
                return False
            if status:
                # Successfully sent everything.
                return True
            await asyncio.sleep(1)

    async def on_end_of_data():
        logger.debug("end of data")
        # Our input stream was closed.
        # A "traditional" response is to finish sending whatever data we already have, but not accept any new messages.
        status = await send_last_message()
        if not status:
            # We probably have left the room.
            # TODO: but what if not?
            return
        response = await _infinite_retry(context.client.room_send, room_id, "me.molyboha.anton.marker", {})
        if isinstance(response, matrix.RoomSendError):
            # We probably have left the room.
            # TODO: but what if not?
            return
        last_event_id.append(response.event_id)
        # TODO: consider other ways to react. For example:
        #  * wait for stdout to close
        #  * wait for the bot to leave the room (be kicked, leave from another client)
        #  * out-of-band commands

    async def queue_to_fd_stop_condition(msg):
        if msg.event_id in last_event_id:
            return True
        if isinstance(msg, matrix.RoomMemberEvent):
            if msg.state_key == context.client.user_id:
                if msg.membership in ["leave", "ban"]:
                    return True
        return False

    async def on_queue_to_fd_stop():
        logger.debug("Stopping queue -> fd task")
        # Stop matrix_reader
        stop_event.set()
        drain_task = asyncio.Task(drain_queue(matrix_queue))
        # Close child_writer.
        timeout = 60
        start_timestamp = time.monotonic()
        while not await child_writer.ready() and time.monotonic() <= start_timestamp + timeout:
            await asyncio.sleep(1)
        if await child_writer.ready():
            await child_writer.close()
            start_timestamp = time.monotonic()
            while not await child_writer.ready() and time.monotonic() <= start_timestamp + timeout:
                await asyncio.sleep(1)
        # Drain matrix_queue
        await asyncio.wait_for(drain_task, None)

    async def on_queue_to_fd_stop_condition():
        return await on_queue_to_fd_stop()

    async def on_queue_to_fd_stop_event():
        return await on_queue_to_fd_stop()

    async def on_queue_to_fd_eof():
        return await on_queue_to_fd_stop()

    async def on_matrix_read_error():
        return await on_queue_to_fd_stop()

    tasks = [
        asyncio.Task(_queue_to_matrix(
            room_context, child_queue,
            queue_to_matrix_stop_event,
            on_queue_to_matrix_stop_event, on_matrix_write_error, on_end_of_data, watchdog_event)),
        asyncio.Task(_queue_to_fd(
            context, matrix_queue, child_writer,
            queue_to_fd_stop_condition, queue_to_fd_stop_event,
            on_queue_to_fd_stop_condition, on_queue_to_fd_stop_event, on_queue_to_fd_eof, on_matrix_read_error))
    ]
    for task in tasks:
        await asyncio.wait_for(task, None)

    # Clean-up
    if room_context.leave_room_when_done:
        response = await _infinite_retry(context.client.room_leave, room_id)
        if not isinstance(response, matrix.RoomLeaveResponse) and not isinstance(response, matrix.RoomLeaveError):
            raise AssertionError("room_leave() returned neither RoomLeaveResponse nor RoomLeaveError")
        if isinstance(response, matrix.RoomLeaveError):
            logger.warning("Error sending the RoomLeave event to room: %s", response)
        response = await _infinite_retry(context.client.room_forget, room_id)
        if not isinstance(response, matrix.RoomForgetResponse) and not isinstance(response, matrix.RoomForgetError):
            raise AssertionError("room_forget() returned neither RoomForgetResponse nor RoomForgetError")
        if isinstance(response, matrix.RoomForgetError):
            logger.warning("Error sending the RoomForget event to room: %s", response)
    # else:
    #     response = await _infinite_retry(context.client.room_send, room_id, "me.molyboha.anton.marker", {})
    #     if isinstance(response, matrix.RoomSendError):
    #         logger.warning("Error sending a marker event to room: %s", response)
    #     elif not isinstance(response, matrix.RoomSendResponse):
    #         raise AssertionError("room_send() returned neither RoomSendResponse nor RoomSendError")
    #     last_event_id.append(response.event_id)

    for task in child_tasks:
        await asyncio.wait_for(task, None)


async def _infinite_retry(func, *args, **kwargs):
    while True:
        sleep_delay = 5
        try:
            response = await func(*args, **kwargs)
            if isinstance(response, matrix.ErrorResponse) and response.retry_after_ms is not None:
                sleep_delay = response.retry_after_ms / 1000.0
            else:
                return response
        except (aiohttp.client_exceptions.ClientConnectionError, TimeoutError, asyncio.TimeoutError):
            await asyncio.sleep(sleep_delay)


async def _forget_room(client: matrix.AsyncClient, room_id: str, logger: Logger):
    response = await _infinite_retry(client.room_forget, room_id)
    if isinstance(response, matrix.RoomForgetError):
        logger.warning("Failed to forget the room: %s", response)


async def _leave_and_forget_room(client: matrix.AsyncClient, room_id: str, logger: Logger):
    response = await _infinite_retry(client.room_leave, room_id)
    if isinstance(response, matrix.RoomLeaveResponse):
        return await _forget_room(client, room_id, logger)
    else:
        # If the response is an error, we should move on and try to forget the room.
        logger.warning("Failed to leave the room: %s", response)
        return await _forget_room(client, room_id, logger)


async def _state_leave_room_after_no_subprocess(client: matrix.AsyncClient, room_id: str,
                                                child_tasks: List[asyncio.Task], task_queues: List[asyncio.Queue],
                                                stop_event: asyncio.Event, logger: Logger):
    logger.debug("Entering _state_leave_room_after_no_subprocess")
    await _leave_and_forget_room(client, room_id, logger)
    return await _state_cleanup(child_tasks, task_queues, stop_event, logger)


async def _state_cleanup(child_tasks: List[asyncio.Task], task_queues: List[asyncio.Queue], stop_event: asyncio.Event,
                         logger: Logger):
    logger.debug("Entering _state_cleanup")
    stop_event.set()
    goon = True
    while goon:
        need_sleep = True
        for queue in task_queues:
            if not queue.empty():
                await queue.get()
                need_sleep = False
        if need_sleep:
            await asyncio.sleep(1)
        goon = False
        for task in child_tasks:
            if not task.done():
                goon = True
    return 0


async def main(homeserver: str, auth_token: str, admin_ids: List[str],
               room_name: str, room_id: str, wait_join: bool, pseudoterminal: bool, prog: str, args: List[str]):
    client = matrix.AsyncClient(homeserver)
    client.access_token = auth_token
    if not await set_user_id(client):
        return 1
    logger = logging.getLogger("Main loop")
    logger.setLevel("DEBUG")
    if room_id is None:
        room_intent = RoomIntent(room_name, True, admin_ids, wait_join)
    else:
        room_intent = RoomIntent(room_id, False, [], False)
    if prog == "-":
        context = IntentAndContext(client, logger, room_intent, StdioIntent())
    else:
        context = IntentAndContext(client, logger, room_intent, RunProgramIntent(prog, args, pseudoterminal))
    if room_intent.create:
        res = await _state_create_room(context)
    else:
        res = await _state_join_room(context)
    await client.close()
    return res


def entry_point():
    # TODO: accept parameters from a config file.
    # TODO: when no program name is given, redirect our own stdin/stdout.
    # TODO: a special program argument --login to login and generate auth_token.
    parser = argparse.ArgumentParser(description="Redirect a program input/output into a Matrix room.",
                                     fromfile_prefix_chars="^")
    parser.add_argument("--homeserver", required=True)
    parser.add_argument("--auth_token", required=True)
    parser.add_argument("--admin_id", nargs="+")
    parser.add_argument("--room_name")
    parser.add_argument("--room_id")
    parser.add_argument("--wait", action="store_true")
    parser.add_argument("--pty", action="store_true")
    parser.add_argument("--log", help="The name of the log file.")
    parser.add_argument("prog")
    parser.add_argument("args", nargs="*")
    args = parser.parse_args()

    if args.log is not None:
        logging.basicConfig(filename=args.log)
    else:
        logging.basicConfig(stream=sys.stderr)
    logging.getLogger().debug("Logging started")

    asyncio.run(main(
        homeserver=args.homeserver,
        auth_token=args.auth_token,
        admin_ids=args.admin_id,
        room_name=args.room_name,
        room_id=args.room_id,
        wait_join=args.wait,
        pseudoterminal=args.pty,
        prog=args.prog,
        args=args.args
    ))
