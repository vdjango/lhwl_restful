#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-25 21:25:09
# @Author  : Job (Job@6box.net)
# @Link    : http://www.6box.net
# @Version : $Id$
import json

from django.http import HttpResponse
from django.shortcuts import render

from account.models import User
from lhwill.util import log
from lhwill.views import error_


def get_ip(func):
    '''
    用于验证处理GET请求
    :param func:
    :return:
    '''

    def ip(request, *args, **kwargs):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        log.i(globals(), 'IP: ', ip)

        return func(request, *args, **kwargs)

    return ip


'''验证用户名和邮箱是否注册'''


def auth_register(func):
    '''
    验证用户名和邮箱是否注册
    :param func:
    :return:
    '''

    def register(request, *args, **kwargs):
        email = request.POST.get('email')
        username = request.POST.get('username')
        if User.objects.filter(email=email):
            dic = {
                'error': '邮箱已存在！',
                'state': 'error',
                'code': '403'
            }
            return HttpResponse(json.dumps(dic))
            pass
        if User.objects.filter(username=username):
            dic = {
                'error': '用户已存在！',
                'state': 'error',
                'code': '403'
            }
            return HttpResponse(json.dumps(dic))
            pass
        return func(request, *args, **kwargs)
        pass

    return register
    pass


'''用于验证处理POST请求'''


def _POST(func):
    '''
    用于验证处理POST请求
    :param func:
    :return:
    '''

    def POST(request, *args, **kwargs):
        if request.method != 'POST':
            return error_(request, content='请求错误')
        return func(request, *args, **kwargs)

    return POST


'''用于验证处理GET请求'''


def _GET(func):
    '''
    用于验证处理GET请求
    :param func:
    :return:
    '''

    def GET(request, *args, **kwargs):
        if request.method != 'GET':
            return error_(request, content='请求错误')
        return func(request, *args, **kwargs)

    return GET


'''用于验证操作目标[不能是自己]'''


def _state(func):
    '''
    用于验证操作目标[不能是自己]
    :param func:
    :return:
    '''

    def state(request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        user = request.user.username
        if user == username:
            u = User.objects.get(username=user, )
            if u.email == email:
                dic = {
                    'state': '操作目标不能是自己哦！',
                    'code': '403'
                }
                return HttpResponse(json.dumps(dic))
            pass
        return func(request, *args, **kwargs)

    return state


def Web_Maintain(func):
    @get_ip
    def Maintain(request, *args, **kwargs):
        from managestage.models import maintain
        mm = maintain.objects.filter(inta_allwo=True)
        if mm and not User.objects.filter(username=request.user.username, is_staff=True):
            content = {
                'title': '站点正在维护',
                'content': mm[0].inta_info,
                'code': 'STOP',
                'page': '站点正在维护中！',

            }
            return render(request, 'defaule/error/maintain.html', content)
            pass
        return func(request, *args, **kwargs)

    return Maintain
