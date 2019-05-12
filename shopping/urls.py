from django.conf.urls import url
from django.urls import path

from shopping import views, view
from django.contrib.auth.decorators import login_required, permission_required

from shopping.view.IndexCartToolpApi import CartToolp

app_name = 'shop'

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='shopping'),
    url(r'^CartToolp/$', view.IndexCartToolpApi.CartToolp.as_view(), name='CartToolp'),
    url(r'^settleAccounts/$', views.PlaceOrderView.as_view(), name='settleAccounts'),
    path('BuyGoods/<int:app_id>/', views.BuyGoods.as_view(), name='BuyGoods'),

    path('PlaceOrder/', views.PlaceOrderView.as_view(), name='PlaceOrderView'),
    path('PlaceOrder/<int:ware_id>/', views.PlaceOrderView.as_view(), name='PlaceOrderView'),
    path('success/<str:order_id>/', views.SuccessView.as_view(), name='success'),
]


