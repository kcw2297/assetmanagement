from app.config.bithumb_client import BithumbClient
from app.services.account_service import AccountService
from app.services.ticker_service import TickerService
from app.services.candle_service import CandleService
from app.services.order_service import OrderService
from app.strategies.turtle_coordinator import TurtleCoordinator
from app.enums import MajorCoin, SignalType


class TurtleTrader:
    """터틀 트레이딩 자동화 실행기"""

    def __init__(self, dry_run: bool = True):
        self.dry_run = dry_run  # True: 시뮬레이션, False: 실제 거래

        # 서비스 초기화
        self.client = BithumbClient()
        self.account_service = AccountService(self.client)
        self.ticker_service = TickerService(self.client)
        self.candle_service = CandleService(self.client)
        self.order_service = OrderService(self.client)

        # 전략 코디네이터 초기화
        self.coordinator = TurtleCoordinator(
            ticker_service=self.ticker_service,
            candle_service=self.candle_service,
            account_service=self.account_service
        )

    def run_single_analysis(self, market: str) -> dict:
        """단일 마켓 분석 및 주문 실행"""
        try:
            print(f"\n🔍 [{market}] 분석 시작...")

            # 신호 분석
            signal = self.coordinator.analyze_comprehensive_signal(market)

            print(f"📊 신호: {signal.signal_type.value}")
            print(f"📝 이유: {signal.reason}")
            print(f"💰 현재가: {signal.current_price:,.0f}원")

            if signal.target_amount > 0:
                print(f"💳 거래금액: {signal.target_amount:,.0f}원")

            if signal.confidence > 0:
                print(f"📈 신뢰도: {signal.confidence:.1%}")

            # 주문 실행
            if signal.signal_type != SignalType.HOLD:
                return self._execute_order(signal)
            else:
                return {"action": "HOLD", "message": "주문 실행 없음"}

        except Exception as e:
            print(f"❌ {market} 분석 실패: {e}")
            return {"error": str(e)}

    def run_full_analysis(self) -> dict:
        """전체 주요 코인 분석 및 주문 실행"""
        print("🐢 터틀 트레이딩 자동화 시작")
        print("=" * 50)

        results = {}

        # 현재 자산 상태 출력
        self._print_account_status()

        # 주요 코인별 분석
        for coin in MajorCoin:
            market = coin.market
            results[market] = self.run_single_analysis(market)

        print("\n" + "=" * 50)
        print("🎯 분석 완료!")

        return results

    def _execute_order(self, signal) -> dict:
        """주문 실행 (dry_run 모드 지원)"""
        if self.dry_run:
            print(f"🔄 [시뮬레이션] {signal.signal_type.value} 주문")
            return {
                "action": signal.signal_type.value,
                "market": signal.market,
                "amount": signal.target_amount,
                "simulation": True
            }
        else:
            print(f"⚡ [실제거래] {signal.signal_type.value} 주문 실행...")
            result = self.order_service.execute_signal_order(signal)

            if "error" in result:
                print(f"❌ 주문 실패: {result['error']}")
            elif "status_code" in result and result["status_code"] == 201:
                print(f"✅ 주문 성공: {result['data'].get('uuid', 'Unknown')}")

            return result

    def _print_account_status(self):
        """현재 계좌 상태 출력"""
        try:
            accounts = self.account_service.get_accounts()

            print("\n📊 현재 자산 상태")
            print("-" * 30)

            total_krw = 0
            for account in accounts:
                if account.currency == "KRW":
                    total_krw = account.balance
                    print(f"💰 {account.currency}: {account.balance:,.0f}원")
                elif account.balance > 0:
                    print(f"🪙 {account.currency}: {account.balance:.6f}")

            print(f"총 원화 잔고: {total_krw:,.0f}원")

        except Exception as e:
            print(f"❌ 계좌 정보 조회 실패: {e}")

    def set_live_trading(self):
        """실제 거래 모드로 변경"""
        self.dry_run = False
        print("⚠️  실제 거래 모드로 변경되었습니다!")

    def set_simulation_mode(self):
        """시뮬레이션 모드로 변경"""
        self.dry_run = True
        print("🔄 시뮬레이션 모드로 변경되었습니다.")


def main():
    """메인 실행 함수"""
    # 시뮬레이션 모드로 시작
    trader = TurtleTrader(dry_run=True)

    print("🐢 터틀 트레이딩 자동화 봇")
    print(f"모드: {'시뮬레이션' if trader.dry_run else '실제거래'}")

    # 전체 분석 실행
    results = trader.run_full_analysis()

    # 실행된 신호 요약
    executed_signals = [
        f"{market}: {result.get('action', 'ERROR')}"
        for market, result in results.items()
        if result.get('action') != 'HOLD'
    ]

    if executed_signals:
        print(f"\n📋 실행된 신호: {', '.join(executed_signals)}")
    else:
        print(f"\n📋 실행된 신호: 없음 (모든 코인 HOLD)")


if __name__ == "__main__":
    main()