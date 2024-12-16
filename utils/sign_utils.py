from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

from utils.key_utils import BaseKey


class Sign(BaseKey):
    def __init__(self):
        super().__init__()

    # 生成签名
    def generate_registration_signature(self, user_data):
        """
        使用私钥生成注册数据的签名
        :param user_data: 注册时的数据（如用户名、密码）
        :return: 签名（字节形式）
        """

        # 将用户数据转为JSON字符串
        message = str(user_data)

        # 加载私钥
        private_key = self.load_private_key()

        # 计算消息的哈希值
        message_hash = hashes.Hash(hashes.SHA256())
        message_hash.update(message.encode('utf-8'))
        digest = message_hash.finalize()

        # 使用私钥对哈希值进行签名
        signature = private_key.sign(
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return signature

    # 验证签名
    def verify_registration_signature(self, user_data, signature):
        """
        使用公钥验证注册数据的签名
        :param user_data: 注册时的数据（如用户名、密码）
        :param signature: 前端传来的签名
        :return: 验证是否通过（True/False）
        """

        # 将用户数据转为JSON字符串
        message = str(user_data)

        # 加载公钥
        public_key = self.load_public_key()

        # 计算消息的哈希值
        message_hash = hashes.Hash(hashes.SHA256())
        message_hash.update(message.encode('utf-8'))
        digest = message_hash.finalize()

        # 使用公钥验证签名
        try:
            public_key.verify(
                signature,
                digest,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            print("Signature is valid, registration is authorized.")
            return True
        except Exception as e:
            print(f"Invalid signature, registration is not authorized. Error: {e}")
            return False
