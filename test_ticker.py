from app.config.bithumb_client import BithumbClient
from app.services.ticker_service import TickerService


def main():
    client = BithumbClient()
    ticker_service = TickerService(client)

    print("=== 비트코인 티커 정보 ===")
    btc_ticker = ticker_service.get_bitcoin_ticker()
    if btc_ticker:
        print(f"마켓: {btc_ticker.market}")
        print(f"현재가: {btc_ticker.trade_price:,.0f}원")
        print(f"시가: {btc_ticker.opening_price:,.0f}원")
        print(f"고가: {btc_ticker.high_price:,.0f}원")
        print(f"저가: {btc_ticker.low_price:,.0f}원")
        print(f"전일종가: {btc_ticker.prev_closing_price:,.0f}원")
        print(f"변화: {btc_ticker.change} ({btc_ticker.change_rate:.2%})")
        print(f"거래량: {btc_ticker.trade_volume:.4f}")
        print(f"24시간 거래량: {btc_ticker.acc_trade_volume_24h:.2f}")

    print("\n=== 주요 암호화폐 현재가 ===")
    for currency in ["BTC", "ETH", "XRP"]:
        price = ticker_service.get_current_price(currency)
        if price:
            print(f"{currency}: {price:,.0f}원")


if __name__ == "__main__":
    main()