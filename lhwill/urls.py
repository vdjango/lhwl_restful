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
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.views.static import serve

from lhwill import views
from lhwill.settings import MEDIA_ROOT
from lhwill.util.AutomaticCollection import ZnanrenSitemaps
from search.views import RestfulSearchView

sitemaps = {
    'WareApp': ZnanrenSitemaps,
}


urlpatterns = [
    path('', include('app.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('error/', views.error_),


    path('admin/', include('managestage.urls')),

    path('auth/', include('account.urls')),
    path('shopping/', include('shopping.urls')),
    path('auth/', include('social_django.urls')),
    path('home/', include('home.urls')),
    url('^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('favicon.ico', RedirectView.as_view(url=r'static/favicon.ico', permanent=True)),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('plate/', include('plate.urls'))
    # url(r'^payment/', include('payment.urls'))

]
