from pydantic import BaseModel, Field
from strategies.turtle.enums import SignalType


class TurtleSignal(BaseModel):
    signal_type: SignalType = Field(description="BUY, SELL, PYRAMID, HOLD")
    reason: str = Field(description="신호 발생 이유")
    current_price: float = Field(description="현재가")
    target_amount: float = Field(default=0.0 , description="거래 금액")
 

class Position(BaseModel):
    market: str
    currency: str
    total_volume: float  # 총 보유량
    avg_buy_price: float  # 평균매수가
    total_paid: float    # 총 투입금액
    current_value: float # 현재 평가금액
    profit_rate: float   # 수익률 (%)
    profit_amount: float # 수익금액
    last_updated: str    # 마지막 업데이트 시간