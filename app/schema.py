from pydantic import BaseModel

class Account(BaseModel):
    currency: str
    balance: float