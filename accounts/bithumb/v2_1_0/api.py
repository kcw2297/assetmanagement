from accounts.bithumb.v2_1_0.config.bithumb_client import BithumbClient
from accounts.bithumb.v2_1_0.services.account_service import AccountService
from accounts.bithumb.v2_1_0.services.ticker_service import TickerService
from accounts.bithumb.v2_1_0.services.order_service import OrderService
from accounts.bithumb.v2_1_0.services.candle_service import CandleService


class BithumbAPI:
    def __init__(self):
        self._client = BithumbClient()
        self._account_service = None
        self._ticker_service = None
        self._order_service = None
        self._candle_service = None

    @property
    def account(self) -> AccountService:
        """계정 관련 서비스"""
        if self._account_service is None:
            self._account_service = AccountService(self._client)
        return self._account_service

    @property
    def ticker(self) -> TickerService:
        """시세 조회 서비스"""
        if self._ticker_service is None:
            self._ticker_service = TickerService(self._client)
        return self._ticker_service

    @property
    def order(self) -> OrderService:
        """주문 서비스"""
        if self._order_service is None:
            self._order_service = OrderService(self._client)
        return self._order_service

    @property
    def candle(self) -> CandleService:
        """캔들 조회 서비스"""
        if self._candle_service is None:
            self._candle_service = CandleService(self._client)
        return self._candle_service
