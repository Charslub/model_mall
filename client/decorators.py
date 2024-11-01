from functools import wraps


def client_token_authenticator(func):
    """
    token检测
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        return result

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
