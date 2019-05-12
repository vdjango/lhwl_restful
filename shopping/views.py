import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Avg, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views import generic

from account.models import User
from app.models import WareApp, images, Lease, WareAppPrefix, RateClassgUid
from home.models import Discount, Invoices, Address, Order
from lhwill.util.log import log
from lhwill.view import HttpCodeError
from managestage.utli.datetimenow import datetimenow, _order_num
from managestage.utli.wrapper import Web_Maintain
# Create your views here.
from shopping import models
from shopping.util import WareCartJson
from shopping.util.ListDictresource import Duplicate
from shopping.util.WareCartUnsealOrder import Unseal

logger = log(globals())

decorators = [login_required]


@method_decorator(decorators, name='dispatch')
class Index(generic.TemplateView):
    '''
    购物车首页视图 shop:shopping
    '''
    template_name = 'defaule/shopping/index.html'

    def getZycgPrice(self, raw):
        '''
        计算央采用户价钱
        :param raw: 购物车Models Objects.filter List
        :return: Json 格式商品信息及央采用户价 优惠率等/普通用户返回空dict
        '''
        cart = []

        try:
            for i in raw:
                logger.i('raw for ', raw)
                cart_ = False  # 不支持大于100w的金额订单

                defaule_money = 0
                discon = 0
                total = 0.00
                zycg = False
                try:
                    classify = WareAppPrefix.objects.get(wareApp_key=i.key)
                    theress_id = classify.classifythere_key.id
                except:
                    theress_id = None
                    classify = None

                if i.user.usercode and classify:
                    zycg = True
                    dismoney = 0  # 优惠率
                    money = float(i.price) * int(i.numb)

                    theress = classify.classifythere_key

                    discon = Discount.objects.get(classif_there=theress)
                    if int(money) <= 100000:
                        # a1
                        dismoney = discon.a1
                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('int(number_money) <= 100000', defaule_money, '原价', money, '折扣价',
                                 defaule_money)
                        pass

                    elif 100000 < int(money) and int(money) <= 300000:
                        # a2
                        dismoney = discon.a2
                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('100000 < int(number_money) and int(number_money) <= 300000', '原价', money,
                                 '折扣价', defaule_money)
                        pass

                    elif 300000 < int(money) and int(money) <= 600000:
                        # a3
                        dismoney = discon.a3
                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('300000 < int(number_money) and int(number_money) <= 600000', '原价', money,
                                 '折扣价', defaule_money)
                        pass

                    elif 600000 < int(money) and int(money) < 1000000:
                        # a4
                        dismoney = discon.a4
                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('600000 < int(number_money) and int(number_money) <= 1000000', '原价', money,
                                 '折扣价', defaule_money)

                    elif float(money) >= 1000000:
                        logger.i('订单错误', '单笔订单不可大于等于100万人民币')
                        cart_ = True  # 单笔订单不可大于等于100万人民币
                        # return error_(self.request, code=403, title='订单错误', page='Order error', content='单笔订单不可大于等于100万人民币')
                        pass

                    discon = dismoney  # 优惠率
                    total = Decimal(defaule_money).quantize(Decimal('0.00'))  # 优惠总价
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
                    'discon': str(discon),
                    'total': str(total),
                    'cart_': cart_,
                    'theress_id': theress_id,
                    'key': {
                        'id': i.key.id
                    }
                })
                pass
        except:
            logger.i('raw try ', raw)
            cart_ = False  # 不支持大于100w的金额订单

            defaule_money = 0
            discon = 0
            total = 0.00
            zycg = False
            try:
                classify = WareAppPrefix.objects.get(wareApp_key=raw.key)
                theress_id = classify.classifythere_key.id
            except:
                theress_id = None
                classify = None

            if raw.user.usercode and classify:
                zycg = True
                dismoney = 0  # 优惠率
                money = float(raw.price) * int(raw.numb)

                theress = classify.classifythere_key

                discon = Discount.objects.get(classif_there=theress)
                if float(money) <= 100000:
                    # a1
                    dismoney = discon.a1
                    defaule_money = (100 - float(dismoney)) / 100 * float(money)

                    logger.i('int(number_money) <= 100000', '原价', money, '折扣价', defaule_money)
                    pass

                elif 100000 < float(money) and float(money) <= 300000:
                    # a2
                    dismoney = discon.a2
                    defaule_money = (100 - float(dismoney)) / 100 * float(money)
                    logger.i('100000 < int(number_money) and int(number_money) <= 300000', '原价', money, '折扣价',
                             defaule_money)
                    pass

                elif 300000 < float(money) and float(money) <= 600000:
                    # a3
                    dismoney = discon.a3
                    defaule_money = (100 - float(dismoney)) / 100 * float(money)
                    logger.i('300000 < int(number_money) and int(number_money) <= 600000', '原价', money, '折扣价',
                             defaule_money)
                    pass

                elif 600000 < float(money) and float(money) < 1000000:
                    # a4
                    dismoney = discon.a4
                    defaule_money = (100 - float(dismoney)) / 100 * float(money)
                    logger.i('600000 < int(number_money) and int(number_money) <= 1000000', '原价', money, '折扣价',
                             defaule_money)

                elif float(money) >= 1000000:
                    logger.i('订单错误', '单笔订单不可大于等于100万人民币')
                    cart_ = True  # 单笔订单不可大于等于100万人民币
                    # return error_(self.request, code=403, title='订单错误', page='Order error', content='单笔订单不可大于等于100万人民币')
                    pass

                discon = dismoney  # 优惠率
                total = Decimal(defaule_money).quantize(Decimal('0.00'))  # 优惠总价
                pass

            cart.append({
                'id': raw.id,
                'name': raw.name,
                'image': raw.image,
                'numb': raw.numb,
                'price': str(Decimal(raw.price).quantize(Decimal('0.00'))),
                'money': str(Decimal(raw.money).quantize(Decimal('0.00'))),
                'meal': raw.meal,
                'time': str(raw.time.astimezone()),
                'discon': str(discon),
                'total': str(total),
                'cart_': cart_,
                'theress_id': theress_id,
                'key': {
                    'id': raw.key.id
                }
            })

            pass

        WareCart = []

        for i in cart:
            dic = {}
            for u in cart:
                if i['theress_id'] == u['theress_id']:
                    dic['id'] = i['id']
                    dic['name'] = i['name']
                    dic['image'] = i['image']
                    dic['numb'] = i['numb']
                    dic['price'] = i['price']
                    dic['money'] = i['money']
                    dic['meal'] = i['meal']
                    dic['time'] = i['time']
                    dic['total'] = i['total']
                    dic['cart_'] = i['cart_']
                    dic['theress_id'] = i['theress_id']
                    dic['key'] = i['key']

                    if i['discon'] > u['discon']:
                        print(dic['name'], '> ', i['numb'], i['discon'])
                        dic['discon'] = i['discon']
                    else:
                        print(dic['name'], '< ', u['numb'], u['discon'])
                        dic['discon'] = u['discon']
                        pass
                    WareCart.append(dic)
                pass
            pass

        ''' list嵌套dict 去重 '''
        WareCart = Duplicate(WareCart).isRemoval()

        logger.i(WareCart)

        return WareCart, json.dumps(cart)
        pass

    def get_context_data(self, **kwargs):
        Carts = models.Cart.objects.filter(user=self.request.user)
        Cart, _ = WareCartJson.cart(self.request).getListPrice(Carts)

        if self.request.user.usercode:
            zycg = True
        else:
            zycg = False
            pass

        content = {
            # 'zycg': zycg,
            'Cart': Cart
        }
        kwargs.update(content)
        return kwargs

    def post(self, request):
        '''商品添加到购物车'''
        id = request.POST.get('id')
        leas = request.POST.get('purchase')
        number = request.POST.get('number')

        if int(number) < 1:
            content = {
                'state': 'error',
                'code': 403,
                'error': '添加购物车商品数量需大于0'
            }
            return HttpResponse(json.dumps(content))
            pass
        users = User.objects.get(username=request.user.username)

        '''商品'''
        wareapp = WareApp.objects.get(id=id)

        '''商品首图'''

        '''商品套餐 价钱'''
        if leas:
            leas_app = Lease.objects.get(ware_key=wareapp, id=leas)
        else:
            leas_app = Lease.objects.get(ware_key=wareapp, defaule=True)

        money = leas_app.money

        logger.i('shopping', '尝试获取购物车商品信息')
        ''' 商品不存在，或者商品存在。套餐不同 则创建商品'''
        Cart = models.Cart.objects.filter(key=wareapp, key_meal=leas_app, user=users)
        if Cart.exists():
            Cart.update(
                numb=int(number) + int(Cart[0].numb),
                money=float(money) + float(Cart[0].money),
                name=wareapp.name,
                image=wareapp.get_image_url_200x200(),
                price=leas_app.money,
                meal=leas_app.name,
                user=users,
                key=wareapp,
                key_meal=leas_app
            )
            Cart = Cart.get(key=wareapp, key_meal=leas_app, user=users)
            logger.i('shopping', '修改以有商品到购物车成功', Cart.name, '商品数量', number)
        else:
            Cart = models.Cart.objects.create(
                numb=number,
                money=money,
                name=wareapp.name,
                image=wareapp.get_image_url_200x200(),
                price=leas_app.money,
                meal=leas_app.name,
                user=users,
                key=wareapp,
                key_meal=leas_app
            )
            logger.i('shopping', '成功创建商品到购物车', Cart.name, '商品数量', number)
            pass

        wcart = WareCartJson.cart(self.request)
        wcart.setCartTotal(Cart)
        wcart.setListRate(Cart)

        logger.i('shopping', '保存商品到购物车', Cart.name, '商品数量', number)

        content = {
            'state': 'success',
            'data': {
                'id': id,
                'number': number,
                'leas': leas,
                'money': float(money)
            },
            'code': 200
        }
        return HttpResponse(json.dumps(content))
        pass

    pass


