from strategies.turtle.constants import (
    MAX_POSITION_UNIT,
    PYRAMID_N_MULTIPLIER,
    STOP_LOSS_N_MULTIPLIER,
    L1_BASE_BUY_PERIOD,
    L2_BASE_BUY_PERIOD,
    L1_BASE_SELL_PERIOD,
    L2_BASE_SELL_PERIOD
)
from strategies.turtle.schema import TurtlePosition
from strategies.turtle.enums import TurtleSystemType
from common.schema import OHLC
from indicators.moving_average import MovingAverage


class TurtleStrategy():
    def __init__(
        self,
        max_position_unit: float = MAX_POSITION_UNIT,
        pyramid_n_multiplier: float = PYRAMID_N_MULTIPLIER,
        stop_loss_n_multiplier: float = STOP_LOSS_N_MULTIPLIER,
        system1_buy_period: int = L1_BASE_BUY_PERIOD,
        system2_buy_period: int = L2_BASE_BUY_PERIOD,
        system1_sell_period: int = L1_BASE_SELL_PERIOD,
        system2_sell_period: int = L2_BASE_SELL_PERIOD
    ):
        self.max_position_unit = max_position_unit
        self.pyramid_n_multiplier = pyramid_n_multiplier
        self.stop_loss_n_multiplier = stop_loss_n_multiplier
        self.system1_buy_period = system1_buy_period
        self.system2_buy_period = system2_buy_period
        self.system1_sell_period = system1_sell_period
        self.system2_sell_period = system2_sell_period
        self.positions: list[TurtlePosition] = []
        self.last_trade_was_profitable: bool | None = None
        self.entry_system: TurtleSystemType = TurtleSystemType.ONE

    def buy(self, current_price: float, ohlcs: list[OHLC]) -> bool:
        if self.positions: # 이미 매수 기록 존재 => pyramid_buy 수행
            return False
        
        if self.entry_system == TurtleSystemType.ONE:
            self._validate_ohlcs_period(ohlcs, self.system1_buy_period)
        elif self.entry_system == TurtleSystemType.TWO:
            self._validate_ohlcs_period(ohlcs, self.system2_buy_period)

        return current_price > max(ohlc.close for ohlc in ohlcs)

    def sell(self, current_price: float, ohlcs: list[OHLC], N: float) -> bool:
        if not self.positions:
            return False

        if self.entry_system == TurtleSystemType.ONE:
            self._validate_ohlcs_period(ohlcs, self.system1_sell_period)
        elif self.entry_system == TurtleSystemType.TWO:
            self._validate_ohlcs_period(ohlcs, self.system2_sell_period)

        if current_price < min(ohlc.close for ohlc in ohlcs): # system 최저가 이탈
            return True

        latest_position: TurtlePosition | None = self._get_latest_position()
        
        # 2N 손절
        if latest_position and current_price < latest_position.price - (self.stop_loss_n_multiplier * N):
            return True

        return False

    def pyramid_buy(self, current_price: float, N: float) -> bool:
        if not self.positions:
            return False

        # 최대 유닛 검증
        if len(self.positions) >= self.max_position_unit:
            return False


        latest_position: TurtlePosition | None = self._get_latest_position()
        if not latest_position:
            return False

        # 최근 진입가 대비 1N 상승 시 추가 매수
        return current_price >= latest_position.price + (self.pyramid_n_multiplier * N)

    def add_position(self, price: float, quantity: int, trade_date: str):
        position = TurtlePosition(
            price=price,
            quantity=quantity,
            trade_date=trade_date,
        )
        self.positions.append(position)

    def _get_latest_position(self) -> TurtlePosition | None:
        if not self.positions:
            return None
        return max(self.positions, key=lambda p: p.trade_date)

    def _get_earliest_position(self) -> TurtlePosition | None:
        if not self.positions:
            return None
        return min(self.positions, key=lambda p: p.trade_date)

    def _validate_ohlcs_period(self, ohlcs: list[OHLC], period: int):
        if len(ohlcs) != period:
            raise ValueError(f"ohlcs 개수({len(ohlcs)})가 period({period})와 동일하지 않습니다.")
