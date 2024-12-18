from django.http import JsonResponse
from rest_framework.views import APIView

from client.pojo.cart import Cart


class CartView(APIView):
    def get(self, request):
        """
        获取购物车列表信息
        :param request:
        :return:
        """
        try:
            params = request.GET
            uid = int(params["uid"])
            type_id = params.get("type_id")
            if type_id:
                type_id = int(params["type_id"])
        except (ValueError, TypeError, KeyError) as e:
            return JsonResponse(status=400, data={"msg": "参数类型不合法/缺少必要参数"})

        cart = Cart(uid)
        commodities_rs = cart.get_commodity_list(params)

        return JsonResponse(status=200, data=commodities_rs)

    def post(self, request):
        """
        购物车添加商品
        :param request:
        :return:
        """
        try:
            params = request.POST
            uid = int(params["uid"])
            model_ids = [int(_) for _ in params["model_ids"]]
        except (ValueError, TypeError, KeyError) as e:
            return JsonResponse(status=400, data={"msg": "参数类型不合法/缺少必要参数"})

        cart = Cart(uid)
        add_res = cart.add_commodities(model_ids)

        if not add_res:
            return JsonResponse(status=422, data={"msg": "购物车添加失败"})
        return JsonResponse(status=200, data={"msg": "添加成功"})

    def delete(self, request):
        """
        购物车添加商品
        :param request:
        :return:
        """
        try:
            params = request.POST
            uid = int(params["uid"])
            model_ids = [int(_) for _ in params["model_ids"]]
        except (ValueError, TypeError, KeyError) as e:
            return JsonResponse(status=400, data={"msg": "参数类型不合法/缺少必要参数"})

        cart = Cart(uid)
        add_res = cart.add_commodities(model_ids)

        if not add_res:
            return JsonResponse(status=422, data={"msg": "购物车删除商品失败"})
        return JsonResponse(status=200, data={"msg": "删除成功"})
