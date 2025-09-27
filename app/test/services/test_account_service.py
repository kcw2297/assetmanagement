import pytest
from unittest.mock import Mock, patch
from app.services.account_service import AccountService
from app.schema import Account


class TestAccountService:
    def test_get_accounts_success(self):
        # given
        mock_client = Mock()
        mock_response = {
            "data": [
                {"currency": "KRW", "balance": "1000000.0"},
                {"currency": "BTC", "balance": "0.5"},
                {"currency": "ETH", "balance": "2.0"}
            ]
        }
        mock_client.call_private_api.return_value = mock_response
        service = AccountService(mock_client)

        # when
        accounts = service.get_accounts()

        # then
        assert len(accounts) == 3
        assert accounts[0].currency == "KRW"
        assert accounts[0].balance == 1000000.0
        assert accounts[1].currency == "BTC"
        assert accounts[1].balance == 0.5
        mock_client.call_private_api.assert_called_once_with("/v1/accounts")

    def test_get_accounts_api_failure(self):
        # given
        mock_client = Mock()
        mock_client.call_private_api.side_effect = Exception("API Error")
        service = AccountService(mock_client)

        # when
        accounts = service.get_accounts()

        # then
        assert accounts == []

    def test_get_accounts_error_response(self):
        # given
        mock_client = Mock()
        mock_response = {"data": {"error": "Invalid request"}}
        mock_client.call_private_api.return_value = mock_response
        service = AccountService(mock_client)

        # when
        accounts = service.get_accounts()

        # then
        assert accounts == []

    def test_get_accounts_invalid_currency(self):
        # given
        mock_client = Mock()
        mock_response = {
            "data": [
                {"currency": "INVALID", "balance": "1000.0"},
                {"currency": "BTC", "balance": "0.5"}
            ]
        }
        mock_client.call_private_api.return_value = mock_response
        service = AccountService(mock_client)

        # when
        accounts = service.get_accounts()

        # then
        assert len(accounts) == 1  # INVALID currency filtered out
        assert accounts[0].currency == "BTC"

    def test_get_accounts_empty_data(self):
        # given
        mock_client = Mock()
        mock_response = {"data": []}
        mock_client.call_private_api.return_value = mock_response
        service = AccountService(mock_client)

        # when
        accounts = service.get_accounts()

        # then
        assert accounts == []

    def test_get_accounts_with_exception(self):
        # given
        mock_client = Mock()
        mock_client.call_private_api.side_effect = Exception("API Error")
        service = AccountService(mock_client)

        # when
        accounts = service.get_accounts()

        # then
        assert accounts == []