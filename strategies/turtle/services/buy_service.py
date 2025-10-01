from assetmanagement.strategies.turtle.services.base_service import BaseStrategy
from strategies.turtle.schema import TurtleSignal
from strategies.turtle.constants import POSITION_SIZE_PERCENT


class BuyStrategy(BaseStrategy):
    def __init__(self, unit: float):
        super().__init__(unit)

    def analyze(self) -> TurtleSignal:

        
        
        return