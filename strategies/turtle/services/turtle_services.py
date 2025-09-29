from assetmanagement.strategies.turtle.services.buy_service import BuyStrategy
from assetmanagement.strategies.turtle.services.sell_service import SellStrategy
from assetmanagement.strategies.turtle.services.pyramid_service import PyramidStrategy
from assetmanagement.accounts.bithumb.v2_1_0.services.ticker_service import TickerService
from assetmanagement.accounts.bithumb.v2_1_0.services.candle_service import CandleService
from assetmanagement.accounts.bithumb.v2_1_0.services.account_service import AccountService
from assetmanagement.strategies.turtle.schema import TurtleSignal
from assetmanagement.strategies.turtle.enums import SignalType
from accounts.bithumb.v2_1_0.schema import Ticker



class TurtleCoordinator:
    def __init__(
        self,
        ticker_service: TickerService,
        candle_service: CandleService,
        account_service: AccountService,
        client
    ):
        self.ticker_service = ticker_service
        self.candle_service = candle_service
        self.account_service = account_service
        self.buy_strategy = BuyStrategy()
        self.sell_strategy = SellStrategy()
        self.pyramid_strategy = PyramidStrategy(client)

    def analyze_comprehensive_signal(self, market: str) -> TurtleSignal:
        ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        if not ticker or not market_analysis:
            return TurtleSignal(
                market=market,
                signal_type=SignalType.HOLD,
                reason="데이터 조회 실패",
                current_price=0.0
            )

        currency = market.split('-')[1]
        holding_account = None
        for acc in accounts:
            if acc.currency == currency:
                holding_account = acc
                break

        if holding_account and holding_account.balance > 0:
            sell_signal = self.sell_strategy.analyze(market, ticker, market_analysis, accounts)
            if sell_signal.signal_type == SignalType.SELL:
                return sell_signal

            return self.pyramid_strategy.analyze(market, ticker, market_analysis, accounts)
        else:
            return self.buy_strategy.analyze(market, ticker, market_analysis, accounts)

    def analyze_buy_signal(self, market: str) -> TurtleSignal:
        ticker: Ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        return self.buy_strategy.analyze(market, ticker, market_analysis, accounts)

    def analyze_sell_signal(self, market: str) -> TurtleSignal:
        ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        return self.sell_strategy.analyze(market, ticker, market_analysis, accounts)

    def analyze_pyramid_signal(self, market: str) -> TurtleSignal:
        ticker = self.ticker_service.get_ticker(market)
        market_analysis = self.candle_service.get_market_analysis(market)
        accounts = self.account_service.get_accounts()

        return self.pyramid_strategy.analyze(market, ticker, market_analysis, accounts)