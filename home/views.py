import json
# from _pydecimal import Decimal
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import TemplateView
from django_pdfkit import PDFView

from OAuth2.util import capitalizationPrice
from OAuth2.util.autograph import AutoRsaGraph
from account.models import UserInfo, User, UnitInfo
from api.serializers import SerializersMethodl
from app import models
from app.models import parameter
from home.forms.addAddress_form import Form_Address
from home.models import Order, Suborderlist, Goodslist, Address, Discount, Logistics, Invoices, Contracts, Gusid, \
    Acceptance
from lhwill import settings
from lhwill.util.log import log
from lhwill.views import error_
from managestage.utli.datetimenow import datetimenow, _order_num
from managestage.utli.wrapper import _POST, _GET

logger = log(globals())




decorators = [login_required]


@method_decorator(decorators, name='dispatch')
class Index(generic.ListView):
    template_name = 'defaule/home/index.html'

    context_object_name = 'context'

    queryset = Order.objects.filter().exclude(state='-2')

    model = Order

    paginate_by = 20

    def get_queryset(self):
        queryset = self.queryset.filter(key=self.request.user)

        queryset = SerializersMethodl.OrderSerializer(data=queryset, many=True)
        queryset.is_valid()

        return queryset.data
    pass





@login_required
def personal(request):
    return render(request, 'defaule/home/personal.html')
    pass


@login_required
def Invoice(request):
    '''
    添加或创建发票
    '''
    stype = request.POST.get('actionid')  # '普通发票 1/2'
    users = User.objects.get(username=request.user.username)

    if stype == '1':
        content = request.POST.get('content')  # '商品明细 0/1'
        taxpayer = request.POST.get('taxpayer')  # '纳税人识别号'
        phone = request.POST.get('phone')  # '收票人手机'
        email = request.POST.get('email')  # '收票人邮箱'
        head = request.POST.get('head')  # '抬头'
        logger.i('1', head)
        try:
            inv = Invoices.objects.get(key=users)
            inv.stype = stype
            inv.content = content
            inv.taxpayer = taxpayer
            inv.phone = phone
            inv.email = email
            inv.head = head
            inv.save()
            logger.i('普通发票， 修改信息')
        except:
            Invoices(
                stype=stype,
                content=content,
                taxpayer=taxpayer,
                phone=phone,
                email=email,
                head=head,
                key=users
            ).save()
            logger.i('普通发票， 创建信息')

    if stype == '2':
        taxpayer = request.POST.get('taxpayer')  # '纳税人识别号'
        phone = request.POST.get('phone')  # '收票人手机'
        email = request.POST.get('email')  # '收票人邮箱

        unitName = request.POST.get('unitName')  # '单位名称'
        registeredAddress = request.POST.get('registeredAddress')  # '注册地址'
        registeredTelephone = request.POST.get('registeredTelephone')  # '注册电话'
        accountOpening = request.POST.get('accountOpening')  # '开户银行'
        account = request.POST.get('account')  # '银行账户'

        log.i(registeredTelephone, account)
        try:
            inv = Invoices.objects.get(key=users)
            inv.stype = stype
            inv.taxpayer = taxpayer
            inv.unitName = unitName
            inv.registeredAddress = registeredAddress
            inv.registeredTelephone = registeredTelephone
            inv.accountOpening = accountOpening
            inv.account = account
            inv.save()
        except:
            Invoices(
                stype=stype,
                taxpayer=taxpayer,
                unitName=unitName,
                registeredAddress=registeredAddress,
                registeredTelephone=registeredTelephone,
                accountOpening=accountOpening,
                account=account,
                key=users
            ).save()

    content = {
        'code': 200,
        'state': 'success'
    }

    return HttpResponse(json.dumps(content))
    pass


'''用户电子合同View'''


@login_required
def Contract(request):
    '''
    用户电子合同View
    :param request:
    :return:
    '''
    user = User.objects.get(username=request.user.username)
    orde = Order.objects.filter(key=user).exclude(state=-2)
    ors = Contracts.objects.filter(key=user)  # 订单完成状态
    logger.i(ors)
    content = {
        'ordercontract': ors,
        'orde': orde
    }
    return render(request, 'defaule/home/contract.html', content)
    pass


'''生成合同页View，打印合同等'''

