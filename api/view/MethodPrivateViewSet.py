'''
功能相关接口
私有访问权限
'''
from django.db.models.query import QuerySet
from rest_framework.response import Response

from OAuth2.util import capitalizationPrice
from OAuth2.util.autograph import AutoRsaGraph
from account import models as AccountModels
from api.serializers import SerializersMethodl, SerializersModel
from api.util import ContractUtils
from api.util.ModelViewUtil import ModelViewSet
from home import models as HomeModels
from lhwill.util.log import log
from managestage.utli.datetimenow import datetimenow

logger = log(globals())


class ModelPrivateViewSet(ModelViewSet):
    '''
    私有权限，添加IsAuthenticated验证
    需要实现： 禁止修改非验证用户的数据
    '''
    permission_pubilc_write = False


class OrderViewSet(ModelPrivateViewSet):
    '''
    订单相关信息

    >## 提供订单操作接口

    ### 提交取消订单申请

        PATCH /api/v2/method-private/order/{ID}/
        DATE: {
            'isgotuaddress': true
        }

    >
    ### 驳回用户取消订单

        PATCH /api/v2/method-private/order/{ID}/
        DATE: {
            'type': 'reject'
        }

    注：

    * 如果指定 type 为 reject 则按照 驳回用户取消订单
    * 如果指定 type 为 approval 则按照 批准用户取消订单
    * 注意，需要此订单以 提交取消订单申请 操作方可继续

    >
    ### 批准用户取消订单

        PATCH /api/v2/method-private/order/{ID}/
        DATE: {
            'type': 'approval'
        }

    注：

    * 如果指定 type 为 reject 则按照 驳回用户取消订单
    * 如果指定 type 为 approval 则按照 批准用户取消订单
    * 注意，需要此订单以 提交取消订单申请 操作方可继续

    >
    ### 发货处理

        PATCH /api/v2/method-private/order/{ID}/
        DATE: {
            'ordtype': 0
        }

    注：

    * 发货处理将会 生成验收单 生成合同 针对央采用户

    * 发货处理后，央采用户即可查看验收单和合同

    >
    ### 收货处理

        PATCH /api/v2/method-private/order/{ID}/
        DATE: {
            'ordtype': 1
        }

    >
    ### 完成支付[订单结账]处理

        PATCH /api/v2/method-private/order/{ID}/
        DATE: {
            'ispaid': 1
        }

    '''
    queryset = HomeModels.Order.objects.filter()
    serializer_class = SerializersMethodl.OrderSerializer
    filter_fields = (
        'ordispaid',
        'ordContract',
        'state',
        'invoice',
        'isgotuaddress',
        'orderid',
        'total',
        'linkman',
        'linkmobile',
        'paymethod',
        'ispaid',
        'usercode',
        'ordtype',
        'key'
    )

    def perform_update(self, serializer):
        super(OrderViewSet, self).perform_update(serializer)

    def respone(self, data):
        '''
        通过dict修改数据字段
        :param data:
        :return:
        '''
        partial = self.kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def reject(self, instance):
        '''
        驳回用户取消订单
        :return:
        '''
        context = {
            'isgotuaddress': False
        }
        return self.respone(context)

    def approval(self, instance):
        '''
        批准用户取消订单
        :return:
        '''
        context = {
            'ordtype': -2,
            'ordispaid': -1,
            'ordContract': -1,
            'isgotuaddress': False
        }
        if instance.usercode:
            au = AutoRsaGraph(usercode=instance.usercode, orderid=instance.orderid)
            au.order_delete()
        return self.respone(context)

    def update(self, request, *args, **kwargs):
        from home.models import Logistics
        from OAuth2.util.autograph import AutoRsaGraph

        instance = self.get_object()

        if 'isgotuaddress' in request.data:
            if instance.state == 5 or \
                    instance.state == 3 or \
                    instance.state == 4 or \
                    instance.state == 0 or \
                    instance.state == -2 or \
                    not request.data['isgotuaddress'] or \
                    instance.isgotuaddress:
                context = {
                    'detail': '此订单状态不可操作。可能订单已完成，或以被取消！'
                }
                return Response(data=context, status=403)
            return super(OrderViewSet, self).update(request, *args, **kwargs)

        if 'type' in request.data:
            '''驳回用户取消订单'''
            if request.data['type'] == 'reject':
                return self.reject(instance)

            '''批准用户取消订单'''
            if request.data['type'] == 'approval':
                return self.approval(instance)

            return super(OrderViewSet, self).update(request, *args, **kwargs)

        if 'ordtype' in request.data:
            '''
            发货处理
            推送央采接口信息
            Shipping Handler
            Push logistics information
            '''
            if request.data['ordtype'] == 0:
                Logistics(
                    username='系统',
                    info='系统以确认订单，商品正在出库',
                    time=datetimenow(),
                    key=instance
                ).save()
                if instance.usercode:
                    AutoRsa = AutoRsaGraph(usercode=instance.usercode, orderid=instance.orderid)

                    '''
                    生成验收单
                    Generating acceptance sheet
                    '''
                    if instance.ordispaid == 0:
                        instance.ordispaid = 2
                        instance.save()
                        # AutoRsa.order_knot()
                        AutoRsa.order_update()
                        logger.i('生成验收单')
                        pass

                    AutoRsa.order_logistics()

                    '''
                    合同转正
                    Contract renewal
                    '''
                    from home.models import Contracts
                    try:
                        ins = instance.contracts_set.get()
                    except Contracts.DoesNotExist:
                        ContractUtils.Contract(instance).getpulContract()
                        ins = instance.contracts_set.get()
                        pass

                    ins.stype = 0
                    ins.save()
                    pass

                return self.respone({
                    'state': 2,
                    'ordispaid': 2,
                    'ordContract': 1,
                    'ordtype': 0
                })

            '''
            收货处理
            推送央采接口信息
            '''
            if request.data['ordtype'] == 1:
                instance.state = 0
                instance.save()
                Logistics(
                    username='系统',
                    info='您的订单已签收。感谢您在未来办公网购物，欢迎再次光临。',
                    time=datetimenow(),
                    key=instance
                ).save()
                if instance.usercode:
                    au = AutoRsaGraph(usercode=instance.usercode, orderid=instance.orderid)
                    au.order_logistics()
                    pass

                return self.respone({
                    'state': 0,
                    'ordtype': 1
                })


        if 'ispaid' in request.data:

            '''
            完成支付处理
            推送央采接口信息
            '''
            if request.data['ispaid'] == 1:
                if instance.usercode:
                    au = AutoRsaGraph(usercode=instance.usercode, orderid=instance.orderid)
                    au.order_PaymentCompletion()
                    pass

                return self.respone({
                    'ispaid': 1
                })


        return super(OrderViewSet, self).update(request, *args, **kwargs)
    pass


