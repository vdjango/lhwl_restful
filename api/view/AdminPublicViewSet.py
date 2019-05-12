'''
admin相关接口，可用于公共读，可开放给用户
本接口若需要修改数据，需要管理员的身份验证 [基于管理的身份验证，基于普通用户的身份验证]

以下操作需要身份验证
[PATCH PUT POST DELETE]

以下操作不需要身份验证
[GET HEAD OPTIONS]
'''
from rest_framework.response import Response

from api.serializers import SerializersAdmin
from api.util.ModelViewUtil import MethodPubilcViewSet
from app import models as AppModels


class StepCategoryViewSet(MethodPubilcViewSet):
    '''
    获取商品分类，梯级分类数据
    基本信息, 商品筛选分类

    > ### 获取商品筛选器分类数据
    > `GET /api/v2/admin/category/?type=sizer&srid=1`
    >
    > Data:
    >
    >     {
    >         "type": "sizer",
    >         "srid": 1
    >     }
    >
    > Return:
    >
    >     [
    >          {
    >               "value": 481,
    >               "label": "品牌",
    >               "children": [
    >                    {
    >                         "value": 185,
    >                         "label": "晨光"
    >                    },
    >                    ...
    >               ]
    >          },
    >          ...
    >     ]

    注意：

    1. type类型为 `sizer` ，获取商品筛选器分类数据，需传入 `srid` 参数
    2. 参数 `srid` 为商品分类二级分类ID[Models app.Classification_There]
    3. 参数 `srid` 为下面json数据路径格式 [{'value: 0', 'label': '', children: [ {value: `ID`} ]}] ，取红色标注ID数值，即当前页面请求json数据

    '''
    queryset = AppModels.Classification.objects.filter()
    serializer_class = SerializersAdmin.Category
    user_key = None

    _serialize = False

    def list(self, request, *args, **kwargs):
        if self.request.GET.get('type', None) == 'sizer':
            if not self.request.GET.get('srid', None):
                return Response({
                    'detail': '缺少 srid 参数！'
                },
                    status=412)
                pass

            text = SerializersAdmin.WareSetupPrefixSerializer(
                AppModels.Classification_There.objects.get(
                    id=self.request.GET.get('srid', None)
                ).waresetupprefix_set.filter(),
                many=True
            ).data

            prefix_brand = {}
            prefix_product_type = {}
            prefix_technology = {}
            prefix_scene = {}
            prefix_pricer_range = {}

            for jsn in text:
                if jsn['filter_id'] == 0:
                    prefix_brand.update(
                        {
                            'value': jsn['id'],
                            'label': jsn['t1'],
                            'children': SerializersAdmin.BrandSerializer(
                                AppModels.Brand.objects.filter(
                                    PrefixKey_id=jsn['id'],
                                    key_id=self.request.GET.get('srid', None)
                                ), many=True
                            ).data
                        }
                    )
                    pass

                if jsn['filter_id'] == 1:
                    prefix_product_type.update(
                        {
                            'value': jsn['id'],
                            'label': jsn['t2'],
                            'children': SerializersAdmin.ProductTypeSerializer(
                                AppModels.ProductType.objects.filter(
                                    PrefixKey_id=jsn['id'],
                                    key_id=self.request.GET.get('srid', None)
                                ), many=True
                            ).data
                        }
                    )
                    pass

                if jsn['filter_id'] == 2:
                    prefix_technology.update(
                        {
                            'value': jsn['id'],
                            'label': jsn['t3'],
                            'children': SerializersAdmin.TechnologySerializer(
                                AppModels.Technology.objects.filter(
                                    PrefixKey_id=jsn['id'],
                                    key_id=self.request.GET.get('srid', None)
                                ), many=True
                            ).data
                        }
                    )
                    pass

                if jsn['filter_id'] == 3:
                    prefix_scene.update(
                        {
                            'value': jsn['id'],
                            'label': jsn['t4'],
                            'children': SerializersAdmin.SceneSerializer(
                                AppModels.Scene.objects.filter(
                                    PrefixKey_id=jsn['id'],
                                    key_id=self.request.GET.get('srid', None)
                                ), many=True
                            ).data
                        }
                    )
                    pass

                if jsn['filter_id'] == 4:
                    prefix_pricer_range.update(
                        {
                            'value': jsn['id'],
                            'label': jsn['t5'],
                            'children': SerializersAdmin.PriceRangeSerializer(
                                AppModels.PriceRange.objects.filter(
                                    PrefixKey_id=jsn['id'],
                                    key_id=self.request.GET.get('srid', None)
                                ), many=True
                            ).data
                        }
                    )
                    pass
                pass

            context = [
                prefix_brand,
                prefix_product_type,
                prefix_technology,
                prefix_scene,
                prefix_pricer_range,
            ]

            return Response(context)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'goods': serializer.data,
            'goods_zycg': SerializersAdmin.RateClassgUidSerializer(
                AppModels.RateClassgUid.objects.filter(),
                many=True
            ).data
        })

    pass


class WareParProfixViewSet(MethodPubilcViewSet):
    '''
    获取商品参数信息，不同分类的商品参数信息不一致

    > #### 获取某个商品的参数信息
    >
    > `GET /api/v2/admin/goods-info/13/?goods-id=227`
    >
    > Data:
    >
    >     {
    >         'goods-id': 227
    >     }
    >
    > Return:
    >
    >     response: {
    >         'id': 13,
    >         'restful': [
    >             {
    >                 'value': 'brands',
    >                 'label': '品牌',
    >                 'data': {
    >                     'name': '理光',
    >                 },
    >             },
    >             ....
    >         ].
    >         ....
    >     }

    1. 参数 `goods-id` 为 app.WareApp 模型ID字段
    2. 在不传入 `goods-id` 字段的情况下，不会出现 `response.restful.data` 数据

    '''
    queryset = AppModels.WareParProfix.objects.filter()
    serializer_class = SerializersAdmin.WareParProfixSerizlizer
    # filter_fields = ['key']

    def get_context(self, serializer):
        context = serializer.data
        restful = context['restful']
        goods_id = self.request.GET.get('goods-id', None)
        if goods_id:
            goods_info = AppModels.WareApp.objects.get(
                id=goods_id
            ).parameter_set.get()
            goods_info_serializer = SerializersAdmin.GoodsInfoSerizlizer(goods_info).data
            for item in restful:
                context['restful'][restful.index(item)].update({
                    'data': {
                        'name': goods_info_serializer[item['value']]
                    }
                })
                pass
            pass
        return context

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(self.get_context(serializer))

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    pass
