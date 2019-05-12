import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from account.models import User
from account.util.decorator import auth_admin
from home import models
from home.models import Contracts, Acceptance
from OAuth2.util.autograph import AutoRsaGraph
from lhwill import settings
from lhwill.util import log
from managestage.utli.wrapper import _POST, Web_Maintain
from managestage.utli.datetimenow import datetimenow

decorators = [Web_Maintain, login_required, auth_admin]


@method_decorator(decorators, name='dispatch')
class orderCartWare(View):
    '''后台订单详情'''
    template_name = 'defaule/admin/order/CartWareInfo.html'

    def get(self, request):
        id = request.GET.get('id')
        order = models.Order.objects.get(id=id)
        orderlist = models.Suborderlist.objects.get(key=order)
        goods = []
        for i in models.Goodslist.objects.filter(key=orderlist):
            goods.append({
                'goodsname': i.goodsname,
                'goodsid': i.goodsid,
                'spu': i.spu,
                'sku': i.sku,
                'model': i.model,
                'goodsbrandname': i.goodsbrandname,
                'qty': i.qty,
                'total': i.total,
                'price': i.price,
                'originalprice': i.originalprice,
                'imgurl': i.get_image_url(),
                'taoc': i.taoc,
                'goodsurl': i.goodsurl
            })

        content = {
            'order': order,
            'goods': goods
        }

        return render(request, self.template_name, content)
        pass

    pass


def UserOrder(request):
    '''
    用户订单
    :param request:
    :return:
    '''
    ordtype = models.Order.objects.filter(ordtype=-1).exclude(state=-2)

    ordadd = models.Order.objects.filter(ordtype=0).exclude(state=-2)
    isgotuaddress = models.Order.objects.filter(isgotuaddress=True).exclude(state=-2)
    ordall = models.Order.objects.filter(Q(state=0) | Q(state=-2))

    content = {
        'ordall': ordall,
        'ordtype': ordtype,
        'ordadd': ordadd,
        'isgotuaddress': isgotuaddress
    }
    log.i(globals(), 'isgotuaddress', isgotuaddress)

    return render(request, 'defaule/admin/order/userorder.html', content)
    pass


'''确认订单发货状态'''


@_POST
@Web_Maintain
@auth_admin
def setOnOrder(request):
    '''
    确认订单发货状态
    :param request:
    :return:
    '''
    id = request.POST.get('id')

    try:
        o = models.Order.objects.get(id=id)
        if not o.isgotuaddress:
            o.ordtype = 0
            o.save()

            models.Logistics(
                username='系统',
                info='系统以确认订单，商品正在出库',
                time=datetimenow(),
                key=o
            ).save()
            log.i(globals(), '确认订单发货状态')
            pass

        if o.usercode:
            au = AutoRsaGraph(usercode=o.usercode, orderid=o.orderid)
            au.order_logistics()
        else:
            log.i(globals(), '非国采用户，跳过物流接口')

    except Exception as e:
        content = {
            'state': 'error',
            'error': ''.format(e.args),
            'code': '404'
        }
        return HttpResponse(json.dumps(content))

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


