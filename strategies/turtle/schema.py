from pydantic import BaseModel, Field, computed_field


class TurtlePosition(BaseModel):
    price: float = Field(..., gt=0, description="매수 가격")
    quantity: int = Field(..., gt=0, description="매수 수량")
    N: float = Field(..., gt=0, description="매수 시점의 ATR(N) 값")
    trade_date: str = Field(..., description="거래일시 (ISO 8601 형식)")
    unit_number: int = Field(..., ge=1, description="유닛 번호 (1=초기매수, 2~4=추격매수)")

    @computed_field
    @property
    def value(self) -> float:
        return self.price * self.quantity


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