from abc import ABC, abstractmethod
from app.schema import TurtleSignal, Ticker, Account


class BaseStrategy(ABC):
    """터틀 트레이딩 전략 기본 인터페이스"""

    @abstractmethod
    def analyze(self, market: str, ticker: Ticker, market_analysis: dict, accounts: list[Account]) -> TurtleSignal:
        """전략 분석 실행"""
        pass

    def _get_account_by_currency(self, accounts: list[Account], currency: str) -> Account | None:
        """통화별 계좌 조회 헬퍼 메서드"""
        for acc in accounts:
            if acc.currency == currency:
                return acc
        return None

    def _get_krw_balance(self, accounts: list[Account]) -> float:
        """원화 잔액 조회 헬퍼 메서드"""
        krw_account = self._get_account_by_currency(accounts, 'KRW')
        return krw_account.balance if krw_account else 0.0