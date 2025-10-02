from datetime import datetime
from strategies.turtle.turtle_strategy import TurtleStrategy
from strategies.turtle.constants import (
    L1_BASE_BUY_PERIOD,
    L1_BASE_SELL_PERIOD,
    L2_BASE_BUY_PERIOD,
    L2_BASE_SELL_PERIOD,
    BASE_UNIT_PERCENT
)
from strategies.turtle.schema import TradeSignal, TurtlePosition
from strategies.turtle.enums import StrategyLevel, SignalAction, BuyType


class TurtleTrader:
    def __init__(
        self,
        initial_capital: float,
        strategy_level: StrategyLevel = StrategyLevel.L1
    ):
        buy_period = L1_BASE_BUY_PERIOD if strategy_level == StrategyLevel.L1 else L2_BASE_BUY_PERIOD
        sell_period = L1_BASE_SELL_PERIOD if strategy_level == StrategyLevel.L1 else L2_BASE_SELL_PERIOD

        self.strategy = TurtleStrategy(
            buy_period=buy_period,
            sell_period=sell_period
        )
        self.strategy_level = strategy_level
        self.initial_capital = initial_capital
        self.current_unit_percent = BASE_UNIT_PERCENT

    def process(
        self,
        current_price: float,
        historical_prices: list[float],
        N: float,
        total_asset: float,
        trade_date: str | None = None
    ) -> TradeSignal:
        if trade_date is None:
            trade_date = datetime.now().isoformat()

        if self.strategy.sell(current_price, historical_prices, N):
            return self._create_sell_signal(current_price, trade_date)

        if self.strategy.buy(current_price, historical_prices):
            quantity = self._calculate_quantity(current_price)
            return self._create_buy_signal(current_price, quantity, N, trade_date)

        if self.strategy.pyramid_buy(current_price, total_asset, N):
            quantity = self._calculate_quantity(current_price)
            return self._create_pyramid_signal(current_price, quantity, N, trade_date)

        return TradeSignal(
            action=SignalAction.HOLD,
            reason="No signal"
        )

    def _calculate_quantity(self, current_price: float) -> int:
        unit_amount = self.initial_capital * (self.current_unit_percent / 100)
        return int(unit_amount / current_price)

    def _create_buy_signal(
        self,
        price: float,
        quantity: int,
        N: float,
        trade_date: str
    ) -> TradeSignal:
        self.strategy.add_position(price, quantity, N, trade_date)

        return TradeSignal(
            action=SignalAction.BUY,
            type=BuyType.INITIAL,
            price=price,
            quantity=quantity,
            N=N,
            trade_date=trade_date,
            reason=f'{self.strategy.buy_period}일 신고가 돌파'
        )

    def _create_pyramid_signal(
        self,
        price: float,
        quantity: int,
        N: float,
        trade_date: str
    ) -> TradeSignal:
        self.strategy.add_position(price, quantity, N, trade_date)

        return TradeSignal(
            action=SignalAction.BUY,
            type=BuyType.PYRAMID,
            price=price,
            quantity=quantity,
            N=N,
            trade_date=trade_date,
            unit_number=self.strategy.total_units,
            reason=f'추격 매수 (유닛 #{self.strategy.total_units})'
        )

    def _create_sell_signal(self, price: float, trade_date: str) -> TradeSignal:
        total_quantity = sum(pos.quantity for pos in self.strategy.positions)

        signal = TradeSignal(
            action=SignalAction.SELL,
            price=price,
            quantity=total_quantity,
            trade_date=trade_date,
            reason=f'{self.strategy.sell_period}일 최저가 하단 돌파 또는 손절'
        )

        self.strategy.clear_positions()

        return signal

    def adjust_unit_size(self, profit_rate: float):
        if profit_rate <= -10:
            adjustment_factor = 1 - (abs(profit_rate) // 10) * 0.2
            self.current_unit_percent = BASE_UNIT_PERCENT * max(adjustment_factor, 0.2)
        elif profit_rate >= 10:
            adjustment_factor = 1 + (profit_rate // 10) * 0.2
            self.current_unit_percent = min(
                BASE_UNIT_PERCENT * adjustment_factor,
                BASE_UNIT_PERCENT
            )

    def get_positions(self) -> list[TurtlePosition]:
        return self.strategy.positions
