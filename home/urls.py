"""Retailers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    url(r'^generateOrder_delete/$', views.generateOrder_delete, name='generateOrder_delete'),
    url(r'^address/$', views.address, name='address'),
    url(r'^addaddress/$', views.addAddress, name='addaddress'),
    url(r'^setaddress/$', views.setaddress, name='setaddress'),
    url(r'^deladdress/$', views.deladdress, name='deladdress'),
    url(r'^getaddress/$', views.getAddress, name='getaddress'),
    url(r'^settlement/$', views.Settlement, name='settlement'),
    url(r'^delorider/$', views.delorider, name='delorider'),
    url(r'^getlogistics/$', views.getlogistics, name='getlogistics'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^invoice/$', views.Invoice, name='invoice'),
    url(r'^contract/$', views.Contract, name='contract'),
    url(r'^ordercontract1/(\d+)/$', views.OrderContract, name='ordercontract'),

    path('ordercontract/<str:id>/', views.PDFOrderContract.as_view(), name='ordercontract'),
    path('', views.Index.as_view(), name='index'),

    url(r'^getpulContract/$', views.getpulContract, name='getpulContract'),
    url(r'^setContract/$', views.setContract, name='setContract'),
]
