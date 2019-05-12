from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import render

from account import models
from lhwill import settings
from lhwill.util import log
from lhwill.views import error_
from social_django.models import UserSocialAuth
from account.models import User, UserProfix, Md5Salt


def auth_login_url(func):
    '''跳转 next=/.../.../'''

    def auth_url(request, *args, **kwargs):
        if request.method == 'GET' and request.GET.get('next'):
            return HttpResponseRedirect(request.GET.get('next'))

        return func(request, *args, **kwargs)

    return auth_url


'''设置最近登陆时间'''


def auth_login_access(func):
    '''
    设置最近登陆时间
    :param func:
    :return:
    '''

    @login_required(redirect_field_name='next', login_url='/auth/login/')
    def login(request, *args, **kwargs):
        username = request.user.username
        u = models.User.objects.get(username=username)
        u.save()
        return func(*args, **kwargs)

    return login
    pass


'''装饰器-账号注册-找回密码
验证账号注册，邮箱是否完成验证
'''


def auth_access(send_type='register'):
    def a_access(func):
        '''
        验证账号注册，邮箱是否完成验证
        send_type: [register/retrieve] [注册/找回密码]
        :param func:
        :return:
        '''

        def access(request, send_type=send_type, *args, **kwargs):
            email = request.GET.get('email')
            if email:
                if send_type == 'register':
                    send_type = 'register'
                    print('send_type', send_type)

                    if not models.UserProfix.objects.filter(email=email, send_type=send_type, defaule=False):
                        return render(request, 'defaule/auth/retrieve.html', {
                            'error': '无效的地址,非法操作'
                        })
                    pass
                else:
                    send_type = 'retrieve'
                    print('send_type', send_type)
                    if not models.UserProfix.objects.filter(email=email, send_type=send_type, code_defaule=True):
                        return render(request, 'defaule/auth/retrieve.html', {
                            'error': '无效的地址,非法操作'
                        })
                    pass

            return func(request, *args, **kwargs)

        return access

    return a_access


'''验证第三方登陆是否设置密码'''


def auth_filter(func):
    '''
    验证第三方登陆是否设置密码
    :param func:
    :return:
    '''

    def filter(request, *args, **kwargs):
        username = request.user.username
        if not UserSocialAuth.objects.filter(user__username=username, defaule=False):
            print('UserSocialAuth')
            if request.GET.get('next'):
                return HttpResponsePermanentRedirect(request.GET.get('next'))
            return HttpResponsePermanentRedirect('/')
            pass
        return func(request, *args, **kwargs)

    return filter


'''验证用户是否是管理员'''


def auth_admin(func):
    '''
    验证用户是否是管理员
    登陆以验证
    否则返回403
    :param func:
    :return:
    '''
    from managestage.utli.auth_permissions import user_admin
    from django.views.decorators.cache import never_cache
    @login_required()
    @never_cache
    def is_auth(*args, **kwargs):
        request = args[0]
        username = request.user.username
        if user_admin(str(username)) != True:
            print('您不是管理员哦！')
            return error_(request, 404)
        return func(*args, **kwargs)

    return is_auth


def auth_AtomSigns(func):
    def AtomSigns(request, *args, **kwargs):
        print('AtomText', request.get_full_path())
        email = request.GET.get('email')
        auto = request.GET.get('auto')
        path = str(request.get_full_path()).split('?')[1].split('&')
        Atom = {}
        for i in path:
            vk = i.split('=')
            if len(vk) > 1:
                Atom[vk[0]] = vk[1]

        print('path', Atom)
        u = ''
        for a in Atom:
            u += a
            u += '='
            u += Atom[a]
            u += '&'

        from account.util.AtomSign import AtomSig
        url = "{}/?{}".format(settings.HTTP_HOST, u)
        md5salt = Md5Salt.objects.filter(email=email)
        if md5salt:
            As, salt = AtomSig(request, url, stype='unlock', salt=md5salt[0].salt)
            salt = bytes.decode(salt)
            print('As', As, salt)

        return func(request, *args, **kwargs)

    return AtomSigns
    pass


'''
''验证并设置用户状态[未验证|普通|管理员] ''
auth.models.User类里面的is_staff决定了是否为超级管理员
account.UserProfix类的state决定了用户的状态[未验证|普通|管理员]

UserProfix和User类 互相关联但不存在Forkey关系
当User为超级管理员时：UserProfix.state = 2 [目前只能判断User是否为超级管理员]
'''


def auth_state(func):
    def state(request, *args, **kwargs):
        username = request.user.username
        defaultUser = User.objects.filter(username=username)
        if defaultUser:
            '''当User[is_staff]为超级管理员 设置state状态为超级管理员 '''
            for i in defaultUser:

                '''设置state状态为超级管理员'''
                if i.is_staff:
                    i.state = 2
                    i.save()

        return func(request, *args, **kwargs)
        pass

    return state
    pass


def auth_LoginClose(func):
    '''
    设置用户登录失效时间 - 用户浏览器关闭失效【记住登录状态】
    :param func:
    :return:
    '''

    def LoginClose(request, *args, **kwargs):
        if request.method == 'POST':
            log.i(globals(), '设置登录失效方式: get', request.POST.get('keepcheckbox'))
            if not request.POST.get('keepcheckbox'):
                request.session.set_expiry(0)
                log.i(globals(), '设置登录失效方式: 浏览器关闭失效')
        return func(request, *args, **kwargs)

    return LoginClose


def auth_RegisterAgreement(func):
    '''
    验证用户注册是否勾选 用户协议
    :param func:
    :return:
    '''

    def RegisterAgreement(request, *args, **kwargs):
        if request.method == 'POST':
            if request.POST.get('keepcheckbox') != '0':
                email = request.POST.get('email')
                username = request.POST.get('username')
                content = {
                    'email': email,
                    'username': username,
                    'error': '请您仔细阅读用户协议并勾选'
                }
                return render(request, 'defaule/auth/register.html', content)
        return func(request, *args, **kwargs)

    return RegisterAgreement
    pass
