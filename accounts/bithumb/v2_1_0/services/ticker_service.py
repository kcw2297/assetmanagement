from accounts.bithumb.v2_1_0.config.bithumb_client import BithumbClient
from strategies.turtle.enums import AccountCurrency


from accounts.bithumb.v2_1_0.schema import Ticker



class TickerService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def get_ticker(self, market: str) -> list[Ticker] | None:
        try:
            result = self.client.call_public_api("/v1/ticker", {"markets": market})

            if result['status_code'] != 200:
                raise ValueError(f"Ticker API 에러: {result['status_code']}")

            data = result['data']
            if not data or not isinstance(data, list) or len(data) == 0:
                raise ValueError(f"Ticker API 에러: {result['status_code']}")

            result = []
            for ticker_data in data:
                ticker_data:dict
                ticker = Ticker(
                    market=ticker_data.get('market', ''),
                    trade_date=ticker_data.get('trade_date', ''),
                    trade_time=ticker_data.get('trade_time', ''),
                    trade_date_kst=ticker_data.get('trade_date_kst', ''),
                    trade_time_kst=ticker_data.get('trade_time_kst', ''),
                    trade_timestamp=int(ticker_data.get('trade_timestamp', 0)),
                    opening_price=float(ticker_data.get('opening_price', 0.0)),
                    high_price=float(ticker_data.get('high_price', 0.0)),
                    low_price=float(ticker_data.get('low_price', 0.0)),
                    trade_price=float(ticker_data.get('trade_price', 0.0)),
                    prev_closing_price=float(ticker_data.get('prev_closing_price', 0.0)),
                    change=ticker_data.get('change', 'EVEN'),
                    change_price=float(ticker_data.get('change_price', 0.0)),
                    change_rate=float(ticker_data.get('change_rate', 0.0)),
                    signed_change_price=float(ticker_data.get('signed_change_price', 0.0)),
                    signed_change_rate=float(ticker_data.get('signed_change_rate', 0.0)),
                    trade_volume=float(ticker_data.get('trade_volume', 0.0)),
                    acc_trade_price=float(ticker_data.get('acc_trade_price', 0.0)),
                    acc_trade_price_24h=float(ticker_data.get('acc_trade_price_24h', 0.0)),
                    acc_trade_volume=float(ticker_data.get('acc_trade_volume', 0.0)),
                    acc_trade_volume_24h=float(ticker_data.get('acc_trade_volume_24h', 0.0)),
                    highest_52_week_price=float(ticker_data.get('highest_52_week_price', 0.0)),
                    highest_52_week_date=ticker_data.get('highest_52_week_date', ''),
                    lowest_52_week_price=float(ticker_data.get('lowest_52_week_price', 0.0)),
                    lowest_52_week_date=ticker_data.get('lowest_52_week_date', ''),
                    timestamp=int(ticker_data.get('timestamp', 0))
                )
                result.append(ticker)

            return result

        except Exception:
            return None

    def get_bitcoin_ticker(self) -> list[Ticker] | None:
        return self.get_ticker("KRW-BTC")
        

    def get_crypto_tickers(self) -> list[Ticker]:
        tickers = []
        crypto_currencies = AccountCurrency.get_crypto_currencies()

        for currency in crypto_currencies:
            market = f"KRW-{currency}"
            ticker_list = self.get_ticker(market)
            if ticker_list:
                tickers.extend(ticker_list)

        return tickers

    def get_current_price(self, currency: str) -> float | None:
        market = f"KRW-{currency.upper()}"
        tickers = self.get_ticker(market)
        return tickers[0].trade_price if tickers else None