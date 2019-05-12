'''
业务逻辑相关API接口

公共接口
'''

from rest_framework import routers

from api.view import MethodPublicViewSet, ModelPrivateVIewSet
from api.view import MethodPublicViewSet

''' 
name='SectionViewSet-list'
name='SectionViewSet-detail'
'''


class Router(object):

    def __init__(self):
        self.router = routers.DefaultRouter()

    def register_router(self):
        self.router.register('index', MethodPublicViewSet.IndexViewSet, base_name='index')
        self.router.register('sector', MethodPublicViewSet.IndexSectorViewSet, base_name='sector')
        self.router.register('wheel', MethodPublicViewSet.IndexWheelViewSet, base_name='wheel')
        self.router.register('searching-list', MethodPublicViewSet.IndexSearchingList, base_name='searching-list')
        self.router.register('search', MethodPublicViewSet.SearchViewSet, base_name='search')
        pass

    def get_router(self):
        self.register_router()
        return self.router.urls
