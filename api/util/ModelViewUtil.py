# 实现接口ModelViewSet方法
# 添加分页， 统一返回数据格式
from collections import OrderedDict

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.util.LimitOffsetPagination import Pagination

try:
    from hmac import compare_digest
except ImportError:
    def compare_digest(a, b):
        return a == b

from rest_framework import viewsets, pagination, views

from api.permissions import IsAdminOrPublicReadOnlyAndUserInterface, IsPrivateWriteUserInterface
from lhwill.util.log import log

logger = log(globals())

from django.middleware.csrf import get_token


def getToken(request):
    token = get_token(request)
    return token


class LimitOffsetPagination(pagination.LimitOffsetPagination):
    """
    自定义分页方法
    """
    page_size_query_param = "page_size"
    page_query_param = 'page'
    page_size = 60
    default_limit = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    pass


class ModelViewSet(viewsets.ModelViewSet):
    '''
    :param user_key: 模型用户外键key值
    :param permission_pubilc_write: 接口公共写入状态[True/False]
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。

        IsAuthenticated: 需要身份令牌验证
    :param pagination_class: 接口分页
    :param code: 接口内部返回值[未实现]
    '''
    user_key = 'key'
    permission_pubilc_write = False

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)

    permission_classes = (IsAdminOrPublicReadOnlyAndUserInterface, IsAuthenticated,)

    pagination_class = Pagination
    code = 200

    '''
    @ensure_csrf_cookie Django官方解释 对于完全的前后分离，是拿不到csrf的。 通过这种方式将csrf设置cookie里面
    '''

    # @ensure_csrf_cookie
    def dispatch(self, request, *args, **kwargs):
        if self.permission_pubilc_write:
            self.permission_classes = (IsAdminOrPublicReadOnlyAndUserInterface,)
        else:
            self.permission_classes = (IsAuthenticated,)
            pass

        print(getToken(request))

        return super(ModelViewSet, self).dispatch(request, *args, **kwargs)


class MethodPubilcViewSet(viewsets.ModelViewSet):
    '''
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。

        IsAuthenticated: 需要身份令牌验证
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAdminOrPublicReadOnlyAndUserInterface, IsAuthenticated,)

    def dispatch(self, request, *args, **kwargs):
        return super(MethodPubilcViewSet, self).dispatch(request, *args, **kwargs)


class MethodPrivateViewSet(viewsets.ModelViewSet):
    '''
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。

        IsAuthenticated: 需要身份令牌验证
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)


    def dispatch(self, request, *args, **kwargs):
        return super(MethodPrivateViewSet, self).dispatch(request, *args, **kwargs)







class ModelPrivateWriteViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsPrivateWriteUserInterface,)

    pass


