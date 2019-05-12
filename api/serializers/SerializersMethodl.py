from django.http import QueryDict
from rest_framework import serializers

from account import models as Acc
from account.models import User
from api.serializers.SerializersModel import WareSetupPrefixSerializer
from app import models as App
from app.models import RateClassgUid, Brand, ProductType, Technology, Scene, PriceRange
from home import models as Home
from home.models import Gusid
from lhwill import settings


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active')


class WareAppPackage(serializers.ModelSerializer):
    '''商品套餐'''

    class Meta:
        model = App.Lease
        fields = ['id', 'name', 'money', 'defaule']


class WareAppParameter(serializers.ModelSerializer):
    '''序列号商品参数'''

    class Meta:
        model = App.parameter
        fields = '__all__'


class WareAppPrefix(serializers.ModelSerializer):
    '''序列化商品配置相关参数'''
    classify = serializers.CharField(source='classify_key')
    classifythere = serializers.CharField(source='classifythere_key')
    pricerange = serializers.CharField(source='pricerange_key')
    producttype = serializers.CharField(source='producttype_key')
    technology = serializers.CharField(source='technology_key')
    scene = serializers.CharField(source='scene_key')
    brand = serializers.CharField(source='brand_key')
    rate_classg = serializers.IntegerField(source='rate_classg_key.uid')

    class Meta:
        model = App.WareAppPrefix
        fields = ['id', 'classify', 'classifythere', 'pricerange', 'producttype', 'technology', 'scene', 'brand',
                  'rate_classg']


class WareAppImageList(serializers.ModelSerializer):
    '''序列号商品图片List'''
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return '{}{}'.format(settings.HTTP_HOST, instance.image.url)

    class Meta:
        model = App.images
        fields = ['id', 'image', 'defaule']


class Address(serializers.ModelSerializer):
    class Meta:
        model = Home.Address
        fields = '__all__'


class WareApp(serializers.ModelSerializer):
    '''
    序列号商品详细参数及信息等

    包括 商品图片，商品套餐，商品参数，商品配置信息等
    '''

    images_set = WareAppImageList(many=True, read_only=True)
    lease_set = WareAppPackage(many=True, read_only=True)
    wareappprefix_set = WareAppPrefix(many=True, read_only=True)
    parameter_set = WareAppParameter(many=True, read_only=True)

    class Meta:
        model = App.WareApp
        fields = [
            'id',
            'name',
            'money',
            'unix',
            'connet',
            'describe',
            'characteristic',
            'commodity_description',
            'time_add',
            'images_set',
            'wareappprefix_set',
            'lease_set',
            'parameter_set'
        ]

    pass


class ContractsSerializer(serializers.ModelSerializer):
    '''
    用户订单合同
    '''

    class Meta:
        model = Home.Contracts
        fields = '__all__'

    pass


class GoodslistSerializer(serializers.ModelSerializer):
    '''
    订单商品
    '''
    goodsclassguid_zycg = serializers.SerializerMethodField()

    def get_goodsclassguid_zycg(self, objects):
        # print('goods_uig', objects)
        goods_uig = QueryDict(mutable=True)

        rate = RateClassgUid.objects.get(uid=objects.goodsclassguid)
        goods_uig.update({
            'name': rate.get_uid_display(),
            'uid': rate.uid,
            'a1': rate.a1,
            'a2': rate.a2,
            'a3': rate.a3,
            'a4': rate.a4,
            'defaule': rate.defaule
        })
        # print('goods_uig', goods_uig)

        return goods_uig

    class Meta:
        model = Home.Goodslist
        fields = '__all__'


class SuborderlistSerializer(serializers.ModelSerializer):
    '''
    子订单
    '''
    goodslist_set = GoodslistSerializer(many=True, read_only=True)

    class Meta:
        model = Home.Suborderlist
        fields = '__all__'


class InvoicesSerializer(serializers.ModelSerializer):
    '''
    发票信息序列化
    '''

    class Meta:
        model = Home.Invoices
        fields = '__all__'

    pass


class UserInfoSerializer(serializers.ModelSerializer):
    '''
    用户信息序列化
    '''

    class Meta:
        model = Acc.UserInfo
        fields = '__all__'

    pass


class UnitInfoSerializer(serializers.ModelSerializer):
    '''
    单位信息序列化
    '''

    class Meta:
        model = Acc.UnitInfo
        fields = '__all__'

    pass


