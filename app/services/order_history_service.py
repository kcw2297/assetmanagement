from app.config.bithumb_client import BithumbClient
from app.schema import Order, Trade
from app.enums import OrderSide, OrderType
from app.constants import PYRAMID_PROFIT_LEVELS


class OrderHistoryService:
    """터틀 트레이딩용 주문 이력 추적 서비스"""

    def __init__(self, client: BithumbClient):
        self.client = client

    def get_orders(self, market: str, state: str = "done") -> list[Order]:
        """완료된 주문 목록 조회"""
        try:
            endpoint = "/v1/orders"
            result = self.client.call_private_api(endpoint)
            data = result.get('data', [])

            if 'error' in data:
                return []

            orders = []
            for order_data in data:
                # 해당 마켓과 상태의 주문만 필터링
                if (order_data.get('market') == market and
                    order_data.get('state') == state):

                    order = Order(
                        uuid=order_data.get('uuid', ''),
                        market=order_data.get('market', ''),
                        side=order_data.get('side', ''),
                        ord_type=order_data.get('ord_type', ''),
                        state=order_data.get('state', ''),
                        volume=order_data.get('volume', '0'),
                        price=order_data.get('price', '0'),
                        paid_fee=order_data.get('paid_fee', '0'),
                        remaining_fee=order_data.get('remaining_fee', '0'),
                        reserved_fee=order_data.get('reserved_fee', '0'),
                        remaining_volume=order_data.get('remaining_volume', '0'),
                        executed_volume=order_data.get('executed_volume', '0'),
                        created_at=order_data.get('created_at', ''),
                        trades_count=order_data.get('trades_count', 0)
                    )
                    orders.append(order)

            return orders

        except Exception:
            return []

    def get_trades(self, market: str) -> list[Trade]:
        """체결 내역 조회"""
        try:
            endpoint = "/v1/order/trades"
            result = self.client.call_private_api(endpoint)
            data = result.get('data', [])

            if 'error' in data:
                return []

            trades = []
            for trade_data in data:
                if trade_data.get('market') == market:
                    trade = Trade(
                        uuid=trade_data.get('uuid', ''),
                        price=trade_data.get('price', '0'),
                        volume=trade_data.get('volume', '0'),
                        funds=trade_data.get('funds', '0'),
                        side=trade_data.get('side', ''),
                        created_at=trade_data.get('created_at', '')
                    )
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

            # 시장가 매수 주문들의 체결 내역에서 평균매수가 계산
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
        """해당 종목의 총 매수 횟수 조회"""
        try:
            buy_orders = [order for order in self.get_orders(market) if order.side == OrderSide.BID]
            return len(buy_orders)
        except Exception:
            return 0

    def get_current_pyramid_level(self, market: str, current_price: float) -> int:
        """현재 피라미딩 단계 확인 (0: 초기매수, 1: 첫번째 피라미딩, ...)"""
        profit_rate = self.get_profit_rate(market, current_price)

        for i, level in enumerate(PYRAMID_PROFIT_LEVELS):
            if profit_rate < level:
                return i

        return len(PYRAMID_PROFIT_LEVELS)  # 모든 단계 완료

    def should_pyramid(self, market: str, current_price: float) -> tuple[bool, str]:
        """피라미딩 조건 확인 (단계별 진입)"""
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