import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition
from django_pdfkit import PDFView
# from haystack.views import SearchView
from reportlab.pdfgen import canvas

from account.util.email import login_mail
from app import models
from app.util.classify import getClassify
from app.util.condition_Etag import latest_entry
from app.util.screeningWasher import modelsObjectsfilter
from home.models import Discount, Contracts, Goodslist, Suborderlist
from lhwill import settings
from lhwill.util.log import log
from lhwill.view import AppGenric
from lhwill.view.HttpCodeError import HttpResponseError
from lhwill.views import error_
from managestage.models import SearchStatistics
from managestage.utli.wrapper import Web_Maintain, _GET, get_ip

logger = log(globals())


# PDFView
class PDF(PDFView):
    template_name = 'defaule/home/pdf.html'
    # template_name = 'defaule/home/downloadcontract.html'
    filename = '领航未来_采购协议供货合同'
    inline = True
    html = True

    pdfkit_options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': "UTF-8"
    }

    def get_context_data(self, **kwargs):
        con = Contracts.objects.get(id=9)
        so = Suborderlist.objects.get(key=con.key_order)
        gso = Goodslist.objects.filter(key=so)
        context = {
            'Contracts': con,
            'gso': gso,
            'site_url': settings.HTTP_HOST
        }
        kwargs.update(context)
        return kwargs

    def get(self, request, *args, **kwargs):
        """
        Return a HTTPResponse either of a PDF file or HTML.

        :rtype: HttpResponse
        """
        if self.html:
            content = self.render_html(*args, **kwargs)
            return HttpResponse(content)

        css = '{}/static/css/bootstrap4.min.css'.format(settings.STATIC_ROOT_PDF)
        kwargs.update({'css': css})

        return super(PDF, self).get(request, *args, **kwargs)

    pass


def PDFS(request):
    response = HttpResponse(content_type='application/pdf')

    p = canvas.Canvas(response)
    p.drawString(25, 100, "Hello world.")
    p.showPage()
    p.save()

    return response


def r(request):
    for i in models.WareApp.objects.filter():
        i.save()
    return HttpResponse('')
    pass


