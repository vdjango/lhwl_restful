'''
Models模型相关接口
公共访问权限
'''
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from api.serializers import SerializersModel, SerializersMethodl
from api.util.ModelViewUtil import ModelViewSet
from app import models as AppModels
from lhwill import settings
from plate import models as PlateModels
from lhwill.util.log import log
from stock import models as stock_model

logger = log(globals())


class ModelPublicViewSet(ModelViewSet):
    permission_pubilc_write = True


class ImageViewSet(ModelPublicViewSet):
    '''商品首图,记录商品首图及商品默认展示图[默认展示图需要关联WareApp.image字段]'''
    queryset = AppModels.images.objects.filter()
    serializer_class = SerializersModel.ImageSerializer
    user_key = None
    filter_fields = ('key',)

    def create(self, request, *args, **kwargs):
        return super(ImageViewSet, self).create(request, *args, **kwargs)


class ClassificationViewSet(ModelPublicViewSet):
    """
    V1 即将废弃
    全部分类API，首页的全部分类
    """

    queryset = AppModels.Classification.objects.filter().order_by('time_add')
    serializer_class = SerializersModel.Category

    user_key = None


class Classification_ThereViewSet(ModelPublicViewSet):
    """
    V1 即将废弃
    子分类API，首页的全部分类的子分类，统计了所有商品分类信息
    """

    queryset = AppModels.Classification_There.objects.filter().order_by('-time_add')
    serializer_class = SerializersModel.SubCategory
    user_key = None

    def get_queryset(self):
        id = self.request.GET.get('id')
        logger.i('额外操作 ', id)
        if id:
            return self.queryset.filter(Classifykey_id=id)
        return self.queryset


class plateModelsViewSet(ModelPublicViewSet):
    """
    导航页面API，一级导航和二级导航 类似于 文章等
    """
    queryset = PlateModels.plateModels.objects.filter().order_by('time_add')
    serializer_class = SerializersModel.plateModelsSerializer
    user_key = None


class plateContentViewSet(ModelPublicViewSet):
    """
    导航页面的板块API，导航页面的板块信息
    """
    queryset = PlateModels.plateContent.objects.filter().order_by('time_add')
    serializer_class = SerializersModel.plateContentSerializer
    user_key = None


class LeaseViewSet(ModelPublicViewSet):
    """
    商品套餐API，商品套餐信息
    """
    queryset = AppModels.Lease.objects.filter()
    serializer_class = SerializersModel.LeaseSerializer
    user_key = None
    filter_fields = ('name', 'money', 'defaule', 'ware_key')

    def perform_update(self, serializer):
        from app.models import Lease

        if self.request.data['defaule'] == 'true':
            logger.i('设置套餐默认为', self.request.data['defaule'])
            Lease.objects.filter(ware_key=self.request.data['ware_key']).update(defaule=False)
        super(LeaseViewSet, self).perform_update(serializer)


class WareAppPrefixViewSet(ModelPublicViewSet):
    '''
    # 商品Prefix API，
    ### 记录商品所有关键信息。
    ### 如： 商品分类，商品筛选器，以及商品本身信息

    '''
    queryset = AppModels.WareAppPrefix.objects.filter()
    serializer_class = SerializersModel.WareAppPrefixSerializer
    filter_fields = (
        'classify_key', 'classifythere_key', 'pricerange_key', 'producttype_key', 'technology_key', 'scene_key',
        'brand_key', 'wareApp_key', 'rate_classg_key',)
    user_key = None
    pass


class CarouselViewSet(ModelPublicViewSet):
    '''轮播图'''
    queryset = AppModels.Carousel.objects.filter()
    serializer_class = SerializersModel.CarouselSerializer


class SectionViewSet(ModelPublicViewSet):
    '''首页板块数据'''
    queryset = AppModels.MiddleTop.objects.filter()
    serializer_class = SerializersModel.MiddleTopSerializer

    def Section_queryset(self, data=None):
        '''根据以分页的数据去对比查询相关数据'''
        models_ware = []
        url = settings.HTTP_HOST
        for i in data:
            plate = []
            for w in AppModels.commodity.objects.filter(key_id=i['id']):
                plate.append({
                    'id': w.ware_key.id,
                    'name': w.ware_key.name,
                    'image': {
                        'image': '{}{}'.format(url, w.ware_key.get_image_url()),
                        'image_64x64': '{}{}'.format(url, w.ware_key.get_image_url_64x64()),
                        'image_125x125': '{}{}'.format(url, w.ware_key.get_image_url_125x125()),
                        'image_200x200': '{}{}'.format(url, w.ware_key.get_image_url_200x200()),
                        'image_400x400': '{}{}'.format(url, w.ware_key.get_image_url_400x400()),
                        'image_800x800': '{}{}'.format(url, w.ware_key.get_image_url_800x800()),
                    },
                    'money': w.ware_key.money
                })
                pass
            models_ware.append({
                'id': i['id'],
                'name': i['name'],
                'plate': plate
            })

        return models_ware
        pass

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.Section_queryset(serializer.data)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = self.Section_queryset(serializer.data)
        return Response(data=data)

    pass


