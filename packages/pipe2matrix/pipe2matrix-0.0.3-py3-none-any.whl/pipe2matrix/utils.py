import asyncio


class MessageStream(asyncio.Queue):
    def __init__(self, queue_size=100):
        super().__init__(queue_size)
        self.eof_event = asyncio.Event()

    def close(self):
        self.eof_event.set()

    def eof(self):
        return self.eof_event.is_set() and self.empty()

    async def put(self, item) -> None:
        if self.eof_event.is_set():
            raise ValueError("MessageStream is closed")
        return await super().put(item)

    def put_nowait(self, item) -> None:
        if self.eof_event.is_set():
            raise ValueError("MessageStream is closed")
        super().put_nowait(item)

    async def get(self):
        if self.eof():
            raise EOFError()
        super_get = asyncio.create_task(super().get())
        wait_eof = asyncio.create_task(self.eof_event.wait())
        try:
            await asyncio.wait([super_get, wait_eof], return_when=asyncio.FIRST_COMPLETED)
        except asyncio.CancelledError:
            super_get.cancel()
            wait_eof.cancel()
            raise
        super_get.cancel()
        if not wait_eof.done():
            wait_eof.cancel()
        # Avoid the race condition when both tasks complete simultaneously.
        # If get() has a chance at completing successfully, return the result, not EOF.
        while not super_get.done():
            try:
                await asyncio.wait([super_get])
            except asyncio.CancelledError:
                pass
        try:
            return super_get.result()
        except asyncio.CancelledError:
            raise EOFError()
