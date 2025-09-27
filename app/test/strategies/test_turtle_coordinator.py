import pytest
from unittest.mock import Mock
from app.strategies.turtle_coordinator import TurtleCoordinator
from app.schema import Ticker, Account, TurtleSignal
from app.enums import SignalType


class TestTurtleCoordinator:
    def test_analyze_comprehensive_signal_data_failure(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()
        mock_ticker_service.get_ticker.return_value = None
        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_comprehensive_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"
        assert signal.current_price == 0.0

    def test_analyze_comprehensive_signal_sell_priority(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=47500000.0,
            opening_price=50000000.0,
            high_price=50500000.0,
            low_price=47000000.0,
            prev_closing_price=50000000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.05,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": True,
            "moving_averages": {"ma5": 48000000.0, "ma10": 45000000.0}
        }
        accounts = [Account(currency="BTC", balance=0.5)]

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = market_analysis
        mock_account_service.get_accounts.return_value = accounts

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_comprehensive_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.SELL
        assert "당일 5% 이상 급락" in signal.reason

    def test_analyze_comprehensive_signal_pyramid_when_holding(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="RISE",
            change_rate=0.01,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": True,
            "moving_averages": {"ma5": 48000000.0, "ma10": 45000000.0}
        }
        accounts = [
            Account(currency="BTC", balance=0.1),
            Account(currency="KRW", balance=100000000.0)  # 1억원으로 증가
        ]

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = market_analysis
        mock_account_service.get_accounts.return_value = accounts

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_comprehensive_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "피라미딩 조건 미충족" in signal.reason

    def test_analyze_comprehensive_signal_buy_when_not_holding(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=52000000.0,
            opening_price=51000000.0,
            high_price=52500000.0,
            low_price=50500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.02,
            timestamp=1640995200000
        )
        market_analysis = {"recent_high_20d": 51000000.0}
        accounts = [Account(currency="KRW", balance=10000000.0)]

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = market_analysis
        mock_account_service.get_accounts.return_value = accounts

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_comprehensive_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.BUY
        assert "20일 신고가" in signal.reason

    def test_analyze_comprehensive_signal_no_btc_holdings(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="RISE",
            change_rate=0.01,
            timestamp=1640995200000
        )
        market_analysis = {"recent_high_20d": 52000000.0}
        accounts = [
            Account(currency="ETH", balance=1.0),  # 다른 코인은 보유
            Account(currency="KRW", balance=10000000.0)
        ]

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = market_analysis
        mock_account_service.get_accounts.return_value = accounts

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_comprehensive_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "미돌파" in signal.reason

    def test_analyze_buy_signal(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=52000000.0,
            opening_price=51000000.0,
            high_price=52500000.0,
            low_price=50500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.02,
            timestamp=1640995200000
        )
        market_analysis = {"recent_high_20d": 51000000.0}
        accounts = [Account(currency="KRW", balance=10000000.0)]

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = market_analysis
        mock_account_service.get_accounts.return_value = accounts

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_buy_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.BUY
        mock_ticker_service.get_ticker.assert_called_with("KRW-BTC")
        mock_candle_service.get_market_analysis.assert_called_with("KRW-BTC")
        mock_account_service.get_accounts.assert_called_once()

    def test_analyze_sell_signal(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=47500000.0,
            opening_price=50000000.0,
            high_price=50500000.0,
            low_price=47000000.0,
            prev_closing_price=50000000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.05,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": True,
            "moving_averages": {"ma5": 48000000.0, "ma10": 45000000.0}
        }
        accounts = [Account(currency="BTC", balance=0.5)]

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = market_analysis
        mock_account_service.get_accounts.return_value = accounts

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_sell_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.SELL
        mock_ticker_service.get_ticker.assert_called_with("KRW-BTC")
        mock_candle_service.get_market_analysis.assert_called_with("KRW-BTC")
        mock_account_service.get_accounts.assert_called_once()

    def test_analyze_pyramid_signal(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="RISE",
            change_rate=0.01,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": True
        }
        accounts = [
            Account(currency="BTC", balance=0.1),
            Account(currency="KRW", balance=50000000.0)
        ]

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = market_analysis
        mock_account_service.get_accounts.return_value = accounts

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_pyramid_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.HOLD
        mock_ticker_service.get_ticker.assert_called_with("KRW-BTC")
        mock_candle_service.get_market_analysis.assert_called_with("KRW-BTC")
        mock_account_service.get_accounts.assert_called_once()

    def test_analyze_comprehensive_signal_market_analysis_failure(self):
        # given
        mock_ticker_service = Mock()
        mock_candle_service = Mock()
        mock_account_service = Mock()

        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="RISE",
            change_rate=0.01,
            timestamp=1640995200000
        )

        mock_ticker_service.get_ticker.return_value = ticker
        mock_candle_service.get_market_analysis.return_value = None
        mock_account_service.get_accounts.return_value = []

        coordinator = TurtleCoordinator(mock_ticker_service, mock_candle_service, mock_account_service)

        # when
        signal = coordinator.analyze_comprehensive_signal("KRW-BTC")

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"