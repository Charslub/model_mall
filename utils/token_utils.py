import jwt

from utils.key_utils import BaseKey
from utils.redis_utils import set_value, get_value


class Token(BaseKey):
    def __init__(self):
        super().__init__()

    # 创建 JWT Token
    def create_jwt_token(self, params):
        # 载入私钥
        private_key = self.load_private_key()

        # 使用私钥签名 JWT Token
        encoded_jwt = jwt.encode(params, private_key, algorithm='RS256')

        # token缓存到redis中
        set_value(encoded_jwt, params["id"])

        return encoded_jwt

    # 解密并验证 JWT Token
    def verify_jwt_token(self, token):
        # 缓存校验
        redis_token_res = get_value(token)
        if not redis_token_res:
            return False, "Token has expired"

        # 内容校验
        try:
            # 载入公钥
            public_key = self.load_public_key()
            # 解码和验证 JWT Token
            jwt.decode(token, public_key, algorithms=['RS256'])
            return True, ""
        except jwt.ExpiredSignatureError:
            return False, "Token has expired"
        except jwt.InvalidTokenError:
            return False, "Invalid token"
