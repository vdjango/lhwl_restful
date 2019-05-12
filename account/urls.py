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
from django.conf.urls import url, include
from account import views

app_name = 'auth'

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(), name='login'),  # 登陆
    url(r'^register/$', views.RegisterView.as_view(), name='register'),  # 注册
    url(r'^logout/$', views.logout_access, name='logout'),  # 登出
    url(r'^retrieve/$', views.retrieve_access, name='retrieve'),  # 找回密码
    url(r'^active/(?P<active_code>.*)/', views.activeUser_access, name="activeuser"),  # 注册账号邮箱验证
    url(r'^auth_retrieve/$', views.auth_retrieve, name='auth_retrieve'),  # 找回密码验证
    url(r'^new_password/$', views.new_password_access, name='new_password'),  # 密码修改操作
    url(r'^update_code/$', views.updateCode_access, name='updatecode'),  # 重新获取注册账号邮箱验证码
    url(r'^setpass/(?P<usercode>.*)/$', views.setthisPass, name='setthispass'),
    url(r'^login/oauth2/', include('OAuth2.urls'), name='oauth2')
]


