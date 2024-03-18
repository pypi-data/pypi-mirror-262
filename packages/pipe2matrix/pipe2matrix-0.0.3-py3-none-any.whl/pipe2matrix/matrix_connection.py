from typing import Union, Optional
import asyncio
import aiohttp.client_exceptions
import nio as matrix
import logging
from logging import Logger
from .utils import MessageStream


class MatrixConnectionError(Exception):
    pass


class MatrixConnectionErrorResponse(MatrixConnectionError):
    def __init__(self, response: matrix.responses.ErrorResponse):
        self.response = response


class MatrixConnectionErrorNotInRoom(MatrixConnectionError):
    pass


class MatrixConnection(object):
    """
    Gets all events from a matrix room, and puts them in a queue, until asked to stop.
    """


async def _get_all_previous_events(client: matrix.AsyncClient, room_id: str, initial_sync: matrix.SyncResponse,
                                   output_queue: asyncio.Queue, stop_event: asyncio.Event, since_event: str):
    max_retries = 10
    message_stack = []
    if room_id in initial_sync.rooms.join:
        sync_marker = initial_sync.rooms.join[room_id].timeline.prev_batch
    elif room_id in initial_sync.rooms.leave:
        sync_marker = initial_sync.rooms.leave[room_id].timeline.prev_batch
    else:
        await output_queue.put(MatrixConnectionErrorNotInRoom())
        return False
    retry_counter = 0
    goon = True
    while goon:
        if stop_event.is_set():
            return False
        messages = await client.room_messages(room_id, sync_marker, direction=matrix.MessageDirection.back)
        if isinstance(messages, matrix.RoomMessagesError):
            retry_counter += 1
            if retry_counter >= max_retries:
                await output_queue.put(MatrixConnectionErrorResponse(messages))
                return False
            await asyncio.sleep(1)
            continue
        if not isinstance(messages, matrix.RoomMessagesResponse):
            raise AssertionError("Result of AsyncClient.room_messages is neither RoomMessagesResponse nor RoomMessagesError")
        retry_counter = 0
        for event in messages.chunk:
            message_stack.append(event)
            if since_event is not None and event.event_id == since_event:
                goon = False
                break
        if messages.end is None:
            goon = False
        else:
            sync_marker = messages.end
    for event in message_stack[::-1]:
        await output_queue.put(event)
    return True


def _sync_contains_event(room_id: str, initial_sync: matrix.SyncResponse, event_id: str):
    if room_id in initial_sync.rooms.join:
        timeline = initial_sync.rooms.join[room_id].timeline
    elif room_id in initial_sync.rooms.leave:
        timeline = initial_sync.rooms.leave[room_id].timeline
    else:
        return False
    for event in timeline.events:
        if event.event_id == event_id:
            return True
    return False


async def _process_sync_events(client: matrix.AsyncClient, room_id: str, initial_sync: matrix.SyncResponse,
                               output_queue: asyncio.Queue, stop_event: asyncio.Event, since_event: str):
    if room_id in initial_sync.rooms.join:
        timeline = initial_sync.rooms.join[room_id].timeline
    elif room_id in initial_sync.rooms.leave:
        timeline = initial_sync.rooms.leave[room_id].timeline
    else:
        await output_queue.put(MatrixConnectionErrorNotInRoom())
        return False
    if stop_event.is_set():
        return False
    enabled = (since_event is None)
    for event in timeline.events:
        if event.event_id == since_event:
            enabled = True
        if enabled:
            await output_queue.put(event)
    if stop_event.is_set():
        return False
    return True


