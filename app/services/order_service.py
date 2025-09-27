from app.config.bithumb_client import BithumbClient
from app.schema import TurtleSignal
from app.enums import SignalType, OrderSide, OrderType


class OrderService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def execute_market_buy_order(self, market: str, price: float) -> dict:
        try:
            request_body = {
                'market': market,
                'side': OrderSide.BID,
                'price': str(int(price)),
                'ord_type': OrderType.PRICE  # 시장가 매수 (KRW 금액 기준)
            }

            response = self.client.call_order_api(request_body)
            return response

        except Exception as e:
            print(f"시장가 매수 주문 실행 실패: {e}")
            return {"error": str(e)}

    def execute_market_sell_order(self, market: str, volume: float) -> dict:
        try:
            request_body = {
                'market': market,
                'side': OrderSide.ASK,
                'volume': str(volume),
                'ord_type': OrderType.MARKET  # 시장가 매도
            }

            response = self.client.call_order_api(request_body)
            return response

        except Exception as e:
            print(f"시장가 매도 주문 실행 실패: {e}")
            return {"error": str(e)}

    def execute_signal_order(self, signal: TurtleSignal) -> dict:
        try:
            if signal.signal_type == SignalType.BUY:
                return self.execute_market_buy_order(signal.market, signal.target_amount)

            elif signal.signal_type == SignalType.SELL:
                return self.execute_market_sell_order(signal.market, signal.target_amount)

            elif signal.signal_type == SignalType.PYRAMID:
                return self.execute_market_buy_order(signal.market, signal.target_amount)

            else:
                return {"message": "주문 실행 없음 - HOLD 신호"}

        except Exception as e:
            print(f"신호 기반 주문 실행 실패: {e}")
            return {"error": str(e)}

