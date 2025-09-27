import jwt
import uuid
import time
import requests

from app.config.settings import settings


class BithumbClient:
    BASE_URL = "https://api.bithumb.com"

    def __init__(self):
        self.api_key = settings.BITHUMB_API_KEY
        self.secret_key = settings.BITHUMB_SECRET_KEY

    def _generate_jwt_token(self) -> str:
        """JWT 토큰 생성"""
        payload = {
            'access_key': self.api_key,
            'nonce': str(uuid.uuid4()),
            'timestamp': round(time.time() * 1000)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def _get_headers(self) -> dict[str, str]:
        jwt_token = self._generate_jwt_token()
        return {'Authorization': f'Bearer {jwt_token}'}

    def call_api(self, endpoint: str) -> dict:
        headers = self._get_headers()

        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", headers=headers)
            return {
                'status_code': response.status_code,
                'data': response.json()
            }
        except Exception as e:
            return {
                'status_code': 0,
                'data': {"error": str(e)}
            }