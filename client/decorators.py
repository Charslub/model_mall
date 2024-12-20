from functools import wraps

from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed

from utils.sign_utils import Sign
from utils.token_utils import Token


def token_authenticator(func):
    """
    token检测
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            token = request.META.get("TOKEN")
            if not token:
                raise AuthenticationFailed("Missing required parameters Token")
            # 校验token正确性
            token = Token()
            verify_res, verify_msg = token.verify_jwt_token(token)
            if not verify_res:
                raise AuthenticationFailed(verify_msg)
            kwargs["uid"] = verify_msg["uid"]
            return func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(status=401, data={"data": {}, "msg": str(e)})
    return wrapper


def sign_authenticator(func):
    """
    签名检测
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            sign = request.META.get("sign")
            username = request.POST["username"]
            password = request.POST["password"]
            if not sign:
                raise AuthenticationFailed("Missing required parameters sign")

            # 验证签名
            sign = Sign()
            user_data = {"username": username, "password": password}
            verify_res, verify_msg = sign.verify_registration_signature(user_data, sign)
            if not verify_res:
                raise AuthenticationFailed(verify_msg)

            return func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(status=401, data={"data": {}, "msg": str(e)})
    return wrapper


def params_validator(func):
    """
    入参检测
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        return result

    return wrapper


def params_converter(func):
    """
    转换特殊返回参数类型
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        return result

    return wrapper
