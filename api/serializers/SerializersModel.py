from django.contrib.auth.models import Group
from rest_framework import serializers

from account.models import User
from api.serializers.SerializersAdmin import WareParProfixSerizlizer
from home import models as home
from app import models as app
from lhwill import settings
from plate import models as plate
from stock import models as stock_model


class ApiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'version')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'groups', 'usercode', 'update_time', 'state')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name')


# class ClassificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = app.Classification
#         fields = ('id', 'name')


class SubCategory(serializers.ModelSerializer):
    '''
    子分类
    '''

    # waresetupprefix_set = WareSetupPrefixSerializer(many=True, read_only=True)

    class Meta:
        model = app.Classification_There
        exclude = ('time_add', 'time_now')

    pass


class Category(serializers.ModelSerializer):
    '''
    一级分类
    '''

    # classification_there_set = SubCategory(many=True, read_only=True)

    class Meta:
        model = app.Classification
        exclude = ('time_add', 'time_now')

    pass


class BrandSerializer(serializers.ModelSerializer):
    '''A1 商品筛选器'''

    class Meta:
        model = app.Brand
        fields = ('id', 'name')


class ProductTypeSerializer(serializers.ModelSerializer):
    '''A2 商品筛选器'''

    class Meta:
        model = app.ProductType
        fields = ('id', 'name')


class TechnologySerializer(serializers.ModelSerializer):
    '''A3 商品筛选器'''

    class Meta:
        model = app.Technology
        fields = ('id', 'name')


class SceneSerializer(serializers.ModelSerializer):
    '''A4 商品筛选器'''

    class Meta:
        model = app.Scene
        fields = ('id', 'name')


class PriceRangeSerializer(serializers.ModelSerializer):
    '''A5 商品筛选器'''

    class Meta:
        model = app.PriceRange
        fields = ('id', 'name')


class WareSetupPrefixSerializer(serializers.ModelSerializer):
    '''商品搜索筛选器'''
    brand_set = BrandSerializer(many=True, read_only=False)
    producttype_set = ProductTypeSerializer(many=True, read_only=False)
    technology_set = TechnologySerializer(many=True, read_only=False)
    scene_set = SceneSerializer(many=True, read_only=False)
    pricerange_set = PriceRangeSerializer(many=True, read_only=False)

    class Meta:
        model = app.WareSetupPrefix
        fields = '__all__'


class LeaseSerializer(serializers.ModelSerializer):
    '''商品套餐'''

    class Meta:
        model = app.Lease
        fields = ('id', 'name', 'money', 'defaule', 'ware_key', 'time_add')


class ImageSerializer(serializers.ModelSerializer):
    '''商品首图'''

    url = serializers.SerializerMethodField()

    def get_url(self, objects):
        return '{}{}'.format(settings.HTTP_HOST, objects.image.url)

    class Meta:
        model = app.images
        fields = ('id', 'image', 'url', 'defaule', 'key')


class WareAppPrefixSerializer(serializers.ModelSerializer):
    '''商品Prefix '''
    category = serializers.SerializerMethodField()
    subcategory = serializers.SerializerMethodField()

    pricescope = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    technology = serializers.SerializerMethodField()
    usescene = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    def get_context(self, lizers):
        context = {}
        context.update(lizers)
        return context

    def get_category(self, objects):
        return self.get_context(Category(objects.classify_key).data)

    def get_subcategory(self, objects):
        return self.get_context(Category(objects.classifythere_key).data)

    def get_pricescope(self, objects):
        return self.get_context(Category(objects.pricerange_key).data)

    def get_product(self, objects):
        return self.get_context(Category(objects.producttype_key).data)

    def get_technology(self, objects):
        return self.get_context(Category(objects.technology_key).data)

    def get_usescene(self, objects):
        return self.get_context(Category(objects.scene_key).data)

    def get_brand(self, objects):
        return self.get_context(Category(objects.brand_key).data)

    class Meta:
        model = app.WareAppPrefix
        exclude = ['classifys', 'classifytwos', 'classifytheres', 'priceranges', 'producttypes', 'technologys',
                   'scenes', 'brands', 'classifytwo_key']


