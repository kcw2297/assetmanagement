from pydantic import BaseModel
from app.enums import SignalType


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


class Candle(BaseModel):
    market: str                    # 종목 구분 코드
    candle_date_time_kst: str     # KST 기준 캔들 시간
    opening_price: float          # 시가
    high_price: float             # 고가
    low_price: float              # 저가
    trade_price: float            # 종가
    candle_acc_trade_volume: float # 누적 거래량
    timestamp: int                # 타임스탬프


class MovingAverage(BaseModel):
    ma5: float = 0.0    # 5일 이동평균
    ma10: float = 0.0   # 10일 이동평균
    ma20: float = 0.0   # 20일 이동평균


class TurtleSignal(BaseModel):
    market: str
    signal_type: SignalType  # BUY, SELL, PYRAMID, HOLD
    reason: str              # 신호 발생 이유
    current_price: float
    target_amount: float = 0.0  # 거래 금액
    confidence: float = 0.0     # 신호 신뢰도 (0-1)