'''
业务逻辑相关API接口

废弃淘汰
'''

from rest_framework import routers

from api.view import MethodPublicViewSet, ModelPublicVIewSet, MethodPrivateViewSet

'''
[<URLPattern <URLPattern '^CategoryViewSet/$' [name='CategoryViewSet-list']>, <URLPattern '^CategoryViewSet\.(?P<format>[a-z0-9]+)/?$' [name='CategoryViewSet-list']>, <URLPattern '^CategoryViewSet/(?P<pk>[^/.]+)/$' [name='CategoryViewSet-detail']>, <URLPattern '^CategoryViewSet/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='CategoryViewSet-detail']>, <URLPattern '^PlateViewSet/$' [name='PlateViewSet-list']>, <URLPattern '^PlateViewSet\.(?P<format>[a-z0-9]+)/?$' [name='PlateViewSet-list']>, <URLPattern '^PlateViewSet/(?P<pk>[^/.]+)/$' [name='PlateViewSet-detail']>, <URLPattern '^PlateViewSet/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='PlateViewSet-detail']>, <URLPattern '^CommodityDetails/$' [name='CommodityDetailsViewSet-list']>, <URLPattern '^CommodityDetails\.(?P<format>[a-z0-9]+)/?$' [name='CommodityDetailsViewSet-list']>, <URLPattern '^CommodityDetails/(?P<pk>[^/.]+)/$' [name='CommodityDetailsViewSet-detail']>, <URLPattern '^CommodityDetails/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='CommodityDetailsViewSet-detail']>, <URLPattern '^OrderViewSet/$' [name='OrderViewSet-list']>, <URLPattern '^OrderViewSet\.(?P<format>[a-z0-9]+)/?$' [name='OrderViewSet-list']>, <URLPattern '^OrderViewSet/(?P<pk>[^/.]+)/$' [name='OrderViewSet-detail']>, <URLPattern '^OrderViewSet/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='OrderViewSet-detail']>, <URLPattern '^$' [name='api-root']>, <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>]
name='SectionViewSet-list'
name='SectionViewSet-detail'
'''


class RouterModel(object):

    def __init__(self):
        self.router = routers.DefaultRouter()

    def register_router(self):

        self.router.register('SectionViewSet', ModelPublicVIewSet.SectionViewSet, base_name='SectionViewSet')
        self.router.register('CategoryViewSet', ModelPublicVIewSet.CategoryViewSet, base_name='CategoryViewSet')
        self.router.register('PlateViewSet', ModelPublicVIewSet.PlateViewSet, base_name='PlateViewSet')
        self.router.register('CommodityDetails', ModelPublicVIewSet.CommodityDetailsViewSet, base_name='CommodityDetailsViewSet')
        self.router.register('OrderViewSet', MethodPrivateViewSet.OrderViewSet, base_name='OrderViewSet')
        self.router.register('CreateContractsViewSet', MethodPrivateViewSet.CreateContractsViewSet,
                             base_name='CreateContractsViewSet')

    def get_router(self):
        self.register_router()
        return self.router.urls