class CreateContractsViewSet(ModelPrivateViewSet):
    '''
    央采用户订单电子合同
    创建电子合同接口
    '''
    queryset = HomeModels.Contracts.objects.filter()
    serializer_class = SerializersModel.CreateContractsSerializer

    def create(self, request, *args, **kwargs):
        if not self.request.user.usercode:
            return Response({
                'detail': '非央采用户，不允许申请合同'
            }, status=403)

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # userinfo = UserInfo.objects.get(key=self.request.user)
        uninfo = AccountModels.UnitInfo.objects.get(key=self.request.user)
        o = HomeModels.Order.objects.get(id=data['key_order'])

        try:
            acc = HomeModels.Acceptance.objects.get(orderid=o.orderid).ysd_code
            if not acc:
                acc = '-'
        except HomeModels.Acceptance.DoesNotExist:
            acc = '-'
            pass

        if o.area and o.city and o.deliveryaddress:
            adder = '{} {} {} {}'.format(o.province, o.city, o.area, o.deliveryaddress)
        else:
            adder = '{} {} {}'.format(o.province, o.city, o.deliveryaddress)
            pass

        createtime = o.createtime.astimezone()

        timelist = str(createtime).split(' ')

        tlist = timelist[0]  # 2018-06-25
        tlist_all = tlist.split('-')  # ['2018', '06', '25']

        tlist_0 = tlist_all[0]  # 2018
        tlist_1 = tlist_all[1]  # 06
        tlist_2 = tlist_all[2]  # 25

        tlist_2 = int(tlist_2) + 2

        newtime = '{}年{}月{}日'.format(tlist_0, tlist_1, str(tlist_2))
        logger.i('订单送货时间+2天', newtime)

        HomeModels.Contracts(
            Acceptance=acc,  # 验收单编号 Done
            DAXTOTAL=capitalizationPrice.price(o.total),
            phlone=o.linkmobile,  # 电话号
            createtime=o.createtime,  # 订单创建时间
            username=o.linkman,  # 收货人
            unit=uninfo.name,  # 单位
            service='0.00',  # 服务费
            usercode=o.usercode,  # 采购人唯一识别码
            orderid=o.orderid,  # 合同编号
            total=o.total,  # 合计[商品总价]
            DeliveryTime=newtime,  # 送货时间[这个时间前到达目的地]
            DeliverylaceP=adder,  # 送货地点

            price=11,  # gso.price,  # 商品单价成交价
            number=1,  # gso.qty,  # 数量
            name='',  # o.name,  # 产品名称[商品名称]
            brands='',  # gso.goodsbrandname,  # 品牌
            model='',  # gso.model,  # 产品型号
            content='',  # gso.sku,  # 技术规格合主要配置

            images=o.images,  # 订单首页图片
            url=o.url,  # 订单链接
            time=datetimenow(),
            key_order=o,
            key=self.request.user
        ).save()

        o.ordContract = -1
        o.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
