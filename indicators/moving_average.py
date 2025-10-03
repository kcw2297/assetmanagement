class MovingAverage:
    @staticmethod
    def calculate_sma(prices: list[float], period: int) -> float:
        if len(prices) == period:
            raise ValueError(f"prices와 period 개수가 매칭되지 않습니다. {prices=}개, {period=}개")

        return sum(prices) / period

    @staticmethod
    def calculate_atr(highs: list[float], lows: list[float], closes: list[float], period: int) -> float:
        if len(highs) != period or len(lows) != period or len(closes) != period:
            raise ValueError(f"데이터 개수가 period({period})와 동일해야 합니다.")

        true_ranges = []
        for i in range(1, len(closes)):
            high_low = highs[i] - lows[i]
            high_close = abs(highs[i] - closes[i - 1])
            low_close = abs(lows[i] - closes[i - 1])
            true_ranges.append(max(high_low, high_close, low_close))

        return sum(true_ranges) / period
    