'''
业务逻辑相关API接口

私有接口， 需要授权Token
'''

from rest_framework import routers

from api.view import MethodPrivateViewSet

''' 
name='SectionViewSet-list'
name='SectionViewSet-detail'
'''


class Router(object):

    def __init__(self):
        self.router = routers.DefaultRouter()

    def register_router(self):
        self.router.register('order', MethodPrivateViewSet.OrderViewSet, base_name='order')
        self.router.register('new-contract', MethodPrivateViewSet.CreateContractsViewSet, base_name='new-contract')

    def get_router(self):
        self.register_router()
        return self.router.urls
