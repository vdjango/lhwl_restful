from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.permissions import IsAdminOrPublicReadOnlyAndUserInterface


class IsPublicReadUserSet(object):
    '''
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。允许具有管理权限用户修改操作
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAdminOrPublicReadOnlyAndUserInterface,)

    pass


class IsUserSet(object):
    '''
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。

        IsAuthenticated: 需要身份令牌验证
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    pass


class IsAdminSet(object):
    '''
    :param permission_classes: 接口访问权限
        IsAdminOrPublicReadOnlyAndUserInterface:
            公共读，写需要身份令牌验证。对修改操作进行用户验证，允许用户修改自己的数据。

        IsAuthenticated: 需要身份令牌验证
    '''

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAdminUser,)

    pass
