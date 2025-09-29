from accounts.bithumb.v2_1_0.config.bithumb_client import BithumbClient
from assetmanagement.core.schema import MovingAverage
from accounts.bithumb.v2_1_0.schema import Candle
from assetmanagement.common.decorators.validators import validate_range


class CandleService:
    def __init__(self, client: BithumbClient):
        self.client = client

    @validate_range('count', min_value=1, max_value=200)
    def get_daily_candles(self, market: str, count: int = 20) -> list[Candle]:
        try:
            params = {
                "market": market,
                "count": count
            }
            result = self.client.call_public_api("/v1/candles/days", params)

            if result['status_code'] != 200:
                return []

            data = result['data']

            candles = []
            for candle_data in data:
                candle = Candle(
                    market=candle_data.get('market', ''),
                    candle_date_time_utc=candle_data.get('candle_date_time_utc', ''),
                    candle_date_time_kst=candle_data.get('candle_date_time_kst', ''),
                    opening_price=float(candle_data.get('opening_price', 0.0)),
                    high_price=float(candle_data.get('high_price', 0.0)),
                    low_price=float(candle_data.get('low_price', 0.0)),
                    trade_price=float(candle_data.get('trade_price', 0.0)),
                    timestamp=int(candle_data.get('timestamp', 0)),
                    candle_acc_trade_price=float(candle_data.get('candle_acc_trade_price', 0.0)),
                    candle_acc_trade_volume=float(candle_data.get('candle_acc_trade_volume', 0.0)),
                    prev_closing_price=float(candle_data.get('prev_closing_price', 0.0)),
                    change_price=float(candle_data.get('change_price', 0.0)),
                    change_rate=float(candle_data.get('change_rate', 0.0)),
                    converted_trade_price=float(candle_data.get('converted_trade_price')) if 'converted_trade_price' in candle_data else None
                )
                candles.append(candle)

            candles.reverse()
            return candles

        except Exception:
            return []

    def calculate_moving_averages(self, candles: list[Candle]) -> MovingAverage:
        if not candles:
            return MovingAverage()

        closing_prices = [candle.trade_price for candle in candles]

        ma5 = self._calculate_ma(closing_prices, 5)
        ma10 = self._calculate_ma(closing_prices, 10)
        ma20 = self._calculate_ma(closing_prices, 20)

        return MovingAverage(ma5=ma5, ma10=ma10, ma20=ma20)

    def _calculate_ma(self, prices: list[float], period: int) -> float:
        if len(prices) < period:
            return 0.0

        recent_prices = prices[-period:]
        return sum(recent_prices) / period

    def get_market_analysis(self, market: str) -> dict:
        candles = self.get_daily_candles(market, 20)
        if not candles:
            return {}

        ma = self.calculate_moving_averages(candles)
        current_candle = candles[-1]  # 최신 캔들

        return {
            'market': market,
            'current_price': current_candle.trade_price,
            'moving_averages': {
                'ma5': ma.ma5,
                'ma10': ma.ma10,
                'ma20': ma.ma20
            },
            'is_above_ma5': current_candle.trade_price > ma.ma5,
            'is_above_ma10': current_candle.trade_price > ma.ma10,
            'is_above_ma20': current_candle.trade_price > ma.ma20,
            'recent_high_20d': max([c.high_price for c in candles]),
            'candles_count': len(candles)
        }
        
        
        