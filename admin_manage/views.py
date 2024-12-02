from django.http import JsonResponse
from django.shortcuts import render

from utils.sql_utils import fetchone


# Create your views here.

def login(request):
    """
    管理端登录
    :param request:
    :return:
    """
    try:
        params = request.POST
        username = params["username"]
        password = params["password"]
    except (ValueError, TypeError, KeyError):
        return JsonResponse(status=400, data={})

    sql = "SELECT id, username, avater, role FROM user WHERE username = %s AND password = %s;"
    user_res = fetchone(sql, params=(username, password))
    if not user_res:
        return JsonResponse(status=200, data={"data": {}, "msg": "用户名/密码错误"})
    if user_res["role"] not in ("admin", "super"):
        return JsonResponse(status=200, data={"data": {}, "msg": "权限不足"})

    return JsonResponse(status=200, data=user_res)


# 模型上传（包含识别，核心）
def add_model():

    pass


# 模型列表获取
def get_model_list():
    pass


# 模型编辑
def edit_model():
    pass

