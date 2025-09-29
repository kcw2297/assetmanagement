from accounts.bithumb.config.bithumb_client import BithumbClient
from assetmanagement.core.schema import MovingAverage
from accounts.bithumb.schema import Candle


class CandleService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def get_daily_candles(self, market: str, count: int = 20) -> list[Candle]:
        try:
            params = {
                "market": market,
                "count": count
            }
            result = self.client.call_public_api("/v1/candles/days", params)

            if result['status_code'] != 200:
                print(f"❌ Candle API 에러: {result['status_code']}")
                return []

            data = result['data']

            candles = []
            for candle_data in data:
                candle = Candle(
                    market=candle_data['market'],
                    candle_date_time_kst=candle_data['candle_date_time_kst'],
                    opening_price=float(candle_data['opening_price']),
                    high_price=float(candle_data['high_price']),
                    low_price=float(candle_data['low_price']),
                    trade_price=float(candle_data['trade_price']),
                    candle_acc_trade_volume=float(candle_data['candle_acc_trade_volume']),
                    timestamp=int(candle_data['timestamp'])
                )
                candles.append(candle)

            candles.reverse()
            return candles

        except Exception as e:
            print(f"Error getting candles: {e}")
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
        
        
        