from app.config.bithumb_client import BithumbClient
from app.services.account_service import AccountService
from app.services.ticker_service import TickerService
from app.services.candle_service import CandleService
from app.strategies.turtle_coordinator import TurtleCoordinator
from app.enums import MajorCoin
from app.schema import Account

def main():
    print("🐢 터틀 트레이딩 자동화 시스템")
    print("=" * 50)

    # 서비스 초기화
    client = BithumbClient()
    account_service = AccountService(client)
    ticker_service = TickerService(client)
    candle_service = CandleService(client)

    # 터틀 코디네이터 초기화
    coordinator = TurtleCoordinator(
        ticker_service=ticker_service,
        candle_service=candle_service,
        account_service=account_service
    )

    # 보유 자산 정보 출력
    accounts: list[Account] = account_service.get_accounts()
    print("\n📊 보유 자산 정보")
    print("-" * 30)
    total_krw = 0
    for account in accounts:
        if account.currency == "KRW":
            total_krw = account.balance
            print(f"💰 {account.currency}: {account.balance:,.0f}원")
        elif account.balance > 0:
            print(f"🪙 {account.currency}: {account.balance:.6f}")

    print(f"\n총 원화 잔고: {total_krw:,.0f}원")

    # 주요 코인별 전략 분석
    print("\n🎯 주요 코인별 투자 전략")
    print("=" * 50)

    for coin in MajorCoin:
        market = coin.market
        print(f"\n[{coin.value}] 분석:")
        print("-" * 20)

        try:
            signal = coordinator.analyze_comprehensive_signal(market)

            print(f"📈 현재가: {signal.current_price:,.0f}원")
            print(f"🚦 신호: {signal.signal_type.value}")
            print(f"📝 이유: {signal.reason}")

            if signal.target_amount > 0:
                print(f"💳 거래금액: {signal.target_amount:,.0f}원")

            if signal.confidence > 0:
                print(f"📊 신뢰도: {signal.confidence:.1%}")

        except Exception as e:
            print(f"❌ 분석 실패: {str(e)}")

    print("\n" + "=" * 50)
    print("분석 완료! 📈")

if __name__ == "__main__":
    main()