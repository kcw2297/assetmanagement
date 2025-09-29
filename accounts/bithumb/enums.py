from enum import StrEnum



class AccountCurrency(StrEnum):
    KRW = "KRW"    # 원화
    BTC = "BTC"    # 비트코인
    ETH = "ETH"    # 이더리움
    XRP = "XRP"    # 리플
    DOGE = "DOGE"  # 도지코인
    SOL = "SOL"    # 솔라나
    BNB = "BNB"    # 바이낸스 코인

    @classmethod
    def is_valid_currency(cls, currency: str) -> bool:
        return currency.upper() in [c.value for c in cls]

    @classmethod
    def get_crypto_currencies(cls) -> list[str]:
        return [c.value for c in cls if c not in [cls.KRW]]



class OrderSide(StrEnum):
    BID = "bid"  # 매수
    ASK = "ask"  # 매도
    
    
    
class OrderType(StrEnum):
    LIMIT = "limit"   # 지정가 주문
    PRICE = "price"   # 시장가 주문(매수)
    MARKET = "market" # 시장가 주문(매도)