@method_decorator(decorators, name='dispatch')
class settleAccounts(generic.TemplateView):
    '''
    购物车结算页,创建订单
    '''
    template_name = 'defaule/shopping/settleAccounts.html'

    cart_response = False

    def dispatch(self, request, *args, **kwargs):

        return super(settleAccounts, self).dispatch(request, *args, **kwargs)

    def getCounl(self, cart):
        '''
        计算央采优惠率
        :param cart: 购物车 objects get
        :return: 优惠价格 优惠率
        '''
        try:
            classify = WareAppPrefix.objects.get(wareApp_key=cart.key)
        except:
            classify = None

        dismoney = 0
        defaule_money = 0
        if cart['user']['usercode'] and classify:
            zycg = True
            dismoney = 0  # 优惠率
            money = float(cart.price) * int(cart.numb)

            theress = classify.classifythere_key

            discon = Discount.objects.get(classif_there=theress)
            if int(money) <= 100000:
                # a1
                dismoney = discon.a1
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('int(number_money) <= 100000', defaule_money, '原价', money, '折扣价',
                         defaule_money)
                pass

            elif 100000 < int(money) and int(money) <= 300000:
                # a2
                dismoney = discon.a2
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('100000 < int(number_money) and int(number_money) <= 300000', '原价', money,
                         '折扣价', defaule_money)
                pass

            elif 300000 < int(money) and int(money) <= 600000:
                # a3
                dismoney = discon.a3
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('300000 < int(number_money) and int(number_money) <= 600000', '原价', money,
                         '折扣价', defaule_money)
                pass

            elif 600000 < int(money) and int(money) < 1000000:
                # a4
                dismoney = discon.a4
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('600000 < int(number_money) and int(number_money) <= 1000000', '原价', money,
                         '折扣价', defaule_money)

            elif float(money) >= 1000000:
                logger.i('订单错误', '单笔订单不可大于等于100万人民币')
                cart_ = True  # 单笔订单不可大于等于100万人民币
                # return error_(self.request, code=403, title='订单错误', page='Order error', content='单笔订单不可大于等于100万人民币')
                pass

        discon = dismoney  # 优惠率
        total = Decimal(defaule_money).quantize(Decimal('0.00'))  # 优惠总价
        return total, discon

    def get_context_data(self, **kwargs):
        '''
        结算页·View
        :param request:
        :return:
        '''

        request = self.request
        users = User.objects.get(username=request.user.username)
        cartlist = request.GET.getlist('cartlist')
        if not cartlist:
            self.cart_response = True
            pass

        cart = models.Cart.objects.filter(id__in=cartlist, user=users)  # type(cartlist) = List
        if not cart.exists():
            self.cart_response = True

        ''' 商品信息 '''
        totals = 0.00  # 商品折扣价
        moneys = 0.00  # 商品原价

        WaCart, _ = WareCartJson.cart(request).getListPrice(raw=cart)

        for i in WaCart:
            totals += float(i['total'])
            moneys += float(i['money'])
            pass
        logger.i('cartlist', WaCart)
        favourable = float(moneys - totals)  # 优惠了多少

        ''' 优惠报表 '''
        moneytable = []
        for i in Discount.objects.filter(defaule=True):
            moneytable.append({
                'id': i.id,
                'name': i.classif_there.name,
                'a1': i.a1.to_integral,
                'a2': i.a2.to_integral,
                'a3': i.a3.to_integral,
                'a4': i.a4.to_integral
            })
            pass

        ''' 收货人信息 '''
        add = Address.objects.filter(key=users, defaule=True)
        if not add:
            add = Address.objects.filter(key=users)[:1]
            pass
        if add:
            add = add[0]
            pass

        ''' 发票信息 '''
        try:
            invs = Invoices.objects.get(key=users)
            logger.i(invs.stype)
            inv = {
                'stype': invs.stype,
                'content': invs.content,
                'taxpayer': invs.taxpayer,
                'phone': invs.phone,
                'email': invs.email,
                'head': invs.head,
                'unitName': invs.unitName,
                'registeredAddress': invs.registeredAddress,
                'registeredTelephone': invs.registeredTelephone,
                'accountOpening': invs.accountOpening,
                'account': invs.account
            }
        except:
            inv = {}
            pass

        logger.i('totals ', totals)

        content = {
            'cart': WaCart,
            'address': add,
            'inv': inv,
            'totals': Decimal(totals).quantize(Decimal('0.00')),
            'moneys': Decimal(moneys).quantize(Decimal('0.00')),
            'favourable': favourable,
            'moneytable': moneytable,
            'cartlist': ','.join(cartlist)
        }
        kwargs.update(content)
        return kwargs
        pass

    def post(self, request):
        '''
        提交订单 创建订单等
        :param request:
        :return:
        '''
        # 购物车商品List id
        cartlist_id = request.POST.get('id')

        # 收货地址
        address_id = request.POST.get('address')

        # 支付方式
        paymethod = request.POST.get('paymethod')

        # 发票类型
        invoicess = request.POST.get('invoices')

        # 订单备注
        remark = request.POST.get('invoices')

        # 转List 商品
        cartlist = str(cartlist_id).split(',')
        user = models.User.objects.get(username=request.user.username)

        cart = models.Cart.objects.filter(id__in=cartlist, user=user)

        try:
            add = Address.objects.get(id=address_id, key=user)
        except Exception as e:
            return redirect(reverse('home:address'))

        logger.i(invoicess)
        try:
            invoices = Invoices.objects.get(key=user)  # 发票信息
        except Invoices.DoesNotExist:
            invoices = None
            pass

        uns = Unseal(request, address=add, paymethod=paymethod, invoices=invoices, invoicess=invoicess)
        uns.getOrder(cart)

        # cart.delete()

        return HttpResponseRedirect('/home/success/?orderId={}'.format(uns.orderid))
        pass

    pass