async def _listen_to_future_events(client: matrix.AsyncClient, room_id: str, initial_sync: matrix.SyncResponse,
                                   output_queue: asyncio.Queue, stop_event: asyncio.Event, logger: Logger):
    max_retries = 10
    if room_id in initial_sync.rooms.join:
        sync_marker = initial_sync.rooms.join[room_id].timeline.prev_batch
    elif room_id in initial_sync.rooms.leave:
        sync_marker = initial_sync.rooms.leave[room_id].timeline.prev_batch
    else:
        await output_queue.put(MatrixConnectionErrorNotInRoom())
        return False
    sync_marker = initial_sync.next_batch
    retry_counter = 0
    while True:
        if stop_event.is_set():
            return False
        logger.debug("Calling sync")
        response = await client.sync(timeout=1000, full_state=False, since=sync_marker)
        if isinstance(response, matrix.SyncError):
            logger.debug("Sync error")
            retry_counter += 1
            if retry_counter >= max_retries:
                await output_queue.put(MatrixConnectionErrorResponse(response))
                return False
            await asyncio.sleep(1)
            continue
        if not isinstance(response, matrix.SyncResponse):
            logger.debug("Result of AsyncClient.sync is neither SyncResponse nor SyncError: %s", response)
            raise AssertionError("Result of AsyncClient.sync is neither SyncResponse nor SyncError")
        logger.debug("Sync successful")
        retry_counter = 0
        if room_id in response.rooms.join:
            timeline = response.rooms.join[room_id].timeline
        elif room_id in response.rooms.leave:
            timeline = response.rooms.leave[room_id].timeline
        else:
            # No new events in my room.
            continue
        for event in timeline.events:
            await output_queue.put(event)
        sync_marker = response.next_batch


async def listen_to_room(client: matrix.AsyncClient, room_id: str, output_queue: MessageStream,
                         stop_event: asyncio.Event, since_event: Optional[str] = None):
    """
    Gets all events from a matrix room, and puts them in a queue, until asked to stop.
    """
    logger = logging.getLogger("listen_to_room")
    initial_sync_result = await client.sync(full_state=True)
    if isinstance(initial_sync_result, matrix.SyncError):
        await output_queue.put(MatrixConnectionErrorResponse(initial_sync_result))
        output_queue.close()
        return
    if not isinstance(initial_sync_result, matrix.SyncResponse):
        raise AssertionError("Result of AsyncClient.sync is neither SyncError nor SyncResponse.")
    if stop_event.is_set():
        output_queue.close()
        return
    if since_event is None or not _sync_contains_event(room_id, initial_sync_result, since_event):
        logger.debug("Getting all previous events")
        if not await _get_all_previous_events(client, room_id, initial_sync_result, output_queue, stop_event, since_event):
            output_queue.close()
            return
        since_event = None
    logger.debug("Processing events from the current SyncResponse")
    if not await _process_sync_events(client, room_id, initial_sync_result, output_queue, stop_event, since_event):
        output_queue.close()
        return
    logger.debug("Starting the loop to forward all future events")
    await _listen_to_future_events(client, room_id, initial_sync_result, output_queue, stop_event, logger)
    logger.debug("Exiting")
    output_queue.close()


class TextMessageSender(object):
    def __init__(self, client: matrix.AsyncClient, room_id: str):
        self._client = client
        self._room_id = room_id
        self._message = None
        self._status = None

    async def _try_send(self, message: str) -> Union[bool, matrix.RoomSendError]:
        try:
            response = await self._client.room_send(self._room_id, "m.room.message", {"msgtype": "m.text", "body": message})
            if isinstance(response, matrix.RoomSendError):
                return response
            return True
        except (aiohttp.client_exceptions.ClientConnectionError, TimeoutError, asyncio.TimeoutError):
            return False

    async def send(self, message: str):
        if self._status is not None or self._message is not None:
            raise AssertionError("Don't call send() if ready() returned False.")
        response = await self._try_send(message)
        if isinstance(response, matrix.RoomSendError):
            self._status = response
        elif response == False:
            # Back off and retry.
            self._message = message

    async def ready(self) -> Union[bool, matrix.RoomSendError]:
        """
        Is this TextMessageSender ready to start sending the next message?
        Check that the previous message has been sent; if appropriate, retry sending it; if sending the message failed,
        return the error.

        :return: True if the next message can be sent, False if we are still trying to send the previous message,
                 an instance of RoomSendError if the server has returned an error, and we believe the error is fatal and
                 are not going to try sending messages anymore.
        """
        if self._status is not None:
            return self._status
        if self._message is not None:
            # TODO: implement a back-off timeout, don't just retry as-fast-as-we-can.
            response = await self._try_send(self._message)
            if isinstance(response, matrix.RoomSendError):
                self._status = response
            elif response == True:
                self._message = None
        if self._status is not None:
            return self._status
        return self._message is None


async def set_user_id(client: matrix.AsyncClient) -> bool:
    logger = logging.getLogger("set_user_id")
    response = await client.whoami()
    if isinstance(response, matrix.WhoamiResponse):
        client.user_id = response.user_id
        logger.info("My user id is \"%s\"", client.user_id)
        return True
    else:
        logger.error("Could not get my user id: %s", response)
        return False
