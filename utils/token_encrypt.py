import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class Token:
    def __init__(self):
        pass

    @staticmethod
    def load_private_key():
        with open("private_key.pem", "r") as key_file:
            private_key = key_file.read()

        return serialization.load_pem_private_key(
            private_key.encode(), password=None, backend=default_backend()
        )

    @staticmethod
    # 读取公钥
    def load_public_key():
        with open("public_key.pem", "r") as key_file:
            public_key = key_file.read()

        return serialization.load_pem_public_key(
            public_key.encode(), backend=default_backend()
        )

    # 创建 JWT Token
    def create_jwt_token(self, params):
        # 载入私钥
        private_key = self.load_private_key()

        # 使用私钥签名 JWT Token
        encoded_jwt = jwt.encode(params, private_key, algorithm='RS256')

        return encoded_jwt

    # 解密并验证 JWT Token
    def verify_jwt_token(self, token):
        # 载入公钥
        public_key = self.load_public_key()

        # 解码和验证 JWT Token
        try:
            decoded_payload = jwt.decode(token, public_key, algorithms=['RS256'])
            print("JWT is valid")
            print(f"Decoded payload: {decoded_payload}")
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
