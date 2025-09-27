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

    @classmethod
    def get_top_coins(cls) -> list[str]:
        return [
            cls.BTC, cls.ETH, cls.XRP, cls.DOGE, cls.LINK,
            cls.WLD, cls.BNB, cls.TRX, cls.BCH
        ]

