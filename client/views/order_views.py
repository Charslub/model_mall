from datetime import datetime

from django.http import JsonResponse

from client.decorators import token_authenticator
from utils.sql_utils import SQLManager


@token_authenticator
def take_order_handler(request, **kwargs):
    """
    模型购买下单
    :param request:
    :return:
    """
    try:
        params = request.POST
        uid = kwargs["uid"]
        for model in params["model_list"]:
            model_id = int(model["model_id"])
            merchant_id = int(model["merchant_id"])
        model_ids = [_["model_id"] for _ in params["model_list"]]
        assert params["model_list"], "模型列表不可为空"
    except (AssertionError, ValueError, KeyError, TypeError) as e:
        return JsonResponse(status=400, data={"data": {}, "msg": f"参数错误，{e}"})

    # 校验模型下架情况
    sql = "SELECT id, price, model_name, is_available FROM model.models WHERE id IN %s;"
    model_rs = SQLManager.fetchmany(sql, params=(model_ids,))
    if not model_rs:
        return JsonResponse(status=410, data={"data": {}, "msg": "模型不存在"})

    unavailable_model_names = [_["model_name"] for _ in model_rs if not _["is_available"]]
    if unavailable_model_names:
        # 结算未下架部分
        model_prices = round(sum([float(_["price"]) for _ in model_rs if _["is_available"]]), 2)
        # TODO:用户账户扣费

        unavailable_names = ", ".join(unavailable_model_names)
        return JsonResponse(status=200, data={"data": {}, "msg": f"已自动结算，总价：{model_prices}，{unavailable_names}模型已下架；"})
    model_prices = round(sum([float(_["price"]) for _ in model_rs]), 2)
    # TODO:用户账户扣费
    return JsonResponse(status=200, data={"data": {}, "msg": f"已结算，总价：{model_prices}；"})


@token_authenticator
def get_order_list_handler(request, **kwargs):
    """
    获取指定用户订单列表
    :param request:
    :param kwargs:
    :return:
    """
    try:
        uid = kwargs["uid"]
        params = request.GET
        page = int(params.get("page", 1))
        limit = int(params.get("limit", 10))
        order_by = params.get("order_by", "DESC")
        filter_str = params.get("filter_str", "")
        start_time = params.get("start_time", "")
        end_time = params.get("end_time", "")
        offset = (page - 1) * limit
        if order_by.upper() not in ("DESC", "ASC"):
            raise ValueError("不合法的排序方式")
        if start_time:
            start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        if end_time:
            end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    except (KeyError, TypeError, ValueError) as e:
        return JsonResponse(status=400, data={"data": {}, "msg": f"参数错误，{e}"})

    condition_sql, condition_list = [], []
    if filter_str:
        # 筛选模型名称
        condition_sql.append("model_name LIKE %s")
        condition_list.append(filter_str)
        # 筛选商店名称
        sql = "SELECT id FROM model.users WHERE role = 'merchant' AND username LIKE %s;"
        merchant_rs = SQLManager.fetchmany(sql, params=(filter_str,))
        if not merchant_rs:
            return JsonResponse(status=200, data={"data": {"total": 0, "data": []}})
        condition_sql.append("uid IN %s")
        condition_list.append([_["id"] for _ in merchant_rs])
    if start_time:
        condition_sql.append("create_time >= %s")
        condition_list.append(start_time)
    if end_time:
        condition_sql.append("create_time <= %s")
        condition_list.append(end_time)

    # sql = "SELECT SQL_CALC_FOUND_ROWS * FROM model.orders WHERE"
