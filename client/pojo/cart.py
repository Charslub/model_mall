from typing import List

from django.core.cache import cache

from utils.sql_utils import SQLManager


class Cart:
    def __init__(self, uid):
        self.uid = uid
        self.cart_rs = cache.get(self.uid)

    def add_commodities(self, model_ids: List[int]):
        if self.cart_rs:
            cart_list: List[int] = eval(self.cart_rs)
            cart_list.extend(model_ids)
            sql = "SELECT * FROM model.models WHERE id IN %s;"
            model_rs = SQLManager.fetchmany(sql, cart_list)
            cache.set(self.uid, str(cart_list))
        else:
            sql = "SELECT * FROM model.models WHERE id IN %s;"
            model_rs = SQLManager.fetchone(sql, model_ids)
            cache.set(self.uid, str(model_ids))
        return model_rs

    def delete_commodities(self, model_ids: List[int]):
        if not self.cart_rs:
            return []
        cart_list = [_ for _ in eval(self.cart_rs) if _ not in model_ids]
        sql = "SELECT * FROM model.models WHERE id IN %s;"
        model_rs = SQLManager.fetchmany(sql, cart_list)
        cache.set(self.uid, str(cart_list))
        return model_rs

    def get_commodity_list(self):
        if not self.cart_rs:
            return []
        cart_list = eval(self.cart_rs)
        sql = "SELECT * FROM model.models WHERE id IN %s;"
        model_rs = SQLManager.fetchmany(sql, cart_list)
        return model_rs
