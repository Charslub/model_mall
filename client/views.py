from django.http import JsonResponse
from django.shortcuts import render

from utils.sql_utils import execute, fetchone


# Create your views here.
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

    sql = "SELECT id, username, avater, role FROM `user` WHERE username = %s AND password = %s;"
    user_res = fetchone(sql, params=(username, password))
    if not user_res:
        return JsonResponse(status=200, data={"data": {}, "msg": "用户名/密码错误"})

    return JsonResponse(status=200, data=user_res)


def register(request):
    try:
        params = request.POST
        username = params["username"]
        password = params["password"]
        role = params["role"]
        if role not in ("user", "merchant"):
            raise ValueError("用户类型错误")
    except (ValueError, TypeError, KeyError) as e:
        return JsonResponse(status=400, data={"data": {}, "msg": e})

    sql = "SELECT 1 FROM `user` WHERE username = %s;"
    user_res = fetchone(sql, (username,))
    if user_res:
        return JsonResponse(status=200, data={"data": {}, "msg": "用户名已存在"})

    sql = "INSERT INTO `user` (username, password) VALUES (%s, %s);"
    user_id = execute(sql, (username, password))

    data = {
        "id": user_id,
        "role": role,
        "username": username,
        "avatar": ""  # 初始头像链接
    }

    return JsonResponse(status=200, data=data)


def get_model_list(request):
    try:
        params = request.GET
        merchant_id = int(params["merchant_id"])

        page = int(params.get("page", "1"))
        limit = int(params.get("page", "20"))
        page = 1 if page < 1 else page
        limit = 500 if limit > 500 else limit
        offset = (page - 1) * limit
    except (ValueError, TypeError, KeyError) as e:
        return JsonResponse(status=400, data={"data": {}, "msg": e})


