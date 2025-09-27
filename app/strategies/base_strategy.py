from abc import ABC, abstractmethod
from app.schema import TurtleSignal, Ticker, Account


class BaseStrategy(ABC):
    @abstractmethod
    def analyze(self, market: str, ticker: Ticker, market_analysis: dict, accounts: list[Account]) -> TurtleSignal:
        pass

    def _get_account_by_currency(self, accounts: list[Account], currency: str) -> Account | None:
        for acc in accounts:
            if acc.currency == currency:
                return acc
        return None

    def _get_krw_balance(self, accounts: list[Account]) -> float:
        krw_account = self._get_account_by_currency(accounts, 'KRW')
        return krw_account.balance if krw_account else 0.0