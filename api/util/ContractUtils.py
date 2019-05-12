'''
合同创建工具类 Modles
'''

from django.utils.datetime_safe import datetime

from OAuth2.util import capitalizationPrice
from account import models
from home.models import Contracts, Acceptance, Goodslist


class Contract(object):
    def __init__(self, model):
        self.model = model
        self.user = models.User.objects.get(usercode=self.model.usercode)
        self.userinfo = models.UserInfo.objects.get(key=self.user)
        self.uninfo = models.UnitInfo.objects.get(key=self.user)
        self.goods = Goodslist.objects.filter(key=self.model.suborderlist_set.get())

    def getpulContract(self):
        '''
        创建用户合同数据
        :param request:
        :return:
        '''
        try:
            acceptance = Acceptance.objects.get(orderid=self.model.orderid).ysd_code
            if not acceptance:
                acceptance = '-'
        except Acceptance.DoesNotExist:
            acceptance = '-'

        if self.model.area and self.model.city and self.model.deliveryaddress:
            adder = '{} {} {} {}'.format(self.model.province, self.model.city, self.model.area,
                                         self.model.deliveryaddress)
        else:
            adder = '{} {} {}'.format(self.model.province, self.model.city, self.model.deliveryaddress)
            pass

        createtime = self.model.createtime.astimezone()
        timelist = str(createtime).split(' ')

        tlist = timelist[0]  # 2018-06-25
        tlist_all = tlist.split('-')  # ['2018', '06', '25']

        tlist_0 = tlist_all[0]  # 2018
        tlist_1 = tlist_all[1]  # 06
        tlist_2 = tlist_all[2]  # 25

        tlist_2 = int(tlist_2) + 2

        newtime = '{}年{}月{}日'.format(tlist_0, tlist_1, str(tlist_2))

        Contracts.objects.create(
            Acceptance=acceptance,  # 验收单编号 Done
            DAXTOTAL=capitalizationPrice.price(self.model.total),
            phlone=self.model.linkmobile,  # 电话号
            createtime=self.model.createtime,  # 订单创建时间
            username=self.model.linkman,  # 收货人
            unit=self.uninfo.name,  # 单位
            service='0.00',  # 服务费
            usercode=self.model.usercode,  # 采购人唯一识别码
            orderid=self.model.orderid,  # 合同编号
            total=self.model.total,  # 合计[商品总价]
            DeliveryTime=newtime,  # 送货时间[这个时间前到达目的地]
            DeliverylaceP=adder,  # 送货地点

            price='',  # self.goods.price,  # 商品单价成交价
            number='',  # self.goods.qty,  # 数量
            name='',  # self.model.name,  # 产品名称[商品名称]
            brands='',  # self.goods.goodsbrandname,  # 品牌
            model='',  # self.goods.model,  # 产品型号
            content='',  # self.goods.sku,  # 技术规格合主要配置

            images=self.model.images,  # 订单首页图片
            url=self.model.url,  # 订单链接
            time=datetime.utcnow(),
            key_order=self.model,
            key=self.user
        )

        self.model.ordContract = 1
        self.model.save()
        pass

    pass
