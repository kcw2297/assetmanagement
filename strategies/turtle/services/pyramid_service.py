from assetmanagement.strategies.turtle.services.base_service import BaseStrategy



class PyramidStrategy(BaseStrategy):
    def __init__(self, unit: float):
        super().__init__(unit)

    def run(self) -> bool:
        
        return