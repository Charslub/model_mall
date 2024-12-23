from django.urls import path

from client.views import user_views, model_views, cart_views
from client.views.cart_views import CartView

urlpatterns = [
    # 用户接口
    path(r'client/login/', user_views.login, name='client_login'),
    path(r'client/register/', user_views.register, name='client_register'),

    # 模型接口
    path(r'models/', model_views.get_model_list, name='get_model_list'),

    # 购物车相关接口
    path(r'carts/', CartView.as_view(), name='cart_operations'),
]
