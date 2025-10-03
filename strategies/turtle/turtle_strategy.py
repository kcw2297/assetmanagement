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

    def buy(self, current_price: float, system1_closes: list[float], system2_closes: list[float]) -> bool:
        if self.positions:
            return False

        if len(system1_closes) != self.system1_buy_period:
            raise ValueError(f"system1_closes 개수({len(system1_closes)})가 system1_buy_period({self.system1_buy_period})와 동일하지 않습니다.")
        if len(system2_closes) != self.system2_buy_period:
            raise ValueError(f"system2_closes 개수({len(system2_closes)})가 system2_buy_period({self.system2_buy_period})와 동일하지 않습니다.")

        if current_price > max(system1_closes) and not self.last_trade_was_profitable:
            return True

        if current_price > max(system2_closes):
            return True

        return False

    def sell(self, current_price: float, system_closes: list[float], ohlcs: list[OHLC]) -> bool:
        if not self.positions:
            return False

        N = MovingAverage.calculate_atr(ohlcs, len(ohlcs))

        if current_price < min(system_closes):
            return True

        latest_position: TurtlePosition | None = self._get_latest_position()
        if latest_position and current_price < latest_position.price - (self.stop_loss_n_multiplier * N):
            return True

        return False

    def pyramid_buy(self, current_price: float, ohlcs: list[OHLC]) -> bool:
        if not self.positions:
            return False

        if len(self.positions) >= self.max_position_unit:
            return False

        latest_position = self._get_latest_position()
        if not latest_position:
            return False

        period = len(ohlcs)
        N = MovingAverage.calculate_atr(ohlcs, period)
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

