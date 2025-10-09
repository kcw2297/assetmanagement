from pydantic import BaseModel
from datetime import date

class OHLC(BaseModel):
    high: float
    low: float
    close: float
    trade_date: date
