from pydantic import BaseModel
from assetmanagement.strategies.turtle.enums import SignalType


class TurtleSignal(BaseModel):
    market: str
    signal_type: SignalType  # BUY, SELL, PYRAMID, HOLD
    reason: str              # 신호 발생 이유
    current_price: float
    target_amount: float = 0.0  # 거래 금액
    confidence: float = 0.0     # 신호 신뢰도 (0-1)


class Position(BaseModel):
    """특정 종목의 포지션 정보"""
    market: str
    currency: str
    total_volume: float  # 총 보유량
    avg_buy_price: float  # 평균매수가
    total_paid: float    # 총 투입금액
    current_value: float # 현재 평가금액
    profit_rate: float   # 수익률 (%)
    profit_amount: float # 수익금액
    last_updated: str    # 마지막 업데이트 시간