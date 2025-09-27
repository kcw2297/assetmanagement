import pytest
from unittest.mock import Mock
from app.strategies.sell_strategy import SellStrategy
from app.schema import Ticker, Account, TurtleSignal
from app.enums import SignalType


class TestSellStrategy:
    def test_analyze_sharp_decline_sell(self):
        # given
        strategy = SellStrategy()
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

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.SELL
        assert signal.target_amount == 0.5
        assert signal.confidence == 1.0
        assert "당일 5% 이상 급락" in signal.reason

    def test_analyze_ma10_break_sell(self):
        # given
        strategy = SellStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=47500000.0,
            opening_price=48000000.0,
            high_price=48500000.0,
            low_price=47000000.0,
            prev_closing_price=48000000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.01,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": False,
            "moving_averages": {"ma5": 46000000.0, "ma10": 48000000.0}
        }
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.SELL
        assert signal.target_amount == 1.0
        assert signal.confidence == 0.9
        assert "10일선" in signal.reason
        assert "손절" in signal.reason

    def test_analyze_ma5_break_partial_sell(self):
        # given
        strategy = SellStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=47500000.0,
            opening_price=48000000.0,
            high_price=48500000.0,
            low_price=47000000.0,
            prev_closing_price=48000000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.01,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": False,
            "is_above_ma10": True,
            "moving_averages": {"ma5": 48000000.0, "ma10": 45000000.0}
        }
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.SELL
        assert signal.target_amount == 0.5  # 50% 매도
        assert signal.confidence == 0.7
        assert "5일선" in signal.reason
        assert "50% 익절" in signal.reason

    def test_analyze_no_sell_condition(self):
        # given
        strategy = SellStrategy()
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
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "매도 조건 미충족" in signal.reason

    def test_analyze_no_holdings(self):
        # given
        strategy = SellStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.05,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": False,
            "is_above_ma10": False,
            "moving_averages": {"ma5": 48000000.0, "ma10": 45000000.0}
        }
        accounts = [Account(currency="KRW", balance=10000000.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "보유 중이지 않음" in signal.reason

    def test_analyze_zero_balance(self):
        # given
        strategy = SellStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.05,
            timestamp=1640995200000
        )
        market_analysis = {
            "is_above_ma5": False,
            "is_above_ma10": False,
            "moving_averages": {"ma5": 48000000.0, "ma10": 45000000.0}
        }
        accounts = [Account(currency="BTC", balance=0.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert "보유 중이지 않음" in signal.reason

    def test_analyze_no_ticker(self):
        # given
        strategy = SellStrategy()
        market_analysis = {
            "is_above_ma5": True,
            "is_above_ma10": True,
            "moving_averages": {"ma5": 48000000.0, "ma10": 45000000.0}
        }
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", None, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"

    def test_analyze_no_market_analysis(self):
        # given
        strategy = SellStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.05,
            timestamp=1640995200000
        )
        accounts = [Account(currency="BTC", balance=1.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, None, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"

    def test_is_sharp_decline_true(self):
        # given
        strategy = SellStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
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

    def test_is_sharp_decline_false_not_fall(self):
        # given
        strategy = SellStrategy()
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
            change_rate=0.05,
            timestamp=1640995200000
        )

        # when
        result = strategy._is_sharp_decline(ticker)

        # then
        assert result is False

    def test_is_sharp_decline_false_small_decline(self):
        # given
        strategy = SellStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=49500000.0,
            high_price=50500000.0,
            low_price=49000000.0,
            prev_closing_price=49500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.03,
            timestamp=1640995200000
        )

        # when
        result = strategy._is_sharp_decline(ticker)

        # then
        assert result is False