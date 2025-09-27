import pytest
from unittest.mock import Mock, patch
from app.trader import TurtleTrader
from app.schema import TurtleSignal, Account
from app.enums import SignalType


class TestTurtleTrader:
    def test_init_dry_run_mode(self):
        # given & when
        trader = TurtleTrader(dry_run=True)

        # then
        assert trader.dry_run is True
        assert trader.client is not None
        assert trader.coordinator is not None

    def test_init_live_trading_mode(self):
        # given & when
        trader = TurtleTrader(dry_run=False)

        # then
        assert trader.dry_run is False

    @patch('app.trader.TurtleCoordinator')
    def test_run_single_analysis_buy_signal(self, mock_coordinator_class):
        # given
        mock_coordinator = Mock()
        mock_coordinator_class.return_value = mock_coordinator

        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.BUY,
            reason="20일 신고가 돌파",
            current_price=50000000.0,
            target_amount=200000.0,
            confidence=0.8
        )
        mock_coordinator.analyze_comprehensive_signal.return_value = signal

        trader = TurtleTrader(dry_run=True)
        trader.coordinator = mock_coordinator

        # when
        result = trader.run_single_analysis("KRW-BTC")

        # then
        assert result["action"] == "BUY"
        assert result["simulation"] is True
        assert result["market"] == "KRW-BTC"
        assert result["amount"] == 200000.0

    @patch('app.trader.TurtleCoordinator')
    def test_run_single_analysis_hold_signal(self, mock_coordinator_class):
        # given
        mock_coordinator = Mock()
        mock_coordinator_class.return_value = mock_coordinator

        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.HOLD,
            reason="매수 조건 미충족",
            current_price=48000000.0
        )
        mock_coordinator.analyze_comprehensive_signal.return_value = signal

        trader = TurtleTrader(dry_run=True)
        trader.coordinator = mock_coordinator

        # when
        result = trader.run_single_analysis("KRW-BTC")

        # then
        assert result["action"] == "HOLD"
        assert result["message"] == "주문 실행 없음"

    @patch('app.trader.TurtleCoordinator')
    def test_run_single_analysis_exception(self, mock_coordinator_class):
        # given
        mock_coordinator = Mock()
        mock_coordinator_class.return_value = mock_coordinator
        mock_coordinator.analyze_comprehensive_signal.side_effect = Exception("API Error")

        trader = TurtleTrader(dry_run=True)
        trader.coordinator = mock_coordinator

        # when
        result = trader.run_single_analysis("KRW-BTC")

        # then
        assert "error" in result
        assert "API Error" in result["error"]

    @patch('app.trader.MajorCoin')
    @patch('app.trader.TurtleCoordinator')
    def test_run_full_analysis(self, mock_coordinator_class, mock_major_coin):
        # given
        mock_coordinator = Mock()
        mock_coordinator_class.return_value = mock_coordinator

        # Mock MajorCoin enum
        mock_coin_btc = Mock()
        mock_coin_btc.market = "KRW-BTC"
        mock_coin_eth = Mock()
        mock_coin_eth.market = "KRW-ETH"
        mock_major_coin.__iter__ = Mock(return_value=iter([mock_coin_btc, mock_coin_eth]))

        # Mock signals
        btc_signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.HOLD,
            reason="매수 조건 미충족",
            current_price=50000000.0
        )
        eth_signal = TurtleSignal(
            market="KRW-ETH",
            signal_type=SignalType.BUY,
            reason="20일 신고가 돌파",
            current_price=3000000.0,
            target_amount=100000.0
        )

        def mock_analyze(market):
            if market == "KRW-BTC":
                return btc_signal
            elif market == "KRW-ETH":
                return eth_signal

        mock_coordinator.analyze_comprehensive_signal.side_effect = mock_analyze

        trader = TurtleTrader(dry_run=True)
        trader.coordinator = mock_coordinator

        with patch.object(trader, '_print_account_status'):
            # when
            results = trader.run_full_analysis()

            # then
            assert "KRW-BTC" in results
            assert "KRW-ETH" in results
            assert results["KRW-BTC"]["action"] == "HOLD"
            assert results["KRW-ETH"]["action"] == "BUY"

    def test_execute_order_simulation_mode(self):
        # given
        trader = TurtleTrader(dry_run=True)
        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.BUY,
            reason="20일 신고가 돌파",
            current_price=50000000.0,
            target_amount=200000.0
        )

        # when
        result = trader._execute_order(signal)

        # then
        assert result["action"] == "BUY"
        assert result["simulation"] is True
        assert result["market"] == "KRW-BTC"
        assert result["amount"] == 200000.0

    def test_execute_order_live_trading_success(self):
        # given
        trader = TurtleTrader(dry_run=False)
        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.SELL,
            reason="손절",
            current_price=45000000.0,
            target_amount=0.5
        )

        mock_order_result = {
            "status_code": 201,
            "data": {"uuid": "order-123", "state": "wait"}
        }

        with patch.object(trader.order_service, 'execute_signal_order') as mock_execute:
            mock_execute.return_value = mock_order_result

            # when
            result = trader._execute_order(signal)

            # then
            assert result["status_code"] == 201
            assert result["data"]["uuid"] == "order-123"
            mock_execute.assert_called_once_with(signal)

    def test_execute_order_live_trading_failure(self):
        # given
        trader = TurtleTrader(dry_run=False)
        signal = TurtleSignal(
            market="KRW-BTC",
            signal_type=SignalType.BUY,
            reason="매수",
            current_price=50000000.0,
            target_amount=100000.0
        )

        mock_order_result = {"error": "Insufficient balance"}

        with patch.object(trader.order_service, 'execute_signal_order') as mock_execute:
            mock_execute.return_value = mock_order_result

            # when
            result = trader._execute_order(signal)

            # then
            assert "error" in result
            assert "Insufficient balance" in result["error"]

    def test_print_account_status_success(self):
        # given
        trader = TurtleTrader(dry_run=True)
        accounts = [
            Account(currency="KRW", balance=10000000.0),
            Account(currency="BTC", balance=0.5),
            Account(currency="ETH", balance=2.0)
        ]

        with patch.object(trader.account_service, 'get_accounts') as mock_get_accounts:
            mock_get_accounts.return_value = accounts

            # when
            trader._print_account_status()

            # then
            mock_get_accounts.assert_called_once()

    def test_print_account_status_exception(self):
        # given
        trader = TurtleTrader(dry_run=True)

        with patch.object(trader.account_service, 'get_accounts') as mock_get_accounts:
            mock_get_accounts.side_effect = Exception("API Error")

            # when
            trader._print_account_status()

            # then
            mock_get_accounts.assert_called_once()

    def test_set_live_trading(self):
        # given
        trader = TurtleTrader(dry_run=True)

        # when
        trader.set_live_trading()

        # then
        assert trader.dry_run is False

    def test_set_simulation_mode(self):
        # given
        trader = TurtleTrader(dry_run=False)

        # when
        trader.set_simulation_mode()

        # then
        assert trader.dry_run is True