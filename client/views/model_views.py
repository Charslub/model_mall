from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_GET

from utils.sql_utils import SQLManager


@require_GET
def get_model_list(request):
    """
    获取模型列表信息
    :param request:
    :return:
    """
    try:
        params = request.GET
        merchant_id = int(params.get("merchant_id", "0"))
        type_id = int(params.get("type_id", "0"))
        is_available = int(params.get("is_available", "-1"))

        page = int(params.get("page", "1"))
        limit = int(params.get("limit", "20"))
        page = 1 if page < 1 else page
        limit = 500 if limit > 500 else limit
        offset = (page - 1) * limit
    except (ValueError, TypeError, KeyError) as e:
        return JsonResponse(status=400, data={"data": {}, "msg": e})

    condition_sql, condition_list = [], []
    if merchant_id:
        condition_sql.append("m.uid = %s")
        condition_list.append(merchant_id)
    if type_id:
        condition_sql.append("mt.type_id = %s")
        condition_list.append(type_id)
    if is_available >= 0:
        condition_sql.append("m.is_available = %s")
        condition_list.append(is_available)

    condition_sql = " AND ".join(condition_sql)
    if condition_sql:
        condition_sql = "AND " + condition_sql
    condition_list.extend([offset, limit])

    sql = (
        "SELECT SQL_CALC_FOUND_ROWS "
        "m.id, uid, model_name, img_url, is_available, m.create_time, m.update_time, t.type_name, "
        "mt.type_id, t.type_level, t.is_system, m.uid AS merchant_id, "
        "u.username AS merchant_name "
        "FROM model.models_types mt "
        "LEFT JOIN model.models m on m.id = mt.model_id "
        "LEFT JOIN model.types t on t.id = mt.type_id "
        "LEFT JOIN model.users u ON m.uid = u.id "
        f"WHERE m.delete_flag = 0 {condition_sql} LIMIT %s, %s;"
    )
    model_rs, total = SQLManager.fetchmany_total(sql, condition_list)

    model_dict = {}
    for model in model_rs:
        if model["id"] in model_dict.keys():
            model_dict[model["id"]]["types"].append({
                "id": model["type_id"],
                "type_name": model["type_name"],
                "type_level": model["type_level"],
                "is_system": model["is_system"],
            })
        else:
            model_dict[model["id"]] = {
                "id": model["id"],
                "merchant_id": model["merchant_id"],
                "merchant_name": model["merchant_name"],
                "model_name": model["model_name"],
                "img_url": model["img_url"],
                "types": [
                    {
                        "id": model["type_id"],
                        "type_name": model["type_name"],
                        "type_level": model["type_level"],
                        "is_system": model["is_system"],
                    }
                ]
            }

    return JsonResponse(status=200, data={"total": total, "data": model_dict.values()})


def upload_models(request):
    """
    模型上传
    :param request:
    :return:
    """
    pass


def download_models(request):
    """
    模型下载
    :param request:
    :return:
    """
    pass


def discern_models(request):
    """
    模型类型识别
    :param request:
    :return:
    """
    # TODO: 微服务调用识别模型内容
    pass
