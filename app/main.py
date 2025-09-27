from app.config.bithumb_client import BithumbClient
from app.services.account_service import AccountService


def main():
    client = BithumbClient()
    account_service = AccountService(client)

    accounts = account_service.get_accounts()

    print(f"{accounts=}")



if __name__ == "__main__":
    main()