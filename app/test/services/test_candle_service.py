import pytest
from unittest.mock import Mock
from app.services.candle_service import CandleService
from app.schema import Candle


class TestCandleService:
    def test_get_daily_candles_success(self):
        # given
        mock_client = Mock()
        mock_response = {
            "status_code": 200,
            "data": [
                {
                    "market": "KRW-BTC",
                    "candle_date_time_kst": "2024-01-20T09:00:00",
                    "opening_price": "49000000.0",
                    "high_price": "51000000.0",
                    "low_price": "48000000.0",
                    "trade_price": "50000000.0",
                    "candle_acc_trade_volume": "100.0",
                    "timestamp": "1640995200000"
                },
                {
                    "market": "KRW-BTC",
                    "candle_date_time_kst": "2024-01-19T09:00:00",
                    "opening_price": "48000000.0",
                    "high_price": "49500000.0",
                    "low_price": "47000000.0",
                    "trade_price": "49000000.0",
                    "candle_acc_trade_volume": "150.0",
                    "timestamp": "1640908800000"
                }
            ]
        }
        mock_client.call_public_api.return_value = mock_response
        service = CandleService(mock_client)

        # when
        candles = service.get_daily_candles("KRW-BTC", 2)

        # then
        assert len(candles) == 2
        assert candles[0].market == "KRW-BTC"
        assert candles[0].trade_price == 49000000.0  # 역순 정렬됨
        mock_client.call_public_api.assert_called_once_with("/v1/candles/days", {"market": "KRW-BTC", "count": 2})

    def test_get_daily_candles_api_failure(self):
        # given
        mock_client = Mock()
        mock_client.call_public_api.return_value = {"status_code": 400}
        service = CandleService(mock_client)

        # when
        candles = service.get_daily_candles("KRW-BTC", 20)

        # then
        assert candles == []

    def test_get_daily_candles_with_exception(self):
        # given
        mock_client = Mock()
        mock_client.call_public_api.side_effect = Exception("API Error")
        service = CandleService(mock_client)

        # when
        candles = service.get_daily_candles("KRW-BTC", 20)

        # then
        assert candles == []

    def test_calculate_moving_averages_success(self):
        # given
        candles = [
            Candle(market="KRW-BTC", candle_date_time_kst="2024-01-25",
                   opening_price=50000, high_price=51000, low_price=49000,
                   trade_price=50500, candle_acc_trade_volume=100, timestamp=1640995200000),
            Candle(market="KRW-BTC", candle_date_time_kst="2024-01-24",
                   opening_price=49000, high_price=50000, low_price=48000,
                   trade_price=49500, candle_acc_trade_volume=100, timestamp=1640908800000),
            Candle(market="KRW-BTC", candle_date_time_kst="2024-01-23",
                   opening_price=48000, high_price=49000, low_price=47000,
                   trade_price=48500, candle_acc_trade_volume=100, timestamp=1640822400000),
            Candle(market="KRW-BTC", candle_date_time_kst="2024-01-22",
                   opening_price=47000, high_price=48000, low_price=46000,
                   trade_price=47500, candle_acc_trade_volume=100, timestamp=1640736000000),
            Candle(market="KRW-BTC", candle_date_time_kst="2024-01-21",
                   opening_price=46000, high_price=47000, low_price=45000,
                   trade_price=46500, candle_acc_trade_volume=100, timestamp=1640649600000)
        ]
        service = CandleService(Mock())

        # when
        ma = service.calculate_moving_averages(candles)

        # then
        assert ma.ma5 == 48500.0  # (50500+49500+48500+47500+46500)/5
        assert ma.ma10 == 0.0     # 데이터 부족
        assert ma.ma20 == 0.0     # 데이터 부족

    def test_calculate_moving_averages_insufficient_data(self):
        # given
        candles = [
            Candle(market="KRW-BTC", candle_date_time_kst="2024-01-25",
                   opening_price=50000, high_price=51000, low_price=49000,
                   trade_price=50500, candle_acc_trade_volume=100, timestamp=1640995200000)
        ]
        service = CandleService(Mock())

        # when
        ma = service.calculate_moving_averages(candles)

        # then
        assert ma.ma5 == 0.0
        assert ma.ma10 == 0.0
        assert ma.ma20 == 0.0

    def test_calculate_moving_averages_empty_candles(self):
        # given
        candles = []
        service = CandleService(Mock())

        # when
        ma = service.calculate_moving_averages(candles)

        # then
        assert ma.ma5 == 0.0
        assert ma.ma10 == 0.0
        assert ma.ma20 == 0.0

    def test_get_market_analysis_success(self):
        # given
        mock_client = Mock()
        mock_response = {"status_code": 200, "data": []}
        for i in range(20):
            mock_response["data"].append({
                "market": "KRW-BTC",
                "candle_date_time_kst": f"2024-01-{20-i:02d}T09:00:00",
                "opening_price": str(49000000.0 + i * 100000),
                "high_price": str(51000000.0 + i * 100000),
                "low_price": str(48000000.0 + i * 100000),
                "trade_price": str(50000000.0 + i * 100000),
                "candle_acc_trade_volume": "100.0",
                "timestamp": str(1640995200000 - i * 86400000)
            })
        mock_client.call_public_api.return_value = mock_response
        service = CandleService(mock_client)

        # when
        analysis = service.get_market_analysis("KRW-BTC")

        # then
        assert analysis is not None
        assert "recent_high_20d" in analysis
        assert "moving_averages" in analysis
        assert "is_above_ma5" in analysis
        assert "is_above_ma10" in analysis
        assert "is_above_ma20" in analysis

    def test_get_market_analysis_no_candles(self):
        # given
        mock_client = Mock()
        mock_client.call_public_api.return_value = {"status_code": 400}
        service = CandleService(mock_client)

        # when
        analysis = service.get_market_analysis("KRW-BTC")

        # then
        assert analysis == {}