import jwt
import uuid
import time
import json
import hashlib
from urllib.parse import urlencode
import requests

from app.config.settings import settings


class BithumbClient:
    BASE_URL = "https://api.bithumb.com"

    def __init__(self):
        self.api_key = settings.BITHUMB_API_KEY
        self.secret_key = settings.BITHUMB_SECRET_KEY

    def _generate_jwt_token(self) -> str:
        payload = {
            'access_key': self.api_key,
            'nonce': str(uuid.uuid4()),
            'timestamp': round(time.time() * 1000)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def _get_headers(self) -> dict[str, str]:
        jwt_token = self._generate_jwt_token()
        return {'Authorization': f'Bearer {jwt_token}'}

    def call_private_api(self, endpoint: str) -> dict:
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

    def call_public_api(self, endpoint: str, params: dict) -> dict:
        headers = {"accept": "application/json"}

        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", headers=headers, params=params)
            return {
                'status_code': response.status_code,
                'data': response.json()
            }
        except Exception as e:
            return {
                'status_code': 400,
                'data': {"error": str(e)}
            }

    def call_order_api(self, request_body: dict) -> dict:
        """주문 API 호출 (JWT + query_hash 인증)"""
        try:
            # query_hash 생성
            query = urlencode(request_body).encode()
            hash_obj = hashlib.sha512()
            hash_obj.update(query)
            query_hash = hash_obj.hexdigest()

            # JWT 토큰 생성
            payload = {
                'access_key': self.api_key,
                'nonce': str(uuid.uuid4()),
                'timestamp': round(time.time() * 1000),
                'query_hash': query_hash,
                'query_hash_alg': 'SHA512',
            }

            jwt_token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            authorization_token = f'Bearer {jwt_token}'

            headers = {
                'Authorization': authorization_token,
                'Content-Type': 'application/json'
            }

            # API 호출
            response = requests.post(
                f"{self.BASE_URL}/v1/orders",
                data=json.dumps(request_body),
                headers=headers
            )

            return {
                "status_code": response.status_code,
                "data": response.json()
            }

        except Exception as e:
            return {"error": str(e)}