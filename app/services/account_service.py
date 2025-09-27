from app.config.bithumb_client import BithumbClient
from app.schema import Account
from app.enums import AccountCurrency


class AccountService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def get_accounts(self) -> list[Account]:
        try:
            result = self.client.call_api("/v1/accounts")
            data = result['data']

            if 'error' in data:
                return []

            results = []
            for account_data in data:
                currency = account_data.get('currency', '').upper()
                balance = account_data.get('balance', 0.0)

                if AccountCurrency.is_valid_currency(currency):
                    account = Account(
                        currency=currency,
                        balance=float(balance),
                    )
                    results.append(account)

            return results

        except Exception as e:
            print(f"Error getting accounts: {e}")
            return []
