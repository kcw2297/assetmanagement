import requests
from decimal import Decimal

from app.config.bithumb_client import BithumbClient
from app.schema import Account


class AccountService:
    """계좌 및 자산 관련 서비스"""

    def __init__(self, client: BithumbClient):
        self.client = client

    def get_accounts(self) -> list[Account]:
        """보유 자산 정보 조회"""
        response = requests.get(
            f'{self.client.BASE_URL}/v1/accounts',
            headers=self.client.get_headers()
        )
        response.raise_for_status()

        data = response.json()
        return [Account(**acc) for acc in data if isinstance(acc, dict)]

    def get_balance(self, currency: str = 'KRW') -> Account:
        """특정 통화 잔액 조회"""
        accounts = self.get_accounts()
        for account in accounts:
            if account.currency == currency.upper():
                return account
        return Account(currency=currency, balance=Decimal('0'))

    def get_current_price(self, ticker: str) -> float | None:
        """현재가 조회"""
        price = self.client.public_client.get_current_price(ticker)
        return float(price) if price else None