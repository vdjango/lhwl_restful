'''
数据模型相关API接口

废弃淘汰
'''

from rest_framework import routers

from api.view import ModelPrivateVIewSet, ModelPublicVIewSet


class RouterModel(object):

    def __init__(self):
        self.router = routers.DefaultRouter()
        pass

    def register_router(self):
        self.router.register('UserViewSet', ModelPrivateVIewSet.UserViewSet, base_name='UserViewSet')
        self.router.register('RateDisplayViewSet', ModelPrivateVIewSet.RateDisplayViewSet,
                             base_name='RateDisplayViewSet')
        self.router.register('InvoicesViewSet', ModelPrivateVIewSet.InvoicesViewSet, base_name='InvoicesViewSet')
        self.router.register('AddressViewSet', ModelPrivateVIewSet.AddressViewSet, base_name='AddressViewSet')

        self.router.register('classification', ModelPublicVIewSet.ClassificationViewSet, base_name='classification')
        self.router.register('subclassification', ModelPublicVIewSet.Classification_ThereViewSet,
                             base_name='subclassification')
        self.router.register('goodsPrefix', ModelPublicVIewSet.WareAppPrefixViewSet, base_name='goodsPrefix')
        self.router.register('ScreeningResultsViewSet', ModelPublicVIewSet.ScreeningResultsViewSet,
                             base_name='ScreeningResultsViewSet')
        self.router.register('plateModelsViewSet', ModelPublicVIewSet.plateModelsViewSet,
                             base_name='plateModelsViewSet')
        self.router.register('plateContentViewSet', ModelPublicVIewSet.plateContentViewSet,
                             base_name='plateContentViewSet')
        self.router.register('WareAppViewSet', ModelPublicVIewSet.WareAppViewSet, base_name='WareAppViewSet')
        self.router.register('LeaseViewSet', ModelPublicVIewSet.LeaseViewSet, base_name='LeaseViewSet')
        self.router.register('ImageViewSet', ModelPublicVIewSet.ImageViewSet, base_name='ImageViewSet')

        self.router.register('CarouselViewSet', ModelPublicVIewSet.CarouselViewSet, base_name='CarouselViewSet')

    def get_router(self):
        self.register_router()
        return self.router.urls