@method_decorator(decorators, name='dispatch')
class PDFOrderContract(PDFView):
    template_name = 'defaule/home/pdf.html'
    filename = '领航未来_采购协议供货合同'
    inline = True



    pdfkit_options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        'title': '领航未来_采购协议供货合同'
    }



    def get_context_data(self, **kwargs):
        try:
            con = Contracts.objects.get(id=self.kwargs['id'])
        except Contracts.DoesNotExist:
            con = Contracts.objects.get(orderid=self.kwargs['id'])
            pass

        so = Suborderlist.objects.get(key=con.key_order)
        gso = Goodslist.objects.filter(key=so)
        context = {
            'Contracts': con,
            'gso': gso,
            'site_url': settings.HTTP_HOST
        }

        kwargs.update(context)
        return kwargs



# @login_required
def OrderContract(request, id):
    '''
    生成合同页View，打印合同等
    :param request:
    :return:
    '''

    try:
        con = Contracts.objects.get(id=id)
        so = Suborderlist.objects.get(key=con.key_order)
        gso = Goodslist.objects.filter(key=so)
    except:
        if request.user.is_staff:
            con = Contracts.objects.get(id=id)
            so = Suborderlist.objects.get(key=con.key_order)
            gso = Goodslist.objects.filter(key=so)
            content = {
                'Contracts': con,
                'gso': gso
            }

            return render(request, 'defaule/home/downloadcontract1.html', content)
        return error_(request, code=404, title='合同未申请', content='您的合同未申请或者合同不存在')

    content = {
        'Contracts': con,
        'gso': gso
    }

    return render(request, 'defaule/home/downloadcontract1.html', content)
    pass


'''创建用户合同数据'''


@login_required
def getpulContract(request):
    '''
    创建用户合同数据
    :param request:
    :return:
    '''
    id = request.POST.get('id')

    user = models.User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(key=user)
    uninfo = UnitInfo.objects.get(key=user)
    o = Order.objects.get(id=id)
    # so = Suborderlist.objects.get(key=o)
    # gso = Goodslist.objects.get(key=so)

    try:
        acceptance = Acceptance.objects.get(orderid=o.orderid).ysd_code
        if not acceptance:
            acceptance = '-'
    except Acceptance.DoesNotExist:
        acceptance = '-'

    # addess = Address.objects.get()

    if o.area and o.city and o.deliveryaddress:
        adder = '{} {} {} {}'.format(o.province, o.city, o.area, o.deliveryaddress)
    else:
        adder = '{} {} {}'.format(o.province, o.city, o.deliveryaddress)
        pass

    logger.i('adder', adder)

    createtime = o.createtime.astimezone()
    logger.i('订单起草时间', createtime)

    timelist = str(createtime).split(' ')

    tlist = timelist[0]  # 2018-06-25
    tlist_all = tlist.split('-')  # ['2018', '06', '25']

    tlist_0 = tlist_all[0]  # 2018
    tlist_1 = tlist_all[1]  # 06
    tlist_2 = tlist_all[2]  # 25

    tlist_2 = int(tlist_2) + 2

    newtime = '{}年{}月{}日'.format(tlist_0, tlist_1, str(tlist_2))
    logger.i('订单送货时间+2天', newtime)

    Contracts(
        Acceptance=acceptance,  # 验收单编号 Done
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
        key=user
    ).save()

    o.ordContract = -1
    o.save()
    content = {
        'code': 200,
        'state': 'success'
    }

    return HttpResponse(json.dumps(content))
    pass


'''合同转正'''


def setContract(request):
    '''
    合同转正
    :param request:
    :return:
    '''
    id = request.POST.get('id')

    con = Contracts.objects.get(id=id)
    con.stype = 0
    con.save()
    content = {
        'code': 200,
        'state': 'success'
    }

    return HttpResponse(json.dumps(content))
    pass


'''返回物流信息'''


