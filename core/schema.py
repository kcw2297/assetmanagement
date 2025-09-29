from pydantic import BaseModel

class MovingAverage(BaseModel):
    ma5: float = 0.0    # 5일 이동평균
    ma10: float = 0.0   # 10일 이동평균
    ma20: float = 0.0   # 20일 이동평균
    ma50: float = 0.0   # 50일 이동평균
    
    