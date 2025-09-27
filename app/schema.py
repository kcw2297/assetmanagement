from pydantic import BaseModel


class Account(BaseModel):
    """계좌 정보 스키마"""
    currency: str
    balance: float


class Ticker(BaseModel):
    market: str                  # 종목 구분 코드 (예: KRW-BTC)
    trade_price: float          # 현재가
    opening_price: float        # 시가
    high_price: float          # 고가
    low_price: float           # 저가
    prev_closing_price: float  # 전일 종가
    trade_volume: float        # 거래량
    acc_trade_volume_24h: float # 24시간 누적 거래량
    change: str                # EVEN/RISE/FALL
    change_rate: float         # 변화율
    timestamp: int             # 타임스탬프