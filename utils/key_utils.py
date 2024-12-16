from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class BaseKey:
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
