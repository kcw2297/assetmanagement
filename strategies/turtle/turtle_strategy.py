from strategies.turtle.constants import MAX_POSITION_UNIT
from strategies.turtle.schema import TurtlePosition


class TurtleStrategy():
    def __init__(
        self,
        max_position_unit: float = MAX_POSITION_UNIT,
    ):
        self.max_position_unit = max_position_unit

        self.positions: list[TurtlePosition] = []
        self.total_units = 0
        self.last_trade_was_profitable: bool | None = None
        self.entry_system: int | None = None

    def buy(self, current_price: float, system1_max_price: float, system2_max_price: float) -> bool:
        if self.positions:
            return False

        if current_price > system1_max_price and not self.last_trade_was_profitable:
            self.entry_system = 1
            return True

        if current_price > system2_max_price:
            self.entry_system = 2
            return True

        return False

    def sell(self, current_price: float, system_min_price: float, N: float) -> bool:
        if not self.positions:
            return False

        if current_price < system_min_price:
            return True

        latest_position: TurtlePosition | None = self.get_latest_position()
        if latest_position and current_price < latest_position.price - (2 * N):
            return True

        return False


    def pyramid_buy(self, current_price: float, total_asset: float, N: float) -> bool:
        if not self.positions:
            return False

        current_position_value = sum(pos.value for pos in self.positions)
        if current_position_value >= total_asset * self.max_position_unit:
            return False

        latest_position = self.get_latest_position()
        if not latest_position:
            return False

        return current_price >= latest_position.price + (0.5 * N)

    def add_position(self, price: float, quantity: int, N: float, trade_date: str):
        unit_number = self.total_units + 1
        position = TurtlePosition(
            price=price,
            quantity=quantity,
            N=N,
            trade_date=trade_date,
            unit_number=unit_number
        )
        self.positions.append(position)
        self.total_units += 1

    def get_latest_position(self) -> TurtlePosition | None:
        if not self.positions:
            return None
        return max(self.positions, key=lambda p: p.trade_date)

    def clear_positions(self, sell_price: float):
        if not self.positions:
            self.positions = []
            self.total_units = 0
            self.entry_system = None
            return

        avg_buy_price = sum(pos.value for pos in self.positions) / sum(pos.quantity for pos in self.positions)
        self.last_trade_was_profitable = sell_price > avg_buy_price

        self.positions = []
        self.total_units = 0
        self.entry_system = None
