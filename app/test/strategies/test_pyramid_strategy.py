import pytest
from unittest.mock import Mock, patch
from app.strategies.pyramid_strategy import PyramidStrategy
from app.schema import Ticker, Account, TurtleSignal
from app.enums import SignalType


class TestPyramidStrategy:
    def test_analyze_no_holdings(self):
        # given
        strategy = PyramidStrategy()
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
        accounts = [Account(currency="KRW", balance=10000000.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "보유 중이지 않음" in signal.reason

    def test_analyze_zero_balance(self):
        # given
        strategy = PyramidStrategy()
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
        accounts = [Account(currency="BTC", balance=0.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "보유 중이지 않음" in signal.reason

    def test_analyze_ma_break(self):
        # given
        strategy = PyramidStrategy()
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
            "is_above_ma5": False,
            "is_above_ma10": True
        }
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "5일/10일선 이탈로 피라미딩 중단" in signal.reason

    def test_analyze_sharp_decline(self):
        # given
        strategy = PyramidStrategy()
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
            "is_above_ma10": True
        }
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "당일 5% 급락으로 피라미딩 중단" in signal.reason

    def test_analyze_max_position_reached(self):
        # given
        strategy = PyramidStrategy()
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
            Account(currency="KRW", balance=5000000.0),  # 500만원
            Account(currency="BTC", balance=1.0)  # 1 BTC = 5000만원 (500만원 대비 1000% = 10% 초과)
        ]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "최대 포지션 한도(10%) 도달" in signal.reason

    def test_analyze_pyramid_conditions_not_met(self):
        # given
        strategy = PyramidStrategy()
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
            Account(currency="KRW", balance=100000000.0),  # 1억원
            Account(currency="BTC", balance=0.1)  # 500만원 (총 1.05억원 대비 약 4.7%)
        ]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "피라미딩 조건 미충족" in signal.reason

    def test_analyze_no_ticker(self):
        # given
        strategy = PyramidStrategy()
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": True
        }
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", None, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"

    def test_analyze_no_market_analysis(self):
        # given
        strategy = PyramidStrategy()
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
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, None, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"

    def test_is_ma_break_true_ma5(self):
        # given
        strategy = PyramidStrategy()
        market_analysis = {
            "is_above_ma5": False,
            "is_above_ma10": True
        }

        # when
        result = strategy._is_ma_break(market_analysis)

        # then
        assert result is True

    def test_is_ma_break_true_ma10(self):
        # given
        strategy = PyramidStrategy()
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": False
        }

        # when
        result = strategy._is_ma_break(market_analysis)

        # then
        assert result is True

    def test_is_ma_break_false(self):
        # given
        strategy = PyramidStrategy()
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": True
        }

        # when
        result = strategy._is_ma_break(market_analysis)

        # then
        assert result is False

    def test_is_sharp_decline_true(self):
        # given
        strategy = PyramidStrategy()
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

        # when
        result = strategy._is_sharp_decline(ticker)

        # then
        assert result is True

    def test_is_sharp_decline_false(self):
        # given
        strategy = PyramidStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=49000000.0,
            opening_price=50000000.0,
            high_price=50500000.0,
            low_price=48500000.0,
            prev_closing_price=50000000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.02,
            timestamp=1640995200000
        )

        # when
        result = strategy._is_sharp_decline(ticker)

        # then
        assert result is False

    def test_is_max_position_reached_true(self):
        # given
        strategy = PyramidStrategy()
        holding_account = Account(currency="BTC", balance=1.0)
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
        accounts = [
            Account(currency="KRW", balance=45000000.0),  # 4500만원
            Account(currency="BTC", balance=1.0)  # 5000만원 (총 9500만원 대비 약 52.6% > 10%)
        ]

        # when
        result = strategy._is_max_position_reached(holding_account, ticker, accounts)

        # then
        assert result is True

    def test_is_max_position_reached_false(self):
        # given
        strategy = PyramidStrategy()
        holding_account = Account(currency="BTC", balance=0.1)
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
        accounts = [
            Account(currency="KRW", balance=100000000.0),  # 1억원
            Account(currency="BTC", balance=0.1)  # 500만원 (총 1.05억원 대비 약 4.7% < 10%)
        ]

        # when
        result = strategy._is_max_position_reached(holding_account, ticker, accounts)

        # then
        assert result is False

    def test_is_max_position_reached_zero_balance(self):
        # given
        strategy = PyramidStrategy()
        holding_account = Account(currency="BTC", balance=1.0)
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
        accounts = [Account(currency="KRW", balance=0.0)]

        # when
        result = strategy._is_max_position_reached(holding_account, ticker, accounts)

        # then
        assert result is True

    @patch('app.strategies.pyramid_strategy.MAX_POSITION_PERCENT', 15.0)
    def test_max_position_from_constants(self):
        # given
        strategy = PyramidStrategy()

        # when & then
        assert strategy.max_position_percent == 15.0