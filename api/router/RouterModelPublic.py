'''
Models模型相关API接口

公共接口
'''

from rest_framework import routers

from api.view import ModelPublicVIewSet

''' 
name='SectionViewSet-list'
name='SectionViewSet-detail'
'''


class Router(object):

    def __init__(self):
        self.router = routers.DefaultRouter()

    def register_router(self):
        self.router.register('category', ModelPublicVIewSet.CategoryViewSet, base_name='category')
        self.router.register('sub-category', ModelPublicVIewSet.SubCategoryViewSet, base_name='sub-category')

        self.router.register('selection', ModelPublicVIewSet.ScreeningResultsViewSet, base_name='selection')
        self.router.register('card', ModelPublicVIewSet.plateModelsViewSet, base_name='card')
        self.router.register('card-content', ModelPublicVIewSet.plateContentViewSet, base_name='card-content')
        self.router.register('goods', ModelPublicVIewSet.WareAppViewSet, base_name='goods')
        self.router.register('goods-prefix-info', ModelPublicVIewSet.WareAppPrefixViewSet, base_name='goods-prefix-info')
        self.router.register('goods-with-info', ModelPublicVIewSet.WareAppWithInfoViewSet, base_name='goods-with-info')
        self.router.register('goods-meal-info', ModelPublicVIewSet.LeaseViewSet, base_name='goods-meal-info')
        self.router.register('goods-image', ModelPublicVIewSet.ImageViewSet, base_name='goods-image')
        self.router.register('goods-stock-info', ModelPublicVIewSet.StockInfoViewSet, base_name='goods-stock-info')
        self.router.register('goods-label-info', ModelPublicVIewSet.GoodsLabelInfoView, base_name='goods-label-info')
        self.router.register('sowing-map', ModelPublicVIewSet.CarouselViewSet, base_name='sowing-map'),
        self.router.register('wheel', ModelPublicVIewSet.WhellViewSet, base_name='wheel')
        self.router.register('sector', ModelPublicVIewSet.SectorViewSet, base_name='sector')

        pass

    def get_router(self):
        self.register_router()
        return self.router.urls
