'''
序列化网站首页 接口
'''
from rest_framework import serializers

from app import models
from lhwill import settings

class _WareAppImage(serializers.ModelSerializer):
    '''
    序列化商品图片，首页分类子分类图标
    '''
    image = serializers.SerializerMethodField()
    image_64x64 = serializers.SerializerMethodField()
    image_125x125 = serializers.SerializerMethodField()
    image_200x200 = serializers.SerializerMethodField()
    image_400x400 = serializers.SerializerMethodField()
    image_800x800 = serializers.SerializerMethodField()

    def get_image(self, instance):
        if instance.image:
            return '{}/media{}'.format(settings.HTTP_HOST, instance.image)
        return None

    def get_image_64x64(self, instance):
        if instance.image_64x64:
            return '{}/media{}'.format(settings.HTTP_HOST, instance.image_64x64)
        return None

    def get_image_125x125(self, instance):
        if instance.image_125x125:
            return '{}/media{}'.format(settings.HTTP_HOST, instance.image_125x125)
        return None

    def get_image_200x200(self, instance):
        if instance.image_200x200:
            return '{}/media{}'.format(settings.HTTP_HOST, instance.image_200x200)
        return None

    def get_image_400x400(self, instance):
        if instance.image_400x400:
            return '{}/media{}'.format(settings.HTTP_HOST, instance.image_400x400)
        return None

    def get_image_800x800(self, instance):
        if instance.image_800x800:
            return '{}/media{}'.format(settings.HTTP_HOST, instance.image_800x800)
        return None

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset.select_related('id')
        queryset.select_related('image')
        queryset.select_related('image_64x64')
        queryset.select_related('image_125x125')
        queryset.select_related('image_200x200')
        queryset.select_related('image_400x400')
        queryset.select_related('image_800x800')
        return queryset

    class Meta:
        model = models.WareApp
        fields = ['id', 'image', 'image_64x64', 'image_125x125', 'image_200x200', 'image_400x400', 'image_800x800']
    pass

class _SubCategory(serializers.ModelSerializer):
    '''
    首页分类，商品分类
    '''
    label = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_label(self, instance):
        return instance.name

    def get_image(self, instance):
        w = instance.wareappprefix_set.filter()
        data = {}
        if w.exists():
            data = _WareAppImage(instance.wareappprefix_set.filter()[0].wareApp_key).data['image_125x125']
        return data

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset.select_related('id')
        queryset.select_related('label')
        queryset.select_related('image')
        return queryset

    class Meta:
        model = models.Classification_There
        fields = ['id', 'label', 'image']
    pass

class IndexSerializer(serializers.ModelSerializer):
    '''
    序列化首页分类
    '''
    label = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    def get_label(self, instance):
        return instance.name

    def get_children(self, instance):
        return _SubCategory(instance.classification_there_set.filter(), many=True).data

    def setup_eager_loading(self, queryset):
        """ Perform necessary eager loading of data. """
        queryset.prefetch_related('name')
        return queryset

    class Meta:
        # 序列化list key
        serializers_label_name = 'category'
        model = models.Classification
        fields = ['id', 'label', 'children']
    pass



class WheelSerializer(serializers.ModelSerializer):
    '''
    序列化首页轮播图
    '''
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return '{}{}'.format(settings.HTTP_HOST, instance.image.url)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset.select_related('id')
        queryset.select_related('image')
        return queryset

    class Meta:
        serializers_label_name = 'wheel'
        model = models.WheelModel
        fields = ['id', 'image']
    pass


class _GoodsImageSerializer(serializers.ModelSerializer):

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset.select_related('id')
        queryset.select_related('image')
        return queryset

    class Meta:
        model = models.images
        fields = ['id', 'image',]
    pass

class _GoodsSubCategory(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    money = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.wareApp_key.id
    def get_name(self, instance):
        return instance.wareApp_key.name

    def get_money(self, instance):
        return instance.wareApp_key.money

    def get_image(self, instance):
        image = []

        _image = _GoodsImageSerializer(instance.wareApp_key.images_set.filter(), many=True).data
        for i in _image:
            image.append('{}{}'.format(settings.HTTP_HOST, i.get('image')))
            pass
        return image

    def get_time_add(self, instance):
        return instance.wareApp_key.time_add

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset.select_related('id')
        queryset.select_related('name')
        queryset.select_related('money')
        queryset.select_related('image')
        queryset.select_related('time_add')
        return queryset

    class Meta:
        model = models.WareAppPrefix
        fields = ['id', 'name', 'money', 'image', 'time_add']
    pass

class SectorSerializer(serializers.ModelSerializer):
    '''
    首页下半部分商品板块展示栏目 序列化
    '''

    label = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    def get_label(self, instance):
        return instance.name

    def get_children(self, instance):
        return _GoodsSubCategory(instance.key.wareappprefix_set.filter()[:instance.number*5], many=True).data

    def get_brand(self, instance):
        return []

    def setup_eager_loading(self, queryset):
        """ Perform necessary eager loading of data. """
        queryset.select_related('name', 'label')

        return queryset

    class Meta:
        serializers_label_name = 'sector'
        model = models.SectorModel
        fields = ['id', 'label', 'children', 'brand']
    pass


