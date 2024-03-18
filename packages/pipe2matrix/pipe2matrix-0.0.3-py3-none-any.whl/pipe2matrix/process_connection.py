from typing import Optional, Union, Callable, List, Tuple, Any, Coroutine, AsyncIterator
import os
import io
import socket
import asyncio
import logging
import aiofiles
from .utils import MessageStream
from logging import Logger

if os.name == "posix":
    async def write_fully(fd: int, buf: bytes):
        total_written = 0
        while total_written < len(buf):
            try:
                actually_written = os.write(fd, buf[total_written:])
                total_written += actually_written
            except BlockingIOError:
                pass
            if total_written < len(buf):
                await asyncio.sleep(0.5)


    async def stream_from_fd(fd: int, read: bool = False, write: bool = False,
                             eof_event: Optional[asyncio.Event] = None) \
            -> Tuple[Optional[asyncio.StreamReader], Optional[asyncio.StreamWriter]]:
        """
        Create an asyncio.StreamReader and/or asyncio.StreamWriter to access a POSIX file descriptor.
        """
        os.set_blocking(fd, False)
        local, remote = socket.socketpair()
        local_reader, local_writer = await asyncio.open_connection(sock=local)
        remote_reader, remote_writer = await asyncio.open_connection(sock=remote)
        wait_for = []
        if read:
            async def reader(fd, write_stream, eof_event):
                bufsize = 3200
                buf = bytearray(bufsize)
                while True:
                    try:
                        numbytes = os.readv(fd, [buf])
                        if numbytes == 0:
                            write_stream.write_eof()
                            await write_stream.drain()
                            return
                        else:
                            write_stream.write(buf[:numbytes])
                            await write_stream.drain()
                    except BlockingIOError:
                        if eof_event is not None and eof_event.is_set():
                            write_stream.write_eof()
                            await write_stream.drain()
                            return
                        await asyncio.sleep(0.5)
            wait_for.append(asyncio.create_task(reader(fd, local_writer, eof_event)))
        if write:
            async def flush_stream(read_stream):
                while True:
                    buf = await read_stream.read(100)
                    if len(buf) == 0:
                        return

            async def writer(read_stream, fd, eof_event):
                if eof_event is not None:
                    eof_task = asyncio.create_task(eof_event.wait())
                while True:
                    ### Read data from the client code.
                    if eof_event is None:
                        buf = await read_stream.read(1)
                        if len(buf) == 0:
                            # Our user has closed their "write" stream. We are done.
                            return
                    else:
                        read_task = asyncio.create_task(read_stream.read(1))
                        done, pending = await asyncio.wait([read_task, eof_task], return_when=asyncio.FIRST_COMPLETED)
                        if read_task in done:
                            buf = read_task.result()
                            if len(buf) == 0:
                                # Our user has closed their "write" stream. We are done.
                                if not eof_task.done():
                                    eof_task.cancel()
                        else:
                            # eof_event has been set. The fd file descriptor is not valid any more, but we still want
                            # to read and discard everything in read_stream, to make sure that the code using this
                            # function does not get blocked forever trying to write into its "write" stream.
                            read_task.cancel()
                            return await flush_stream(read_stream)
                    ### Write data into the fd.
                    if eof_event is None:
                        await write_fully(fd, buf)
                    else:
                        write_task = asyncio.create_task(write_fully(fd, buf))
                        done, pending = await asyncio.wait([write_task, eof_task], return_when=asyncio.FIRST_COMPLETED)
                        if eof_task in done:
                            if not write_task.done():
                                write_task.cancel()
                            return
                        if write_task in done:
                            e = write_task.exception()
                            if e is not None:
                                if not eof_task.done():
                                    eof_task.cancel()
                                return
            wait_for.append(asyncio.create_task(writer(local_reader, fd, eof_event)))
        if wait_for:
            async def closer(wait_for, fd):
                await asyncio.wait(wait_for, return_when=asyncio.ALL_COMPLETED)
                remote_writer.close()
                os.close(fd)
            asyncio.create_task(closer(wait_for, fd))
        return (remote_reader if read else None, remote_writer if write else None)


async def read_part(queue: MessageStream, timeout: float, sep: bytes = b'\n') -> (bytes, bool):
    result = bytearray()
    try:
        while True:
            try:
                char = await asyncio.wait_for(queue.get(), timeout=timeout)
            except EOFError:
                return bytes(result), True
            result.append(char)
            if char == sep[0]:
                break
    except asyncio.TimeoutError:
        pass
    return bytes(result), False


