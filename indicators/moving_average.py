from common.schema import OHLC


class MovingAverage:
    @staticmethod
    def calculate_sma(prices: list[float], period: int) -> float:
        if len(prices) == period:
            raise ValueError(f"prices와 period 개수가 매칭되지 않습니다. {prices=}개, {period=}개")

        return sum(prices) / period

    @staticmethod
    def calculate_atr(ohlcs: list[OHLC], period: int) -> float:
        if not len(ohlcs) == period + 1:
            raise ValueError(f"ATR 계산을 위해 period보다 1개 더 많은 ohlcs 개수가 필요합니다.")

        true_ranges = []
        for i in range(1, len(ohlcs)):
            high_low = ohlcs[i].high - ohlcs[i].low
            high_close = abs(ohlcs[i].high - ohlcs[i - 1].close)
            low_close = abs(ohlcs[i].low - ohlcs[i - 1].close)
            true_ranges.append(max(high_low, high_close, low_close))

        atr = sum(true_ranges[:period]) / period # 초기 ATR: 첫 period개의 True Range 단순 평균

        for i in range(period, len(true_ranges)):
            atr = ((period - 1) * atr + true_ranges[i]) / period # (19 × 이전ATR + 새TR) / 20

        return atr
    