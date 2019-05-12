import json
from decimal import Decimal

from django.http import HttpResponse

from account.models import User
from lhwill.util import log
from shopping import models
from shopping.util import WareCartJson
from shopping.util.WareCartJson import cart
from shopping.views import Index

'''
购物车相关操作 API 请求接口

: 获取购物车商品 GET
: 增加数量 POST
: 减少数量 POST
: 批量删除 POST
: 单个删除 POST
'''


class CartToolp(Index):
    '''
    购物车相关操作
    '''

    def post(self, request):
        '''
        增加数量，减少数量，批量删除，单个删除
        :param request:
        :return:
        '''
        id = request.POST.get('id')
        stype = request.POST.get('type')
        self.data = []

        wcart = WareCartJson.cart(self.request)

        if stype == '-' or stype == '+':
            carts = models.Cart.objects.get(id=id)

            '''商品数量增加或减少'''

            if stype == '-':
                carts.numb -= 1
                pass

            if stype == '+':
                carts.numb += 1
                pass

            carts.money = carts.numb * carts.price
            carts.save()

            wcart.cancelCartTotal(carts)

            # 计算商品优惠率等信息，将其写入购物车商品信息
            wcart.setListRate(carts)

            ca = cart(request)
            self.data = ca.getPrice(raw=carts)
            pass

        if stype == 'del':
            list_id = str(id).split('&')
            try:
                for i in list_id:
                    ''' 
                    添加被删除商品ID到list 
                    : 用于前端Js删除商品DIV块
                    '''
                    ids = i.split('=')[1]
                    self.data.append(ids)
                    del_cart = models.Cart.objects.get(id=ids).delete()
                    wcart.setListRate(del_cart, request=request)
                    pass
            except:
                ''' 
                添加被删除商品ID到list 
                : 用于前端Js删除商品DIV块
                '''
                del_cart = models.Cart.objects.get(id=id).delete()
                wcart.setListRate(del_cart, request=request)
                self.data.append(id)
                pass
            pass

        try:
            content = {
                'state': 'success',
                'data': json.loads(json.dumps(self.data)),
                'code': 200
            }
        except:
            content = {
                'state': 'success',
                'data': self.data,
                'code': 200
            }

        log.i(globals(), json.dumps(content))
        return HttpResponse(json.dumps(content))
        pass

    def get(self, request, *args, **kwargs):
        data = self.get_context_data()

        context = {
            'data': data,
            'number': len(data['Cart']),
            'code': 200
        }
        return HttpResponse(json.dumps(context))

    pass
