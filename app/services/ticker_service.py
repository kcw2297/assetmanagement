from app.config.bithumb_client import BithumbClient
from app.schema import Ticker
from app.enums import AccountCurrency


class TickerService:
    """티커 정보 조회 서비스"""

    def __init__(self, client: BithumbClient):
        self.client = client

    def get_ticker(self, market: str) -> Ticker | None:
        """특정 마켓의 티커 정보 조회"""
        try:
            result = self.client.call_public_api("/v1/ticker", {"markets": market})

            if result['status_code'] != 200:
                print(f"❌ Ticker API 에러: {result['status_code']}")
                return None

            data = result['data']
            if not data or not isinstance(data, list) or len(data) == 0:
                print(f"❌ {market} 티커 데이터가 없습니다.")
                return None

            ticker_data = data[0]  # 첫 번째 데이터 사용

            ticker = Ticker(
                market=ticker_data['market'],
                trade_price=float(ticker_data['trade_price']),
                opening_price=float(ticker_data['opening_price']),
                high_price=float(ticker_data['high_price']),
                low_price=float(ticker_data['low_price']),
                prev_closing_price=float(ticker_data['prev_closing_price']),
                trade_volume=float(ticker_data['trade_volume']),
                acc_trade_volume_24h=float(ticker_data['acc_trade_volume_24h']),
                change=ticker_data['change'],
                change_rate=float(ticker_data['change_rate']),
                timestamp=int(ticker_data['timestamp'])
            )

            return ticker

        except Exception as e:
            print(f"Error getting ticker: {e}")
            return None

    def get_bitcoin_ticker(self) -> Ticker | None:
        """비트코인 티커 정보 조회"""
        return self.get_ticker("KRW-BTC")

    def get_crypto_tickers(self) -> list[Ticker]:
        """주요 암호화폐 티커 정보 조회"""
        tickers = []
        crypto_currencies = AccountCurrency.get_crypto_currencies()

        for currency in crypto_currencies:
            market = f"KRW-{currency}"
            ticker = self.get_ticker(market)
            if ticker:
                tickers.append(ticker)

        return tickers

    def get_current_price(self, currency: str) -> float | None:
        """특정 통화의 현재가만 조회"""
        market = f"KRW-{currency.upper()}"
        ticker = self.get_ticker(market)
        return ticker.trade_price if ticker else None