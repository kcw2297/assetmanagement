from pydantic import BaseModel, Field

class Account(BaseModel):
    currency: str = Field(description="화폐를 의미하는 영문 대문자 코드")
    balance: float = Field(description="주문가능 금액/수량")
    locked: float = Field(description="주문 중 묶여있는 금액/수량")
    avg_buy_price: float = Field(description="매수평균가")
    avg_buy_price_modified: bool = Field(description="매수평균가 수정 여부")
    unit_currency: str = Field(description="평단가 기준 화폐")
    
    
    
class Candle(BaseModel):
    market: str = Field(description="마켓명")
    candle_date_time_utc: str = Field(description="캔들 기준 시각(UTC 기준) 포맷: yyyy-MM-dd'T'HH:mm:ss")
    candle_date_time_kst: str = Field(description="캔들 기준 시각(KST 기준) 포맷: yyyy-MM-dd'T'HH:mm:ss")
    opening_price: float = Field(description="시가")
    high_price: float = Field(description="고가")
    low_price: float = Field(description="저가")
    trade_price: float = Field(description="종가")
    timestamp: int = Field(description="캔들 종료 시각(KST 기준)")
    candle_acc_trade_price: float = Field(description="누적 거래 금액")
    candle_acc_trade_volume: float = Field(description="누적 거래량")
    prev_closing_price: float = Field(description="전일 종가(UTC 0시 기준)")
    change_price: float = Field(description="전일 종가 대비 변화 금액")
    change_rate: float = Field(description="전일 종가 대비 변화량")
    converted_trade_price: float | None = Field(default=None, description="종가 환산 화폐 단위로 환산된 가격")
    
    
class Order(BaseModel):
    uuid: str = Field(description="주문의 고유 아이디")
    side: str = Field(description="주문 종류")
    ord_type: str = Field(description="주문 방식")
    price: str = Field(description="주문 당시 화폐 가격")
    state: str = Field(description="주문 상태")
    market: str = Field(description="마켓의 유일키")
    created_at: str = Field(description="주문 생성 시간")
    volume: str | None = Field(default=None, description="사용자가 입력한 주문 양")
    remaining_volume: str | None = Field(default=None, description="체결 후 남은 주문 양")
    reserved_fee: str = Field(description="수수료로 예약된 비용")
    remaining_fee: str = Field(description="남은 수수료")
    paid_fee: str = Field(description="사용된 수수료")
    locked: str = Field(description="거래에 사용중인 비용")
    executed_volume: str = Field(description="체결된 양")
    trades_count: int = Field(description="해당 주문에 걸린 체결 수")
    
    
class Trade(BaseModel):
    uuid: str
    price: str
    volume: str
    funds: str  # 체결금액
    side: str  # bid, ask
    created_at: str
    
    
class Ticker(BaseModel):
    market: str = Field(description="종목 구분 코드")
    trade_date: str = Field(description="최근 거래 일자(UTC) 포맷: yyyyMMdd")
    trade_time: str = Field(description="최근 거래 시각(UTC) 포맷: HHmmss")
    trade_date_kst: str = Field(description="최근 거래 일자(KST) 포맷: yyyyMMdd")
    trade_time_kst: str = Field(description="최근 거래 시각(KST) 포맷: HHmmss")
    trade_timestamp: int = Field(description="최근 거래 일시(UTC) 포맷: Unix Timestamp")
    opening_price: float = Field(description="시가")
    high_price: float = Field(description="고가")
    low_price: float = Field(description="저가")
    trade_price: float = Field(description="종가(현재가)")
    prev_closing_price: float = Field(description="전일 종가(KST 0시 기준)")
    change: str = Field(description="EVEN:보합, RISE:상승, FALL:하락")
    change_price: float = Field(description="변화액의 절대값")
    change_rate: float = Field(description="변화율의 절대값")
    signed_change_price: float = Field(description="부호가 있는 변화액")
    signed_change_rate: float = Field(description="부호가 있는 변화율")
    trade_volume: float = Field(description="가장 최근 거래량")
    acc_trade_price: float = Field(description="누적 거래대금(KST 0시 기준)")
    acc_trade_price_24h: float = Field(description="24시간 누적 거래대금")
    acc_trade_volume: float = Field(description="누적 거래량(KST 0시 기준)")
    acc_trade_volume_24h: float = Field(description="24시간 누적 거래량")
    highest_52_week_price: float = Field(description="52주 신고가")
    highest_52_week_date: str = Field(description="52주 신고가 달성일 포맷: yyyy-MM-dd")
    lowest_52_week_price: float = Field(description="52주 신저가")
    lowest_52_week_date: str = Field(description="52주 신저가 달성일 포맷: yyyy-MM-dd")
    timestamp: int = Field(description="타임스탬프")