from assetmanagement.strategies.turtle.services.base_services import BaseStrategy
from assetmanagement.strategies.turtle.schema import TurtleSignal
from assetmanagement.strategies.turtle.constants import POSITION_SIZE_PERCENT
from assetmanagement.strategies.turtle.enums import SignalType

from accounts.bithumb.v2_1_0.schema import Ticker, Account

class BuyStrategy(BaseStrategy):
    def __init__(self):
        self.position_size_percent = POSITION_SIZE_PERCENT

    def analyze(self, market: str, ticker: Ticker, market_analysis: dict, accounts: list[Account]) -> TurtleSignal:
        if not ticker or not market_analysis:
            return self._create_hold_signal(market, "데이터 조회 실패", 0.0)

        current_price = ticker.trade_price
        recent_high_20d = market_analysis['recent_high_20d']

        breakout_signal = self._is_breakout(current_price, recent_high_20d)

        volume_decline = self._is_volume_decline_bear(ticker)

        if breakout_signal and volume_decline:
            return self._create_buy_signal(market, current_price, recent_high_20d, accounts)
        elif breakout_signal:
            return self._create_hold_signal(
                market,
                f"20일 신고가 돌파했으나 거래량 감소 음봉 대기 중",
                current_price,
                confidence=0.5
            )
        else:
            return self._create_hold_signal(
                market,
                f"20일 신고가({recent_high_20d:,.0f}) 미돌파",
                current_price
            )

    def _is_breakout(self, current_price: float, high_20d: float) -> bool:
        return current_price >= high_20d

    def _is_volume_decline_bear(self, ticker: Ticker) -> bool:
        return ticker.change == "FALL" and abs(ticker.change_rate) <= 0.03

    def _create_buy_signal(self, market: str, current_price: float, high_20d: float, accounts: list[Account]) -> TurtleSignal:
        krw_balance = self._get_krw_balance(accounts)
        target_amount = krw_balance * (self.position_size_percent / 100)

        return TurtleSignal(
            market=market,
            signal_type=SignalType.BUY,
            reason=f"20일 신고가({high_20d:,.0f}) 돌파 + 거래량 감소 음봉",
            current_price=current_price,
            target_amount=target_amount,
            confidence=0.8
        )

    def _create_hold_signal(self, market: str, reason: str, current_price: float, confidence: float = 0.0) -> TurtleSignal:
        return TurtleSignal(
            market=market,
            signal_type=SignalType.HOLD,
            reason=reason,
            current_price=current_price,
            confidence=confidence
        )