class PlateViewSet(ModelPublicViewSet):
    '''首页子导航接口，获取导航相关数据，改变数据相关展示方法'''
    queryset = PlateModels.plateModels.objects.filter()
    serializer_class = SerializersModel.plateModelsSerializer

    def Section_queryset(self, data=None):
        '''根据以分页的数据去对比查询相关数据'''

        models_ware = []
        url = settings.HTTP_HOST

        for i in data:
            plates = []
            for w in PlateModels.plateContent.objects.filter(key_id=i['id']):
                ware = w.content.wareappprefix_set.filter(wareApp_key__release=True)[:10]
                ware_list = []
                for app in ware:
                    image = {
                        'image': '{}{}'.format(url, app.wareApp_key.get_image_url()),
                        'image_64x64': '{}{}'.format(url, app.wareApp_key.get_image_url_64x64()),
                        'image_125x125': '{}{}'.format(url, app.wareApp_key.get_image_url_125x125()),
                        'image_200x200': '{}{}'.format(url, app.wareApp_key.get_image_url_200x200()),
                        'image_400x400': '{}{}'.format(url, app.wareApp_key.get_image_url_400x400()),
                        'image_800x800': '{}{}'.format(url, app.wareApp_key.get_image_url_800x800()),
                    }
                    ware_list.append({
                        'id': app.wareApp_key.id,
                        'name': app.wareApp_key.name,
                        'slug': app.wareApp_key.slug,
                        'money': app.wareApp_key.money,
                        'connet': app.wareApp_key.connet,
                        'describe': app.wareApp_key.describe,
                        'image': image
                    })

                plates.append({
                    'id': w.id,
                    'name': w.name,
                    'number': w.number,
                    'time_add': w.time_add,
                    'time_now': w.time_now,
                    'ware': ware_list
                })
            models_ware.append({
                'id': i['id'],
                'name': i['name'],
                'slug': i['slug'],
                'time_add': i['time_add'],
                'time_now': i['time_now'],
                'plate': plates
            })

        return models_ware
        pass

    def retrieve(self, request, *args, **kwargs):
        logger.i('aaa')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = self.Section_queryset([serializer.data])
        return Response(data=data[0])

    pass


class CommodityDetailsViewSet(ModelPublicViewSet):
    '''
    返回商品相关信息

    包含: [商品套餐，商品图片List，商品配置相关, 商品参数]
    '''
    queryset = AppModels.WareApp.objects.filter(release=True)
    serializer_class = SerializersMethodl.WareApp


class WareAppImageListViewSet(ModelPublicViewSet):
    '''
    获取某个商品的全部首图

    常用于 商品详情的商品大图[主图]展示

    GET: retrieve

    '''
    queryset = AppModels.WareApp.objects.filter(release=True)
    serializer_class = SerializersModel.WareAppSerializer

    def Section_queryset(self, data=None):
        '''根据以分页的数据去对比查询相关数据'''

        models_ware = {}
        url = settings.HTTP_HOST

        image = SerializersModel.ImageSerializer()

        return models_ware
        pass

    def retrieve(self, request, *args, **kwargs):
        logger.i('aaa')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = self.Section_queryset(serializer.data)
        return Response(data=data[0])

    pass


'''
New V2 接口
'''


class CategoryViewSet(ModelPublicViewSet):
    '''
    获取首页分类
    详细到子分类
    '''
    queryset = AppModels.Classification.objects.filter()
    serializer_class = SerializersModel.Category
    filter_fields = ('name',)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data)


class SubCategoryViewSet(ModelPublicViewSet):
    '''
    获取首页子分类
    '''
    queryset = AppModels.Classification_There.objects.filter()
    serializer_class = SerializersModel.SubCategory
    filter_fields = ('name', 'Classifykey',)
    pass


class WareAppViewSet(ModelPublicViewSet):
    '''
    商品信息，用于记录商品信息

    release 为 Flase 的时候 数据查询不到
    '''
    queryset = AppModels.WareApp.objects.filter()
    serializer_class = SerializersModel.WareAppSerializer
    filter_fields = ('name', 'money', 'release', 'release_version', 'time_add')
    user_key = None