@get_ip
def setPlus(request):
    from decimal import Decimal
    '''
    商品价格计算
    :param request:
    :return:
    '''
    therid = request.POST.get('therid')
    v1 = request.POST.get('v1')
    v2 = request.POST.get('v2')

    money = float(v1) + float(v2)
    dismoney = 0
    defaule_money = None

    try:
        if models.User.objects.get(username=request.user.username).usercode:
            logger.i('国采用户价格', therid)
            defaule_money = 0

            theress = models.Classification_There.objects.get(id=therid)
            discon = Discount.objects.get(classif_there=theress)
            logger.i('三级分类获取，优惠率获取')

            if float(money) <= 100000:
                # a1
                if discon:
                    dismoney = discon.a1
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('float(money) <= 100000', defaule_money)

                pass
            elif 100000 < float(money) and float(money) <= 300000:
                # a2
                if discon:
                    dismoney = discon.a2
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('100000 < float(money) and float(money) <= 300000', defaule_money)
                pass

            elif 300000 < float(money) and float(money) <= 600000:
                # a3
                if discon:
                    dismoney = discon.a3
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('300000 < float(money) and float(money) <= 600000', defaule_money)
                pass

            elif 600000 < float(money) and float(money) <= 1000000:
                # a4
                if discon:
                    dismoney = discon.a4
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('600000 < float(money) and float(money) <= 1000000', defaule_money)
                pass
            defaule_money = Decimal(defaule_money).quantize(Decimal('0.00'))
    except:

        logger.i('普通用户价格', therid)
        defaule_money = None

        theress = models.Classification_There.objects.get(id=therid)
        discon = Discount.objects.get(classif_there=theress)
        logger.i('三级分类获取，优惠率获取')

    # defaule_money = Decimal(defaule_money).quantize(Decimal('0.00'))

    moneys = {
        'price': str(Decimal(money).quantize(Decimal('0.00'))),  # '单价'
        'defaule_money': str(defaule_money),  # 折扣后的价钱
        'dismoney': str(dismoney)
    }

    logger.i(moneys)

    content = {
        'state': 'success',
        'data': moneys,
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


@csrf_exempt
@get_ip
@_GET
@Web_Maintain
@login_mail
def index(request):
    Recom = []
    mid = []
    for line in models.MiddleTop.objects.filter():
        '''首页板块'''
        list_dity = []
        number = int(line.number) * 5
        for i in models.commodity.objects.filter(key=line.id, ware_key__release=True)[:number]:
            list_dity.append({
                'id': i.id,
                'wareid': i.ware_key.id,
                'name': i.title,
                'money': i.money,
                'image': '{}{}'.format(settings.HTTP_HOST, i.image),
                'url': i.url,
                'time_now': i.time_now,
                'ware_key': i.ware_key
            })

        mid.append({
            'id': line.id,
            'title': line.name,
            'temp': line.temp,
            'time_add': line.time_add,
            'time_now': line.time_now,
            'mid_search': line.mid_search.filter(),
            'commodity': list_dity
        })

        pass

    context_hread = {
        'statistics': SearchStatistics.objects.filter()[:10],
        'Carousels': models.Carousel.objects.filter(),
        'newProduct': models.WareApp.objects.filter(release=True).order_by('-time_add')[:20]  # 新品上线
    }

    context = {

        'Recommend': Recom,
        'MiddleTop': mid,

    }

    context.update(context_hread)
    context.update(getClassify())

    return render(request, 'defaule/index.html', context)


@Web_Maintain
@login_mail
def Contrast(request):
    '''
    商品对比
    :param request:
    :return:
    '''
    if request.method == 'GET':

        name = request.GET.get('ware_id')

        ware_list = []

        for i in str(name).split(','):
            ware = models.WareApp.objects.get(id=i)
            image = models.images.objects.filter(key=ware)[:1].get().image

            try:
                pers = models.parameter.objects.get(key=ware)
                brands = pers.brands
                model = pers.model
                colorType = pers.colorType
            except:
                brands = '暂无'
                model = '暂无'
                colorType = '暂无'

            ware_list.append({
                'name': ware.name,
                'money': ware.money,
                'image': image,

                'brands': brands,
                'model': model,
                'colorType': colorType
            })

        content = {
            'warelist': ware_list
        }
        logger.i(content)
        return render(request, 'defaule/app/contrast.html', content)
        pass


def sale(request):
    return HttpResponse('退货/保修')
    pass


def personal(request):
    return HttpResponse('退货/保修')
    pass


# 废弃
class commodity():
    @_GET
    @Web_Maintain
    @condition(last_modified_func=latest_entry)
    # @never_cache
    def details(request, tid):
        '''
        商品详情页面
        :param tid:
        :return:
        '''
        Dic = models.WareParProfix.Dis_CHOICES

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
            wareapp = models.WareApp.objects.filter(id=tid)[:1].get()
        except:
            return error_(request, code=404, error={})
            pass
        image = models.images.objects.filter(key=wareapp.id)
        parameter = models.parameter.objects.filter(key=wareapp)

        try:
            classify = models.WareAppPrefix.objects.get(wareApp_key=wareapp)
        except:
            classify = None

        if classify:
            there = classify
        else:
            there = None
        pare = []
        Wpf = None
        if there:
            there = there.classifythere_key
            try:
                Wpf = models.WareParProfix.objects.get(key=there)
            except:
                Wpf = None
                pass

            ''' 商品规格 '''
            if Wpf:
                for i in Wpf.filter_name:
                    ks = parameter.values(i[0])
                    if ks:
                        ks = ks[0]
                        ks = ks[i[0]]
                    else:
                        ks = '无'

                    logger.i('商品规格', i[0])

                    pare.append({
                        'v': Dic[i[0]],
                        'k': ks
                    })

            else:
                Wpf = None
                logger.i('APP', Wpf)
                pass
        else:
            there = None
            pass

        money = 0

        # 租赁Models 配置
        Lease = []
        for q in models.Lease.objects.filter(ware_key=wareapp, select=0):
            Lease.append({
                'id': q.id,
                'name': q.name,
                'money': q.money,
                'defaule': q.defaule,
            })
            pass

        try:
            Lease_Duration_ = models.Duration.objects.get(defaule=True, ware_key=wareapp)
        except:
            Lease_Duration_ = None

        # 购买Models 配置
        purchase = []
        for q in models.Lease.objects.filter(ware_key=wareapp, select=1):
            if q.defaule:
                money = q.money
                pass

            purchase.append({
                'id': q.id,
                'name': q.name,
                'money': q.money,
                'defaule': q.defaule
            })
            pass

        try:
            purchase_Lease = models.Lease.objects.get(defaule=True, ware_key=wareapp, select=1)
        except:
            purchase_Lease = None
            pass

        dismoney = 0
        if classify and defaule:
            theress = classify.classifythere_key
            logger.i('theress多功能一体机 ', theress.id)

            try:
                discon = Discount.objects.get(classif_there=theress)
            except:
                discon = None
                pass

            if float(money) <= 100000:
                # a1
                if discon:
                    dismoney = discon.a1
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('float(money) <= 100000', defaule_money)

                pass
            elif 100000 < float(money) and float(money) <= 300000:
                # a2
                if discon:
                    dismoney = discon.a2
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('100000 < float(money) and float(money) <= 300000', defaule_money)
                pass

            elif 300000 < float(money) and float(money) <= 600000:
                # a3
                if discon:
                    dismoney = discon.a3
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('300000 < float(money) and float(money) <= 600000', defaule_money)
                pass

            elif 600000 < float(money) and float(money) <= 1000000:
                # a4
                if discon:
                    dismoney = discon.a4
                else:
                    dismoney = 0

                defaule_money = (100 - float(dismoney)) / 100 * float(money)
                logger.i('600000 < float(money) and float(money) <= 1000000', defaule_money)
                pass

        thereid = classify.classifythere_key.id
        context = {
            'thereid': thereid,
            'id': tid,
            'defaule': defaule,
            'dismoney': dismoney,
            'defaule_money': round(defaule_money, 2),
            'classify': classify,
            'wareapp': wareapp,
            'money': money,
            'param': pare,
            "Dic": Dic,
            "Wpf": Wpf,
            'image': image,
            'lease': Lease,
            'purchase': purchase,
            'duration': models.Duration.objects.filter(ware_key=wareapp),
            'Lease_Duration_': Lease_Duration_,
            'purchase_Lease': purchase_Lease
        }
        return render(request, 'defaule/app/details.html', context)
        pass


decorators = [Web_Maintain, login_mail, get_ip]


@method_decorator(decorators, name='dispatch')
class IndexView(AppGenric.AppTemplateView):
    template_name = 'defaule/index.html'
    template_mobile_name = 'defaule/m/index.html'

    def get_context_data(self, **kwargs):

        mid = []
        for line in models.MiddleTop.objects.filter():
            '''首页板块'''
            list_dity = []
            number = int(line.number) * 5
            for i in models.commodity.objects.filter(key=line.id, ware_key__release=True)[:number]:
                logger.i('i.ware_key.image_200x200', i.ware_key.get_image_url_200x200())
                list_dity.append({
                    'id': i.id,
                    'wareid': i.ware_key.id,
                    'name': i.title,
                    'money': i.money,
                    'image': i.ware_key.get_image_url_200x200(),
                    'url': i.url,
                    'time_now': i.time_now,
                    'ware_key': i.ware_key
                })

            mid.append({
                'id': line.id,
                'title': line.name,
                'temp': line.temp,
                'time_add': line.time_add,
                'time_now': line.time_now,
                'mid_search': line.mid_search.filter(),
                'commodity': list_dity
            })
            pass

        context_hread = {
            'statistics': SearchStatistics.objects.filter()[:10],
            'Carousels': models.Carousel.objects.filter(),
            'newProduct': models.WareApp.objects.filter(release=True).order_by('-time_add')[:20]  # 新品上线
        }

        context = {

            # 'Recommend': Recom,
            'MiddleTop': mid,

        }

        kwargs.update(context_hread)
        kwargs.update(getClassify())
        kwargs.update(context)

        return kwargs

    pass


# class MySearchView_back(RestSearchView):
#     # 重写相关的变量或方法
#     template = 'defaule/app/search.html'
#     models_objects = None
#
#     filter_num = 0
#
#     def get_filter(self, date):
#         if len(date) < 1:
#             return None
#
#         if not date[self.filter_num].brand_key or not date[self.filter_num].producttype_key \
#                 or not date[self.filter_num].technology_key \
#                 or not date[self.filter_num].scene_key \
#                 or not date[self.filter_num].pricerange_key:
#             self.filter_num += 1
#             self.get_filter(date)
#             pass
#         self.filter_num = 0
#
#         return date[self.filter_num]
#         pass
#
#     def get_results(self):
#         s = self.form.search()
#
#         A1 = self.request.GET.get("A1")
#         A2 = self.request.GET.get("A2")
#         A3 = self.request.GET.get("A3")
#         A4 = self.request.GET.get("A4")
#         A5 = self.request.GET.get("A5")
#
#         self.models_objects = modelsObjectsfilter(
#             search=self.request.GET.get('q'),
#             modrls=s, a1=A1, a2=A2, a3=A3,
#             a4=A4, a5=A5, method='jieba'
#         ).get_objects_pull()
#         return s
#
#     def extra_context(self):
#         cache_search = self.request.GET.get("cac")
#         search = self.request.GET.get("q")
#         # logger.i('extra_context', cache_search)
#
#         if cache_search:
#             clify = models.WareAppPrefix.objects.get(id=cache_search)
#
#         else:
#             if len(self.models_objects) > 0:
#                 clify = self.models_objects[0]
#                 cache_search = clify.id
#             else:
#                 clify = None
#             pass
#
#         # logger.i('extra_context', cache_search)
#         context = {
#             'search': search,
#             'cache_search': cache_search,
#             **getClassify()
#         }
#
#         a1 = a2 = a3 = a4 = a5 = None
#
#         if clify and clify.brand_key:
#             a1 = clify.brand_key.PrefixKey
#             pass
#
#         if clify and clify.producttype_key:
#             a2 = clify.producttype_key.PrefixKey
#             pass
#
#         if clify and clify.technology_key:
#             a3 = clify.technology_key.PrefixKey
#             pass
#
#         if clify and clify.scene_key:
#             a4 = clify.scene_key.PrefixKey
#             pass
#
#         if clify and clify.pricerange_key:
#             a5 = clify.pricerange_key.PrefixKey
#             pass
#
#         try:
#             context = {
#                 **context,
#                 'A1': {
#                     'name': clify.brand_key,
#                     "models": models.Brand.objects.filter(PrefixKey=a1)
#                 },
#                 'A2': {
#                     'name': clify.producttype_key,
#                     "models": models.ProductType.objects.filter(PrefixKey=a2)
#                 },
#                 'A3': {
#                     'name': clify.technology_key,
#                     "models": models.Technology.objects.filter(PrefixKey=a3)
#                 },
#                 'A4': {
#                     'name': clify.scene_key,
#                     "models": models.Scene.objects.filter(PrefixKey=a4)
#                 },
#                 'A5': {
#                     'name': clify.pricerange_key,
#                     "models": models.PriceRange.objects.filter(PrefixKey=a5)
#                 },
#             }
#         except AttributeError:
#             pass
#
#         return context
#
#     # def get_context(self):
#     #     paginator = Paginator(self.models_objects, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
#     #     page = self.request.GET.get("page")
#     #
#     #     try:
#     #         current_page = paginator.page(page)
#     #     except PageNotAnInteger:  # 页码不是整数
#     #         current_page = paginator.page(1)
#     #     except EmptyPage:  # 页码空或者NUll
#     #         current_page = paginator.page(paginator.num_pages)
#     #         pass
#     #
#     #     context = {
#     #         'query': self.query,
#     #         'form': self.form,
#     #         'page': current_page,
#     #         'paginator': paginator,
#     #         'suggestion': None,
#     #     }
#     #
#     #     if hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
#     #         context['suggestion'] = self.form.get_suggestion()
#     #
#     #     context.update(self.extra_context())
#     #
#     #     return context

@method_decorator(decorators, name='dispatch')
class Assortment(AppGenric.AppTemplateView):
    '''商品分类展示View'''
    template_name = 'defaule/app/assortmentSearch.html'

    filter_num = 0

    def dispatch(self, request, *args, **kwargs):
        try:
            self.class_id = kwargs['class_id']
        except KeyError:
            self.class_id = 3

        self.search = self.request.GET.get('search', None)
        return super(Assortment, self).dispatch(request, *args, **kwargs)

    def get_filter(self, date):
        if not date.exists():
            return None

        if not date[self.filter_num].brand_key and date[self.filter_num].producttype_key and date[
            self.filter_num].technology_key and date[
            self.filter_num].scene_key and date[self.filter_num].pricerange_key:
            self.filter_num += 1
            self.get_filter(date)
            pass
        self.filter_num = 0

        return date[self.filter_num]
        pass

    def get_context_data(self, **kwargs):
        # def get(self, request, depth):
        '''
        :param request:
        :param depth:  深度[搜索目录： 1 一级分类， 2 二级分类， 3 三级分类]
        :return:
        '''

        logger.i(self.class_id)

        search = self.request.GET.get('search')
        page = self.request.GET.get("page")
        A1 = self.request.GET.get("A1")
        A2 = self.request.GET.get("A2")
        A3 = self.request.GET.get("A3")
        A4 = self.request.GET.get("A4")
        A5 = self.request.GET.get("A5")

        if not search:
            return redirect(reverse('app:index'))

        if self.class_id == 3:
            logger.i('Assortment', 3)

            clify = models.WareAppPrefix.objects.filter(classifythere_key__name=search, wareApp_key__release=True)

            logger.i('clify', clify)

            object_list = modelsObjectsfilter(
                search=search, modrls=clify,
                a1=A1, a2=A2, a3=A3, a4=A4, a5=A5
            )

            paginator = Paginator(object_list.get_objects_pull(), settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)

            try:
                current_page = paginator.page(page)
            except PageNotAnInteger:  # 页码不是整数
                current_page = paginator.page(1)
            except EmptyPage:  # 页码空或者NUll
                current_page = paginator.page(paginator.num_pages)

            _code_ = {
                'state': 'success',
                'code': 200
            }

            filter_class = self.get_filter(clify)

            filters = {}

            if filter_class:
                # logger.i('clify[0].brand_key', filter_class.brand_key)
                # logger.i('clify[0].producttype_key', filter_class.producttype_key)
                # logger.i('clify[0].technology_key', filter_class.technology_key)
                # logger.i('clify[0].scene_key', filter_class.scene_key)
                # logger.i('clify[0].pricerange_key', filter_class.pricerange_key)
                # logger.i('clify[0].WareAppPrefix', filter_class.id)
                # logger.i('clify[0].wareApp_key', filter_class.wareApp_key)
                # logger.i('clify[0].wareApp_key name', filter_class.wareApp_key.name)

                filters = {
                    'A1': {
                        'name': clify[0].brand_key,
                        "models": models.Brand.objects.filter(PrefixKey=filter_class.brand_key.PrefixKey.id)
                    },
                    'A2': {
                        'name': filter_class.producttype_key,
                        "models": models.ProductType.objects.filter(PrefixKey=filter_class.producttype_key.PrefixKey.id)
                    },
                    'A3': {
                        'name': filter_class.technology_key,
                        "models": models.Technology.objects.filter(PrefixKey=filter_class.technology_key.PrefixKey.id)
                    },
                    'A4': {
                        'name': filter_class.scene_key,
                        "models": models.Scene.objects.filter(PrefixKey=filter_class.scene_key.PrefixKey.id)
                    },
                    'A5': {
                        'name': filter_class.pricerange_key,
                        "models": models.PriceRange.objects.filter(PrefixKey=filter_class.pricerange_key.PrefixKey.id),
                    },
                }

            kwargs = {
                **_code_,
                **kwargs,
                **filters,
                **getClassify(),
                'page': current_page,
                'search': search,
                'paginator': paginator,
                'classify': paginator.object_list,
            }

            return kwargs

        else:
            return {
                'state': 'error',
                'error': '非法请求',
                'code': 403
            }
            # return render(request, self.template_name)  # TODO(job@6box.net): 非法请求 [需要单独设计非法请求页面]
        pass

    def get(self, request, *args, **kwargs):
        if self.search:
            kwargs.update(self.get_context_data(**kwargs))
        return self.render_to_response(kwargs)


@method_decorator(decorators, name='dispatch')
class About(AppGenric.AppTemplateView):
    template_name = 'defaule/about/index.html'
    pass


decorators = [condition(last_modified_func=latest_entry)]


@method_decorator(decorators, name='dispatch')
class IndexDetailsView(AppGenric.AppTemplateView):
    template_name = 'defaule/app/details.html'

    index_response = False

    user = None

    def render_to_response(self, context, **response_kwargs):
        if self.index_response:
            return HttpResponseError(self.request).ResponseError(
                **{'code': '404', 'title': '商品不存在',
                   'content': '出现这个错误是由于商品不存在导致的', 'page': 'models.WareAppPrefix.DoesNotExist'})

        return super(IndexDetailsView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        details_id = self.kwargs['details_id']

        Dic = models.WareParProfix.Dis_CHOICES

        defaule = False  # 是否是国采登录用户
        defaule_money = 0  # 国采用户打折

        try:
            self.user = models.User.objects.get(username=self.request.user.username)
            if self.user.usercode:
                defaule = True
                pass
        except models.User.DoesNotExist:
            pass

        try:
            warePrefix = models.WareAppPrefix.objects.get(wareApp_key_id=details_id,
                                                          wareApp_key__slug=self.kwargs['details_slug'])
            logger.i('===================================== WareAppPrefix =====================================')
        except:
            warePrefix = None
            try:
                warePrefix = models.WareAppPrefix.objects.get(wareApp_key_id=details_id)
            except models.WareAppPrefix.DoesNotExist:
                self.index_response = True

        if not self.index_response:
            pare = []
            image = warePrefix.wareApp_key.images_set.filter()
            parameter = warePrefix.wareApp_key.parameter_set.filter()

            ''' 商品规格 '''

            warePar = warePrefix.classifythere_key.wareparprofix_set.get()

            for i in warePar.filter_name:
                logger.i('i[0] ', i[0])
                ks = parameter.values(i[0])
                if ks:
                    ks = ks[0]
                    ks = ks[i[0]]
                else:
                    ks = '无'

                pare.append({
                    'v': Dic[i[0]],
                    'k': ks
                })

            Duration = warePrefix.rate_classg_key

            # 购买Models 配置
            purchase = []
            Lease = models.Lease.objects.filter(ware_key=warePrefix.wareApp_key)
            for q in Lease.filter(select=1):
                purchase.append({
                    'id': q.id,
                    'name': q.name,
                    'money': q.money,
                    'defaule': q.defaule
                })
                pass
            dismoney = 0
            if Lease.exists():
                SetMeal = Lease.get(defaule=True, select=1)
                money = SetMeal.money
                if warePrefix and defaule:
                    try:
                        discon = warePrefix.rate_classg_key
                    except:
                        discon = None
                        pass

                    if float(money) <= 100000:
                        # a1
                        if discon:
                            dismoney = discon.a1
                        else:
                            dismoney = 0

                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('float(money) <= 100000', defaule_money)

                        pass
                    elif 100000 < float(money) and float(money) <= 300000:
                        # a2
                        if discon:
                            dismoney = discon.a2
                        else:
                            dismoney = 0

                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('100000 < float(money) and float(money) <= 300000', defaule_money)
                        pass

                    elif 300000 < float(money) and float(money) <= 600000:
                        # a3
                        if discon:
                            dismoney = discon.a3
                        else:
                            dismoney = 0

                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('300000 < float(money) and float(money) <= 600000', defaule_money)
                        pass

                    elif 600000 < float(money) and float(money) <= 1000000:
                        # a4
                        if discon:
                            dismoney = discon.a4
                        else:
                            dismoney = 0

                        defaule_money = (100 - float(dismoney)) / 100 * float(money)
                        logger.i('600000 < float(money) and float(money) <= 1000000', defaule_money)
                        pass
            else:
                SetMeal = None
                money = 0

            thereid = warePrefix.classifythere_key_id

            context = {
                'thereid': thereid,
                'id': warePrefix.wareApp_key.id,

                'details_id': warePrefix.wareApp_key.id,

                'defaule': defaule,
                'dismoney': dismoney,
                'defaule_money': round(defaule_money, 2),
                'classify': warePrefix,
                'wareapp': warePrefix.wareApp_key,
                'money': money,
                'param': pare,
                "Dic": Dic,
                "Wpf": warePar,
                'image': image,
                'purchase': purchase,
                # 'duration': Duration,
                # 'Lease_Duration_': Duration_defaule,
                'purchase_Lease': Lease,

                'DefaultSetMeal': SetMeal
            }
            kwargs.update(context)

        return kwargs

    pass


