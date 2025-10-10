from accounts.bithumb.v2_1_0.config.bithumb_client import BithumbClient
from accounts.bithumb.v2_1_0.schema import Candle


class CandleService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def get_daily_candles(self, market: str, count: int = 20) -> list[Candle]:
        if count < 1 or count > 200:
            raise ValueError(f"count는 1 이상 200 이하여야 합니다. 현재 값: {count}")

        params = {
            "market": market,
            "count": count
        }
        result = self.client.call_public_api("/v1/candles/days", params)

        if result['status_code'] != 200:
            raise RuntimeError(f"API 호출 실패: 상태 코드 {result['status_code']}")

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


        
        