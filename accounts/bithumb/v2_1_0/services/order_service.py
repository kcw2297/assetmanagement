from accounts.bithumb.v2_1_0.config.bithumb_client import BithumbClient
from strategies.turtle.schema import TurtleSignal
from strategies.turtle.enums import SignalType
from accounts.bithumb.v2_1_0.enums import OrderSide, OrderType
from accounts.bithumb.v2_1_0.schema import Order


class OrderService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def execute_market_buy_order(self, market: str, price: float) -> Order | None:
        try:
            request_body = {
                'market': market,
                'side': OrderSide.BID,
                'price': str(int(price)),
                'ord_type': OrderType.PRICE 
            }

            response = self.client.call_order_api("/v1/orders", request_body)

            if response.get('status_code') == 201 and 'data' in response:
                return Order(**response['data'])
            else:
                return None

        except Exception:
            return None

    def execute_market_sell_order(self, market: str, volume: float) -> Order | None:
        try:
            request_body = {
                'market': market,
                'side': OrderSide.ASK,
                'volume': str(volume),
                'ord_type': OrderType.MARKET 
            }

            response = self.client.call_order_api("/v1/orders", request_body)

            if response.get('status_code') == 201 and 'data' in response:
                return Order(**response['data'])
            else:
                return None

        except Exception:
            return None

    def execute_signal_order(self, signal: TurtleSignal) -> Order | None:
        try:
            if signal.signal_type == SignalType.BUY:
                return self.execute_market_buy_order(signal.market, signal.target_amount)

            elif signal.signal_type == SignalType.SELL:
                return self.execute_market_sell_order(signal.market, signal.target_amount)

            elif signal.signal_type == SignalType.PYRAMID:
                return self.execute_market_buy_order(signal.market, signal.target_amount)
            else:
                return None

        except Exception:
            return None

