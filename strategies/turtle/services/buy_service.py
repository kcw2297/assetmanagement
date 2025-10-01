from typing import Optional
from assetmanagement.strategies.turtle.services.base_service import BaseStrategy
from assetmanagement.strategies.turtle.schema import TurtleSignal, Position
from assetmanagement.strategies.turtle.enums import SignalType


class BuyStrategy(BaseStrategy):
    def __init__(self, unit: float):
        super().__init__(unit)

    def run(
        self,
        market: str,
        current_price: float,
        high_20: float,
        high_55: float,
        breakout_period: int,
        available_krw: float,
        position: Optional[Position] = None
    ) -> bool:

        # 이미 포지션이 있으면 매수하지 않음 (피라미딩은 별도 로직)
        if position is not None:
            return False

        # 사용 가능한 원화가 없으면 매수 불가
        if available_krw <= 0:
            return False

        # 돌파 기준 선택 (L1: 20일, L2: 55일)
        breakout_high = high_20 if breakout_period == 20 else high_55

        # 신고가 돌파 확인
        if current_price > breakout_high:
            # 초기 매수 금액: 전체 자금의 2% (BASE_UNIT_PERCENT)
            target_amount = available_krw * (self.unit / 100)

            return True

        # 신고가 돌파하지 않으면 홀드
        return False

