from enum import Enum


class StrategyLevel(str, Enum):
    L1 = "L1"
    L2 = "L2"


class SignalAction(str, Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class BuyType(str, Enum):
    INITIAL = "initial"
    PYRAMID = "pyramid"
