from abc import ABC, abstractmethod
from common.schema import OHLC
from typing import Any

class ExchangeInterface(ABC):
    """계좌 API 추상화 인터페이스"""

    @abstractmethod
    def candles(self, market: str, count: int) -> list[OHLC]:
        """캔들 데이터 조회 (과거→최신 순서)"""
        pass

    @abstractmethod
    def current_price(self, market: str) -> float:
        """현재가 조회"""
        pass

    @abstractmethod
    def buy(self, market: str, amount: float) -> Any:
        """매수 주문 실행 (amount: KRW 금액)"""
        pass

    @abstractmethod
    def sell(self, market: str, volume: float) -> Any:
        """매도 주문 실행 (volume: 코인 수량)"""
        pass

    @abstractmethod
    def balance(self, *args, **kwargs) -> float:
        """잔고 조회"""
        pass
