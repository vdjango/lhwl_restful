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
from django.views import generic

from app import views, view
from app.view import app_navaid, AboutView
from app.view.app_navaid import IndexView

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('details/<int:details_id>/', views.IndexDetailsView.as_view(), name='details'),
    path('details/<int:details_id>/<str:details_slug>/', views.IndexDetailsView.as_view(), name='detailsnew'),
    path('Assortment/<int:class_id>/', views.Assortment.as_view(), name='assortment'),
    path('IndexView/', IndexView.as_view(), name='IndexView'),
    path('about/', generic.TemplateView.as_view(template_name='defaule/about/index.html'), name='about'),
    path('about/us/', generic.TemplateView.as_view(template_name='defaule/about/about.html'), name='us'),

    url(r'^setPlus/$', views.setPlus, name='setPlus'),
    url(r'^contrast/$', views.Contrast, name='contrast'),
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^personal/$', views.personal, name='personal'),
    url(r'^navaid/(\d+)/$', app_navaid.navaid, name='app_navaid'),

    path('pdf/', views.PDF.as_view())

]
