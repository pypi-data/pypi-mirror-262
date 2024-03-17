from atb_lib.src.exchange_binance import ExchangeBinanceWS


class ExchangeFactory:
    @staticmethod
    def create(exchange_id, market, symbol, logger, callback):
        if exchange_id.lower() == "binance":
            return ExchangeBinanceWS(market, symbol, logger, callback)
        else:
            raise ValueError(f"Unsupported exchange: '{exchange_id}'")
