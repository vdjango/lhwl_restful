from app import models
from haystack import indexes


# 指定对于某个类的某些数据建立索引
from lhwill import settings


class WareAppPrefixInfoIndex(indexes.ModelSearchIndex, indexes.Indexable):
    id = indexes.IntegerField(model_attr='wareApp_key__id')
    name = indexes.CharField(model_attr='wareApp_key__name')
    money = indexes.DecimalField(model_attr='wareApp_key__money')
    image_400x400 = indexes.CharField(model_attr='wareApp_key__image_400x400')
    unix = indexes.CharField(model_attr='wareApp_key__unix')
    stock = indexes.BooleanField(model_attr='wareApp_key__stock')
    release = indexes.BooleanField(model_attr='wareApp_key__release')
    category = indexes.CharField(model_attr='classify_key__name')
    subcategory = indexes.CharField(model_attr='classifythere_key__name')

    brand = indexes.CharField(model_attr='brand_key__PrefixKey__filter_id')
    scene = indexes.CharField(model_attr='scene_key__PrefixKey__filter_id')
    technology = indexes.CharField(model_attr='technology_key__PrefixKey__filter_id')
    producttype = indexes.CharField(model_attr='producttype_key__PrefixKey__filter_id')
    pricerange = indexes.CharField(model_attr='pricerange_key__PrefixKey__filter_id')

    '''
    分离筛选器参数
    '''
    def get_sid_prefix(self, obj, sid):
        name = ''
        if obj.brand_key and int(obj.brand_key.PrefixKey.filter_id) == sid:
            name = '{}.{}'.format(
                obj.brand_key.PrefixKey.t1,
                obj.brand_key.name
            )
            pass
        if obj.producttype_key and int(obj.producttype_key.PrefixKey.filter_id) == sid:
            name = '{}.{}'.format(
                obj.producttype_key.PrefixKey.t2,
                obj.producttype_key.name
            )
            pass
        if obj.technology_key and int(obj.technology_key.PrefixKey.filter_id) == sid:
            name = '{}.{}'.format(
                obj.technology_key.PrefixKey.t3,
                obj.technology_key.name
            )
            pass
        if obj.scene_key and int(obj.scene_key.PrefixKey.filter_id) == sid:
            name = '{}.{}'.format(
                obj.scene_key.PrefixKey.t4,
                obj.scene_key.name
            )
            pass
        if obj.pricerange_key and int(obj.pricerange_key.PrefixKey.filter_id) == sid:
            name = '{}.{}'.format(
                obj.pricerange_key.PrefixKey.t5,
                obj.pricerange_key.name
            )
            pass
        return name

    def prepare_image_400x400(self, obj):
        return '{}{}{}'.format(settings.HTTP_HOST, settings.MEDIA, obj.wareApp_key.image_400x400)

    def prepare_brand(self, obj):
        return self.get_sid_prefix(obj, 0)

    def prepare_producttype(self, obj):
        return self.get_sid_prefix(obj, 1)

    def prepare_technology(self, obj):
        return self.get_sid_prefix(obj, 2)

    def prepare_scene(self, obj):
        return self.get_sid_prefix(obj, 3)

    def prepare_pricerange(self, obj):
        return self.get_sid_prefix(obj, 4)

    class Meta:
        model = models.WareAppPrefix

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(wareApp_key__release=True)
