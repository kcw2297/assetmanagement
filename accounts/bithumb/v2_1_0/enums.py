from enum import StrEnum


class OrderSide(StrEnum):
    BID = "bid"  # 매수
    ASK = "ask"  # 매도
    
    
    
class OrderType(StrEnum):
    LIMIT = "limit"   # 지정가 주문
    PRICE = "price"   # 시장가 주문(매수)
    MARKET = "market" # 시장가 주문(매도)