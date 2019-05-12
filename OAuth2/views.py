# Create your views here.
from django.contrib.auth import login
from django.shortcuts import HttpResponse, HttpResponseRedirect, reverse, redirect
from django.views.generic import TemplateView

from OAuth2 import models
from OAuth2.models import UserToken
from OAuth2.util.zycg import OAuth2
from account.models import User, UserInfo, UnitInfo
from home.models import Address
from lhwill.util.log import log
from lhwill.view.HttpCodeError import HttpResponseError
from managestage.utli.datetimenow import datetimenow, datetime_unix

logger = log(globals())


class CallbackViewSet(TemplateView):
    '''
    央采回调地址
    : 验证央采用户登录，防止跨域等
    '''

    def render_to_response(self, context, **response_kwargs):
        '''
        验证view_response
        :param context:
        :param response_kwargs:
        :return:
        '''
        try:
            if not self.request.GET.get('code') or not self.request.GET.get('state'):
                return HttpResponseError(self.request).HttpResponse_or_403()

            RegisterState = models.RegisterState.objects.get(state=self.request.GET.get('state'))
        except models.RegisterState.DoesNotExist:
            return HttpResponseError(self.request).HttpResponse_or_403()
            pass

        from managestage.utli.datetimenow import datetime_unix

        RegisterState.state_code = str(datetime_unix()).split('.')[0]
        RegisterState.code = self.request.GET.get('code')
        RegisterState.save()

        return redirect(reverse('auth:oauth2:TokenViewSet', args=[RegisterState.state_code]))

    pass


class TokenViewSet(TemplateView):
    template_name = 'defaule/auth/setpass.html'

    register_auth = False

    OA = OAuth2()

    def get_context_data(self, **kwargs):
        logger.i('state_code', self.kwargs['state_code'])
        kwargs.update({
            'state_code': self.kwargs['state_code']
        })
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        '''
        验证回调code准确性
        :param context:
        :param response_kwargs:
        :return:
        '''

        try:
            state_code = models.RegisterState.objects.get(state_code=self.kwargs['state_code'])

            if self.AuthVerifyToLogin(state_code):
                state_code.delete()
                if self.request.GET.get('next'):
                    return HttpResponseRedirect(self.request.GET.get('next'))

                return redirect(reverse('app:index'))
        except models.RegisterState.DoesNotExist:

            return HttpResponseError(self.request).HttpResponse_or_403()

        return super(TokenViewSet, self).render_to_response(context, **response_kwargs)
 
    def AuthVerifyToLogin(self, objectModels):
        OA = OAuth2()
        token = OA.AuthToken(objectModels.code)
        userInfo = OA.get_UserInfo()
        uitInfo = OA.get_UnitInfo()

        if userInfo['success']:
            try:
                username = models.User.objects.get(usercode=userInfo['rows']['usercode'])
                self.register_auth = False
            except User.DoesNotExist:
                self.register_auth = True
                password = '{}{}'.format(datetime_unix(), range(20000, 90000))
                username = models.User.objects.create_user(
                    username=userInfo['rows']['usercode'],
                    email=userInfo['rows']['email'],
                    usercode=userInfo['rows']['usercode'],
                    state=1,
                    password=password
                )
                logger.i('create_user', username)
                UserInfo(
                    usercode=userInfo['rows']['usercode'],
                    email=userInfo['rows']['email'],
                    name=userInfo['rows']['name'],
                    qq=userInfo['rows']['qq'],
                    sex=userInfo['rows']['sex'],
                    phone=userInfo['rows']['phone'],
                    birthday=userInfo['rows']['birthday'],
                    fax=userInfo['rows']['fax'],
                    job=userInfo['rows']['job'],
                    userlevel=userInfo['rows']['userlevel'],
                    key=username
                ).save()

                UnitInfo(
                    usercode=userInfo['rows']['usercode'],
                    name=uitInfo['rows']['name'],
                    shortname=uitInfo['rows']['shortname'],
                    orgcode=uitInfo['rows']['orgcode'],
                    detailaddress=uitInfo['rows']['detailaddress'],
                    postalcode=uitInfo['rows']['postalcode'],
                    website=uitInfo['rows']['website'],
                    telephone=uitInfo['rows']['telephone'],
                    fax=uitInfo['rows']['fax'],
                    description=uitInfo['rows']['description'],
                    istopunit=uitInfo['rows']['istopunit'],
                    province=uitInfo['rows']['province'],
                    city=uitInfo['rows']['city'],
                    remark=uitInfo['rows']['remark'],
                    topunitname=uitInfo['rows']['topunitname'],
                    topunitcode=uitInfo['rows']['topunitcode'],
                    unitcode=uitInfo['rows']['unitcode'],
                    hyxt1=uitInfo['rows']['hyxt1'],
                    hyxt2=uitInfo['rows']['hyxt2'],
                    key=username
                ).save()

                Address(
                    defaule=True,
                    consigneeName=userInfo['rows']['name'],
                    province=uitInfo['rows']['province'],
                    city=uitInfo['rows']['city'],
                    consigneeAddress=uitInfo['rows']['detailaddress'],
                    consigneeMobile=userInfo['rows']['phone'],
                    email=userInfo['rows']['email'],
                    key=username
                ).save()

                pass

            try:
                UserToken.objects.get(usercode=userInfo['rows']['usercode'])
            except UserToken.DoesNotExist:
                UserToken(
                    usercode=userInfo['rows']['usercode'],
                    username=username,
                    token=token
                ).save()

            self.set_logig(username)

            return True

        return False

        pass

    def set_logig(self, username):
        login(self.request, username, backend='django.contrib.auth.backends.ModelBackend')


def zycg(request):
    OAuth = OAuth2()
    url = OAuth.AuthLogin()
    return HttpResponseRedirect(url)
    pass
