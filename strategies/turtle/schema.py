from pydantic import BaseModel, Field, computed_field
from strategies.turtle.enums import SignalAction, BuyType


class TurtlePosition(BaseModel):
    price: float = Field(..., gt=0, description="매매 가격")
    quantity: int = Field(..., gt=0, description="매매 수량")
    trade_date: str = Field(..., description="거래일시 (ISO 8601 형식)")
    unit_number: int = Field(..., ge=1, description="유닛 번호 (1=초기매수, 2~4=추격매수)")

    @computed_field
    @property
    def value(self) -> float:
        return self.price * self.quantity


class TradeSignal(BaseModel):
    action: SignalAction
    price: float = Field(default=0, gt=0)
    quantity: int = Field(default=0, ge=0)
    N: float = Field(default=0, ge=0)
    trade_date: str = Field(default="")
    reason: str = Field(default="")
    type: BuyType | None = Field(default=None)
    unit_number: int | None = Field(default=None, ge=1)


class Position(BaseModel):
    market: str
    currency: str
    total_volume: float
    avg_buy_price: float
    total_paid: float
    current_value: float
    profit_rate: float
    profit_amount: float
    last_updated: str