@_POST
@Web_Maintain
@auth_admin
def Approval(request):
    '''
    审核用户订单 - 取消订单 通过
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    stype = int(request.POST.get('type'))
    ord = models.Order.objects.get(id=id)

    if ord.isgotuaddress == True:

        if stype == 0:
            # 取消订单-通过
            log.i(globals(), '取消订单-通过')

            ord.state = 5
            ord.isgotuaddress = False

            if ord.ordispaid != 0 and ord.ordispaid != -1:
                # 作废验收单
                auht = AutoRsaGraph(usercode=ord.usercode, orderid=ord.orderid)
                auht.order_delete_on()  # 作废整个订单（生成验收单之后）
                pass
            elif ord.ordispaid == 0:
                # 取消验收单
                auht = AutoRsaGraph(usercode=ord.usercode, orderid=ord.orderid)
                auht.order_delete()  # 取消整个订单（生成验收单之前）
            else:
                log.i(globals(), '取消订单-失败')
                pass
            log.i(globals(), '取消订单-操作成功')
        else:
            # 取消订单-不通过
            log.i(globals(), '取消订单-不通过')
            ord.isgotuaddress = False
            pass

        ord.save()
        content = {
            'state': 'error',
            'code': '403',
            'error': '用户没有申请取消订单'
        }
        return HttpResponse(json.dumps(content))
        pass

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


@_POST
@Web_Maintain
@auth_admin
def setAddesOrder(request):
    '''
    待收货订单 确认收货
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    yancd = 0
    try:
        o = models.Order.objects.get(id=id)
        if o.isgotuaddress != True:
            o.ordtype = 1
            o.state = 0
            yancd = o.ispaid
            o.save()
            models.Logistics(
                username='系统',
                info='您的订单已签收。感谢您在未来办公网购物，欢迎再次光临。',
                time=datetimenow(),
                key=o
            ).save()
            if o.usercode:
                au = AutoRsaGraph(usercode=o.usercode, orderid=o.orderid)
                au.order_logistics()
            pass

        # au.order_update()  # 申请生成验收单
        # au.order_knot() # 如果款结了，则申请生成验收单
        else:
            log.i(globals(), '非国采用户，跳过 推送物流信息接口，')

    except Exception as e:
        content = {
            'state': 'error',
            'error': ''.format(e.args),
            'code': '404'
        }
        return HttpResponse(json.dumps(content))

    content = {
        'state': 'success',
        'code': '200',
        'yancd': yancd
    }
    return HttpResponse(json.dumps(content))
    pass


'''申请生成验收单'''


@_POST
@Web_Maintain
@auth_admin
def getOrderAcceptanceCheck(request):
    '''
    申请生成验收单
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    o = models.Order.objects.get(id=id)

    if o.ordispaid == 0:
        au = AutoRsaGraph(usercode=o.usercode, orderid=o.orderid)
        au.order_update()  # 申请生成验收单[未结账]
        o.ordispaid = 1
        o.save()
    else:
        content = {
            'state': 'success',
            'code': '201'
        }
        log.i(globals(), content)
        return HttpResponse(json.dumps(content))
        pass

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))

    pass


'''验收单管理'''


@Web_Maintain
@auth_admin
def Acceptances(request):
    '''验收单管理'''
    accep = Acceptance.objects.filter(state=0)
    content = {
        'accep': accep
    }
    return render(request, 'defaule/admin/order/acceptances.html', content)
    pass


@_POST
@Web_Maintain
@auth_admin
def delAcceptances(request):
    '''
    作废整个订单（生成验收单之后）
    :param request:
    :return:
    '''
    id = request.POST.get('id')

    user = User.objects.get(username=request.user.username)
    accep = Acceptance.objects.get(id=id)
    auht = AutoRsaGraph(usercode=accep.usercode, orderid=accep.orderid)
    auht.order_delete_on()  # 作废整个订单（生成验收单之后）
    accep.state = -1
    accep.save()
    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''更新支付信息 成功支付'''


@_POST
@Web_Maintain
@auth_admin
def setOrderIspaid(request):
    '''
    更新支付信息 成功支付
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    o = models.Order.objects.get(id=id)
    if o.isgotuaddress != True:
        au = AutoRsaGraph(usercode=o.usercode, orderid=o.orderid)
        au.order_PaymentCompletion()
        log.i(globals(), o.ispaid)
        o.ispaid = 1
        o.save()

    # au.order_knot()  # 如果数据库ispaid为1 则申请生成验收单

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


@Web_Maintain
@auth_admin
def ContractView(request):
    ordercontract = Contracts.objects.filter()
    content = {
        'ordercontract': ordercontract
    }
    return render(request, 'defaule/admin/order/contract.html', content)
    pass