class ScreeningResultsViewSet(ModelPublicViewSet):
    '''
    商品筛选器 GET: 传入`filter-id`参数

    > 通过Classification_There.id 获取app.models.WareSetupPrefix 汇集WareSetupPrefix结果，生成Data数据

    `
    WareSetupPrefix.objects.filter(key_id=filter-id)
    `
    '''

    queryset = AppModels.WareSetupPrefix.objects.filter()
    serializer_class = SerializersModel.WareSetupPrefixSerializer
    filter_fields = ('t1', 't2', 't3', 't4', 't5', 'filter_id', 'key')
    user_key = None

    _serialize = False

    def get_queryset(self):
        _fid = self.request.GET.get('filter-id')
        if _fid:
            self._serialize = True
            waresetup = self.queryset.filter(key_id=_fid)

            print('waresetup.filter(filter_id=)', waresetup.filter(filter_id='0'))

            BrandKey = waresetup.filter(filter_id='0')[0]
            ProductTypeKey = waresetup.filter(filter_id='1')[0]
            TechnologyKey = waresetup.filter(filter_id='2')[0]
            SceneKey = waresetup.filter(filter_id='3')[0]
            PriceRangeKey = waresetup.filter(filter_id='4')[0]

            T1 = AppModels.Brand.objects.filter(PrefixKey=BrandKey)
            T2 = AppModels.ProductType.objects.filter(PrefixKey=ProductTypeKey)
            T3 = AppModels.Technology.objects.filter(PrefixKey=TechnologyKey)
            T4 = AppModels.Scene.objects.filter(PrefixKey=SceneKey)
            T5 = AppModels.PriceRange.objects.filter(PrefixKey=PriceRangeKey)

            contend = []

            data = []
            for i in T1:
                data.append({
                    'id': i.id,
                    'name': i.name
                })
                pass
            contend.append({
                'id': BrandKey.id,
                'name': BrandKey.t1,
                'filter_id': BrandKey.filter_id,
                'data': data
            })

            data = []
            for i in T2:
                data.append({
                    'id': i.id,
                    'name': i.name
                })
                pass
            contend.append({
                'id': ProductTypeKey.id,
                'name': ProductTypeKey.t2,
                'filter_id': ProductTypeKey.filter_id,
                'data': data
            })

            data = []
            for i in T3:
                data.append({
                    'id': i.id,
                    'name': i.name
                })
                pass
            contend.append({
                'id': TechnologyKey.id,
                'name': TechnologyKey.t3,
                'filter_id': TechnologyKey.filter_id,
                'data': data
            })

            data = []
            for i in T4:
                data.append({
                    'id': i.id,
                    'name': i.name
                })
                pass
            contend.append({
                'id': SceneKey.id,
                'name': SceneKey.t4,
                'filter_id': SceneKey.filter_id,
                'data': data
            })

            data = []
            for i in T5:
                data.append({
                    'id': i.id,
                    'name': i.name
                })
                pass
            contend.append({
                'id': PriceRangeKey.id,
                'name': PriceRangeKey.t5,
                'filter_id': PriceRangeKey.filter_id,
                'data': data
            })

            return contend
        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if self._serialize:
            return Response(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class WareAppWithInfoViewSet(ModelPublicViewSet):
    '''
    商品参数信息，例如： 商品的品牌，商品的型号等
    '''
    queryset = AppModels.parameter.objects.filter()
    serializer_class = SerializersModel.WareAppWithInfo
    pass


class StockInfoViewSet(ModelPublicViewSet):
    '''
    商品库存信息
    '''
    queryset = stock_model.StockInfo.objects.filter()
    serializer_class = SerializersModel.StockInfoSerializer
    pass


from search import models as search_model


class GoodsLabelInfoView(ModelPublicViewSet):
    '''
    商品标签信息 用于辅助搜索引擎搜索商品
    为商品打标签
    '''
    queryset = search_model.GoodsLabelInfo.objects.filter()
    serializer_class = SerializersModel.GoodsLabelInfoSerializer
    pass


class WhellViewSet(ModelPublicViewSet):
    '''
    首页轮播图
    '''
    queryset = AppModels.WheelModel.objects.filter()
    serializer_class = SerializersModel.WheelSerializer


class SectorViewSet(ModelPublicViewSet):
    '''
    首页板块栏目， 展示商品等信息
    '''
    queryset = AppModels.SectorModel.objects.filter()
    serializer_class = SerializersModel.SectorSerializer