@_POST
@login_required
def getlogistics(request):
    '''
    返回物流信息
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    Logisticss = []
    orid = Order.objects.get(id=id)
    for logis in Logistics.objects.filter(key=orid):
        Logisticss.append({
            'info': logis.info,
            'username': logis.username,
            'time': str(logis.time.astimezone()).split('+')[0]
        })
        pass

    content = {
        'code': 200,
        'data': Logisticss,
        'state': 'success'
    }

    return HttpResponse(json.dumps(content))
    pass


'''View收货地址/添加收货地址'''


@login_required
def address(request):
    '''
    View收货地址/添加收货地址
    :param request:
    :return:
    '''
    if request.method == 'GET':
        users = models.User.objects.get(username=request.user.username)
        add = Address.objects.filter(key=users)
        content = {
            'address': add,
        }
        return render(request, 'defaule/home/address.html', content)
        pass

    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        consigneeName = request.POST.get('consigneeName')
        province = request.POST.get('province')
        city = request.POST.get('city')
        area = request.POST.get('area')
        consigneeAddress = request.POST.get('consigneeAddress')
        consigneeMobile = request.POST.get('consigneeMobile')
        email = request.POST.get('email')
        users = models.User.objects.get(username=request.user.username)

        formAdd = Form_Address(request.POST)
        if formAdd.is_valid():
            if edit_id:
                add = Address.objects.get(key=users, id=edit_id)
                add.consigneeName = consigneeName
                add.province = province
                add.city = city
                add.area = area
                add.consigneeAddress = consigneeAddress
                add.consigneeMobile = consigneeMobile
                add.email = email
                add.save()
                pass
            else:
                Address(
                    consigneeName=consigneeName,
                    province=province,
                    city=city,
                    area=area,
                    consigneeAddress=consigneeAddress,
                    consigneeMobile=consigneeMobile,
                    email=email,
                    key=users
                ).save()
        else:
            users = models.User.objects.get(username=request.user.username)
            add = Address.objects.filter(key=users)
            content = {
                'address': add,
                'error': '地址信息不完整'
            }
            return render(request, 'defaule/home/address.html', content)

        content = {
            'consigneeName': consigneeName,
            'province': province,
            'city': city,
            'area': area,
            'consigneeAddress': consigneeAddress,
            'consigneeMobile': consigneeMobile,
            'email': email
        }

        return redirect(reverse('home:address'))
        pass
    pass


@_POST
@login_required
def addAddress(request):
    '''
    添加收货地址
    :param request:
    :return:
    '''
    edit_id = request.POST.get('edit_id')
    consigneeName = request.POST.get('consigneeName')
    province = request.POST.get('province')
    city = request.POST.get('city')
    area = request.POST.get('area')
    consigneeAddress = request.POST.get('consigneeAddress')
    consigneeMobile = request.POST.get('consigneeMobile')
    email = request.POST.get('email')
    users = models.User.objects.get(username=request.user.username)

    formAdd = Form_Address(request.POST)
    if formAdd.is_valid():
        if edit_id:
            add = Address.objects.get(key=users, id=edit_id)
            add.consigneeName = consigneeName
            add.province = province
            add.city = city
            add.area = area
            add.consigneeAddress = consigneeAddress
            add.consigneeMobile = consigneeMobile
            add.email = email
            add.save()
            pass
        else:
            Address(
                consigneeName=consigneeName,
                province=province,
                city=city,
                area=area,
                consigneeAddress=consigneeAddress,
                consigneeMobile=consigneeMobile,
                email=email,
                key=users
            ).save()
    else:
        content = {
            'code': 403,
            'state': 'error',
            'error': '有字段未填写',
            'data': formAdd.errors
        }

        return HttpResponse(json.dumps(content))

    content = {
        'code': 200,
        'state': 'success'
    }

    return HttpResponse(json.dumps(content))


'''设置默认地址'''


@login_required
def setaddress(request):
    '''
    设置默认地址
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    username = request.user.username
    U = User.objects.get(username=username)

    Address.objects.filter(key=U, defaule=True).update(defaule=False)

    Address.objects.filter(id=id).update(defaule=True)

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))


