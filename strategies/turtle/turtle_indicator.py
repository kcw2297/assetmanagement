from strategies.turtle.constants import L1_BASE_BUY_PERIOD, L2_BASE_BUY_PERIOD, L1_BASE_SELL_PERIOD, L2_BASE_SELL_PERIOD


class TurtleIndicator:
    def __init__(
        self,
        system1_buy_period: int = L1_BASE_BUY_PERIOD,
        system2_buy_period: int = L2_BASE_BUY_PERIOD,
        system1_sell_period: int = L1_BASE_SELL_PERIOD,
        system2_sell_period: int = L2_BASE_SELL_PERIOD
    ):
        self.system1_buy_period = system1_buy_period
        self.system2_buy_period = system2_buy_period
        self.system1_sell_period = system1_sell_period
        self.system2_sell_period = system2_sell_period

    def get_system1_max_price(self, prices: list[float]) -> float:
        if len(prices) < self.system1_buy_period:
            raise ValueError(f"prices 개수({len(prices)})가 system1_buy_period({self.system1_buy_period})보다 작습니다.")
        return max(prices[-self.system1_buy_period:])

    def get_system2_max_price(self, prices: list[float]) -> float:
        if len(prices) < self.system2_buy_period:
            raise ValueError(f"prices 개수({len(prices)})가 system2_buy_period({self.system2_buy_period})보다 작습니다.")
        return max(prices[-self.system2_buy_period:])

    def get_system1_min_price(self, prices: list[float]) -> float:
        if len(prices) < self.system1_sell_period:
            raise ValueError(f"prices 개수({len(prices)})가 system1_sell_period({self.system1_sell_period})보다 작습니다.")
        return min(prices[-self.system1_sell_period:])

    def get_system2_min_price(self, prices: list[float]) -> float:
        if len(prices) < self.system2_sell_period:
            raise ValueError(f"prices 개수({len(prices)})가 system2_sell_period({self.system2_sell_period})보다 작습니다.")
        return min(prices[-self.system2_sell_period:])
