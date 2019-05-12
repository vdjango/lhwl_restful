import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from lhwill.view import AppGenric

from OAuth2.models import UserToken
from OAuth2.util.zycg import OAuth2
from account import models
from account.form import retrieve_form
from account.util.decorator import auth_AtomSigns, auth_access, auth_LoginClose, auth_RegisterAgreement
# Create your views here.
from account.util.email import login_mail
from account.util.email import nu
from account.util.email_send import send_auth_email, Email
from account.view import auth_login, auth_register as auth_reg
from lhwill.util.log import log
from lhwill.views import error_
from managestage.utli.wrapper import Web_Maintain, get_ip

logger = log(globals())


decorators = [auth_RegisterAgreement, get_ip]


@method_decorator(decorators, name='dispatch')
class RegisterView(AppGenric.AppTemplateView):
    '''
    用户注册
    '''
    template_name = 'defaule/auth/register.html'
    template_mobile_name = 'defaule/m/auth/register.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:index'))
            pass

        return super(RegisterView, self).render_to_response(context, **response_kwargs)

    def post(self, *args, **kwargs):
        return auth_reg.auth_main(self.request)


decorators = [login_mail, auth_LoginClose, get_ip]


@method_decorator(decorators, name='dispatch')
class LoginView(AppGenric.AppTemplateView):
    '''
    用户登录
    '''
    template_name = 'defaule/auth/login.html'
    template_mobile_name = 'defaule/m/auth/login.html'

    def render_to_response(self, context, **response_kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('app:index'))
            pass

        return super(LoginView, self).render_to_response(context, **response_kwargs)

    def post(self, *args, **kwargs):
        login_auto = auth_login.auth_main(self.request)
        return login_auto
        pass

    pass


'''找回密码视图'''


@Web_Maintain
@auth_access(send_type='retrieve')
@get_ip
def retrieve_access(request):
    '''
    找回密码
    :param request:
    :return:
    '''
    if request.method == 'GET':
        return render(request, 'defaule/auth/retrieve.html')

    if request.method == 'POST':
        name = request.POST.get('email')
        forms = retrieve_form.Form(request.POST)
        if forms.is_valid():
            modeUser = models.User.objects.filter(email=name)
            records = models.UserProfix.objects.filter(email=name, send_type='retrieve')

            if modeUser:
                if records:
                    for line in records:
                        datetime = nu(line.addtime)
                        if datetime > 60 or datetime < 0:
                            datetime = 0
                        else:
                            datetime = 60 - datetime
                            pass

                        logger.i(line)

                        if datetime != 0:
                            return render(request, 'defaule/auth/retrieve.html', {'stats': '请在{}秒后重试'.format(datetime)})
                            pass

                        line.code_default = True
                        line.save()
                        pass

                send_auth_email(request, send_type='retrieve', Users=modeUser)

                return render(request, 'defaule/auth/retrieve.html', {'stats': '邮件以发送，请在5分钟内完成操作!'})

            else:
                return render(request, 'defaule/auth/retrieve.html', {'error': '请输入正确的邮箱地址'})

        content = {
            'error': forms.errors
        }
        return render(request, 'defaule/auth/retrieve.html', content)
    pass


'''通过验证码找回密码 '''


@Web_Maintain
@auth_AtomSigns
@get_ip
def auth_retrieve(request):
    if request.method == 'GET':
        auto = request.GET.get('auto')
        email = request.GET.get('email')
        if auto and email:
            all_records = models.UserProfix.objects.filter(email=email, send_type='retrieve', code=auto,
                                                           code_default=True)
            if all_records:
                datetime = nu(all_records[0].addtime)
                if datetime < 300 and datetime > 0:
                    logger.i(datetime)
                    content = {
                        'auto': auto,
                        'email': email,
                        'username': all_records[0].username
                    }
                    return render(request, 'defaule/auth/retrieve_edit.html', content)
    return error_(request, 404)


@Web_Maintain
@auth_access(send_type='retrieve')
@get_ip
def new_password_access(request):
    '''
    密码修改操作[找回密码]
    :param request:
    :return:
    '''
    if request.method == 'POST':
        forms = retrieve_form.new_passwd(request.POST)
        logger.i('forms objects', forms)
        if forms.is_valid():
            email = request.POST.get('email')
            auto = request.POST.get('auto')
            passwd = request.POST.get('password')
            user = models.UserProfix.objects.filter(email=email, code=auto, send_type='retrieve', code_default=True)
            logger.i('User objects', user, email, auto)
            if user:
                U = models.User.objects.filter(username=user[0].username, email=user[0].email)
                logger.i('UUU objects', U)
                if U:
                    U[0].set_password(passwd)
                    U[0].save()
                user[0].code_default = False
                user[0].save()

    return HttpResponseRedirect('/auth/login/')


@login_required
def logout_access(request):
    '''
    登出
    :param request:
    :return:
    '''

    return auth_login.auth_logouts(request)


'''找回密码[未登陆]'''


@Web_Maintain
@get_ip
def activeUser_access(request, active_code):
    '''
    找回密码[未登陆]
    :param request:
    :param active_code:
    :return:
    '''
    logger.i('activeUser_access')
    email = request.GET.get('email')

    all_records = models.UserProfix.objects.filter(email=email, defaule=False, code=active_code)
    logger.i('activeUser_access', all_records)
    if all_records:
        for record in all_records:
            datetime = nu(record.addtime)
            if datetime < 1800 and datetime > 0:
                logger.i('all_records')
                record.defaule = True
                record.oneKey.state = 0
                record.oneKey.save()
                record.save()
            else:
                logger.i('all_records', '地址以过期')
    logger.i('active_code', all_records)
    return HttpResponseRedirect('/')
    pass


# @login_mail
@Web_Maintain
@login_required
@get_ip
def updateCode_access(request):
    if request.method != 'POST':
        return HttpResponse('')
    '''
    注册重新发送验证码
    :param request:
    :return:
    '''
    username = request.user.username
    E = Email()
    send_auth_email(request, send_type="register")

    dic = {
        'code': 200,
        'username': username
    }
    return HttpResponse(json.dumps(dic))
    pass


@get_ip
def setthisPass(request, usercode):
    OA = OAuth2()

    back_url = request.GET.get('next')
    state = request.GET.get('state')

    if request.method == 'GET':
        content = {
            'usercode': usercode
        }
        return render(request, 'defaule/auth/setpass.html', content)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if not username or not password or not password1:
            content = {
                'error': '用户名或密码没有填写',
                'username': username,
                'usercode': usercode,
            }
            return render(request, 'defaule/auth/setpass.html', content)

        if password != password1:
            content = {
                'error': '重复密码不一致',
                'username': username,
                'usercode': usercode,
            }
            return render(request, 'defaule/auth/setpass.html', content)

        uinfo = models.UserInfo.objects.get(usercode=usercode)

        if models.User.objects.filter(Q(username=username)):
            content = {
                'error': '用户以注册，换一个试试',
                'username': username,
                'usercode': usercode,
            }
            return render(request, 'defaule/auth/setpass.html', content)

        uToken = UserToken.objects.get(usercode=usercode)

        user = models.User.objects.create_user(username=username, email=uinfo.email, usercode=usercode,
                                               password=password)
        user.state = 1
        user.save()

        uToken.username = user
        uToken.save()

        uinfo.key = user
        uinfo.save()

        info = models.UnitInfo.objects.get(usercode=usercode)
        info.key = user
        info.save()

        login(request, authenticate(email=uinfo.email, username=username, password=password))

        if back_url:
            return HttpResponseRedirect(back_url)

        return HttpResponseRedirect('/')
