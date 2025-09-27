from pydantic import BaseModel
from app.enums import SignalType


class Account(BaseModel):
    currency: str
    balance: float


class Ticker(BaseModel):
    market: str                  # 종목 구분 코드 (예: KRW-BTC)
    trade_price: float          # 현재가
    opening_price: float        # 시가
    high_price: float          # 고가
    low_price: float           # 저가
    prev_closing_price: float  # 전일 종가
    trade_volume: float        # 거래량
    acc_trade_volume_24h: float # 24시간 누적 거래량
    change: str                # EVEN/RISE/FALL
    change_rate: float         # 변화율
    timestamp: int             # 타임스탬프


class Candle(BaseModel):
    market: str                    # 종목 구분 코드
    candle_date_time_kst: str     # KST 기준 캔들 시간
    opening_price: float          # 시가
    high_price: float             # 고가
    low_price: float              # 저가
    trade_price: float            # 종가
    candle_acc_trade_volume: float # 누적 거래량
    timestamp: int                # 타임스탬프


class MovingAverage(BaseModel):
    ma5: float = 0.0    # 5일 이동평균
    ma10: float = 0.0   # 10일 이동평균
    ma20: float = 0.0   # 20일 이동평균


class TurtleSignal(BaseModel):
    market: str
    signal_type: SignalType  # BUY, SELL, PYRAMID, HOLD
    reason: str              # 신호 발생 이유
    current_price: float
    target_amount: float = 0.0  # 거래 금액
    confidence: float = 0.0     # 신호 신뢰도 (0-1)


class Order(BaseModel):
    uuid: str
    market: str
    side: str  # bid(매수), ask(매도)
    ord_type: str  # limit(지정가), price(시장가매수), market(시장가매도)
    state: str  # wait, done, cancel
    volume: str
    price: str
    paid_fee: str
    remaining_fee: str
    reserved_fee: str
    remaining_volume: str
    executed_volume: str
    created_at: str
    trades_count: int


class Trade(BaseModel):
    uuid: str
    price: str
    volume: str
    funds: str  # 체결금액
    side: str  # bid, ask
    created_at: str


class Position(BaseModel):
    """특정 종목의 포지션 정보"""
    market: str
    currency: str
    total_volume: float  # 총 보유량
    avg_buy_price: float  # 평균매수가
    total_paid: float    # 총 투입금액
    current_value: float # 현재 평가금액
    profit_rate: float   # 수익률 (%)
    profit_amount: float # 수익금액
    last_updated: str    # 마지막 업데이트 시간