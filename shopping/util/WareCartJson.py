import json
from decimal import Decimal

from account.models import User
from app.models import WareAppPrefix, Lease
from home.models import Discount, Gusid
from lhwill.util.log import log
from shopping.util.ListDictresource import Duplicate
from shopping import models

logger = log(globals())


class cart(object):
    '''
    商品优惠率相关
    '''

    def __init__(self, request):
        self.user = request.user
        self.id = None
        self.name = None
        self.image = None
        self.numb = None
        self.price = None
        self.money = None
        self.meal = None
        self.time = None
        self.total = None
        self.theress_id = None
        self.discon_gusid = None
        self.key = None
        self.discon = 0
        pass

    def PriceNumber(self, discon, money):
        '''
        计算央采优惠价格
        返回None 单笔订单大于100万
        :param discon: Discon.objects.filter
        :param money:
        :return:
        '''
        _money, rate = 0, 0
        if float(money) <= 100000:
            rate = discon.a1
        elif 100000 < float(money) and float(money) <= 300000:
            rate = discon.a2
        elif 300000 < float(money) and float(money) <= 600000:
            rate = discon.a3
        elif 600000 < float(money) and float(money) < 1000000:
            rate = discon.a4
        elif float(money) >= 1000000:
            logger.i('订单错误', '单笔订单不可大于等于100万人民币')
            return -1, -1

        _money = (100 - float(rate)) / 100 * float(money)

        logger.i('1', '原价', money, '折扣价', _money)

        return Decimal(_money).quantize(Decimal('0.00')), rate

    def isDiscon(self, cart):
        '''
        计算商品优惠率等商品信息 objects filter方法
        :param cart: list[dict]
        :return: list[dict] 购物车全部商品信息
        '''
        WareCart = []

        for i in cart:
            dic = {}
            self.discon = 0
            for u in cart:
                if i['discon_gusid'] == u['discon_gusid']:
                    self.id = i['id']
                    self.name = i['name']
                    self.image = i['image']
                    self.numb = i['numb']
                    self.price = i['price']
                    self.money = i['money']
                    self.meal = i['meal']
                    self.time = i['time']
                    self.total = i['total']
                    self.theress_id = i['theress_id']
                    self.discon_gusid = i['discon_gusid']
                    self.key = i['key']

                    if float(self.discon) < float(i['discon']):
                        self.discon = float(i['discon'])
                        pass

                    if float(self.discon) < float(u['discon']):
                        self.discon = float(u['discon'])
                        pass
                    pass
                    self.total = (100 - float(self.discon)) / 100 * float(self.money)
                pass

            logger.i('disconSET ', i['id'], i['name'], self.discon)
            dic['id'] = self.id
            dic['name'] = self.name
            dic['image'] = self.image
            dic['numb'] = self.numb
            dic['price'] = str(Decimal(self.price).quantize(Decimal('0.00')))
            dic['money'] = str(Decimal(self.money).quantize(Decimal('0.00')))
            dic['meal'] = self.meal
            dic['time'] = self.time
            dic['total'] = str(Decimal(self.total).quantize(Decimal('0.00')))

            dic['theress_id'] = self.theress_id
            dic['key'] = self.key
            dic['discon'] = self.discon
            dic['discon_gusid'] = self.discon_gusid

            WareCart.append(dic)
            pass

        ''' list嵌套dict 去重 '''
        logger.i(WareCart)

        return Duplicate(WareCart).isRemoval()
        pass

    def isDisconGetdict(self, r):
        '''
        获取商品优惠率等商品信息 objects get方法
        :param r: Cart.objects.get
        :return: dict 商品信息
        '''
        cart = []
        disc = 0
        Cart_object = []
        for i in models.Cart.objects.filter(user=self.user):
            classify_i = i.key.wareappprefix_set.get()
            classify_r = r.key.wareappprefix_set.get()
            total = 0
            discon_gusid = None

            discon = classify_i.rate_classg_key
            discon_gusid = classify_i.rate_classg_key.uid

            if i.user.usercode and classify_i:
                money = Decimal(float(i.price) * int(i.numb)).quantize(Decimal('0.00'))

                ''' 优惠价 优惠率 '''
                total, disc = self.PriceNumber(discon, money)
                pass

            cart.append({
                'id': i.id,
                'name': i.name,
                'image': i.image,
                'numb': i.numb,
                'price': str(Decimal(i.price).quantize(Decimal('0.00'))),
                'money': str(Decimal(i.money).quantize(Decimal('0.00'))),
                'meal': i.meal,
                'time': str(i.time.astimezone()),
                'discon': str(Decimal(disc).quantize(Decimal('0.00'))),
                'total': str(Decimal(total).quantize(Decimal('0.00'))),
                'theress_id': classify_i.classifythere_key.id,
                'discon_gusid': discon_gusid,
                'key': {
                    'id': i.key.id,
                    'release': i.key.release
                }
            })
        WareCart = self.isDiscon(cart)
        for i in WareCart:

            if i['id'] == r.id:
                logger.i('return isDisconGetdict ', i)
                totals = i['total']
                dic = {}
                dic['id'] = i['id']
                dic['name'] = i['name']
                dic['image'] = i['image']
                dic['numb'] = i['numb']
                dic['price'] = i['price']
                dic['money'] = i['money']
                dic['meal'] = i['meal']
                dic['time'] = i['time']
                dic['total'] = totals
                dic['theress_id'] = i['theress_id']
                dic['discon'] = i['discon']
                dic['discon_gusid'] = i['discon_gusid']

                return i
                pass
            pass
        return None
        pass

    def getListPrice(self, raw):
        '''
        计算央采用户价钱
        :param raw: 购物车Models Objects.filter List
        :return: Json 格式商品信息及央采用户价 优惠率等/普通用户返回空dict
        '''
        cart = []
        for i in raw:
            total, disc = 0, 0
            classify = i.key.wareappprefix_set.get()
            discon_gusid = None
            if i.user.usercode and classify:
                money = float(i.price) * int(i.numb)
                ''' 优惠价 优惠率 '''
                discon = classify.rate_classg_key
                discon_gusid = classify.rate_classg_key.uid
                total, disc = self.PriceNumber(discon, money)
                pass

            cart.append({
                'id': i.id,
                'name': i.name,
                'image': i.image,
                'numb': i.numb,
                'price': str(Decimal(i.price).quantize(Decimal('0.00'))),
                'money': str(Decimal(i.money).quantize(Decimal('0.00'))),
                'meal': i.meal,
                'time': str(i.time.astimezone()),
                'discon': str(Decimal(disc).quantize(Decimal('0.00'))),
                'total': str(Decimal(total).quantize(Decimal('0.00'))),
                'theress_id': classify.classifythere_key.id,
                'discon_gusid': discon_gusid,
                'key': {
                    'id': i.key.id,
                    'release': i.key.release
                }
            })
            pass

        ''' list嵌套dict 去重 '''
        return Duplicate(self.isDiscon(cart)).isRemoval(), cart
        pass

    def setListRate(self, raw, request=None):
        '''
        计算央采用户价钱及优惠率
        将其写入购物车以有商品
        :param raw: 购物车Models Objects.filter List
        :return: Json 格式商品信息及央采用户价 优惠率等/普通用户返回空dict
        '''
        cart = []

        if request:
            cart_model = models.Cart.objects.filter(user=request.user)
        else:
            cart_model = models.Cart.objects.filter(user=raw.user)

        for i in cart_model:
            total, disc = 0, 0
            classify = i.key.wareappprefix_set.get()
            discon_gusid = None
            if i.user.usercode and classify:
                money = float(i.price) * int(i.numb)
                ''' 优惠价 优惠率 '''
                discon = classify.rate_classg_key
                discon_gusid = classify.rate_classg_key.uid
                total, disc = self.PriceNumber(discon, money)
                pass

            cart.append({
                'id': i.id,
                'name': i.name,
                'image': i.image,
                'numb': i.numb,
                'price': str(Decimal(i.price).quantize(Decimal('0.00'))),
                'money': str(Decimal(i.money).quantize(Decimal('0.00'))),
                'meal': i.meal,
                'time': str(i.time.astimezone()),
                'discon': str(Decimal(disc).quantize(Decimal('0.00'))),
                'total': str(Decimal(total).quantize(Decimal('0.00'))),
                'theress_id': classify.classifythere_key.id,
                'discon_gusid': discon_gusid,
                'key': {
                    'id': i.key.id,
                    'release': i.key.release
                }
            })
            pass

        ''' list嵌套dict 去重 '''
        set_dict_rate = Duplicate(self.isDiscon(cart)).isRemoval()
        for rate_update in set_dict_rate:
            cart_rate = models.Cart.objects.get(id=rate_update['id'])
            cart_rate.rate = rate_update['discon']
            cart_rate.money = cart_rate.price * cart_rate.numb

            price = Decimal(float(100 - float(cart_rate.rate)) / 100 * float(cart_rate.price)).quantize(
                Decimal('0.00'))

            cart_rate.yc_price = price
            cart_rate.yc_money = cart_rate.yc_price * cart_rate.numb
            cart_rate.save()

        logger.i('setListRate', set_dict_rate)
        return set_dict_rate
        pass

    def getWareAppPrice(self, app):
        '''
        计算央采用户价钱
        :param raw: 购物车Models Objects.filter List
        :return: Json 格式商品信息及央采用户价 优惠率等/普通用户返回空dict
        '''
        WareApps = []

        logger.i('app for ', app)
        total, disc = 0, 0
        classify = WareAppPrefix.objects.get(wareApp_key=app)

        meal = Lease.objects.get(ware_key=app, select=1, defaule=True)

        discon_gusid = None
        if self.user.usercode and classify:
            money = Decimal(meal.money).quantize(Decimal('0.00'))  # 价钱

            discon = Discount.objects.get(classif_there=classify.classifythere_key)  # 优惠率

            discon_gusid = Gusid.objects.get(key=classify.classifythere_key).guid  # 18类ID
            ''' 优惠价 优惠率 '''
            total, disc = self.PriceNumber(discon, money)
            pass

        WareApps.append({
            'id': app.id,
            'name': app.name,
            'image': app.image,
            'numb': 1,
            'price': str(meal.money),
            'money': str(meal.money),
            'meal': '',
            'time': str(app.time_add.astimezone()),
            'discon': str(Decimal(disc).quantize(Decimal('0.00'))),
            'total': str(Decimal(total).quantize(Decimal('0.00'))),
            'theress_id': classify.classifythere_key.id,
            'discon_gusid': discon_gusid,
            'key': {}
        })
        pass

        WareCart = self.isDiscon(WareApps)

        ''' list嵌套dict 去重 '''
        logger.i(WareCart)
        WareCart = Duplicate(WareCart).isRemoval()
        logger.i(WareCart)
        return WareCart, cart
        pass

    def getPrice(self, raw):
        '''
        计算央采用户价钱
        :param raw: 购物车Models Objects.get List
        :return: Json 格式商品信息及央采用户价 优惠率等/普通用户返回空dict
        '''
        WareCart = self.isDisconGetdict(raw)
        return WareCart
        pass

    def getTotal(self, raw):
        '''
        计算央采商品总价格
        :param raw:
        :return:
        '''
        cart = []
        yhl = []
        totals = 0
        if not self.user.usercode:
            for i in raw:
                totals += Decimal(float(i.price) * int(i.numb)).quantize(Decimal('0.00'))
                logger.i('for i in raw', totals)
            return totals, yhl

        for i in raw:
            classify = WareAppPrefix.objects.get(wareApp_key=i.key)

            try:
                discon = Discount.objects.get(classif_there=classify.classifythere_key)
                ''' 优惠价 优惠率 '''
                discon_gusid = Gusid.objects.get(key=classify.classifythere_key).guid

                total, disc = self.PriceNumber(discon,
                                               Decimal(float(i.price) * int(i.numb)).quantize(Decimal('0.00')))

                logger.i('getTotal try self.PriceNumber', total)
                logger.i('getTotal try self.PriceNumber new ', float(i.price) * int(i.numb), i.id)
            except Discount.DoesNotExist:
                logger.e('Discount 优惠率不存在', classify.classifythere_key.name)
                total, disc = Decimal(float(i.price) * int(i.numb)).quantize(Decimal('0.00')), 0
                logger.i('getTotal try Discount.DoesNotExist', total)
                discon_gusid = 0

            cart.append({
                'id': i.id,
                'name': i.name,
                'image': i.image,
                'numb': i.numb,
                'price': str(Decimal(i.price).quantize(Decimal('0.00'))),
                'money': str(Decimal(i.money).quantize(Decimal('0.00'))),
                'meal': i.meal,
                'time': str(i.time.astimezone()),
                'discon': str(Decimal(disc).quantize(Decimal('0.00'))),
                'total': str(Decimal(total).quantize(Decimal('0.00'))),
                'theress_id': classify.classifythere_key.id,
                'discon_gusid': discon_gusid,
                'key': {
                    'id': i.key.id,
                    'release': i.key.release
                }
            })
            pass
        WareCart = self.isDiscon(cart)

        for i in WareCart:
            yhl.append({
                'id': i['id'],
                'discon': i['discon']
            })

            ''' 优惠价 优惠率 '''

            total = Decimal((100 - float(i['discon'])) / 100 * (float(i['price']) * int(i['numb']))).quantize(
                Decimal('0.00'))
            logger.i('getTotal for i in WareCart Decimal', total)

            totals += total
            logger.i('getTotal for i in WareCart totals += total', totals)

        return totals, yhl
        pass

    def setCartTotal(self, raw):
        cart = []
        totals = 0
        if self.user.usercode:

            classify = raw.key.wareappprefix_set.get()

            try:
                ''' 优惠价 优惠率 '''
                discon = classify.rate_classg_key
                discon_gusid = classify.rate_classg_key.uid

                total, disc = self.PriceNumber(discon,
                                               Decimal(float(raw.price) * int(raw.numb)).quantize(Decimal('0.00')))
            except Discount.DoesNotExist:
                logger.e('Discount 优惠率不存在', classify.classifythere_key.name)

                total, disc = Decimal(float(raw.price) * int(raw.numb)).quantize(Decimal('0.00')), 0
                discon_gusid = 0

            cart.append({
                'id': raw.id,
                'name': raw.name,
                'image': raw.image,
                'numb': raw.numb,
                'price': str(Decimal(raw.price).quantize(Decimal('0.00'))),
                'money': str(Decimal(raw.money).quantize(Decimal('0.00'))),
                'meal': raw.meal,
                'time': str(raw.time.astimezone()),
                'discon': str(Decimal(disc).quantize(Decimal('0.00'))),
                'total': str(Decimal(total).quantize(Decimal('0.00'))),
                'theress_id': classify.classifythere_key.id,
                'discon_gusid': discon_gusid,
                'key': {
                    'id': raw.key.id,
                    'release': raw.key.release
                }
            })

            WareCart = self.isDiscon(cart)
            for i in WareCart:
                ''' 优惠价 优惠率 '''

                price = Decimal(float((100 - float(i['discon'])) / 100 * (float(i['price'])))).quantize(
                    Decimal('0.00'))

                raw.yc_price = price
                raw.yc_money = price + raw.yc_money

                raw.rate = i['discon']
                raw.save()
                logger.i('央采用户，购物车商品优惠率设置', float(i['price']) * int(i['numb']))
            pass
        pass

    def cancelCartTotal(self, raw):

        if self.user.usercode:
            classify = raw.key.wareappprefix_set.get()
            ''' 优惠价 优惠率 '''
            total, disc = self.PriceNumber(
                classify.rate_classg_key,
                Decimal(float(raw.price) * int(raw.numb)).quantize(Decimal('0.00'))
            )

            price = Decimal(float(100 - float(disc)) / 100 * float(raw.price)).quantize(
                Decimal('0.00'))

            raw.yc_price = price
            raw.yc_money = total

            raw.rate = disc  # disc

            raw.save()

            logger.i('央采用户，购物车商品优惠率设置', price)
            pass
        pass

    def getMoney(self, money, yuhl):
        return Decimal(float((100 - float(yuhl)) / 100 * float(money))).quantize(Decimal('0.00'))