class WareAppSerializer(serializers.ModelSerializer):
    '''
    商品序列化，提供商品本身及商品参数，商品图片等商品信息
    '''
    images_set = ImageSerializer(many=True, read_only=True)
    lease_set = LeaseSerializer(many=True, read_only=True)
    prefix = serializers.SerializerMethodField(label='商品prefix信息')
    with_info = serializers.SerializerMethodField(label='商品参数信息', help_text='商品参数信息，关于商品的参数有很多。这里定义了需要哪些参数')
    label_info = serializers.SerializerMethodField()

    def get_label_info(self, instance):
        return GoodsLabelInfoSerializer(instance.goodslabelinfo_set.filter(), many=True).data

    def get_with_info(self, instance):
        context = {}
        ins = instance.wareappprefix_set.get().classifythere_key
        with_info_id = instance.parameter_set.get().id
        if not ins:
            return None

        try:
            info = WareParProfixSerizlizer(
                app.WareParProfix.objects.get(key=ins)
            ).data
            goods_info_serializer = GoodsInfoSerizlizer(instance.parameter_set.get()).data

            goods_stock_info = instance.stockinfo_set.filter()

            if not goods_stock_info.exists():
                print('goods_stock_info', goods_stock_info.exists())
                goods_stock_info.create(key=instance)
                pass

            goods_stock_info_serializer = StockInfoSerializer(instance.stockinfo_set.get()).data

            meal = []

            for item in info['restful']:
                meal.append({
                    'value': goods_info_serializer[item['value']],
                    'label': item['label']
                })

                # print(goods_info_serializer[item['value']])
                context.update({
                    item['value']: goods_info_serializer[item['value']]
                })
                pass
            info.update({
                'meal': meal,
                'data': context,
                'with_info_id': with_info_id,
                'stock_info_id': goods_stock_info_serializer
            })
            return info
        except app.WareParProfix.DoesNotExist:
            return None

    def get_prefix(self, objects):
        return WareAppPrefixSerializer(objects.wareappprefix_set.get()).data

    class Meta:
        model = app.WareApp
        fields = '__all__'

    pass

class WareAppWithInfo(serializers.ModelSerializer):
    '''
    商品参数信息序列化字段
    '''
    class Meta:
        model = app.parameter
        fields = '__all__'
    pass

class WareParProfixSerializer(serializers.ModelSerializer):
    class Meta:
        model = app.WareParProfix
        fields = '__all__'


class GoodsInfoSerizlizer(serializers.ModelSerializer):
    '''
    商品参数序列化
    '''
    class Meta:
        model = app.parameter
        fields = '__all__'

class StockInfoSerializer(serializers.ModelSerializer):
    '''
    商品库存信息序列化
    '''
    class Meta:
        model = stock_model.StockInfo
        fields = '__all__'


from search import models as search_model

class GoodsLabelInfoSerializer(serializers.ModelSerializer):
    '''
    商品标签信息 用于辅助搜索引擎搜索商品
    '''
    class Meta:
        model = search_model.GoodsLabelInfo
        fields = '__all__'
    pass

'''plate APP'''


class plateModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = plate.plateModels
        fields = '__all__'


class plateContentSerializer(serializers.ModelSerializer):
    '''页面板块'''

    # content = Classification_ThereSerializer()
    # key = plateModelsSerializer()

    class Meta:
        model = plate.plateContent
        fields = ('id', 'name', 'content', 'key')


class RateDisplaySerializer(serializers.ModelSerializer):
    """央采18类分类"""

    class Meta:
        model = app.RateClassgUid
        fields = '__all__'


class InvoicesSerializer(serializers.ModelSerializer):
    """发票"""

    class Meta:
        model = home.Invoices
        fields = '__all__'

    pass


class AddressSerializer(serializers.ModelSerializer):
    """收货地址"""

    class Meta:
        model = home.Address
        fields = '__all__'


class CarouselSerializer(serializers.ModelSerializer):
    '''首页轮播图片'''

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = app.Carousel
        fields = '__all__'

    def get_image_url(self, model):
        request = self.context.get('request')
        image_url = '/media/carousel/{}'.format(model.image)
        return request.build_absolute_uri(image_url)

    pass


class MiddleTopSerializer(serializers.ModelSerializer):
    '''首页板块'''

    class Meta:
        model = app.MiddleTop
        fields = '__all__'


class CreateContractsSerializer(serializers.ModelSerializer):
    '''
    用户订单合同
    '''

    class Meta:
        model = home.Contracts
        fields = ['id', 'key_order']

    pass


class WheelSerializer(serializers.ModelSerializer):
    '''
    序列化首页轮播图
    '''

    class Meta:
        model = app.WheelModel
        fields = '__all__'
    pass

class SectorSerializer(serializers.ModelSerializer):
    '''
    首页下半部分商品板块展示栏目 序列化
    '''

    class Meta:
        model = app.SectorModel
        fields = ['id', 'name', 'number', 'key']
    pass