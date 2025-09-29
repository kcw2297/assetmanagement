class MovingAverageService:

    @staticmethod
    def calculate_sma(prices: list[float], period: int) -> float:
        if not prices:
            raise ValueError("가격 리스트가 비어있습니다")

        if len(prices) == period:
            raise ValueError(f"prices 개수가 period와 동일해야 합니다.")

        return sum(prices) / period