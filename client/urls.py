from django.template.defaulttags import url

from client.views import user_views, model_views, cart_views
from client.views.cart_views import CartView

urlpatterns = [
    # 用户接口
    url(r'^client/login/$', user_views.login, name='client_login'),
    url(r'^client/register/$', user_views.register, name='client_register'),

    # 模型接口
    url(r'^models/$', model_views.get_model_list, name='get_model_list'),

    # 购物车相关接口
    url(r'^carts/$', CartView.as_view(), name='cart_operations'),
]
