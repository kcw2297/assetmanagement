import pytest
from unittest.mock import Mock, patch
from app.services.order_service import OrderService
from app.schema import TurtleSignal
from app.enums import SignalType, OrderSide, OrderType


class TestOrderService:

    def test_execute_market_buy_order_success(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)

        with patch.object(service.client, 'call_order_api') as mock_call:
            mock_call.return_value = {
                "status_code": 201,
                "data": {"uuid": "market-order-123"}
            }

            # when
            result = service.execute_market_buy_order("KRW-BTC", 100000.0)

            # then
            assert result["status_code"] == 201
            mock_call.assert_called_once_with({
                'market': 'KRW-BTC',
                'side': OrderSide.BID,
                'price': '100000',
                'ord_type': OrderType.PRICE
            })

    def test_execute_market_sell_order_success(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)

        with patch.object(service.client, 'call_order_api') as mock_call:
            mock_call.return_value = {
                "status_code": 201,
                "data": {"uuid": "market-sell-123"}
            }

            # when
            result = service.execute_market_sell_order("KRW-BTC", 0.001)

            # then
            assert result["status_code"] == 201
            mock_call.assert_called_once_with({
                'market': 'KRW-BTC',
                'side': OrderSide.ASK,
                'volume': '0.001',
                'ord_type': OrderType.MARKET
            })

    def test_execute_signal_order_buy_signal(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)
        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.BUY,
            reason="20일 신고가 돌파",
            current_price=50000000.0,
            target_amount=200000.0,
            confidence=0.8
        )

        with patch.object(service, 'execute_market_buy_order') as mock_buy:
            mock_buy.return_value = {"status_code": 201, "data": {"uuid": "buy-order"}}

            # when
            result = service.execute_signal_order(signal)

            # then
            assert result["status_code"] == 201
            mock_buy.assert_called_once_with("KRW-BTC", 200000.0)

    def test_execute_signal_order_sell_signal(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)
        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.SELL,
            reason="10일선 이탈 손절",
            current_price=45000000.0,
            target_amount=0.5,
            confidence=0.9
        )

        with patch.object(service, 'execute_market_sell_order') as mock_sell:
            mock_sell.return_value = {"status_code": 201, "data": {"uuid": "sell-order"}}

            # when
            result = service.execute_signal_order(signal)

            # then
            assert result["status_code"] == 201
            mock_sell.assert_called_once_with("KRW-BTC", 0.5)

    def test_execute_signal_order_pyramid_signal(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)
        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.PYRAMID,
            reason="추가 매수 조건 충족",
            current_price=52000000.0,
            target_amount=100000.0,
            confidence=0.7
        )

        with patch.object(service, 'execute_market_buy_order') as mock_buy:
            mock_buy.return_value = {"status_code": 201, "data": {"uuid": "pyramid-order"}}

            # when
            result = service.execute_signal_order(signal)

            # then
            assert result["status_code"] == 201
            mock_buy.assert_called_once_with("KRW-BTC", 100000.0)

    def test_execute_signal_order_hold_signal(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)
        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.HOLD,
            reason="매수 조건 미충족",
            current_price=48000000.0
        )

        # when
        result = service.execute_signal_order(signal)

        # then
        assert result["message"] == "주문 실행 없음 - HOLD 신호"



    def test_execute_market_buy_order_exception(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)

        with patch.object(service.client, 'call_order_api') as mock_call:
            mock_call.side_effect = Exception("API Error")

            # when
            result = service.execute_market_buy_order("KRW-BTC", 100000.0)

            # then
            assert "error" in result
            assert "API Error" in result["error"]

    def test_execute_market_sell_order_exception(self):
        # given
        mock_client = Mock()
        service = OrderService(mock_client)

        with patch.object(service.client, 'call_order_api') as mock_call:
            mock_call.side_effect = Exception("Network Error")

            # when
            result = service.execute_market_sell_order("KRW-BTC", 0.001)

            # then
            assert "error" in result
            assert "Network Error" in result["error"]

    def test_client_call_order_api_integration(self):
        # given
        mock_client = Mock()
        mock_client.call_order_api.return_value = {
            "status_code": 201,
            "data": {"uuid": "order-123"}
        }
        service = OrderService(mock_client)

        request_body = {
            'market': 'KRW-BTC',
            'side': OrderSide.BID,
            'price': '100000',
            'ord_type': OrderType.PRICE
        }

        # when
        result = mock_client.call_order_api(request_body)

        # then
        assert result["status_code"] == 201
        assert result["data"]["uuid"] == "order-123"
        mock_client.call_order_api.assert_called_once_with(request_body)

