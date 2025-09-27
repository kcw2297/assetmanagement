from app.strategies.base_strategy import BaseStrategy
from app.schema import TurtleSignal, Ticker, Account


class BuyStrategy(BaseStrategy):
    """매수 전략"""

    def __init__(self, position_size_percent: float = 2.0):
        self.position_size_percent = position_size_percent

    def analyze(self, market: str, ticker: Ticker, market_analysis: dict, accounts: list[Account]) -> TurtleSignal:
        """매수 신호 분석"""
        if not ticker or not market_analysis:
            return self._create_hold_signal(market, "데이터 조회 실패", 0.0)

        current_price = ticker.trade_price
        recent_high_20d = market_analysis['recent_high_20d']

        # 20일 신고가 돌파 확인
        breakout_signal = self._is_breakout(current_price, recent_high_20d)

        # 거래량 감소 음봉 확인
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
        """20일 신고가 돌파 여부"""
        return current_price >= high_20d

    def _is_volume_decline_bear(self, ticker: Ticker) -> bool:
        """거래량 감소 음봉 여부 (3% 이내 하락)"""
        return ticker.change == "FALL" and abs(ticker.change_rate) <= 0.03

    def _create_buy_signal(self, market: str, current_price: float, high_20d: float, accounts: list[Account]) -> TurtleSignal:
        """매수 신호 생성"""
        krw_balance = self._get_krw_balance(accounts)
        target_amount = krw_balance * (self.position_size_percent / 100)

        return TurtleSignal(
            market=market,
            signal_type="BUY",
            reason=f"20일 신고가({high_20d:,.0f}) 돌파 + 거래량 감소 음봉",
            current_price=current_price,
            target_amount=target_amount,
            confidence=0.8
        )

    def _create_hold_signal(self, market: str, reason: str, current_price: float, confidence: float = 0.0) -> TurtleSignal:
        """홀드 신호 생성"""
        return TurtleSignal(
            market=market,
            signal_type="HOLD",
            reason=reason,
            current_price=current_price,
            confidence=confidence
        )