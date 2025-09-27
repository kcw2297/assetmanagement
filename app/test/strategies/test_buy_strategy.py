import pytest
from unittest.mock import Mock, patch
from app.strategies.buy_strategy import BuyStrategy
from app.schema import Ticker, Account, TurtleSignal
from app.enums import SignalType


class TestBuyStrategy:
    def test_analyze_breakout_with_volume_decline(self):
        # given
        strategy = BuyStrategy()
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

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.BUY
        assert signal.target_amount == 200000.0  # 10M * 2%
        assert signal.confidence == 0.8
        assert "20일 신고가" in signal.reason
        assert "거래량 감소 음봉" in signal.reason

    def test_analyze_breakout_without_volume_decline(self):
        # given
        strategy = BuyStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=52000000.0,
            opening_price=51000000.0,
            high_price=52500000.0,
            low_price=50500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="RISE",
            change_rate=0.02,
            timestamp=1640995200000
        )
        market_analysis = {"recent_high_20d": 51000000.0}
        accounts = [Account(currency="KRW", balance=10000000.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.confidence == 0.5
        assert "거래량 감소 음봉 대기 중" in signal.reason

    def test_analyze_no_breakout(self):
        # given
        strategy = BuyStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=51000000.0,
            high_price=51500000.0,
            low_price=49500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.03,
            timestamp=1640995200000
        )
        market_analysis = {"recent_high_20d": 52000000.0}
        accounts = [Account(currency="KRW", balance=10000000.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.confidence == 0.0
        assert "미돌파" in signal.reason

    def test_analyze_no_ticker(self):
        # given
        strategy = BuyStrategy()
        market_analysis = {"recent_high_20d": 52000000.0}
        accounts = [Account(currency="KRW", balance=10000000.0)]

        # when
        signal = strategy.analyze("KRW-BTC", None, market_analysis, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"

    def test_analyze_no_market_analysis(self):
        # given
        strategy = BuyStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=51000000.0,
            high_price=51500000.0,
            low_price=49500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.03,
            timestamp=1640995200000
        )
        accounts = [Account(currency="KRW", balance=10000000.0)]

        # when
        signal = strategy.analyze("KRW-BTC", ticker, None, accounts)

        # then
        assert signal.signal_type == SignalType.HOLD
        assert signal.reason == "데이터 조회 실패"

    def test_is_breakout_true(self):
        # given
        strategy = BuyStrategy()

        # when
        result = strategy._is_breakout(52000000.0, 51000000.0)

        # then
        assert result is True

    def test_is_breakout_false(self):
        # given
        strategy = BuyStrategy()

        # when
        result = strategy._is_breakout(50000000.0, 51000000.0)

        # then
        assert result is False

    def test_is_breakout_equal(self):
        # given
        strategy = BuyStrategy()

        # when
        result = strategy._is_breakout(51000000.0, 51000000.0)

        # then
        assert result is True

    def test_is_volume_decline_bear_true(self):
        # given
        strategy = BuyStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=51000000.0,
            high_price=51500000.0,
            low_price=49500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.02,
            timestamp=1640995200000
        )

        # when
        result = strategy._is_volume_decline_bear(ticker)

        # then
        assert result is True

    def test_is_volume_decline_bear_false_rise(self):
        # given
        strategy = BuyStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=51000000.0,
            high_price=51500000.0,
            low_price=49500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="RISE",
            change_rate=0.02,
            timestamp=1640995200000
        )

        # when
        result = strategy._is_volume_decline_bear(ticker)

        # then
        assert result is False

    def test_is_volume_decline_bear_false_large_fall(self):
        # given
        strategy = BuyStrategy()
        ticker = Ticker(
            market="KRW-BTC",
            trade_price=50000000.0,
            opening_price=51000000.0,
            high_price=51500000.0,
            low_price=49500000.0,
            prev_closing_price=51500000.0,
            trade_volume=100.0,
            acc_trade_volume_24h=2000.0,
            change="FALL",
            change_rate=-0.05,
            timestamp=1640995200000
        )

        # when
        result = strategy._is_volume_decline_bear(ticker)

        # then
        assert result is False

    @patch('app.strategies.buy_strategy.POSITION_SIZE_PERCENT', 3.0)
    def test_position_size_from_constants(self):
        # given
        strategy = BuyStrategy()

        # when & then
        assert strategy.position_size_percent == 3.0