@login_required
def getAddress(request):
    '''
    Ajax获取收货地址信息
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    data = []

    i = Address.objects.get(id=id)
    data.append({
        'defaule': i.defaule,
        'consigneeName': i.consigneeName,
        'province': i.province,
        'city': i.city,
        'area': i.area,
        'consigneeAddress': i.consigneeAddress,
        'consigneeMobile': i.consigneeMobile,
        'email': i.email
    })

    content = {
        'state': 'success',
        'data': data,
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


@login_required
def deladdress(request):
    '''
    删除收货地址
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    users = models.User.objects.get(username=request.user.username)
    Address.objects.filter(key=users, id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''下单结算页 [填写并核对订单信息]'''


@login_required
def Settlement(request):
    '''
    下单结算页 [填写并核对订单信息]
    只适合单种商品下单，多种商品下单无法计算价格
    :param request:
    :return:
    '''

    if request.method == 'GET':
        wareid = request.GET.get('id')
        purchase = request.GET.get('purchase')
        duration = request.GET.get('duration')
        number = request.GET.get('number')

        print('purchase', purchase)

        username = request.user.username
        users = models.User.objects.get(username=username)

        add = Address.objects.filter(key=users, defaule=True)
        if not add:
            add = Address.objects.filter(key=users)
            pass

        if add:
            add = add[0]

        ware = models.WareApp.objects.filter(id=wareid)

        lease_or = models.Lease.objects.get(ware_key=ware[0], id=purchase, select=1)  # select 1 购买/select 0 租赁
        money = float(lease_or.money)  # '总金额'
        logger.i('总金额', money)

        defaule = False  # 是否是国采登录用户
        defaule_money = 0  # 国采用户打折

        try:
            U = models.User.objects.get(username=request.user.username)
            if U.usercode:
                defaule = True
                defaule_money = 0
                pass
        except:
            defaule = False
            pass

        try:
            classify = models.WareAppPrefix.objects.get(wareApp_key=ware)
        except:
            classify = None

        dismoney = 0
        number_money = float(money) * float(number)
        if classify and defaule:
            logger.i('优惠率', classify, defaule)
            theress = classify.classifythere_key
            discon = Discount.objects.get(classif_there=theress)
            if int(number_money) <= 100000:
                # a1
                dismoney = discon.a1
                defaule_money = (100 - float(dismoney)) / 100 * float(money)

                logger.i('int(number_money) <= 100000', defaule_money, money)
                pass

            elif 100000 < int(number_money) and int(number_money) <= 300000:
                # a2
                dismoney = discon.a2
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('100000 < int(number_money) and int(number_money) <= 300000', defaule_money)
                pass

            elif 300000 < int(number_money) and int(number_money) <= 600000:
                # a3
                dismoney = discon.a3
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('300000 < int(number_money) and int(number_money) <= 600000', defaule_money)
                pass

            elif 600000 < int(number_money) and int(number_money) < 1000000:
                # a4
                dismoney = discon.a4
                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('600000 < int(number_money) and int(number_money) <= 1000000', defaule_money)

            elif float(number_money) >= 1000000:
                return error_(request, code=403, title='订单错误', page='Order error', content='单笔订单不可大于等于100万人民币')
                pass

        total = float(number) * float(money)
        total_defaule_money = float(number) * float(defaule_money)

        money = Decimal(money).quantize(Decimal('0.00'))
        total = Decimal(total).quantize(Decimal('0.00'))
        total_defaule_money = Decimal(total_defaule_money).quantize(Decimal('0.00'))
        defaule_money = Decimal(defaule_money).quantize(Decimal('0.00'))

        logger.i('单价', money)
        logger.i('单价优惠', defaule_money)
        logger.i('总优惠', total_defaule_money)

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
        content = {
            'moneytable': moneytable,
            'inv': inv,
            'address': add,
            'number': number,
            'ware': ware,
            'total': total,
            'dismoney': dismoney,
            'defaule': defaule,
            'money': money,
            'defaule_money': defaule_money,
            'total_defaule_money': total_defaule_money,
            'wareid': wareid,
            'select': 1,
            'purchase': purchase,
            'duration': duration,
        }
        return render(request, 'defaule/home/settlement.html', content)

    if request.method == 'POST':
        username = request.user.username
        wareid = request.POST.get('id')
        purchase = request.POST.get('purchase')
        duration = request.POST.get('duration')
        number = request.POST.get('number')

        invoices = request.POST.get('invoices')

        '''
        创建订单
        :param request:
        :return:
        '''
        address = request.POST.get('address')
        remark = request.POST.get('remark')  # 订单备注
        paymethod = request.POST.get('paymethod')  # '支付方式'

        logger.i('wareid', wareid)
        ware = models.WareApp.objects.get(id=wareid)
        logger.i('WareApp', ware)

        user = models.User.objects.get(username=username)

        lease_or = models.Lease.objects.get(ware_key=ware, id=purchase, select=1)  # select 1 购买/select 0 租赁
        money = float(lease_or.money)  # '总金额'
        duration_or = None

        # if select == '0':
        #     lease_or = models.Lease.objects.get(ware_key=ware, id=purchase, select=select)  # select 1 购买/select 0 租赁
        #     duration_or = models.Duration.objects.get(ware_key=ware, id=duration)  # 租赁配置 - 分类信息[租赁时间]
        #     money = float(lease_or.money) + float(duration_or.money)  # '总金额'
        # elif select == '1':
        #     lease_or = models.Lease.objects.get(ware_key=ware, id=purchase, select=select)  # select 1 购买/select 0 租赁
        #     money = float(lease_or.money)  # '总金额'
        #     duration_or = None
        # else:
        #     lease_or, duration_or = None, None
        #     money = -1
        #     pass

        # images = models.images.objects.filter(key=ware)[:1].get().image

        add = Address.objects.filter(id=address, key=user)

        if add:
            province = add[0].province
            city = add[0].city
            area = add[0].area
            deliveryaddress = '{}'.format(add[0].consigneeAddress)
            linkman = add[0].consigneeName  # userinfo.name  # 购买人姓名
            linkmobile = add[0].consigneeMobile  # userinfo.phone  # 购买人联系方式
        else:
            return redirect(reverse('home:address'))

        ''''''
        defaule = False  # 是否是国采登录用户
        defaule_money = 0  # 国采用户打折

        orderid = _order_num(package_id=ware.id, user_id=user.id)  # '创建订单号'
        suborderid = orderid  # 子订单号

        try:
            U = models.User.objects.get(username=request.user.username)
            if U.usercode:
                defaule = True
                defaule_money = 0
                pass
        except:
            defaule = False
            pass

        try:
            classify = models.WareAppPrefix.objects.get(wareApp_key=ware)
        except:
            classify = None

        dismoney = 0
        number_money = float(money) * float(number)
        if classify and defaule:
            theress = classify.classifythere_key
            discon = Discount.objects.get(classif_there=theress)
            if float(number_money) <= 100000:
                # a1
                dismoney = discon.a1
                defaule_money = (100 - float(discon.a1)) / 100 * float(money)
                logger.i('float(number_money) <= 100000', defaule_money)

                pass
            elif 100000 < float(number_money) and float(number_money) <= 300000:
                # a2
                dismoney = discon.a2
                defaule_money = (100 - float(discon.a2)) / 100 * float(money)
                logger.i('100000 < float(number_money) and float(number_money) <= 300000', defaule_money)
                pass

            elif 300000 < float(number_money) and float(number_money) <= 600000:
                # a3
                dismoney = discon.a3
                defaule_money = (100 - float(discon.a3)) / 100 * float(money)
                logger.i('300000 < float(number_money) and float(number_money) <= 600000', defaule_money)
                pass

            elif 600000 < float(number_money) and float(number_money) <= 1000000:
                # a4
                dismoney = discon.a4
                defaule_money = (100 - float(discon.a4)) / 100 * float(money)
                logger.i('600000 < float(number_money) and float(number_money) < 1000000', defaule_money)
            elif float(number_money) >= 1000000:
                return error_(request, code=403, title='订单错误', page='Order error', content='单笔订单不可大于等于100万人民币')
                pass

            total_defaule_money = float(number) * float(defaule_money)

            ''''''
            total = float(total_defaule_money)  # 总订单价钱
            Subtotal = total  # 子订单总价 #############
            price = defaule_money  # 商品单价
            originalprice = money  # 订单原价
            ''''''

            logger.i('订单原价： ', money)
            logger.i('优惠率', dismoney)
            logger.i('商品单价优惠： ', defaule_money)
            logger.i('总订单优惠： ', total_defaule_money)
        else:
            total = float(number) * float(money)  # 总订单价钱

            ''''''
            Subtotal = total  # 子订单总价 #############
            price = float(money)  # 商品单价
            originalprice = float(money)  # 订单原价
            ''''''

        money = Decimal(money).quantize(Decimal('0.00'))
        total = Decimal(total).quantize(Decimal('0.00'))
        Subtotal = Decimal(Subtotal).quantize(Decimal('0.00'))
        price = Decimal(price).quantize(Decimal('0.00'))
        originalprice = Decimal(originalprice).quantize(Decimal('0.00'))

        logger.i('订单原价： ', money)
        logger.i('商品单价： ', money)
        logger.i('总订单价： ', total)

        spu = ware.name  # '细化到商品'

        goodsclassguid = goodsclassname = goodsbrandname = sku = model = ''

        if defaule:
            try:
                guid = Gusid.objects.get(key=classify.classifythere_key)
            except:
                return error_(request, content='商品目录ID不完整,或未分类', code=403)

            try:
                per = parameter.objects.get(key=ware)

                sku = '{} {} {}'.format(per.model, per.productType, per.colorType)  # '细化到规格、型号'
                model = '{}'.format(per.model)  # '商品型号、规格'

                goodsbrandname = per.brands  # '品牌名称'
                goodsclassguid = guid.guid  # '商品目录ID 枚举值对照表'
                goodsclassname = guid.name  # '商品类别名'

            except:
                return error_(request, content='商品参数不完整，最少具备的参数： 产品型号， 产品类型， 颜色类型')

        usercode = user.usercode
        url = '/app/details/{}/'.format(wareid)

        logger.i('商品目录ID', goodsclassguid)
        logger.i('商品类别名', goodsclassname)
        logger.i('品牌名称', goodsbrandname)
        try:
            inv = Invoices.objects.get(key=user)
        except:
            inv = None

        if usercode:
            o = Order(
                name='{}（{}）'.format(ware.name, lease_or.name),
                orderid=orderid,
                paymethod=paymethod,
                total=total,
                money=total,
                number=number,
                province=province,
                city=city,
                area=area,
                invoice=invoices,
                linkman=linkman,
                linkmobile=linkmobile,
                deliveryaddress=deliveryaddress,
                remark=remark,
                usercode=usercode,
                createtime=datetimenow(),
                images=ware.image,
                url=url,
                key_inv=inv,
                key=user
            )
        else:
            o = Order(
                name='{}（{}）'.format(ware.name, lease_or.name),
                orderid=orderid,
                paymethod=paymethod,
                total=total,
                number=number,
                province=province,
                city=city,
                area=area,
                invoice=invoices,
                linkman=linkman,
                linkmobile=linkmobile,
                deliveryaddress=deliveryaddress,
                remark=remark,
                createtime=datetimenow(),
                images=ware.image,
                url=url,
                key_inv=inv,
                key=user
            )
        o.save()
        s = Suborderlist(
            suborderid=suborderid,
            url=url,
            total=Subtotal,
            key=o
        )
        s.save()
        Goodslist(
            goodsname='{}（{}）'.format(ware.name, lease_or.name),
            goodsid=ware.id,
            spu=spu,
            sku=sku,
            model=model,
            goodsclassguid=goodsclassguid,
            goodsclassname=goodsclassname,
            goodsbrandname=goodsbrandname,
            qty=number,
            total=total,
            price=price,
            originalprice=originalprice,
            imgurl=ware.image,
            goodsurl=url,
            key=s
        ).save()

        Logistics(
            info='您提交了订单，请等待卖家系统确认',
            time=datetimenow(),
            username='系统',
            key=o
        ).save()

        o.lease_or = lease_or

        if paymethod == '1' or paymethod == '2' or paymethod == '3' or paymethod == '4' or paymethod == '9':
            o.state = 2
            pass
        o.save()

        if usercode:
            auto = AutoRsaGraph(usercode=usercode, orderid=orderid)
            order_create = auto.order_create()
            order_logistics = auto.order_logistics()

            logger.i('央采 创建订单', order_create)
            logger.i('央采 物流推送接口', order_logistics)

        else:
            logger.i('没有usercode')
            pass

        return HttpResponseRedirect('/home/success/?orderId={}'.format(orderid))
        pass
    pass


@login_required
def Acceptances(request):
    '''用户验收单View - 待完成'''
    return render(request, 'defaule/admin/order/acceptances.html')
    pass


@_POST
@login_required
def generateOrder_delete(request):
    '''
    删除订单
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    o = Order.objects.get(id=id)
    o.state = -2
    o.save()

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))

    pass


@_POST
@login_required
def delorider(request):
    '''
    订单提交审核 取消订单
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    der = Order.objects.get(orderid=id)
    der.isgotuaddress = True
    der.save()
    logger.i('订单以提交审核， 取消订单')

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass
