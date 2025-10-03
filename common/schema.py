from pydantic import BaseModel


class OHLC(BaseModel):
    high: float
    low: float
    close: float
