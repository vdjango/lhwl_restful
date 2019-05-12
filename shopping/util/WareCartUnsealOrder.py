from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Sum

from home.models import Order, Suborderlist, Goodslist, Logistics
from OAuth2.util.autograph import AutoRsaGraph
from lhwill import settings
from lhwill.util.log import log
from managestage.utli.datetimenow import _order_num, datetimenow

logger = log(globals())


class Unseal(object):
    def __init__(self, request, address, paymethod, invoices=None, invoicess=None):
        self.request = request
        self.user = self.request.user
        self.orderid = None
        self.cartlist = []
        self.paymethod = paymethod

        self.address = address
        self.province = self.address.province
        self.city = self.address.city
        self.area = self.address.area
        self.deliveryaddress = '{}'.format(self.address.consigneeAddress)
        self.linkman = self.address.consigneeName
        self.linkmobile = self.address.consigneeMobile

        self.invoices = invoices
        try:
            self.invoices_stype = invoicess
            self.invoices.stype = invoicess
            self.invoices.save()
        except:
            self.invoices_stype = 0
            pass

        self.remark = None

        self.error = None
        pass

    def get_error(self):
        return self.error

    def get_money(self, objects):
        '''针对购物车Models 聚合商品总价'''
        if self.request.user.usercode:
            money_aggregate = objects.aggregate(total=Sum("yc_money"))
        else:
            money_aggregate = objects.aggregate(total=Sum("money"))

        return money_aggregate

    def getOrder(self, cart):
        self.orderid = _order_num(package_id=cart[0].key.id, user_id=self.user.id)  # '创建主订单号'
        money_aggregate = self.get_money(cart)

        o = Order.objects.create(
            orderid=self.orderid,
            province=self.province,
            city=self.city,
            total=money_aggregate['total'],
            linkman=self.linkman,
            linkmobile=self.linkmobile,
            deliveryaddress=self.deliveryaddress,
            paymethod=self.paymethod,
            remark=self.remark,
            usercode=self.user.usercode,
            createtime=datetimenow(),
            area=self.area,
            invoice=self.invoices_stype,
            key_inv=self.invoices,
            key=self.user,
            state=2
        )

        subware = Suborderlist.objects.create(
            suborderid=o.orderid,
            total=o.total,
            key=o
        )

        for i in cart:
            try:
                per = i.key.parameter_set.get()
            except MultipleObjectsReturned:
                del_par = i.key.parameter_set.filter()
                per = del_par[0]
                del_par[1].delete()
                logger.e('以清理多余parameter数据 WareApp-ID', i.key.id)

            classify = i.key.wareappprefix_set.get()

            try:
                goodsclassguid = classify.rate_classg_key.uid  # '商品目录ID 枚举值对照表'
                goodsclassname = classify.rate_classg_key.get_uid_display()  # '商品类别名'
            except Exception as e:
                goodsclassguid = 0  # '商品目录ID 枚举值对照表'
                goodsclassname = '其他'  # '商品类别名'
                logger.e(e.args, '商品目录ID不完整')
                pass

            goodsbrandname = per.brands  # '品牌名称'
            if not goodsbrandname:
                self.error = '发现这个商品Prefix[ID={}]，goodsbrandname参数为None， 可能是该商品参数品牌未设置， 商品名称：{}'.format(classify.id,
                                                                                                        i.key.name)
                return None

            suborderid = _order_num(package_id=i.key.id, user_id=self.user.id)  # 子订单号
            name = '{}'.format(i.name)

            spu = '{} {}'.format(i.name, i.meal)
            sku = '{} {} {}'.format(per.model, per.productType, per.colorType)  # '细化到规格、型号'
            logger.i('image', '{}{}'.format(settings.HTTP_HOST, i.key.get_image_url_200x200()))
            Goodslist(
                goodsname=name,
                goodsid='{}-{}-{}'.format(i.id, i.key.id, suborderid),
                spu=spu,
                sku=sku,
                model='{} {}'.format(per.model, per.productType),
                goodsclassguid=goodsclassguid,
                goodsclassname=goodsclassname,
                goodsbrandname=goodsbrandname,
                qty=i.numb,
                total=i.yc_money,
                price=i.yc_price,
                originalprice=i.price,
                imgurl='{}{}'.format(settings.HTTP_HOST, i.key.get_image_url_200x200()),
                goodsurl=i.key.get_absolute_url(),
                key=subware,
                taoc=i.key_meal.name
            ).save()
            pass

        Logistics(
            info='您提交了订单，请等待卖家系统确认',
            time=datetimenow(),
            username='系统',
            key=o
        ).save()

        logger.i('订单成功创建')

        # 创建验收单
        if self.user.usercode:
            auto = AutoRsaGraph(usercode=self.user.usercode, orderid=self.orderid)
            order_create = auto.order_create()
            order_logistics = auto.order_logistics()

            logger.i('order_create', order_create)
            logger.i('order_logistics', order_logistics)

        else:
            logger.i('没有usercode')
            pass

        return True

        pass

    pass
