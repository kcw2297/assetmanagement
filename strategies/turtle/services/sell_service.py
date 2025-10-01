from strategies.turtle.services.base_service import BaseStrategy


class SellStrategy(BaseStrategy):
    def __init__(self, unit: float):
        super().__init__(unit)
        

    def run(self) -> bool:

        return