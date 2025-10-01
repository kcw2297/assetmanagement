from abc import ABC, abstractmethod
from strategies.turtle.schema import TurtleSignal
from strategies.turtle.constants import POSITION_SIZE_PERCENT

class BaseStrategy(ABC):
    def __init__(self, unit: float = POSITION_SIZE_PERCENT):
        self.unit = unit

    @abstractmethod
    def analyze(self) -> TurtleSignal:
        pass

   