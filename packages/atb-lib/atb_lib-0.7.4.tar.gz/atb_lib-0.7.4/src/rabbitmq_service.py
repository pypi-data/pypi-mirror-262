from typing import Callable, Awaitable, Optional

import aio_pika

from atb_lib.src.color_logger import ColoredLogger


class RabbitMqService:
    def __init__(self,
                 rabbitmq_url: str,
                 queue_name: str,
                 message_ttl_ms: int,
                 logger: ColoredLogger,
                 callback: Optional[Callable[..., Awaitable[None]]] = None,
                 ):

        self._logger = logger
        self._rabbitmq_url = rabbitmq_url
        self._queue_name = queue_name
        self._message_ttl_ms = message_ttl_ms
        self._connection = None
        self._channel = None
        self._queue = None
        self._callback = callback
        self._logger.debug("RabbitMqService initialized.")

    async def connect(self):
        self._connection = await aio_pika.connect_robust(self._rabbitmq_url)
        self._channel = await self._connection.channel()
        queue_args = {'x-message-ttl': self._message_ttl_ms}
        self._queue = await self._channel.declare_queue(self._queue_name,
                                                        durable=False,
                                                        arguments=queue_args)

    async def _process_message(self, message):
        try:
            await self._callback(message.body)
            await message.ack()
        except Exception as e:
            self._logger.error(f"Error processing message: {e} from {self._queue_name}")
            await message.nack(requeue=True)

    async def receive_messages(self):
        async for message in self._queue:
            await self._process_message(message)  # use the new method

    async def send_message(self, message):
        if not self._channel or self._channel.is_closed:
            raise Exception("RabbitMQ channel is not open. Call connect() first.")
        await self._channel.default_exchange.publish(
            aio_pika.Message(body=message, delivery_mode=aio_pika.DeliveryMode.NOT_PERSISTENT),
            routing_key=self._queue_name,
        )

    async def close(self):
        if self._channel and not self._channel.is_closed:
            await self._channel.close()
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
