from strategies.turtle.constants import MAX_POSITION_UNIT, PYRAMID_N_MULTIPLIER, STOP_LOSS_N_MULTIPLIER
from strategies.turtle.schema import TurtlePosition


class TurtleStrategy():
    def __init__(
        self,
        max_position_unit: float = MAX_POSITION_UNIT,
        pyramid_n_multiplier: float = PYRAMID_N_MULTIPLIER,
        stop_loss_n_multiplier: float = STOP_LOSS_N_MULTIPLIER,
    ):
        self.max_position_unit = max_position_unit
        self.pyramid_n_multiplier = pyramid_n_multiplier
        self.stop_loss_n_multiplier = stop_loss_n_multiplier
        self.positions: list[TurtlePosition] = []

    def buy(self, current_price: float, system1_max_price: float, system2_max_price: float, last_trade_was_profitable: bool | None) -> bool:
        if self.positions:
            return False

        if current_price > system1_max_price and not last_trade_was_profitable:
            return True

        if current_price > system2_max_price:
            return True

        return False

    def sell(self, current_price: float, system_min_price: float, N: float) -> bool:
        if not self.positions:
            return False

        if current_price < system_min_price:
            return True

        latest_position: TurtlePosition | None = self._get_latest_position()
        if latest_position and current_price < latest_position.price - (self.stop_loss_n_multiplier * N):
            return True

        return False


    def pyramid_buy(self, current_price: float, N: float) -> bool:
        if not self.positions:
            return False

        if len(self.positions) >= self.max_position_unit:
            return False

        latest_position = self._get_latest_position()
        if not latest_position:
            return False

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

