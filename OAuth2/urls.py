from django.conf.urls import url
from django.urls import path

from OAuth2 import views

app_name = 'oauth2'

urlpatterns = [
    # url(r'^zycg/$', views.backzycg, name='zycg'),  # 登陆
    url(r'^login_zycg/$', views.zycg, name='login_zycg'),
    path('protocol/<str:state_code>/', views.TokenViewSet.as_view(), name='TokenViewSet'),
    path('zycg/', views.CallbackViewSet.as_view(), name='zycg') # 回调地址
]