class AcceptanceSerializer(serializers.ModelSerializer):
    '''
    验收单序列化
    '''

    class Meta:
        model = Home.Acceptance
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    '''
    序列化商品订单
    关于优惠率，同等商品类型
    '''
    contracts_set = ContractsSerializer(many=True, read_only=True)
    suborderlist_set = SuborderlistSerializer(many=True, read_only=True)

    user = serializers.SerializerMethodField()
    userinfo = serializers.SerializerMethodField()
    unitinfo = serializers.SerializerMethodField()
    acceptance = serializers.SerializerMethodField()

    key_inv = InvoicesSerializer()

    def get_user(self, objects):
        user_info = objects.key
        return UsersSerializer(user_info).data

    def get_userinfo(self, objects):
        from account.models import UserInfo
        try:
            user_info = objects.key.userinfo_set.get()
        except UserInfo.DoesNotExist:
            return []
            pass
        return UserInfoSerializer(user_info).data

    def get_unitinfo(self, objects):
        from account.models import UnitInfo
        try:
            unit_info = objects.key.unitinfo_set.get()
        except UnitInfo.DoesNotExist:
            return []
            pass
        return UnitInfoSerializer(unit_info).data

    def get_acceptance(self, objects):
        from home.models import Acceptance
        try:
            acceptances = Acceptance.objects.get(usercode=objects.usercode, orderid=objects.orderid)
        except Acceptance.DoesNotExist:
            return []
        return AcceptanceSerializer(acceptances).data
        pass

    class Meta:
        model = Home.Order
        fields = '__all__'


class _SearchingListWareApp(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    money = serializers.SerializerMethodField()
    unix = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    release = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.wareApp_key.id

    def get_name(self, instance):
        return instance.wareApp_key.name

    def get_money(self, instance):
        return instance.wareApp_key.money

    def get_unix(self, instance):
        return instance.wareApp_key.unix

    def get_stock(self, instance):
        return instance.wareApp_key.stock

    def get_release(self, instance):
        return instance.wareApp_key.release

    def get_image(self, instance):
        return WareAppImageList(instance.wareApp_key.images_set.filter(), many=True).data

    class Meta:
        model = App.WareAppPrefix
        fields = ['id', 'name', 'money', 'unix', 'stock', 'release', 'image']

    pass


class BrandSerializer(serializers.ModelSerializer):
    '''A1 商品筛选器'''

    class Meta:
        model = Brand
        fields = ('id', 'name')


class ProductTypeSerializer(serializers.ModelSerializer):
    '''A2 商品筛选器'''

    class Meta:
        model = ProductType
        fields = ('id', 'name')


class TechnologySerializer(serializers.ModelSerializer):
    '''A3 商品筛选器'''

    class Meta:
        model = Technology
        fields = ('id', 'name')


class SceneSerializer(serializers.ModelSerializer):
    '''A4 商品筛选器'''

    class Meta:
        model = Scene
        fields = ('id', 'name')


class PriceRangeSerializer(serializers.ModelSerializer):
    '''A5 商品筛选器'''

    class Meta:
        model = PriceRange
        fields = ('id', 'name')


class SearchingList(serializers.ModelSerializer):
    prefix = serializers.SerializerMethodField()

    def get_prefix(self, instance):
        context = []
        c = WareSetupPrefixSerializer(instance.waresetupprefix_set.filter(), many=True).data
        for i in c:
            if i['filter_id'] == 0:
                context.append({
                    'label': i['t1'],
                    'children': BrandSerializer(instance.brand_set.filter(), many=True).data
                })
                print(i['filter_id'], '商品品牌', i['t1'])
                pass
            if i['filter_id'] == 1:
                context.append({
                    'label': i['t2'],
                    'children': ProductTypeSerializer(instance.producttype_set.filter(), many=True).data
                })
                print(i['filter_id'], '产品类型', i['t2'])
                pass
            if i['filter_id'] == 2:
                context.append({
                    'label': i['t3'],
                    'children': TechnologySerializer(instance.technology_set.filter(), many=True).data
                })
                print(i['filter_id'], '技术类型', i['t3'])
                pass
            if i['filter_id'] == 3:
                context.append({
                    'label': i['t4'],
                    'children': SceneSerializer(instance.scene_set.filter(), many=True).data
                })
                print(i['filter_id'], '使用场景', i['t4'])
                pass
            if i['filter_id'] == 4:
                context.append({
                    'label': i['t5'],
                    'children': PriceRangeSerializer(instance.pricerange_set.filter(), many=True).data
                })
                print(i['filter_id'], '价格范围', i['t5'])
                pass

        return context

    class Meta:
        model = App.Classification_There
        fields = ['id', 'name', 'level', 'prefix']

    pass
