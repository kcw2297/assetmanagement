from pydantic import BaseModel

class Account(BaseModel):
    currency: str
    balance: float
    
    
class Candle(BaseModel):
    market: str                    # 종목 구분 코드
    candle_date_time_kst: str     # KST 기준 캔들 시간
    opening_price: float          # 시가
    high_price: float             # 고가
    low_price: float              # 저가
    trade_price: float            # 종가
    candle_acc_trade_volume: float # 누적 거래량
    timestamp: int                # 타임스탬프
    
    
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