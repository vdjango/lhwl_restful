from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, HttpResponsePermanentRedirect
from django.utils.decorators import method_decorator
from django.views import View

from account.models import User
from account.models import UserVipGroup
from account.util.decorator import auth_admin
from app import models
from home.models import Order

from lhwill.util.complete import MainTain
from lhwill.util.log import log
from managestage import models as Manmodels
from managestage.utli import HttpUrl
from managestage.utli import datetimenow
from managestage.utli.wrapper import _GET, Web_Maintain, _POST

logger = log(globals())


def index(request):
    contenet = {
        'username': 'Job'
    }
    return render(request, 'index.html')
    pass


decorators = [auth_admin]

from django.views import generic

@method_decorator(decorators, name='dispatch')
class UserView(generic.ListView):
    model = User
    paginate_by = 20

    context_object_name = 'context'
    template_name = 'defaule/admin/user/user.html'
    pass


def AdmUser(request, lens=1):
    '''
    用户-首页
    :return:
    '''
    Front, After = HttpUrl.UrlSection(int(lens), '/admin/user/')
    usermodel = User.objects.filter()[Front:After]
    usergroup = Group.objects.filter()
    vipgroup = UserVipGroup.objects.filter()
    tain = MainTain()
    maintain = tain.get_tain()
    logger.i('GROUP', usergroup)
    usersize = len(usermodel)
    content = {
        'usergroup': usergroup,
        'vipgroup': vipgroup,
        'userlist': usermodel,
        'usersize': usersize,
        'Front': Front,
        'After': After,
        'maintain': maintain
    }
    return render(request, 'defaule/admin/user/user.html', content)
    pass


def TIMEDATES():
    return datetimenow.datetimenow()


def USERNAME(request):
    return User.objects.get(username=request.user.username)


def WAREOBJECTSKEY(id):
    return models.WareApp.objects.filter(id=id)[0]


'''订单管理部分'''


class AdmOrder(View):
    '''订单管理部分'''

    def get(self, request):
        data = datetimenow.datetimenow()
        logger.i('index', '{}-{}-{}'.format(data.year, data.month, data.day))

        info = Order.objects.filter(
            createtime__gt='{}-{}-{}'.format(data.year, data.month, data.day),
        )  # 今日下单人数

        deal = Order.objects.filter(
            createtime__gt='{}-{}-{}'.format(data.year, data.month, data.day),
            state__in=[0, 3, 4]
        ).exclude(state__in=[1, 2, 5, -1, -2])  # 今日成交订单

        dealAll = Order.objects.filter(
            createtime__gt='{}-{}-{}'.format(int(data.year) - 1, data.month, data.day),
            # ispaid=1,
        ).exclude(state__in=[1, 2, 5, -1, -2])  # 今年成交总订单

        content = {
            'info': len(info),
            'deal': len(deal),
            'dealAll': len(dealAll)
        }

        return render(request, 'defaule/admin/order/index.html', content)
        pass

    def post(self):
        pass

    pass


class plate():
    '''
    后台所有功能板块
    '''

    '''全局'''

    @_GET
    @Web_Maintain
    @auth_admin
    def AdmComplete(request):
        '''
        全局-首页
        :return:
        '''
        system = Manmodels.systemSetup.objects.filter()
        maintain = Manmodels.maintain.objects.filter()

        try:
            setclassify = Manmodels.Setclassify.objects.filter()[:1].get()
        except:
            setclassify = None

        content = {
            'system': system,
            'maintain': maintain,
            'setclassify': setclassify
        }
        return render(request, 'defaule/admin/complete/index.html', content)
        pass

    '''商品'''

    @_GET
    @Web_Maintain
    @auth_admin
    def AdmCommodity(request):
        '''
        商品
        :param lend:
        :return:
        '''
        page = request.GET.get('page')

        WareAppPrefix = models.WareAppPrefix.objects.filter(classifythere_key__isnull=False, classify_key__isnull=False)
        app_isnull = models.WareApp.objects.filter(image__isnull=True, release=True)
        wareAppReleaseFalseLen = len(WareAppPrefix.filter(wareApp_key__release=False))
        wareApp = WareAppPrefix.filter(wareApp_key__release=True)

        max_page = 12
        paginator = Paginator(wareApp, max_page)

        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:  # 页码不是整数
            current_page = paginator.page(1)
        except EmptyPage:  # 页码空或者NUll
            current_page = paginator.page(paginator.num_pages)

        classify_list = current_page.object_list

        temp = models.MiddleTop.objects.filter()

        content = {
            'wareAppReleaseFalseLen': wareAppReleaseFalseLen,
            'temp': temp,
            'classify': classify_list,
            'page': current_page,
            'max_page': paginator.count,
            'app_isnull': app_isnull
        }

        return render(request, 'defaule/admin/commodity/index.html', content)
        # return render(request, 'defaule/admin/applist/applist.html', content)
        pass


    '''板块'''

    @_GET
    @Web_Maintain
    @auth_admin
    def AdmSector(request):
        '''
        商品-板块管理
        :return:
        '''
        MiddleTop = []
        for i in models.MiddleTop.objects.filter():
            MiddleTop.append({
                'id': i.id,
                'name': i.name,
                'temp': i.temp,
                'number': i.number,
                'time_now': i.time_now,
                'commodity': models.commodity.objects.filter(key=i)
            })
            pass
        content = {
            'middleTop': MiddleTop
        }
        return render(request, 'defaule/admin/sector/sector.html', content)
        pass

    '''添加Page页面'''

    @_GET
    @Web_Maintain
    @auth_admin
    def Page(request):
        '''
        添加Page页面
        :return:
        '''
        return render(request, 'defaule/admin/page/index.html')
        pass