@method_decorator(decorators, name='dispatch')
class BuyGoods(generic.TemplateView):
    '''
    购物车结算页,创建订单
    '''
    template_name = 'defaule/shopping/settleAccounts.html'

    def dispatch(self, request, *args, **kwargs):
        self.app_id = kwargs['app_id']
        super(BuyGoods, self).dispatch(request, *args, **kwargs)

    def getCounl(self, cart):
        '''
        计算央采优惠率
        :param cart: 购物车 objects get
        :return: 优惠价格 优惠率
        '''
        try:
            classify = WareAppPrefix.objects.get(wareApp_key_id=self.app_id)
        except:
            classify = None

        dismoney = 0
        defaule_money = 0
        if cart['user']['usercode'] and classify:
            zycg = True
            dismoney = 0  # 优惠率
            money = float(cart.price) * int(cart.numb)

            theress = classify.classifythere_key

            discon = Discount.objects.get(classif_there=theress)
            if int(money) <= 100000:
                # a1
                dismoney = discon.a1
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('int(number_money) <= 100000', defaule_money, '原价', money, '折扣价',
                         defaule_money)
                pass

            elif 100000 < int(money) and int(money) <= 300000:
                # a2
                dismoney = discon.a2
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('100000 < int(number_money) and int(number_money) <= 300000', '原价', money,
                         '折扣价', defaule_money)
                pass

            elif 300000 < int(money) and int(money) <= 600000:
                # a3
                dismoney = discon.a3
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('300000 < int(number_money) and int(number_money) <= 600000', '原价', money,
                         '折扣价', defaule_money)
                pass

            elif 600000 < int(money) and int(money) < 1000000:
                # a4
                dismoney = discon.a4
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('600000 < int(number_money) and int(number_money) <= 1000000', '原价', money,
                         '折扣价', defaule_money)

            elif float(money) >= 1000000:
                logger.i('订单错误', '单笔订单不可大于等于100万人民币')
                cart_ = True  # 单笔订单不可大于等于100万人民币
                # return error_(self.request, code=403, title='订单错误', page='Order error', content='单笔订单不可大于等于100万人民币')
                pass

        discon = dismoney  # 优惠率
        total = Decimal(defaule_money).quantize(Decimal('0.00'))  # 优惠总价
        return total, discon

    def get_context_data(self, **kwargs):
        '''
        结算页·View
        :param request:
        :return:
        '''

        users = User.objects.get(username=self.request.user.username)
        cartlist = self.request.GET.get('cartlist')

        cart = models.WareApp.objects.filter(id=self.app_id)

        ''' 商品信息 '''
        totals = 0.00  # 商品折扣价
        moneys = 0.00  # 商品原价

        WaCart, _ = WareCartJson.cart(self.request).getWareAppPrice(app=cart[0])

        for i in WaCart:
            totals += float(i['total'])
            moneys += float(i['money'])
            pass
        logger.i('cartlist', WaCart)
        favourable = float(moneys - totals)  # 优惠了多少

        ''' 优惠报表 '''
        moneytable = []
        for i in Discount.objects.filter(defaule=True):
            moneytable.append({
                'id': i.id,
                'name': i.classif_there.name,
                'a1': i.a1.to_integral,
                'a2': i.a2.to_integral,
                'a3': i.a3.to_integral,
                'a4': i.a4.to_integral
            })
            pass

        ''' 收货人信息 '''
        add = Address.objects.filter(key=users, defaule=True)
        if not add:
            add = Address.objects.filter(key=users)[:1]
            pass
        if add:
            add = add[0]
            pass

        ''' 发票信息 '''
        try:
            invs = Invoices.objects.get(key=users)
            logger.i(invs.stype)
            inv = {
                'stype': invs.stype,
                'content': invs.content,
                'taxpayer': invs.taxpayer,
                'phone': invs.phone,
                'email': invs.email,
                'head': invs.head,
                'unitName': invs.unitName,
                'registeredAddress': invs.registeredAddress,
                'registeredTelephone': invs.registeredTelephone,
                'accountOpening': invs.accountOpening,
                'account': invs.account
            }
        except:
            inv = {}
            pass

        logger.i('totals ', totals)

        content = {
            'cart': WaCart,
            'address': add,
            'inv': inv,
            'totals': totals,
            'moneys': moneys,
            'favourable': favourable,
            'moneytable': moneytable,
            'cartlist': ','.join(cartlist)
        }
        kwargs.update(content)
        return kwargs
        pass

    def post(self, request):
        '''
        提交订单 创建订单等
        :param request:
        :return:
        '''
        # 购物车商品List id
        cartlist_id = request.POST.get('id')

        # 收货地址
        address_id = request.POST.get('address')

        # 支付方式
        paymethod = request.POST.get('paymethod')

        # 发票类型
        invoicess = request.POST.get('invoices')

        # 订单备注
        remark = request.POST.get('invoices')

        # 转List 商品
        cartlist = str(cartlist_id).split(',')
        user = models.User.objects.get(username=request.user.username)

        cart = models.Cart.objects.filter(id__in=cartlist, user=user)

        try:
            add = Address.objects.get(id=address_id, key=user)
        except Exception as e:
            return redirect(reverse('home:address'))

        logger.i(invoicess)
        try:
            invoices = Invoices.objects.get(key=user)  # 发票信息
        except Invoices.DoesNotExist:
            invoices = None
            pass

        uns = Unseal(request, address=add, paymethod=paymethod, invoices=invoices, invoicess=invoicess)
        uns.getOrder(cart)

        cart.delete()

        return HttpResponseRedirect('/home/success/?orderId={}'.format(uns.orderid))
        pass

    pass


