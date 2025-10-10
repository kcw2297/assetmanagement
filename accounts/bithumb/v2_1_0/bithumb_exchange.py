from datetime import datetime

from interfaces.exchange import ExchangeInterface
from accounts.bithumb.v2_1_0.api import BithumbAPI
from common.schema import OHLC
from accounts.bithumb.v2_1_0.constants import ACCOUNT_BASE_CURRENCY

class BithumbExchange(ExchangeInterface):
    def __init__(self, api: BithumbAPI):
        self.api = api

    def candles(self, market: str, count: int) -> list[OHLC]:
        candles = self.api.candle.get_daily_candles(market, count=count)

        ohlcs = [
            OHLC(
                high=candle.high_price,
                low=candle.low_price,
                close=candle.trade_price,
                trade_date=datetime.fromisoformat(candle.candle_date_time_kst).date()
            )
            for candle in candles
        ]

        return ohlcs

    def current_price(self, market: str) -> float:
        tickers = self.api.ticker.get_ticker(market)
        if not tickers or len(tickers) == 0:
            raise ValueError(f"{market}의 현재가를 조회할 수 없습니다.")
        return tickers[0].trade_price

    def buy(self, market: str, amount: float):
        return self.api.order.execute_market_buy_order(market, amount)

    def sell(self, market: str, volume: float):
        return self.api.order.execute_market_sell_order(market, volume)

    def balance(self, currency: str = ACCOUNT_BASE_CURRENCY) -> float:
        """잔고 조회 - 'KRW', 'BTC' 가능"""
        accounts = self.api.account.get_accounts()
        for account in accounts:
            if account.currency == currency:
                return account.balance
        return 0.0
