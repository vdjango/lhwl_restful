from rest_framework import serializers
from app import models as AppModels
from managestage import models as managestage


class ImportGoodsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = managestage.ImportFile
        fields = '__all__'

    pass


class ImportGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = managestage.ImportGoods
        fields = '__all__'

    pass


class SubCategory(serializers.ModelSerializer):
    '''
    二级分类
    '''
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, objects):
        return objects.id

    def get_label(self, objects):
        return objects.name

    class Meta:
        model = AppModels.Classification_There
        fields = ('value', 'label',)

    pass


class Category(serializers.ModelSerializer):
    '''
    一级分类
    '''
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_value(self, objects):
        return objects.id

    def get_label(self, objects):
        return objects.name

    def get_children(self, objects):
        return SubCategory(objects.classification_there_set.filter(), many=True).data

    class Meta:
        model = AppModels.Classification
        fields = ('value', 'label', 'children')


class WareSetupPrefixSerializer(serializers.ModelSerializer):
    '''
    商品筛选器 筛选器分类 [Model app.WareSetupPrefix]
    '''

    class Meta:
        model = AppModels.WareSetupPrefix
        fields = '__all__'

    pass


class RateClassgUidSerializer(serializers.ModelSerializer):
    '''

    '''
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, instance):
        return instance.id

    def get_label(self, instance):
        return instance.get_uid_display()

    class Meta:
        model = AppModels.RateClassgUid
        fields = ['value', 'label', 'uid']

    pass


class BrandSerializer(serializers.ModelSerializer):
    '''
    商品筛选器 筛选器数据  [Model app.Brand]
    商品品牌
    '''

    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, instance):
        return instance.id

    def get_label(self, instance):
        return instance.name

    class Meta:
        model = AppModels.Brand
        fields = ['value', 'label']


class ProductTypeSerializer(serializers.ModelSerializer):
    '''
    商品筛选器 筛选器数据 [Model app.ProductType]
    产品类型
    '''

    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, instance):
        return instance.id

    def get_label(self, instance):
        return instance.name

    class Meta:
        model = AppModels.ProductType
        fields = ['value', 'label']


class TechnologySerializer(serializers.ModelSerializer):
    '''
    商品筛选器 筛选器数据 [Model app.Technology]
    技术类型
    '''

    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, instance):
        return instance.id

    def get_label(self, instance):
        return instance.name

    class Meta:
        model = AppModels.Technology
        fields = ['value', 'label']


class SceneSerializer(serializers.ModelSerializer):
    '''
    商品筛选器 筛选器数据 [Model app.Technology]
    使用场景
    '''

    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, instance):
        return instance.id

    def get_label(self, instance):
        return instance.name

    class Meta:
        model = AppModels.Scene
        fields = ['value', 'label']


class PriceRangeSerializer(serializers.ModelSerializer):
    '''
    商品筛选器 筛选器数据 [Model app.Technology]
    价格范围
    '''

    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_value(self, instance):
        return instance.id

    def get_label(self, instance):
        return instance.name

    class Meta:
        model = AppModels.PriceRange
        fields = ['value', 'label']


class GoodsInfoSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = AppModels.parameter
        fields = '__all__'

class WareParProfixSerizlizer(serializers.ModelSerializer):
    '''
    商品参数聚合
    根据 app.WareParProfix 模型来聚合 app.parameter 模型字段参数
    '''

    restful = serializers.SerializerMethodField()

    def get_restful(self, instance):
        context = []
        for item in instance.filter_name:
            # print(item[0])
            context.append({
                'value': item[0],
                'label': item[1],
            })
            pass

        return context

    class Meta:
        model = AppModels.WareParProfix
        fields = '__all__'
