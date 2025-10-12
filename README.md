# Asset Management

암호화폐 자동매매를 위한 터틀 트레이딩 전략 라이브러리

## 설치

```bash
pip install assetmanagement
```

## 사용법

```python
from assetmanagement import BithumbAPI, BithumbExchange, TurtleStrategy

# 빗썸 API 초기화
api = BithumbAPI()
exchange = BithumbExchange(api)

# 터틀 전략 초기화
strategy = TurtleStrategy()

# 현재가 조회
current_price = exchange.current_price("KRW-BTC")

# 캔들 데이터 조회
candles = exchange.candles("KRW-BTC", count=20)

# 매매 신호 판단
if strategy.buy(current_price, candles):
    print("매수 신호")
```

## 라이선스

MIT License
