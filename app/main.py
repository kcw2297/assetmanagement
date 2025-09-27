from app.config.bithumb_client import BithumbClient
from app.services.account_service import AccountService
from app.services.ticker_service import TickerService
from app.services.candle_service import CandleService
from app.services.order_service import OrderService
from app.strategies.turtle_coordinator import TurtleCoordinator
from app.enums import MajorCoin, SignalType
from app.schema import TurtleSignal

def main():
    # 서비스 초기화
    client = BithumbClient()
    account_service = AccountService(client)
    ticker_service = TickerService(client)
    candle_service = CandleService(client)
    order_service = OrderService(client)

    coordinator = TurtleCoordinator(
        ticker_service=ticker_service,
        candle_service=candle_service,
        account_service=account_service,
        client=client
    )

    # 보유 자산 출력
    accounts = account_service.get_accounts()
    krw_balance = next((acc.balance for acc in accounts if acc.currency == "KRW"), 0)
    print(f"💰 원화 잔고: {krw_balance:,.0f}원")

    print("🎯 터틀 분석 시작")

    executed_orders = []

    for coin in MajorCoin:
        try:
            signal: TurtleSignal = coordinator.analyze_comprehensive_signal(coin.market)
            print(f"[{coin.value}] {signal.signal_type.value} - {signal.current_price:,.0f}원")

            if signal.signal_type == SignalType.HOLD:
                continue

            # order_result = order_service.execute_signal_order(signal)
            # if "status_code" in order_result and order_result["status_code"] == 201:
            #     print(f"✅ {coin.value} 주문 성공")
            #     executed_orders.append(coin.value)
        except:
            continue

    print(f"\n📈 실행 완료: {len(executed_orders)}개 주문" if executed_orders else "\n📋 실행된 주문 없음")

if __name__ == "__main__":
    main()