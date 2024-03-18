from abc import ABC, abstractmethod
from typing import Callable, Awaitable
import websockets
import websockets.client

from atb_lib.src.color_logger import ColoredLogger
from atb_lib.src.helpers import convert_to_scaled_integer

class ExchangeWS(ABC):

    def __init__(self,
                 url: str,
                 callback: Callable[..., Awaitable[None]],
                 logger: ColoredLogger):

        self.web_socket = None
        self._url = url
        self._callback = callback
        self._logger = logger

    async def connect(self):
        self.web_socket = await websockets.client.connect(self._url)

    async def _receive_messages(self, message: str):
        data = self._parse_message(message)
        await self._callback(data)



    @abstractmethod
    def _parse_message(self, message):
        pass

    async def run_forever(self):
        await self.connect()
        while True:
            message = await self.web_socket.recv()
            await self._receive_messages(message)

    async def close(self):
        if self.web_socket and not self.web_socket.closed:
            await self.web_socket.close()
