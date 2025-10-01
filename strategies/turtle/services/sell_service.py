from strategies.turtle.services.base_service import BaseStrategy
from strategies.turtle.schema import TurtleSignal


class SellStrategy(BaseStrategy):
    def __init__(self, unit: float):
        super().__init__(unit)
        

    def analyze(self) -> TurtleSignal:

        return