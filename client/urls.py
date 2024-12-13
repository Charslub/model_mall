from django.template.defaulttags import url

from client.views import user_views, model_views, cart_views

urlpatterns = [
    url(r'^client/$', user_views),
    url(r'^models/$', model_views),
    url(r'^carts/$', cart_views),
]
