import pytest
from unittest.mock import Mock
from app.services.ticker_service import TickerService
from app.schema import Ticker


class TestTickerService:
    def test_get_ticker_success(self):
        # given
        mock_client = Mock()
        mock_response = {
            "status_code": 200,
            "data": [{
                "market": "KRW-BTC",
                "trade_price": "50000000.0",
                "opening_price": "49000000.0",
                "high_price": "51000000.0",
                "low_price": "48000000.0",
                "prev_closing_price": "49500000.0",
                "trade_volume": "100.5",
                "acc_trade_volume_24h": "2000.0",
                "change": "RISE",
                "change_rate": "0.0101",
                "timestamp": "1640995200000"
            }]
        }
        mock_client.call_public_api.return_value = mock_response
        service = TickerService(mock_client)

        # when
        ticker = service.get_ticker("KRW-BTC")

        # then
        assert ticker is not None
        assert ticker.market == "KRW-BTC"
        assert ticker.trade_price == 50000000.0
        assert ticker.change == "RISE"
        mock_client.call_public_api.assert_called_once_with("/v1/ticker", {"markets": "KRW-BTC"})

    def test_get_ticker_api_failure(self):
        # given
        mock_client = Mock()
        mock_client.call_public_api.return_value = {"status_code": 400}
        service = TickerService(mock_client)

        # when
        ticker = service.get_ticker("KRW-BTC")

        # then
        assert ticker is None

    def test_get_ticker_empty_response(self):
        # given
        mock_client = Mock()
        mock_client.call_public_api.return_value = {"status_code": 200, "data": []}
        service = TickerService(mock_client)

        # when
        ticker = service.get_ticker("KRW-BTC")

        # then
        assert ticker is None

    def test_get_ticker_with_exception(self):
        # given
        mock_client = Mock()
        mock_client.call_public_api.side_effect = Exception("API Error")
        service = TickerService(mock_client)

        # when
        ticker = service.get_ticker("KRW-BTC")

        # then
        assert ticker is None

    def test_get_bitcoin_ticker_success(self):
        # given
        mock_client = Mock()
        mock_response = {
            "status_code": 200,
            "data": [{
                "market": "KRW-BTC",
                "trade_price": "50000000.0",
                "opening_price": "49000000.0",
                "high_price": "51000000.0",
                "low_price": "48000000.0",
                "prev_closing_price": "49500000.0",
                "trade_volume": "100.5",
                "acc_trade_volume_24h": "2000.0",
                "change": "RISE",
                "change_rate": "0.0101",
                "timestamp": "1640995200000"
            }]
        }
        mock_client.call_public_api.return_value = mock_response
        service = TickerService(mock_client)

        # when
        ticker = service.get_bitcoin_ticker()

        # then
        assert ticker is not None
        assert ticker.market == "KRW-BTC"
        mock_client.call_public_api.assert_called_once_with("/v1/ticker", {"markets": "KRW-BTC"})

    def test_get_crypto_tickers_success(self):
        # given
        mock_client = Mock()
        def mock_response_func(endpoint, params):
            if params["markets"] == "KRW-BTC":
                return {
                    "status_code": 200,
                    "data": [{
                        "market": "KRW-BTC",
                        "trade_price": "50000000.0",
                        "opening_price": "49000000.0",
                        "high_price": "51000000.0",
                        "low_price": "48000000.0",
                        "prev_closing_price": "49500000.0",
                        "trade_volume": "100.5",
                        "acc_trade_volume_24h": "2000.0",
                        "change": "RISE",
                        "change_rate": "0.0101",
                        "timestamp": "1640995200000"
                    }]
                }
            elif params["markets"] == "KRW-ETH":
                return {
                    "status_code": 200,
                    "data": [{
                        "market": "KRW-ETH",
                        "trade_price": "3000000.0",
                        "opening_price": "2900000.0",
                        "high_price": "3100000.0",
                        "low_price": "2800000.0",
                        "prev_closing_price": "2950000.0",
                        "trade_volume": "500.0",
                        "acc_trade_volume_24h": "1000.0",
                        "change": "RISE",
                        "change_rate": "0.0169",
                        "timestamp": "1640995200000"
                    }]
                }
            else:
                return {"status_code": 400}

        mock_client.call_public_api.side_effect = mock_response_func
        service = TickerService(mock_client)

        # when
        tickers = service.get_crypto_tickers()

        # then
        assert len(tickers) >= 2  # BTC, ETH는 최소 포함
        btc_ticker = next((t for t in tickers if t.market == "KRW-BTC"), None)
        eth_ticker = next((t for t in tickers if t.market == "KRW-ETH"), None)
        assert btc_ticker is not None
        assert eth_ticker is not None

    def test_get_current_price_success(self):
        # given
        mock_client = Mock()
        mock_response = {
            "status_code": 200,
            "data": [{
                "market": "KRW-BTC",
                "trade_price": "50000000.0",
                "opening_price": "49000000.0",
                "high_price": "51000000.0",
                "low_price": "48000000.0",
                "prev_closing_price": "49500000.0",
                "trade_volume": "100.5",
                "acc_trade_volume_24h": "2000.0",
                "change": "RISE",
                "change_rate": "0.0101",
                "timestamp": "1640995200000"
            }]
        }
        mock_client.call_public_api.return_value = mock_response
        service = TickerService(mock_client)

        # when
        price = service.get_current_price("BTC")

        # then
        assert price == 50000000.0

    def test_get_current_price_no_ticker(self):
        # given
        mock_client = Mock()
        mock_client.call_public_api.return_value = {"status_code": 400}
        service = TickerService(mock_client)

        # when
        price = service.get_current_price("BTC")

        # then
        assert price is None