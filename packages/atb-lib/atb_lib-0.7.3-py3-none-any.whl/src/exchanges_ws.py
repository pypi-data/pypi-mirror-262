import asyncio

from atb_lib import ExchangeFactory


class Exchanges:
    def __init__(self, config: dict, logger, callback):

        self._config = config
        self._logger = logger
        self._callback = callback
        self._ws_connections = {}
        self._reconnect_interval_sec = None

        for exchange_config in config.get('exchanges'):

            exchange_id = exchange_config.get('exchange_id')
            market = exchange_config.get('market')

            self._reconnect_interval_sec = exchange_config.get('reconnect_interval_sec')

            for symbol in exchange_config.get('symbols'):
                ws_key = (exchange_id, market, symbol)
                self._ws_connections[ws_key] = ExchangeFactory.create(
                    exchange_id, market, symbol, self._callback, self._logger)

    async def start_exchange_listening(self):
        self._logger.info("Starting exchange listeners...")
        while True:
            try:
                tasks = [conn.run_forever()
                         for conn in self._ws_connections.values()
                         if ((not conn.web_socket) or (conn.web_socket and not conn.web_socket.closed))]
                await asyncio.gather(*tasks)

            except Exception as e:
                self._logger.error(f"Error starting exchange listeners: {e}")
                self._logger.info("Attempting to reconnect in a few seconds...")
                await asyncio.sleep(self._reconnect_interval_sec)

    @property
    def ws_connections(self):
        return self._ws_connections
