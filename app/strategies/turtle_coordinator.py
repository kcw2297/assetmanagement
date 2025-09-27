from app.strategies.buy_strategy import BuyStrategy
from app.strategies.sell_strategy import SellStrategy
from app.strategies.pyramid_strategy import PyramidStrategy
from app.services.ticker_service import TickerService
from app.services.candle_service import CandleService
from app.services.account_service import AccountService
from app.schema import TurtleSignal


class TurtleCoordinator:
    """터틀 트레이딩 전략 코디네이터 - 전략들을 조합하여 최종 판단"""

    def __init__(
        self,
        ticker_service: TickerService,
        candle_service: CandleService,
        account_service: AccountService,
        position_size_percent: float = 2.0,
        max_position_percent: float = 10.0
    ):
        self.ticker_service = ticker_service
        self.candle_service = candle_service
        self.account_service = account_service

        # 전략 인스턴스 생성
        self.buy_strategy = BuyStrategy(position_size_percent)
        self.sell_strategy = SellStrategy()
        self.pyramid_strategy = PyramidStrategy(max_position_percent)

    def analyze_comprehensive_signal(self, market: str) -> TurtleSignal:
        """종합 신호 분석"""
        # 기본 데이터 수집
        ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        if not ticker or not market_analysis:
            return TurtleSignal(
                market=market,
                signal_type="HOLD",
                reason="데이터 조회 실패",
                current_price=0.0
            )

        # 보유 여부 확인
        currency = market.split('-')[1]
        holding_account = None
        for acc in accounts:
            if acc.currency == currency:
                holding_account = acc
                break

        # 전략 선택 및 실행
        if holding_account and holding_account.balance > 0:
            # 보유 중이면 매도 신호 우선 확인
            sell_signal = self.sell_strategy.analyze(market, ticker, market_analysis, accounts)
            if sell_signal.signal_type == "SELL":
                return sell_signal

            # 매도 신호가 없으면 피라미딩 확인
            return self.pyramid_strategy.analyze(market, ticker, market_analysis, accounts)
        else:
            # 미보유 시 매수 신호 확인
            return self.buy_strategy.analyze(market, ticker, market_analysis, accounts)

    def analyze_buy_signal(self, market: str) -> TurtleSignal:
        """매수 신호만 분석"""
        ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        return self.buy_strategy.analyze(market, ticker, market_analysis, accounts)

    def analyze_sell_signal(self, market: str) -> TurtleSignal:
        """매도 신호만 분석"""
        ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        return self.sell_strategy.analyze(market, ticker, market_analysis, accounts)

    def analyze_pyramid_signal(self, market: str) -> TurtleSignal:
        """피라미딩 신호만 분석"""
        ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        return self.pyramid_strategy.analyze(market, ticker, market_analysis, accounts)