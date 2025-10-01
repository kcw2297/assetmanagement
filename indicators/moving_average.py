class MovingAverageUtils:
    @staticmethod
    def calculate_sma(prices: list[float], period: int) -> float:
        if not prices:
            raise ValueError("가격 리스트가 비어있습니다")

        if len(prices) < period:
            raise ValueError(f"데이터가 부족합니다. 필요: {period}개, 현재: {len(prices)}개")

        recent_prices = prices[-period:]
        return sum(recent_prices) / period