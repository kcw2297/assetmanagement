from app.strategies.base_strategy import BaseStrategy
from app.schema import TurtleSignal, Ticker, Account
from app.constants import MAX_POSITION_PERCENT
from app.enums import SignalType


class PyramidStrategy(BaseStrategy):
    """추격매수(피라미딩) 전략"""

    def __init__(self, pyramid_profit_percent: float = 5.0):
        self.max_position_percent = MAX_POSITION_PERCENT
        self.pyramid_profit_percent = pyramid_profit_percent

    def analyze(self, market: str, ticker: Ticker, market_analysis: dict, accounts: list[Account]) -> TurtleSignal:
        """추격매수 신호 분석"""
        if not ticker or not market_analysis:
            return self._create_hold_signal(market, "데이터 조회 실패", 0.0)

        currency = market.split('-')[1]  # KRW-BTC -> BTC
        holding_account = self._get_account_by_currency(accounts, currency)

        # 보유 중이지 않으면 피라미딩 불가
        if not holding_account or holding_account.balance <= 0:
            return self._create_hold_signal(market, "보유 중이지 않음 - 피라미딩 불가", ticker.trade_price)

        # 1. 5일/10일선 이탈 시 즉시 중단
        if self._is_ma_break(market_analysis):
            return self._create_hold_signal(market, "5일/10일선 이탈로 피라미딩 중단", ticker.trade_price)

        # 2. 당일 5% 이상 급락 시 즉시 중단
        if self._is_sharp_decline(ticker):
            return self._create_hold_signal(market, "당일 5% 급락으로 피라미딩 중단", ticker.trade_price)

        # 3. 종목별 최대 10% 제한 확인
        if self._is_max_position_reached(holding_account, ticker, accounts):
            return self._create_hold_signal(
                market, f"최대 포지션 한도({self.max_position_percent}%) 도달", ticker.trade_price
            )

        # TODO: 수익 5% 증가마다 추가 매수 로직
        # 현재는 평균매수가 정보가 없어서 구현 보류

        return self._create_hold_signal(market, "피라미딩 조건 미충족", ticker.trade_price)

    def _is_ma_break(self, market_analysis: dict) -> bool:
        """5일/10일선 이탈 여부"""
        return not market_analysis['is_above_ma5'] or not market_analysis['is_above_ma10']

    def _is_sharp_decline(self, ticker: Ticker) -> bool:
        """당일 5% 이상 급락 여부"""
        return ticker.change == "FALL" and abs(ticker.change_rate) >= 0.05

    def _is_max_position_reached(self, holding_account: Account, ticker: Ticker, accounts: list[Account]) -> bool:
        """최대 포지션 한도 도달 여부"""
        total_balance = self._get_krw_balance(accounts)
        if total_balance <= 0:
            return True

        current_krw_value = holding_account.balance * ticker.trade_price
        position_ratio = (current_krw_value / total_balance) * 100

        return position_ratio >= self.max_position_percent

    def _create_hold_signal(self, market: str, reason: str, current_price: float) -> TurtleSignal:
        """홀드 신호 생성"""
        return TurtleSignal(
            market=market,
            signal_type=SignalType.HOLD,
            reason=reason,
            current_price=current_price
        )