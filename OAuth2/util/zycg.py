import json

import requests
from rauth import OAuth2Service

from django.shortcuts import HttpResponse, HttpResponseRedirect

from OAuth2 import models
from OAuth2.models import UserToken, RegisterState
from lhwill import settings
from lhwill.util import log

ApiUrl = 'https://oauth.zycg.gov.cn'  # oauth

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36',
    'Connection': 'keep-alive'}


class OAuth2(object):

    def __init__(self):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET
        self.authorize_url = '{}{}'.format(ApiUrl, '/oauth/authorize')
        self.access_token_url = '{}{}'.format(ApiUrl, '/oauth/token')
        self.logout_url = '{}{}'.format(ApiUrl, '/logout.do')
        self.userinfo_url = '{}{}'.format('http://ucenter.zycg.gov.cn', '/admin/admin/product/its/getUserInfo')
        self.unitinfo_url = '{}{}'.format('http://ucenter.zycg.gov.cn', '/admin/admin/product/its/getUnitInfo')
        self.access_token = None

        self.redirect_uri = settings.REDIRECT_URI
        self.service = OAuth2Service(
            client_id=self.client_id,
            client_secret=self.client_secret,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url
        )
        pass

    def AuthLogin(self):
        '''
        国采登录
        :return:
        '''
        from managestage.utli.datetimenow import datetime_unix

        state = str(datetime_unix()).split('.')[0]

        models.RegisterState(state=state).save()

        params = {
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'read',
            'state': str(state),
            'type': 'cgr',
        }

        return self.service.get_authorize_url(**params)
        pass

    def AuthLogout(self):
        '''
        国采登出
        :return:
        '''
        return self.logout_url

    def AuthToken(self, code):

        data = {
            'type': 'cgr',
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
        }

        RegisterState.objects.get(code=code)

        html = self.service.get_raw_access_token(data=data)
        log.i(globals(), 'AuthToken_POST', html.text)

        if 'refresh' in html.text:
            html = self.service.get_raw_access_token(data=data)
            log.i(globals(), 'AuthToken_POST', html.text, '刷新页面')
            pass

        jso = json.loads(html.text)

        try:
            self.access_token = jso['access_token']
        except:
            from managestage.utli.datetimenow import datetime_unix
            error = jso['error']
            if error == 'invalid_grant':
                state = str(datetime_unix()).split('.')[0]
                params = {
                    'redirect_uri': self.redirect_uri,
                    'response_type': 'code',
                    'scope': 'read',
                    'state': str(state),
                    'type': 'cgr',
                }
                response = requests.post(url=self.userinfo_url, data=params)
                print(response.text)
                pass

            print(jso)
            print('-------------------------------------------------------------')
            print('KeyError 错误，重新登录')
            return None

        print('GET获取')

        return self.access_token

    def get_UserInfo(self):
        log.i(globals(), 'TOKEN', self.access_token)
        data = {'access_token': self.access_token}
        if self.access_token:
            pass
        response = requests.post(url=self.userinfo_url, data=data)
        log.i(globals(), 'get_UserInfo ---- ', response.text)
        return json.loads(response.text)
        pass

    def get_UnitInfo(self):
        log.i(globals(), 'TOKEN', self.access_token)
        data = {'access_token': self.access_token}
        response = requests.post(url=self.unitinfo_url, data=data)

        log.i(globals(), 'get_UnitInfo ---- ', json.loads(response.text))

        return json.loads(response.text)
        pass

    pass

# Get a real consumer key & secret from https://dev.twitter.com/apps/new

# data = requests.get(url)
