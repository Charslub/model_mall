from typing import List

from django.core.cache import cache
from django.urls import path
from django.views.decorators.http import require_GET

from utils.sql_utils import SQLManager


@require_GET
@path("", name="get_models")
class Cart:
    def __init__(self, uid):
        self.uid = uid
        self.cart_rs = cache.get(self.uid)

    def add_commodities(self, model_ids: List[int]):
        try:
            if self.cart_rs:
                cart_list: List[int] = eval(self.cart_rs)
                cart_list.extend(model_ids)
                cache.set(self.uid, str(cart_list))
            else:
                cache.set(self.uid, str(model_ids))
            return True
        except Exception as e:
            return False

    def delete_commodities(self, model_ids: List[int]):
        try:
            if not self.cart_rs:
                return []
            cart_list = [_ for _ in eval(self.cart_rs) if _ not in model_ids]
            cache.set(self.uid, str(cart_list))
            return True
        except Exception:
            return False

    def get_commodity_list(self, params):
        try:
            if not self.cart_rs:
                return []
            cart_list = eval(self.cart_rs)
            condition_sql, condition_list = [], []
            type_id = params.get("type_id")

            if type_id:
                sql = "SELECT model_id FROM model.models_types WHERE type_id = %s;"
                model_type_rs = SQLManager.fetchmany(sql, params=(type_id,))
                if not model_type_rs:
                    return {"total": 0, "data": []}
                cart_list = list(set(cart_list.extend([_["model_id"] for _ in model_type_rs])))

            sql = (
                "SELECT SQL_CALC_FOUND_ROWS id, uid, model_name, img_url, create_time, update_time "
                "FROM model.models "
                "WHERE id IN %s AND is_available = 1;"
            )
            model_rs, total = SQLManager.fetchmany_total(sql, cart_list)
            return {"total": total, "data": model_rs}
        except Exception as e:
            # 日志记录
            return {"total": 0, "data": []}
