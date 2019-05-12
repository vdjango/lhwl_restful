'''
Models模型相关API接口

私有接口，需要授权Token
'''

from rest_framework import routers

from api.view import MethodPublicViewSet, ModelPrivateVIewSet

''' 
name='SectionViewSet-list'
name='SectionViewSet-detail'
'''


class Router(object):

    def __init__(self):
        self.router = routers.DefaultRouter()

    def register_router(self):
        self.router.register('user', ModelPrivateVIewSet.UserViewSet, base_name='user')
        self.router.register('central-category', ModelPrivateVIewSet.RateDisplayViewSet, base_name='central-category')
        self.router.register('bill', ModelPrivateVIewSet.InvoicesViewSet, base_name='bill')
        self.router.register('place', ModelPrivateVIewSet.AddressViewSet, base_name='place')
        pass

    def get_router(self):
        self.register_router()
        return self.router.urls