'''提交订单'''


@method_decorator(decorators, name='dispatch')
class PlaceOrderView(generic.TemplateView):
    template_name = 'defaule/shopping/placeOrder.html'

    fields = ('paymethod',)

    '''
    True 表示： 立即购买
    [通过传入商品ID - ware_id 获取商品信息下单]
    False 表示： 购物车方式下单购买
    [通过传入购物车商品ID【非商品ID】 - ware_id 获取购物车商品信息下单]
    '''
    cart_purchase_immediately = False

    def dispatch(self, request, *args, **kwargs):
        try:
            self.ware = kwargs['ware_id']
            self.cart_purchase_immediately = True
        except KeyError:
            self.ware = self.request.GET.getlist('cartlist')

        if self.request.method == 'POST':
            self.ware_id = self.request.POST.get('ware_id')
            self.address = request.POST.get('address')
            self.paymethod = request.POST.get('paymethod')
            self.invoicess = request.POST.get('invoices')
            self.remark = request.POST.get('remark')

        return super(PlaceOrderView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''
        结算页·View
        :param request:
        :return:
        '''

        if not self.cart_purchase_immediately:
            cart_or_wareapp = models.Cart.objects.filter(id__in=self.ware, user=self.request.user)
            money_aggregate = self.get_money(cart_or_wareapp)
            cartlist = ','.join(self.ware)
        else:
            cart_or_wareapp = WareAppPrefix.objects.filter(wareApp_key=self.ware, wareApp_key__release=True)

            money_aggregate = Lease.objects.filter(ware_key=cart_or_wareapp.get(id=cart_or_wareapp[0].id).wareApp_key,
                                                   defaule=True).aggregate(money=Sum("money"))
            cartlist = self.ware
            pass

        if not cart_or_wareapp.exists():
            self.cart_response = True

        ''' 收货人信息 '''
        add = Address.objects.filter(key=self.request.user)

        ''' 发票信息 '''
        try:
            invs = Invoices.objects.get(key=self.request.user)
        except Invoices.DoesNotExist:
            invs = None
            pass

        if self.cart_purchase_immediately:
            i = cart_or_wareapp.get(id=cart_or_wareapp[0].id).wareApp_key
            cart_or_wareapp = {
                'name': i.name,
                'image': i.image,
                'numb': 1,
                'price': i.price,
                'money': i.money,
                'meal': i.meal,
                'time': i.time,
                'rate': i.rate,
                'yc_price': i.yc_price,
                'yc_money': i.yc_money,
            }

        if money_aggregate['total'] > 1000000:
            self.template_name = 'defaule/shopping/error.html'

            content = {
                'error': '订单金额大于一百万，请分批次下单',
            }
            kwargs.update(content)
            return kwargs
            pass

        content = {
            'cart': cart_or_wareapp,
            'address': add,
            'inv': invs,
            'money_aggregate': money_aggregate,
            'moneytable': RateClassgUid.objects.filter(),
            'cartlist': cartlist
        }
        # content.update({'cartlist': self.ware })

        kwargs.update(content)
        return kwargs
        pass

    def get_money(self, objects):
        '''针对购物车Models 聚合商品总价'''
        if self.request.user.usercode:
            money_aggregate = objects.aggregate(total=Sum("yc_money"))
        else:
            money_aggregate = objects.aggregate(total=Sum("money"))

        return money_aggregate

    def post(self, request):
        '''
        提交订单 创建订单等
        :param request:
        :return:
        '''

        remark = self.remark  # 订单备注
        cartlist = str(self.ware_id).split(',')

        cart = models.Cart.objects.filter(id__in=cartlist, user=request.user)

        try:
            add = Address.objects.get(id=self.address, key=request.user)
        except Address.DoesNotExist:
            return redirect(reverse('home:address'))

        try:
            invoices = Invoices.objects.get(key=request.user)  # 发票信息
        except Invoices.DoesNotExist:
            invoices = None
            pass

        uns = Unseal(request, address=add, paymethod=self.paymethod, invoices=invoices, invoicess=self.invoicess)
        if not uns.getOrder(cart):
            return HttpCodeError.HttpResponseError(self.request, **{
                'page': '商品信息可能不完整',
                'code': 500,
                'title': '下单失败',
                'text': uns.get_error()
            }).HttpResponse_or_404()
        # cart.delete()

        # ('/home/success/?orderId={}'.format(uns.orderid))
        return redirect(reverse('shop:success', args=[uns.orderid]))

    pass


@method_decorator(decorators, name='dispatch')
class SuccessView(generic.TemplateView):
    template_name = 'defaule/shopping/success.html'

    response = False

    def dispatch(self, request, *args, **kwargs):
        self.orderId = kwargs['order_id']
        return super(SuccessView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        content = {}
        try:
            o = Order.objects.get(orderid=self.orderId, key=self.request.user)
            content = {
                'orderId': self.orderId,
                'money': o.total
            }
        except:
            self.response = True
            pass

        kwargs.update(content)
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        if not self.orderId:
            return HttpResponseRedirect('/')

        if self.response:
            context = {
                'error': '订单不存在, 页面将在3秒后跳转到首页',
                'state': 'back'  # back 表示跳转
            }

        return super(SuccessView, self).render_to_response(context, **response_kwargs)