class ChunkifyEvent(object):
    pass


class ChunkifyEOF(ChunkifyEvent):
    pass


async def chunckify(stream, timeout: float, sep: bytes, output_queue: MessageStream, stop_event: asyncio.Event):
    """Break up stream content into chunks based on a separator or a timeout, and put each chunk into a queue"""
    logger = logging.getLogger("chunkify")
    stream_queue = MessageStream(1024)

    async def reader():
        while True:
            v = await stream.read(1)
            if len(v) == 0:
                stream_queue.close()
                return
            await stream_queue.put(v[0])

    reader_task = asyncio.create_task(reader())
    while True:
        chunk, eof = await read_part(stream_queue, timeout, sep)
        if chunk != b"":
            try:
                logger.debug("Enqueueing chunk %s", chunk.decode())
            except Exception as e:
                logger.debug("Enqueueing chunk <%s>", e)
            await output_queue.put(chunk)
        elif stop_event.is_set():
            logger.debug("Simulating eof triggered by stop_event")
            await output_queue.put(ChunkifyEOF())
            output_queue.close()
            reader_task.cancel()
            return
        if eof:
            logger.debug("Stream at eof")
            await output_queue.put(ChunkifyEOF())
            output_queue.close()
            reader_task.cancel()
            return


async def run_subprocess(prog: str,
                         args: List[str],
                         pseudoterminal: bool = False) -> \
        (asyncio.StreamReader, asyncio.StreamWriter, asyncio.subprocess.Process):

    def proc_finished_event(proc):
        event = asyncio.Event()

        async def waiter():
            await proc.wait()
            event.set()

        asyncio.create_task(waiter())
        return event

    if pseudoterminal:
        try:
            import pty
        except ImportError:
            # Not a POSIX system, ignore the flag
            pseudoterminal=False
    if pseudoterminal:
        control, child = pty.openpty()
        proc = await asyncio.create_subprocess_exec(prog, *args,
                                                    stdin=child,
                                                    stdout=child,
                                                    stderr=child)
        eof_event = proc_finished_event(proc)
        streams = await stream_from_fd(control, read=True, write=True, eof_event=eof_event)
        return streams[0], streams[1], proc
    else:
        proc = await asyncio.create_subprocess_exec(prog, *args,
                                                    stdin=asyncio.subprocess.PIPE,
                                                    stdout=asyncio.subprocess.PIPE,
                                                    stderr=asyncio.subprocess.STDOUT)
        return proc.stdout, proc.stdin, proc


class BackingOffWriter(object):
    async def write(self, message: bytes):
        raise NotImplementedError()

    async def close(self):
        raise NotImplementedError()

    async def ready(self) -> bool:
        raise NotImplementedError()


class BackingOffWriterStream(BackingOffWriter):
    def __init__(self, stream: asyncio.StreamWriter):
        self._stream = stream
        self._task = None
        self._logger = logging.getLogger("BackingOffWriter")

    async def write(self, message: bytes):
        if not self._ready():
            raise AssertionError("Only call `write` after `ready` returned True.")
        self._stream.write(message)
        self._task = asyncio.create_task(self._stream.drain())

    async def close(self):
        if not self._ready():
            raise AssertionError("Only call `write` after `ready` returned True.")
        if not self._stream.is_closing():
            self._logger.debug("Closing the stream")
            if self._stream.can_write_eof():
                self._stream.write_eof()

            async def closing_task():
                await self._stream.wait_closed()
                self._logger.debug("Stream closed")
            self._task = asyncio.create_task(closing_task())

    def _ready(self) -> bool:
        return self._task is None or self._task.done()

    async def ready(self) -> bool:
        return self._ready()


class BackingOffWriterFile(BackingOffWriter):
    def __init__(self, stream):
        self._stream = stream
        self._task = None
        self._logger = logging.getLogger("BackingOffWriter")

    async def write(self, message: bytes):
        if not self._ready():
            raise AssertionError("Only call `write` after `ready` returned True.")

        async def writer():
            await self._stream.write(message)
            await self._stream.flush()
        self._task = asyncio.create_task(writer())

    async def close(self):
        if not self._ready():
            raise AssertionError("Only call `close` after `ready` returned True.")
        if not self._stream.closed:
            self._logger.debug("Closing the stream")
            self._task = asyncio.create_task(self._stream.close())

    def _ready(self) -> bool:
        return self._task is None or self._task.done()

    async def ready(self) -> bool:
        return self._ready()
