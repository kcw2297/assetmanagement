from common.schema import OHLC


class MovingAverage:
    @staticmethod
    def calculate_sma(prices: list[float], period: int) -> float:
        if len(prices) == period:
            raise ValueError(f"prices와 period 개수가 매칭되지 않습니다. {prices=}개, {period=}개")

        return sum(prices) / period

    @staticmethod
    def calculate_atr(ohlcs: list[OHLC]) -> float:
        true_ranges = []
        for i in range(1, len(ohlcs)):
            high_low = ohlcs[i].high - ohlcs[i].low
            high_close = abs(ohlcs[i].high - ohlcs[i - 1].close)
            low_close = abs(ohlcs[i].low - ohlcs[i - 1].close)
            true_ranges.append(max(high_low, high_close, low_close))

        # TODO: 단순 기간 나누기 아님, 다시 확인 필요
        return sum(true_ranges) / len(ohlcs)
    