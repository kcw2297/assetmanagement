from abc import ABC, abstractmethod
from strategies.turtle.constants import BASE_UNIT_PERCENT

class BaseStrategy(ABC):
    def __init__(self, unit: float = BASE_UNIT_PERCENT):
        self.unit = unit

    @abstractmethod
    def run(self, *args, **kwargs) -> bool:
        pass

   