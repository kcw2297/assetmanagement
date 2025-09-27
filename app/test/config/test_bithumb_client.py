import pytest
from unittest.mock import Mock, patch
from app.config.bithumb_client import BithumbClient
from app.enums import OrderSide, OrderType


class TestBithumbClient:
    @patch('app.config.bithumb_client.settings')
    def test_init(self, mock_settings):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"

        # when
        client = BithumbClient()

        # then
        assert client.api_key == "test_api_key"
        assert client.secret_key == "test_secret_key"

    @patch('app.config.bithumb_client.settings')
    def test_generate_jwt_token(self, mock_settings):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"
        client = BithumbClient()

        # when
        token = client._generate_jwt_token()

        # then
        assert isinstance(token, str)
        assert len(token) > 0

    @patch('requests.get')
    @patch('app.config.bithumb_client.settings')
    def test_call_private_api_success(self, mock_settings, mock_get):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"
        client = BithumbClient()

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"currency": "KRW", "balance": "1000000"}]}
        mock_get.return_value = mock_response

        # when
        result = client.call_private_api("/v1/accounts")

        # then
        assert result["status_code"] == 200
        assert "data" in result
        mock_get.assert_called_once()

    @patch('requests.get')
    @patch('app.config.bithumb_client.settings')
    def test_call_private_api_exception(self, mock_settings, mock_get):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"
        client = BithumbClient()

        mock_get.side_effect = Exception("Network Error")

        # when
        result = client.call_private_api("/v1/accounts")

        # then
        assert result["status_code"] == 0
        assert "error" in result["data"]

    @patch('requests.get')
    @patch('app.config.bithumb_client.settings')
    def test_call_public_api_success(self, mock_settings, mock_get):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"
        client = BithumbClient()

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"market": "KRW-BTC", "trade_price": "50000000"}]
        mock_get.return_value = mock_response

        # when
        result = client.call_public_api("/v1/ticker", {"markets": "KRW-BTC"})

        # then
        assert result["status_code"] == 200
        assert "data" in result
        mock_get.assert_called_once()

    @patch('requests.get')
    @patch('app.config.bithumb_client.settings')
    def test_call_public_api_exception(self, mock_settings, mock_get):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"
        client = BithumbClient()

        mock_get.side_effect = Exception("API Error")

        # when
        result = client.call_public_api("/v1/ticker", {"markets": "KRW-BTC"})

        # then
        assert result["status_code"] == 400
        assert "error" in result["data"]

    @patch('requests.post')
    @patch('app.config.bithumb_client.settings')
    def test_call_order_api_success(self, mock_settings, mock_post):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"
        client = BithumbClient()

        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"uuid": "order-123", "state": "wait"}
        mock_post.return_value = mock_response

        request_body = {
            'market': 'KRW-BTC',
            'side': OrderSide.BID,
            'price': '100000',
            'ord_type': OrderType.PRICE
        }

        # when
        result = client.call_order_api(request_body)

        # then
        assert result["status_code"] == 201
        assert result["data"]["uuid"] == "order-123"
        mock_post.assert_called_once()

    @patch('requests.post')
    @patch('app.config.bithumb_client.settings')
    def test_call_order_api_exception(self, mock_settings, mock_post):
        # given
        mock_settings.BITHUMB_API_KEY = "test_api_key"
        mock_settings.BITHUMB_SECRET_KEY = "test_secret_key"
        client = BithumbClient()

        mock_post.side_effect = Exception("Network Error")

        request_body = {
            'market': 'KRW-BTC',
            'side': OrderSide.BID,
            'price': '100000',
            'ord_type': OrderType.PRICE
        }

        # when
        result = client.call_order_api(request_body)

        # then
        assert "error" in result
        assert "Network Error" in result["error"]