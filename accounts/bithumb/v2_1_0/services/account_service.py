from accounts.bithumb.v2_1_0.config.bithumb_client import BithumbClient
from accounts.bithumb.v2_1_0.schema import Account


class AccountService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def get_accounts(self) -> list[Account]:
        try:
            result = self.client.call_private_api("/v1/accounts")
            data = result['data']

            if 'error' in data:
                return []

            results = []
            for account_data in data:
                account = Account(
                    currency=account_data.get('currency', '').upper(),
                    balance=float(account_data.get('balance', 0.0)),
                    locked=float(account_data.get('locked', 0.0)),
                    avg_buy_price=float(account_data.get('avg_buy_price', 0.0)),
                    avg_buy_price_modified=account_data.get('avg_buy_price_modified', False),
                    unit_currency=account_data.get('unit_currency', 'KRW'),
                )
                results.append(account)

            return results

        except Exception:
            return []
