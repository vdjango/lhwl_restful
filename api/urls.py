from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from api import views
from api.WareApp.getWareApp import getWare
from api.router import routerLogical, routerModel, RouterMethodPrivate, RouterMethodPublic, RouterModelPrivate, \
    RouterModelPublic, RouterAdminPrivate

app_name = 'api'

urlpatterns = [
    # 新接口
    path('v2/', views.IndexV2.as_view()),
    path('v2/', include('search.urls')),
    path('v2/authorization/', obtain_jwt_token),
    path('v2/authorization-refresh/', refresh_jwt_token),
    path('v2/authorization-verify/', verify_jwt_token),
    path('v2/model-public/', include(RouterModelPublic.Router().get_router())),
    path('v2/model-private/', include(RouterModelPrivate.Router().get_router())),
    path('v2/method-public/', include(RouterMethodPublic.Router().get_router())),
    path('v2/method-private/', include(RouterMethodPrivate.Router().get_router())),

    path('v2/admin/', include(RouterAdminPrivate.Router().get_router())),

    # 即将废弃 预留兼容老版本接口
    # 获取令牌
    # 刷新令牌
    # 验证令牌
    path('', views.IndexV1.as_view()),
    path('authorization/', obtain_jwt_token),
    path('authorization-refresh/', refresh_jwt_token),
    path('authorization-verify/', verify_jwt_token),
    path('v1/', include(routerModel.RouterModel().get_router())),
    path('v1/logical/', include(routerLogical.RouterModel().get_router())),

    # 废弃
    path('choice/', views.get_Choice, name='choice'),
    path('imageUp/', views.imageUp, name='imageup'),
    path('getWare/', getWare, name='getWare')
]
