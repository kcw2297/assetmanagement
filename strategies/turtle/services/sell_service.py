from assetmanagement.strategies.turtle.services.base_services import BaseStrategy
from assetmanagement.strategies.turtle.schema import TurtleSignal, Ticker, Account
from assetmanagement.strategies.turtle.enums import SignalType


class SellStrategy(BaseStrategy):
    """매도 전략"""

    def analyze(self, market: str, ticker: Ticker, market_analysis: dict, accounts: list[Account]) -> TurtleSignal:
        """매도 신호 분석"""
        if not ticker or not market_analysis:
            return self._create_hold_signal(market, "데이터 조회 실패", 0.0)

        current_price = ticker.trade_price
        currency = market.split('-')[1]  # KRW-BTC -> BTC
        holding_account = self._get_account_by_currency(accounts, currency)

        # 보유 중이지 않으면 매도 불가
        if not holding_account or holding_account.balance <= 0:
            return self._create_hold_signal(market, "보유 중이지 않음", current_price)

        # 1. 당일 5% 이상 급락 (즉시 전량 매도)
        if self._is_sharp_decline(ticker):
            return self._create_sell_signal(
                market, current_price, holding_account.balance,
                f"당일 5% 이상 급락 ({ticker.change_rate:.2%})", 1.0
            )

        # 2. 10일선 이탈 (손절 - 전량 매도)
        if not market_analysis['is_above_ma10']:
            return self._create_sell_signal(
                market, current_price, holding_account.balance,
                f"10일선({market_analysis['moving_averages']['ma10']:,.0f}) 이탈 손절", 0.9
            )

        # 3. 5일선 이탈 (50% 익절)
        if not market_analysis['is_above_ma5']:
            return self._create_sell_signal(
                market, current_price, holding_account.balance * 0.5,
                f"5일선({market_analysis['moving_averages']['ma5']:,.0f}) 이탈 - 50% 익절", 0.7
            )

        return self._create_hold_signal(market, "매도 조건 미충족", current_price)

    def _is_sharp_decline(self, ticker: Ticker) -> bool:
        """당일 5% 이상 급락 여부"""
        return ticker.change == "FALL" and abs(ticker.change_rate) >= 0.05

    def _create_sell_signal(self, market: str, current_price: float, amount: float, reason: str, confidence: float) -> TurtleSignal:
        """매도 신호 생성"""
        return TurtleSignal(
            market=market,
            signal_type=SignalType.SELL,
            reason=reason,
            current_price=current_price,
            target_amount=amount,
            confidence=confidence
        )

    def _create_hold_signal(self, market: str, reason: str, current_price: float) -> TurtleSignal:
        """홀드 신호 생성"""
        return TurtleSignal(
            market=market,
            signal_type=SignalType.HOLD,
            reason=reason,
            current_price=current_price
        )