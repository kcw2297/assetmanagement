from strategies.turtle.constants import (
    L1_BASE_BUY_PERIOD,
    L1_BASE_SELL_PERIOD,
    MAX_POSITION_PERCENT,
    BASE_UNIT_PERCENT
)
from strategies.turtle.schema import TurtlePosition


class TurtleStrategy():
    def __init__(
        self,
        buy_period: int = L1_BASE_BUY_PERIOD,
        sell_period: int = L1_BASE_SELL_PERIOD,
        max_position: float = MAX_POSITION_PERCENT,
        unit_percent: float = BASE_UNIT_PERCENT
    ):
        self.buy_period = buy_period
        self.sell_period = sell_period
        self.max_position = max_position
        self.unit_percent = unit_percent

        self.positions: list[TurtlePosition] = []
        self.total_units = 0

    def buy(self, current_price: float, prices: list[float]) -> bool:
        if len(prices) < self.buy_period:
            raise ValueError(f"prices의 개수({len(prices)})가 필요한 매수 기간({self.buy_period})보다 작습니다.")

        if self.positions:
            return False

        return current_price > max(prices)

    def sell(self, current_price: float, prices: list[float], N: float) -> bool:
        if len(prices) < self.sell_period:
            raise ValueError(f"prices의 개수({len(prices)})가 필요한 매도 기간({self.sell_period})보다 작습니다.")

        if current_price < min(prices):
            return True

        if self.positions:
            latest_position = self.get_latest_position()
            if latest_position and current_price < latest_position.price - (2 * N):
                return True

        return False

    def pyramid_buy(self, current_price: float, total_asset: float, N: float) -> bool:
        if not self.positions:
            return False

        current_position_value = sum(pos.value for pos in self.positions)
        if current_position_value >= total_asset * self.max_position:
            return False

        latest_position = self.get_latest_position()
        if not latest_position:
            return False

        return current_price >= latest_position.price + N

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

    def clear_positions(self):
        self.positions = []
        self.total_units = 0
