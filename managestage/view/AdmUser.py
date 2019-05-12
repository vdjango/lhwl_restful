'''
后台用户功能实现
'''

import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render

from account import models
from account.models import User, UserProhibit, UserProfix
from account.util.decorator import auth_admin
from lhwill.util.complete import MainTain
from managestage.form import AdmUser_from
from managestage.form.AdmUser_from import add_user_From
from managestage.utli import datetimenow, HttpUrl
from managestage.utli.datetimenow import date_new
from managestage.utli.wrapper import _POST, Web_Maintain, _state, auth_register, _GET
from managestage.views import TIMEDATES

'''用户管理'''


@_POST
@Web_Maintain
@auth_admin
def get_username(request):
    '''
    请求用户列表
    :param request:
    :return:
    '''
    usermodel = User.objects.filter()
    aa = []
    for i in usermodel:
        aa.append({
            'id': i.id,
            'username': i.username
        })
    content = {
        'user': aa,
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


@_POST
@_state  # 自己的账号无法删除
@Web_Maintain
@auth_admin
def del_user(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    User.objects.get(username=username, email=email).delete()
    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''修改邮箱'''


@_POST
@Web_Maintain
@auth_admin
def set_email(request):
    '''
    修改邮箱
    :return:
    '''
    email = request.POST.get('email')
    username = request.POST.get('username')
    newemail = request.POST.get('newemail')
    user = models.User.objects.filter(username=username, email=email)
    if user:
        if models.User.objects.filter(email=newemail):
            content = {
                'state': '邮件已被使用',
                'code': '401'
            }
            return HttpResponse(json.dumps(content))
            pass
        if not newemail:
            content = {
                'state': '您还没有输入邮箱',
                'code': '402'
            }
            return HttpResponse(json.dumps(content))
            pass
        user[0].email = newemail
        user[0].save()
        content = {
            'state': 'success',
            'code': '200'
        }
        return HttpResponse(json.dumps(content))
    content = {
        'state': '用户不存在',
        'code': '400'
    }
    return HttpResponse(json.dumps(content))
    pass


'''修改用户名'''


@_POST
@Web_Maintain
@auth_admin
def set_username(request):
    '''
    修改用户名
    :return:
    '''
    email = request.POST.get('email')
    username = request.POST.get('username')
    newusername = request.POST.get('newusername')
    user = models.User.objects.filter(username=username, email=email)
    if user:
        if models.User.objects.filter(username=newusername):
            content = {
                'state': '称呼已被使用',
                'code': '401'
            }
            return HttpResponse(json.dumps(content))
            pass
        if not newusername:
            content = {
                'state': '您还没有输入称呼',
                'code': '402'
            }
            return HttpResponse(json.dumps(content))
            pass
        user[0].username = newusername
        user[0].save()
        content = {
            'state': 'success',
            'code': '200'
        }
        return HttpResponse(json.dumps(content))
    content = {
        'state': '用户不存在',
        'code': '400'
    }
    return HttpResponse(json.dumps(content))
    pass


'''修改用户密码'''


@_POST
@Web_Maintain
@auth_admin
def set_password(request):
    '''
    修改用户密码
    :return:
    '''
    email = request.POST.get('email')
    username = request.POST.get('username')
    newpassword = request.POST.get('newpassword')
    user = models.User.objects.filter(username=username, email=email)
    if user:
        if not newpassword:
            content = {
                'state': '您还没有输入密码',
                'code': '402'
            }
            return HttpResponse(json.dumps(content))
            pass
        user[0].set_password(newpassword)
        user[0].save()
        if username == request.user.username:
            login(request, authenticate(username=username, password=newpassword))

        content = {
            'state': 'success',
            'code': '200'
        }
        return HttpResponse(json.dumps(content))
    content = {
        'state': '用户不存在',
        'code': '400'
    }
    return HttpResponse(json.dumps(content))



@_POST
@Web_Maintain
@auth_admin
def set_admin(request):
    '''
    设置管理员
    :param request:
    :return:
    '''
    uid = request.POST.get('id')
    try:
        u = User.objects.get(id=uid)
        if u.is_staff:
            u.is_staff = False
        else:
            u.is_staff = True
        u.save()
    except Exception as e:
        content = {
            'state': '用户Error',
            'code': '404'
        }
        return HttpResponse(json.dumps(content))

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))


'''创建用户'''


@_POST
@auth_register  # 判断用户名和邮箱是否注册
@Web_Maintain
@auth_admin
def add_user(request):
    '''
    创建用户
    :return:
    '''
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    groupname = request.POST.get('groupname')
    # vipgroup = request.POST.get('password')

    froms = add_user_From(request.POST)
    if froms.is_valid():
        t = datetimenow.datetimenow()
        User.objects.create_user(username=username, email=email, password=password).save()
        try:
            u = User.objects.get(username=username, email=email)
            G = Group.objects.get(id=groupname)
            u.groups.add(G)
            UserProfix(
                email=email,
                username=username,
                send_type='register',
                defaule=False,
                timedate=t,
                addtime=t,
                oneKey=u
            ).save()
        except Exception as e:
            content = {
                'error': '创建用户失败',
                'state': 'error',
                'code': '500'
            }
            return HttpResponse(json.dumps(content))

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))



'''新用户审核'''


@_GET
@Web_Maintain
@auth_admin
def examine(request, lens=1):
    '''
    用户审核
    :param lens:
    :return:
    '''
    usermodel = User.objects.filter(state=-1)
    Front, After = HttpUrl.UrlSection(int(lens), '/admin/prohibit/')
    tain = MainTain()
    maintain = tain.get_tain()
    usersize = len(usermodel)
    content = {
        'userlist': usermodel,
        'usersize': usersize,
        'Front': Front,
        'After': After,
        'maintain': maintain
    }
    return render(request, 'defaule/admin/user/examine.html', content)
    pass


'''用户审核完成验证'''


@_POST
@Web_Maintain
@auth_admin
def set_examine(request):
    '''
    用户审核完成验证
    :return:
    '''
    uid = request.POST.get('uid')
    u = User.objects.filter(id=uid)
    print('User ', u)
    if u:
        print('User save')
        u[0].state = 0
        u[0].save()
        up = UserProfix.objects.filter(email=u[0].email)
        if up:
            print('UserProhibit save 2')
            up[0].code_default = True
            up[0].defaule = True
            up[0].save()

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''用户组管理'''


