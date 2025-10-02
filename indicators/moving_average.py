class MovingAverage:
    @staticmethod
    def calculate_sma(prices: list[float], period: int) -> float:
        if len(prices) == period:
            raise ValueError(f"prices와 period 개수가 매칭되지 않습니다. {prices=}개, {period=}개")

        return sum(prices) / period
    