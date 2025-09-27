from pydantic import BaseModel
from decimal import Decimal


class Account(BaseModel):
    """계좌 정보 스키마"""
    currency: str
    balance: Decimal
    locked: Decimal = Decimal('0')
    avg_buy_price: Decimal = Decimal('0')
    unit_currency: str = 'KRW'

    @property
    def available(self) -> Decimal:
        """사용 가능 잔액"""
        return self.balance - self.locked