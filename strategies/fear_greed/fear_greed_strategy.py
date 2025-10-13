import fear_and_greed
from fear_and_greed import FearGreedIndex


class FeatGreedStrategy():
    def index(self) -> FearGreedIndex:
        return fear_and_greed.get()
