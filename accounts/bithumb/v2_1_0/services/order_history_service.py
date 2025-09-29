from accounts.bithumb.v2_1_0.config.bithumb_client import BithumbClient
from strategies.turtle.constants import PYRAMID_PROFIT_LEVELS

from accounts.bithumb.v2_1_0.schema import Order, Trade
from accounts.bithumb.v2_1_0.enums import OrderSide



class OrderHistoryService:
    def __init__(self, client: BithumbClient):
        self.client = client

    def get_orders(self, market: str, state: str = "done") -> list[Order]:
        try:
            endpoint = "/v1/orders"
            result = self.client.call_private_api(endpoint)
            data = result.get('data', [])

            if 'error' in data:
                return []

            orders = []
            for order_data in data:
                if (order_data.get('market') == market and
                    order_data.get('state') == state):

                    order = Order(**order_data)
                    orders.append(order)

            return orders

        except Exception:
            return []

    def get_trades(self, market: str) -> list[Trade]:
        try:
            endpoint = "/v1/order/trades"
            result = self.client.call_private_api(endpoint)
            data = result.get('data', [])

            if 'error' in data:
                return []

            trades = []
            for trade_data in data:
                if trade_data.get('market') == market:
                    trade = Trade(**trade_data)
                    trades.append(trade)

            return trades

        except Exception:
            return []

    def get_profit_rate(self, market: str, current_price: float) -> float:
        try:
            buy_orders = [order for order in self.get_orders(market) if order.side == OrderSide.BID]

            if not buy_orders:
                return 0.0

            total_volume = 0.0
            total_paid = 0.0

            trades = self.get_trades(market)

            for order in buy_orders:
                order_trades = [t for t in trades if t.uuid == order.uuid and t.side == OrderSide.BID]

                for trade in order_trades:
                    trade_volume = float(trade.volume)
                    trade_funds = float(trade.funds)

                    total_volume += trade_volume
                    total_paid += trade_funds

            if total_volume <= 0 or total_paid <= 0:
                return 0.0

            current_value = total_volume * current_price
            profit_amount = current_value - total_paid
            profit_rate = (profit_amount / total_paid) * 100

            return profit_rate

        except Exception:
            return 0.0

    def get_buy_count(self, market: str) -> int:
        try:
            buy_orders = [order for order in self.get_orders(market) if order.side == OrderSide.BID]
            return len(buy_orders)
        except Exception:
            return 0

    def get_current_pyramid_level(self, market: str, current_price: float) -> int:
        profit_rate = self.get_profit_rate(market, current_price)

        for i, level in enumerate(PYRAMID_PROFIT_LEVELS):
            if profit_rate < level:
                return i

        return len(PYRAMID_PROFIT_LEVELS)  # 모든 단계 완료

    def should_pyramid(self, market: str, current_price: float) -> tuple[bool, str]:
        try:
            profit_rate = self.get_profit_rate(market, current_price)
            buy_count = self.get_buy_count(market)
            current_level = self.get_current_pyramid_level(market, current_price)

            if buy_count == 0:
                return False, "초기 매수 없음"

            pyramid_count = buy_count - 1

            if current_level > pyramid_count and pyramid_count < len(PYRAMID_PROFIT_LEVELS):
                target_level = PYRAMID_PROFIT_LEVELS[pyramid_count]
                return True, f"{target_level}% 수익 달성 - {pyramid_count + 1}단계 피라미딩"

            return False, f"피라미딩 조건 미충족 (수익률: {profit_rate:.1f}%, 단계: {pyramid_count}/{len(PYRAMID_PROFIT_LEVELS)})"

        except Exception:
            return False, "피라미딩 조건 확인 실패"