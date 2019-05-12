'''
业务逻辑相关API接口

私有接口， 需要授权Token
'''

from rest_framework import routers

from api.view import AdminPrivateViewSet, AdminPublicViewSet

''' 
name='SectionViewSet-list'
name='SectionViewSet-detail'
'''


class Router(object):

    def __init__(self):
        self.router = routers.DefaultRouter()

    def register_router(self):
        self.router.register('importgoods', AdminPrivateViewSet.ImportGoodsViewSet,
                             base_name='importgoods')
        self.router.register('importgoodsset', AdminPrivateViewSet.ImportWareAppViewSet,
                             base_name='importgoodsset')
        self.router.register('category', AdminPublicViewSet.StepCategoryViewSet,
                             base_name='category')



        self.router.register('goods-info', AdminPublicViewSet.WareParProfixViewSet,
                             base_name='goods-info')


    def get_router(self):
        self.register_router()
        return self.router.urls
