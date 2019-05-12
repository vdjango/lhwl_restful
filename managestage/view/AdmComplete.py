'''
后台全局功能实现
'''
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from account.util.decorator import auth_admin
from lhwill.util.complete import MainTain
from managestage import models
from managestage.utli import datetimenow
from managestage.utli.wrapper import _POST, Web_Maintain, _GET

'''站点设置-设置站点属性'''


@_POST
@Web_Maintain
@auth_admin
def set_system(request):
    '''
    站点设置-设置站点属性
    :return:
    '''
    site_name = request.POST.get('site_name')
    site_tags = request.POST.get('site_tags')
    site_url = request.POST.get('site_url')
    site_email = request.POST.get('site_email')
    site_icp = request.POST.get('site_icp')

    site_can_register = request.POST.get('site_can_register')
    site_allow_sending_statistics = request.POST.get('site_allow_sending_statistics')
    if site_can_register:
        site_can_register = True
    else:
        site_can_register = False

    if site_allow_sending_statistics:
        site_allow_sending_statistics = True
    else:
        site_allow_sending_statistics = False

    try:
        system = models.systemSetup.objects.filter()
        if system:
            print('SystemModels', system, site_allow_sending_statistics)
            for i in system:
                i.site_name = site_name
                i.site_tags = site_tags
                i.site_email = site_email
                i.site_icp = site_icp
                i.site_url = site_url
                i.site_can_register = site_can_register
                i.site_allow_sending_statistics = site_allow_sending_statistics
                i.save()
        else:
            print('SystemModelsNo', system)
            models.systemSetup(
                site_name=site_name,
                site_tags=site_tags,
                site_email=site_email,
                site_icp=site_icp,
                site_url=site_url,
                site_can_register=site_can_register,
                site_allow_sending_statistics=site_allow_sending_statistics,
                site_time_now=datetimenow.datetimenow()
            ).save()
    except Exception as e:
        content = {
            'error': '不知道什么错误',
            'state': 'error',
            'code': '403'
        }
        return HttpResponse(json.dumps(content))

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''站点设置-站点维护模式'''


@_POST
@Web_Maintain
@auth_admin
def set_maintain(request):
    '''
    站点设置-站点维护模式
    :return:
    '''
    inta_info = request.POST.get('inta_info')
    inta_datatime = request.POST.get('inia_time')
    inta_allwo = request.POST.get('inta_allwo')
    if inta_allwo:
        inta_allwo = True
    else:
        inta_allwo = False

    # inta_datatime = date_new(str(inta_datatime))

    maintain = models.maintain.objects.filter()
    if maintain:
        print(inta_datatime)
        for i in maintain:
            i.inta_info = inta_info
            if i.inta_allwo == False:
                print('保存时间', inta_datatime)
                i.inta_datatime = inta_datatime
            i.inta_allwo = inta_allwo
            i.save()
    else:
        models.maintain(
            inta_info=inta_info,
            inta_datatime=inta_datatime,
            inta_allwo=inta_allwo,
            inta_time_now=datetimenow.datetimenow()
        ).save()

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''站点SEO设置[VIEW]'''


@_GET
@Web_Maintain
@auth_admin
def seosetup(request):
    '''
    站点SEO设置[VIEW]
    :return:
    '''
    tain = MainTain()
    maintain = tain.get_tain()
    content = {
        'maintain': maintain
    }
    return render(request, 'defaule/admin/complete/seosetup.html', content)


'''全局-设置邮箱SMTP'''


@_POST
@Web_Maintain
@auth_admin
def set_mailsmtp(request):
    '''
    全局-设置邮箱SMTP
    :return:
    '''
    host = request.POST.get('host')
    port = request.POST.get('port')
    user = request.POST.get('user')
    name = request.POST.get('name')
    password = request.POST.get('password')

    try:
        mailstmps = models.systemmail.objects.filter()
        if mailstmps:
            print(host, port, user, name)
            for i in mailstmps:
                i.host = host
                i.port = port
                i.user = user
                i.name = name
                i.passwd = password
                i.save()
        else:
            models.systemmail(
                host=host,
                port=port,
                user=user,
                name=name,
                passwd=password
            ).save()
    except Exception as e:
        content = {
            'error': '',
            'state': 'error',
            'code': '403'
        }
        return HttpResponse(json.dumps(content))

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''全局-邮箱设置-发送测试邮件'''


@_POST
@Web_Maintain
@auth_admin
def send_email(request):
    '''
    全局-邮箱设置-发送测试邮件
    :return:
    '''
    from account.util.email_send import Email
    email = request.POST.get('email')
    try:
        mail = Email()
        mail.__init__()
        mail.send_mail(email_user=email, email_title='这是一封测试邮件',
                       email_body='如果您收到这份邮件，表示邮箱设置没有问题了！'
                       )

    except Exception as e:
        content = {
            'error': '未知错误',
            'state': 'error',
            'code': '403'
        }
        return HttpResponse(json.dumps(content))

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''第三方登陆设置[VIEW]'''


@_GET
@Web_Maintain
@auth_admin
def partysetup(request):
    '''
    第三方登陆设置[VIEW]
    :return:
    '''
    tain = MainTain()
    maintain = tain.get_tain()
    app_qq = models.appid.objects.filter(apptype='qq')
    app_weixin = models.appid.objects.filter(apptype='weixin')

    content = {
        'app_qq': app_qq,
        'app_weixin': app_weixin,
        'maintain': maintain
    }
    return render(request, 'defaule/admin/complete/partysetup.html', content)
    pass


'''第三方登陆设置'''


@_POST
@Web_Maintain
@auth_admin
def set_appid(request):
    '''
    第三方登陆设置
    :return:
    '''
    appstype = request.POST.get('stype')
    appid = request.POST.get('appid')
    appkey = request.POST.get('appkey')

    if appstype == 'qq' or appstype == 'QQ':
        app = models.appid.objects.filter(apptype='qq')
        if app:
            for i in app:
                i.appid = appid
                i.appkey = appkey
                i.save()
            pass
        else:
            models.appid(
                apptype='qq',
                appid=appid,
                appkey=appkey
            ).save()
            pass
    elif appstype == 'weixin' or appstype == 'Weixin':
        app = models.appid.objects.filter(apptype='weixin')
        if app:
            for i in app:
                i.appid = appid
                i.appkey = appkey
                i.save()
            pass
        else:
            models.appid(
                apptype='weixin',
                appid=appid,
                appkey=appkey
            ).save()
            pass
        pass
    else:
        content = {
            'error': '不存在的第三方登陆方式',
            'state': 'error',
            'code': '404'
        }
        return HttpResponse(json.dumps(content))
        pass
    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))


'''首页分类深度设置'''


@_POST
@Web_Maintain
@auth_admin
def setclassify_orthere(request):
    '''
    首页分类深度设置
    :param request:
    :return:
    '''
    redo = request.POST.get('redo')
    try:
        setl = models.Setclassify.objects.filter()[:1].get()
        setl.radio = redo
        setl.save()
    except:
        if models.Setclassify.objects.filter():
            models.Setclassify.objects.filter().delete()

        models.Setclassify(
            radio=redo
        ).save()
    return redirect(reverse('admins:complete'))
    pass
