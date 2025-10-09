from enum import StrEnum, IntEnum



class SignalAction(StrEnum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class BuyType(StrEnum):
    INITIAL = "initial"
    PYRAMID = "pyramid"
    
    
class TurtleSystemType(IntEnum):
    ONE = 1
    TWO = 2
