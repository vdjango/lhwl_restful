from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSetMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api import authmixins, mixins
from api import generics
from api.permissions import IsPublicReadUserSet
from api.util.LimitOffsetPagination import Pagination


class GenericViewSets(ViewSetMixin, generics.GenericAPIView):
    """
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    """
    pass


class MethodViewSet(mixins.CreateMethodMixin,
                    mixins.RetrieveMethodMixin,
                    mixins.ListMethodMixin,
                    mixins.UpdateMethodMixin,
                    mixins.DestroyMethodMixin,
                    GenericViewSets):
    pagination_class = Pagination
    pass


class PublicReadUserMethodViewSet(MethodViewSet):
    '''
    The public reading view permission
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    '''
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsPublicReadUserSet,)


class AdminRetrieveCreateUpdateViewSet(mixins.CreateMethodMixin,
                                       mixins.RetrieveMethodMixin,
                                       mixins.UpdateMethodMixin,
                                       GenericViewSets):
    '''
    ViewSet with Admin permissions，
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    '''
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    # permission_classes = (IsAdminUser,)
    pagination_class = Pagination


class AdminMethodViewSet(MethodViewSet):
    '''
    ViewSet with Admin permissions，
    The GenericViewSet class does not provide any actions by default,
    but does include the base set of generic view behavior, such as
    the `get_object` and `get_queryset` methods.
    '''
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)
    permission_classes = (IsAdminUser,)
