from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from account import models
from django.shortcuts import render
from account.util.email_send import send_auth_email
from managestage.utli.datetimenow import datetimenow


def login_mail(func):
    '''
    激活邮件装饰器
    :param func:
    :return:
    '''

    def UserState(request):
        username = request.user.username
        records = models.UserProfix.objects.filter(username=username)
        if not records:
            send_auth_email(request, send_type='register')
            records = models.UserProfix.objects.filter(username=username)
        return records[0].defaule, records[0].username, records[0].email, records[0].addtime

    def access(request, auto=False, *args, **kwargs):
        '''

        :param request:
        :param auto:  是否跳转邮箱激活页面
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            u = models.User.objects.get(username=request.user.username)
            if u.state == '-1':
                if request.user.is_authenticated:
                    statc, u, e, t = UserState(request)
                    datetime = nu(t)
                    if datetime > 60 or datetime < 0:
                        datetime = 0
                    else:
                        datetime = 60 - datetime
                        pass

                    if statc == False:
                        content = {
                            'username': u,
                            'email': e,
                            'content': '请在30分钟内完成激活账号',
                            'sleep': datetime,
                        }
                        return render(request, 'defaule/auth/activationEmail.html', content)  # 没有经过验证的用户，拒绝访问
        except:
            pass
        return func(request, *args, **kwargs)

    return access


def nu(t):
    '''
    计算以过去多少秒
    :param t: 起点时间
    :return: 过去时间秒
    '''

    datetime = str(t).split('.')[0]
    datetime = datetime.split('-')[0] + datetime.split('-')[1] + datetime.split('-')[2].split(' ')[0] + \
               datetime.split(':')[1] + datetime.split(':')[2]

    time = int(str(datetime).split('+')[0])
    print('time1', time)

    datetime = datetimenow()
    datetime = str(datetime).split('.')[0]
    datetime = datetime.split('-')[0] + datetime.split('-')[1] + datetime.split('-')[2].split(' ')[0] + \
               datetime.split(':')[1] + datetime.split(':')[2]
    datetime = int(datetime)

    print('time2', datetime)
    datetime = (int(datetime) - int(time))
    print('time3', datetime)

    return datetime
    pass
