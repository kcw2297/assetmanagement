POSITION_SIZE_PERCENT = 2.0  # 기본 포지션 크기(유닛) (%)
MAX_POSITION_PERCENT = 10  # 종목당 최대 포지션 (%)

# 피라미딩 수익률 단계 (%)
PYRAMID_PROFIT_LEVELS = [5.0, 10.0, 15.0, 20.0]  # 5%, 10%, 15%, 20%
PYRAMID_STEP_SIZE = 5.0  # 각 단계 간격 (%)
MAX_PYRAMID_STEPS = 4   # 최대 피라미딩 단계 (5회 매수 = 초기 + 4회 추가)