#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-09 01:30:20
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

from OAuth2.util.zycg import OAuth2
from account import models


def auth_main(request):
    username = request.POST.get('email')
    password = request.POST.get('password')
    auth_acc, auth_err = auth_login_access(request, username, password)

    if request.GET.get('next'):
        return auth_return_home(request.GET.get('next'))

    if auth_acc:
        urls = ''

        return auth_return_home(urls)
    else:
        return auth_return_render(request, username, password, auth_err)


def auth_login_access(request, username, password):
    ''' 用户登录认证 '''

    if not username and not password:
        return False, '请输入用户名和密码！'

    if not username:
        return False, '请输入用户名！'

    if not password:
        return False, '请输入密码！'


    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            from account.models import User as UserModel
            um = UserModel.objects.get(username=request.user.username)
            um.save()
            return True, None
        else:
            return False, '密码有效，但帐户已被禁用！'

    return False, '用户名和密码不正确。'


def auth_logouts(request):  # 用户注销
    username = request.user.username
    logout(request)
    state = models.User.objects.get(username=username).state
    print(type(state))
    if state == '1':
        OA = OAuth2()
        url = OA.AuthLogout()
        return auth_return_Redirect(url=url)

    return auth_return_Redirect()


def auth_return_render(request, username=None, password=None, error=None):
    return render(request, 'defaule/auth/login.html', {'email': username, 'password': password, 'error': error})


def auth_return_Redirect(url=None):
    if url:
        return HttpResponseRedirect(url)

    return HttpResponseRedirect('/auth/login')


def auth_return_home(urls=None):
    if urls:
        return HttpResponseRedirect(urls)

    return HttpResponseRedirect('/')
