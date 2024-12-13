from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_GET, require_POST

from utils.sql_utils import SQLManager


# Create your views here.
@require_POST
@path("/login", name="client_login")
def login(request):
    """
    用户端登录
    :param request:
    :return:
    """
    try:
        params = request.POST
        username = params["username"]
        password = params["password"]
    except (ValueError, TypeError, KeyError):
        return JsonResponse(status=400, data={})

    sql = "SELECT id, username, avatar, role FROM model.users WHERE username = %s AND password = %s;"
    user_res = SQLManager.fetchone(sql, params=(username, password))
    if not user_res:
        return JsonResponse(status=200, data={"data": {}, "msg": "用户名/密码错误"})

    return JsonResponse(status=200, data=user_res)


@require_POST
@path("/register", name="client_register")
def register(request):
    """
    用户注册接口
    :param request:
    :return:
    """
    try:
        params = request.POST
        username = params["username"]
        password = params["password"]
        role = params["role"]
        if role not in ("user", "merchant"):
            raise ValueError("用户类型错误")
    except (ValueError, TypeError, KeyError) as e:
        return JsonResponse(status=400, data={"data": {}, "msg": e})

    sql = "SELECT 1 FROM model.users WHERE username = %s;"
    user_res = SQLManager.fetchone(sql, (username,))
    if user_res:
        return JsonResponse(status=200, data={"data": {}, "msg": "用户名已存在"})

    sql = "INSERT INTO model.users (username, password) VALUES (%s, %s);"
    user_id = SQLManager.execute(sql, (username, password))

    data = {
        "id": user_id,
        "role": role,
        "username": username,
        "avatar": ""  # 初始头像链接
    }

    return JsonResponse(status=200, data=data)
