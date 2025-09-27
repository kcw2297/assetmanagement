from app.config.bithumb_client import BithumbClient
from app.services.account_service import AccountService
from app.services.ticker_service import TickerService
from app.enums import MajorCoin
from app.schema import Account

def main():
    client = BithumbClient()
    account_service = AccountService(client)
    ticker_service = TickerService(client)

    accounts: list[Account] = account_service.get_accounts()
    print("=== 보유 자산 정보 ===")
    for account in accounts:
        print(f"{account.currency}: {account.balance:,.2f}")

    major_coins = MajorCoin.get_coins()

    for coin in major_coins:
        TICKER = f"KRW-{coin}"
        ticker = ticker_service.get_ticker(TICKER)

        if ticker:
            print(f"\n{coin} ({ticker.market}):")
            print(f"  현재가: {ticker.trade_price:,.0f}원")
            print(f"  시가: {ticker.opening_price:,.0f}원")
            print(f"  고가: {ticker.high_price:,.0f}원")
            print(f"  저가: {ticker.low_price:,.0f}원")
            print(f"  전일종가: {ticker.prev_closing_price:,.0f}원")
            print(f"  변화: {ticker.change} ({ticker.change_rate:.2%})")
            print(f"  24시간 거래량: {ticker.acc_trade_volume_24h:,.2f}")
        else:
            print(f"\n{coin}: 데이터 조회 실패")




if __name__ == "__main__":
    main()