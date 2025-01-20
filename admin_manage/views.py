from django.http import JsonResponse
from django.shortcuts import render
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from django.core.files.storage import FileSystemStorage

from utils.sql_utils import SQLManager


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
    user_res = SQLManager.fetchone(sql, params=(username, password))
    if not user_res:
        return JsonResponse(status=200, data={"data": {}, "msg": "用户名/密码错误"})
    if user_res["role"] not in ("admin", "super"):
        return JsonResponse(status=200, data={"data": {}, "msg": "权限不足"})

    return JsonResponse(status=200, data=user_res)


# 模型上传（包含识别，核心）
def add_model(request):
    """
    添加新模型，并执行图像识别
    :param request: POST请求，其中包含图像文件
    :return: JsonResponse, 返回分类结果
    """
    try:
        if request.method == "POST" and request.FILES.get("image"):
            img_file = request.FILES["image"]

            # 保存上传的文件到指定目录
            fs = FileSystemStorage(location='media/images')  # 设置文件保存目录
            filename = fs.save(img_file.name, img_file)
            img_url = fs.url(filename)  # 获取文件的URL

            # 使用预训练模型进行图像分类
            image_classification = pipeline(
                Tasks.image_classification,
                model='damo/cv_vit-base_image-classification_Dailylife-labels'
            )
            result = image_classification(img_url)  # 传入文件的URL进行识别

            # 返回识别结果
            return JsonResponse(status=200, data={"result": result, "img_url": img_url})

        else:
            return JsonResponse(status=400, data={"msg": "未上传图片文件"})

    except Exception as e:
        return JsonResponse(status=500, data={"msg": str(e)})


# 模型列表获取
def get_model_list(request):
    """
    获取所有模型列表
    :param request:
    :return: JsonResponse, 返回模型列表
    """
    try:
        # 假设我们从数据库中获取模型列表
        sql = "SELECT id, name, description FROM model;"
        models = SQLManager.fetchone(sql)
        return JsonResponse(status=200, data={"models": models})

    except Exception as e:
        return JsonResponse(status=500, data={"msg": str(e)})


# 模型编辑
def edit_model(request):
    """
    编辑模型的基本信息
    :param request: POST请求，包含模型ID及需要更新的数据
    :return: JsonResponse, 返回操作结果
    """
    try:
        model_id = request.POST.get("model_id")
        model_name = request.POST.get("model_name")
        model_description = request.POST.get("model_description")

        if not model_id or not model_name:
            return JsonResponse(status=400, data={"msg": "缺少必要参数"})

        # 更新模型信息到数据库
        sql = """
            UPDATE model
            SET name = %s, description = %s
            WHERE id = %s;
        """
        SQLManager.execute(sql, params=(model_name, model_description, model_id))

        return JsonResponse(status=200, data={"msg": "模型更新成功"})

    except Exception as e:
        return JsonResponse(status=500, data={"msg": str(e)})
