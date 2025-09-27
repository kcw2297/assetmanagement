from enum import StrEnum


class MajorCoin(StrEnum):
    BTC = "BTC"    # 비트코인
    ETH = "ETH"    # 이더리움
    XRP = "XRP"    # 리플
    DOGE = "DOGE"  # 도지코인
    LINK = "LINK"  # 체인링크
    WLD = "WLD"    # 월드코인
    BNB = "BNB"    # 바이낸스 코인
    TRX = "TRX"    # 트론
    BCH = "BCH"    # 비트코인 캐시

    @property
    def market(self) -> str:
        return f"KRW-{self.value}"

    @classmethod
    def get_coins(cls) -> list[str]:
        return [
            cls.BTC, cls.ETH, cls.XRP, cls.DOGE, cls.LINK,
            cls.WLD, cls.BNB, cls.TRX, cls.BCH
        ]

    @classmethod
    def get_markets(cls) -> list[str]:
        return [coin.market for coin in cls]


class SignalType(StrEnum):
    BUY = "BUY"          # 매수
    SELL = "SELL"        # 매도
    PYRAMID = "PYRAMID"  # 피라미딩
    HOLD = "HOLD"        # 홀드


class AccountCurrency(StrEnum):
    KRW = "KRW"    # 원화
    BTC = "BTC"    # 비트코인
    ETH = "ETH"    # 이더리움
    XRP = "XRP"    # 리플
    DOGE = "DOGE"  # 도지코인
    LINK = "LINK"  # 체인링크
    WLD = "WLD"    # 월드코인
    BNB = "BNB"    # 바이낸스 코인
    TRX = "TRX"    # 트론
    BCH = "BCH"    # 비트코인 캐시

    @classmethod
    def is_valid_currency(cls, currency: str) -> bool:
        return currency.upper() in [c.value for c in cls]

    @classmethod
    def get_crypto_currencies(cls) -> list[str]:
        return [c.value for c in cls if c not in [cls.KRW]]

