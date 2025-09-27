import pytest
from app.strategies.base_strategy import BaseStrategy
from app.schema import Account


class ConcreteStrategy(BaseStrategy):
    def analyze(self, market, ticker, market_analysis, accounts):
        pass


class TestBaseStrategy:
    def test_get_account_by_currency_found(self):
        # given
        strategy = ConcreteStrategy()
        accounts = [
            Account(currency="KRW", balance=10000000.0),
            Account(currency="BTC", balance=1.5),
            Account(currency="ETH", balance=2.0)
        ]

        # when
        account = strategy._get_account_by_currency(accounts, "BTC")

        # then
        assert account is not None
        assert account.currency == "BTC"
        assert account.balance == 1.5

    def test_get_account_by_currency_not_found(self):
        # given
        strategy = ConcreteStrategy()
        accounts = [
            Account(currency="KRW", balance=10000000.0),
            Account(currency="BTC", balance=1.5)
        ]

        # when
        account = strategy._get_account_by_currency(accounts, "ETH")

        # then
        assert account is None

    def test_get_account_by_currency_empty_list(self):
        # given
        strategy = ConcreteStrategy()
        accounts = []

        # when
        account = strategy._get_account_by_currency(accounts, "BTC")

        # then
        assert account is None

    def test_get_krw_balance_found(self):
        # given
        strategy = ConcreteStrategy()
        accounts = [
            Account(currency="KRW", balance=15000000.0),
            Account(currency="BTC", balance=1.5),
            Account(currency="ETH", balance=2.0)
        ]

        # when
        balance = strategy._get_krw_balance(accounts)

        # then
        assert balance == 15000000.0

    def test_get_krw_balance_not_found(self):
        # given
        strategy = ConcreteStrategy()
        accounts = [
            Account(currency="BTC", balance=1.5),
            Account(currency="ETH", balance=2.0)
        ]

        # when
        balance = strategy._get_krw_balance(accounts)

        # then
        assert balance == 0.0

    def test_get_krw_balance_empty_list(self):
        # given
        strategy = ConcreteStrategy()
        accounts = []

        # when
        balance = strategy._get_krw_balance(accounts)

        # then
        assert balance == 0.0

    def test_get_krw_balance_zero_balance(self):
        # given
        strategy = ConcreteStrategy()
        accounts = [
            Account(currency="KRW", balance=0.0),
            Account(currency="BTC", balance=1.5)
        ]

        # when
        balance = strategy._get_krw_balance(accounts)

        # then
        assert balance == 0.0