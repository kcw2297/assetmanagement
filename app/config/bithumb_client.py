import jwt
import uuid
import time

from pybithumb import Bithumb
from app.config.settings import settings


class BithumbClient:
    """빗썸 API 클라이언트 - 연결 담당"""

    BASE_URL = 'https://api.bithumb.com'

    def __init__(self):
        self.api_key = settings.BITHUMB_API_KEY
        self.secret_key = settings.BITHUMB_SECRET_KEY
        self.public_client = Bithumb(self.api_key, self.secret_key)

    def generate_jwt_token(self) -> str:
        """JWT 토큰 생성"""
        payload = {
            'access_key': self.api_key,
            'nonce': str(uuid.uuid4()),
            'timestamp': round(time.time() * 1000)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def get_headers(self) -> dict[str, str]:
        """인증 헤더 생성"""
        return {'Authorization': f'Bearer {self.generate_jwt_token()}'}