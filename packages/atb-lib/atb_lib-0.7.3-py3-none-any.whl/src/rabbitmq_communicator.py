import asyncio
from typing import Dict, Any, Callable, Awaitable, Optional

import aio_pika

from atb_lib import ColoredLogger, RabbitMqService

_DEFAULT_TTL_MS = 5000
_DEFAULT_RECONNECT_SEC = 5


class RabbitMQCommunicator:
    def __init__(self,
                 config: Dict[str, Any],
                 logger: ColoredLogger,
                 callback: Optional[Callable[..., Awaitable[None]]] = None) -> None:

        self._logger = logger
        config = config.get('rabbitmq_consumer', {}) if callback else config.get('rabbitmq_producer', {})
        self._agent_type = 'consumer' if callback else 'producer'

        self._reconnect_interval_sec = config.get('reconnect_interval_sec', _DEFAULT_RECONNECT_SEC)

        self._rabbitmq_agent = RabbitMqService(
            config.get('url', ""),
            config.get('queue_name', ""),
            int(config.get('message_ttl_ms', _DEFAULT_TTL_MS)),
            self._logger,
            callback
        )

    async def send_message(self, message):
        await self.attempt_with_retry(lambda: self._rabbitmq_agent.send_message(message),
                                      "Send message to RabbitMQ",
                                      self._reconnect_interval_sec,
                                      lambda: self._rabbitmq_agent.connect())

    async def receive_messages(self):
        await self.attempt_with_retry(lambda: self._rabbitmq_agent.receive_messages(),
                                      "Start receiving messages from RabbitMQ",
                                      self._reconnect_interval_sec,
                                      lambda: self._rabbitmq_agent.connect())

    async def connect(self):
        await self.attempt_with_retry(lambda: self._rabbitmq_agent.connect(),
                                      f"Connect to RabbitMQ {self._agent_type}",
                                      self._reconnect_interval_sec)

    async def close(self):
        self._logger.info(f"Closing RabbitMQ {self._agent_type} ...")
        try:
            await self._rabbitmq_agent.close()
        except Exception as e:
            self._logger.error(f"Error closing resource: {e}")

    async def attempt_with_retry(self, func: Callable[[], Awaitable[None]],
                                 action_desc: str, interval_sec: int,
                                 reconnect_func: Callable[[], Awaitable[None]] = None) -> None:
        while True:
            try:
                await func()
                break
            except aio_pika.exceptions.AMQPError as e:
                # If it's a recoverable networking error, attempt to reconnect before retrying
                self._logger.error(f"Recoverable networking error during {action_desc}: {e}")
                if reconnect_func is not None:
                    await reconnect_func()
                self._logger.info(f"Attempting to retry {action_desc} in few seconds...")
                await asyncio.sleep(interval_sec)
            except Exception as e:
                # For other errors, just retry
                self._logger.error(f"Error during {action_desc}: {e}")
                self._logger.info(f"Attempting to retry {action_desc} in few seconds...")
                await asyncio.sleep(interval_sec)
