from enum import StrEnum



class SignalAction(StrEnum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class BuyType(StrEnum):
    INITIAL = "initial"
    PYRAMID = "pyramid"
