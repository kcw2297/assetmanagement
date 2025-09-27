import pybithumb
from typing import Optional, Dict
from app.config import settings


class BithumbClient:
    def __init__(self):
        self.api_key = settings.BITHUMB_API_KEY
        self.secret_key = settings.BITHUMB_SECRET_KEY
        self.client = None

        if self.api_key and self.secret_key:
            self.client = pybithumb.Bithumb(self.api_key, self.secret_key)

    def get_current_price(self, coin: str) -> Optional[float]:
        try:
            price = pybithumb.get_current_price(coin)
            return float(price) if price else None
        except Exception as e:
            print(f"가격 조회 실패 {coin}: {e}")
            return None

    def get_ohlcv(self, coin: str, interval: str = "24h") -> Optional[Dict]:
        try:
            df = pybithumb.get_ohlcv(coin, interval)
            if df is not None and not df.empty:
                return df
            return None
        except Exception as e:
            print(f"OHLCV 조회 실패 {coin}: {e}")
            return None

    def get_balance(self) -> Optional[Dict]:
        if not self.client:
            print("API 키가 설정되지 않아 잔고 조회 불가")
            return None

        try:
            balances = self.client.get_balances()
            return balances
        except Exception as e:
            print(f"잔고 조회 실패: {e}")
            return None