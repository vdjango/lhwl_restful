'''商品'''

import json
import os
import random
import shutil

from django.core.exceptions import ValidationError, MultipleObjectsReturned
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, CreateView
from django.views import generic

from account.util.decorator import auth_admin
from app import models
from app.models import RateClassgUid
from lhwill import controller
from lhwill import config, settings
from lhwill.util.AutomaticCollection import ActivePush
from lhwill.util.log import log
from lhwill.view.HttpCodeError import HttpResponseError
from lhwill.views import ImportWareApp
from managestage.form import online_from, commodity_from
from managestage.models import Setclassify, ImportFile
from managestage.utli import datetimenow, HttpUrl
from managestage.utli.wrapper import _GET, Web_Maintain, _POST
from managestage.views import TIMEDATES, WAREOBJECTSKEY

logger = log(globals())


class Initialization(generic.TemplateView):
    template_name = 'defaule/admin/commodity/Initialization.html'


@Web_Maintain
@auth_admin
def import_Wareapp(request):
    if request.method == 'GET':
        return render(request, 'defaule/admin/commodity/import.html')

    if request.method == 'POST':

        url = os.path.join(settings.BASE_DIR, 'import')



        content = {
            'log': []
        }

        return render(request, 'defaule/admin/commodity/import.html', content)
    pass


def importfile(request):
    files = request.FILES.get('upfile')
    path = os.path.join(settings.BASE_DIR, 'import')
    try:
        imfile = ImportFile.objects.filter()[:1].get()
    except:
        imfile = ImportFile(stype=0)
        imfile.save()

    if len(os.listdir(path)) < 1:
        imfile.stype = 0
        imfile.save()
        pass

    if imfile.stype == 0 or imfile.stype == '0':
        if os.path.isdir(path):
            shutil.rmtree(path)
            imfile.stype = 1
            imfile.save()
            os.makedirs(path)
            pass
        f = open(os.path.join(path, files.name), 'wb')
        for chunk in files.chunks():
            f.write(chunk)
        f.close()

        import zipfile
        fz = zipfile.ZipFile(os.path.join(path, files.name), 'r')
        for file in fz.namelist():
            fz.extract(file, path)
        fz.close()
        os.remove(os.path.join(path, files.name))

    else:
        logger.i(os.path.join(settings.BASE_DIR, '有用户正在执行任务，擒等待任务完成', ))
        content = {
            'state': 'error',
            'error': '有用户正在执行任务，擒等待任务完成',
            'code': '403'
        }
        return HttpResponse(json.dumps(content))
        pass

    Im = None
    url = []
    if os.path.exists(path):
        dirs = os.listdir(path)
        for dirc in dirs:
            print(dirc)
            url.append(dirc)
            unix = datetimenow.datetime_unix()
            unix = '{}{}'.format(unix, random.randint(1000000000, 1520000000))
            # 1527735195
            Im = ImportWareApp(os.path.join(path, dirc), unix)
            Im.dirList()
            Im.addModelsObjects()
            pass
        pass
        try:
            imfile = ImportFile.objects.filter()[:1].get()
            imfile.stype = 0
            imfile.save()
        except:
            imfile = ImportFile(stype=0)
            imfile.save()
            pass
        if os.path.isdir(path):
            shutil.rmtree(path)
            os.makedirs(path)
            pass


    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''创建商品或者修改商品'''

decorators = [Web_Maintain, auth_admin]


@method_decorator(decorators, name='dispatch')
class ArticleRelease(TemplateView):
    '''
    发布商品
    '''
    template_name = 'defaule/admin/commodity/create.html'
    model = models.WareApp

    article_editor = False
    wareApp_Res404 = False

    app_id = None
    app_unix = None

    is_valid_error = None

    def dispatch(self, request, *args, **kwargs):
        try:
            self.app_id = self.kwargs['app_id']
            self.app_unix = self.kwargs['app_unix']
        except KeyError:
            self.app_id = None
            self.app_unix = None

        if self.app_id and self.app_unix:
            self.article_editor = True

        if not self.app_unix:
            self.app_unix = int(datetimenow.datetime_unix())

        return super(ArticleRelease, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.article_editor:
            try:
                app = models.WareApp.objects.get(id=self.app_id, unix=self.app_unix)
                rate = RateClassgUid.objects.filter()
                kwargs.update({
                    'WareApp': app,
                    'rate': rate
                })
            except models.WareApp.DoesNotExist as e:
                self.wareApp_Res404 = HttpResponseError(self.request, **{'page': ''.join(e.args)}).HttpResponse_or_404()
                pass
            pass

        content = {
            'setclassifys': 2,
            'unix': self.app_unix
        }
        kwargs.update(content)
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        '''

        :param context:
        :param response_kwargs:
        :return:
        '''
        if self.wareApp_Res404:
            return self.wareApp_Res404

        return super(ArticleRelease, self).render_to_response(context, **response_kwargs)

    def ObjectCreateOrUpdata(self, **kwargs):
        '''
        创建或者修改商品
        :param kwargs:
        :return:
        '''
        com = self.model.objects.filter(id=self.app_id, unix=self.app_unix)
        if com.exists():
            com.update(
                name=kwargs['name'],
                connet=kwargs['connet']
            )
            logger.i('修改商品', com)
            return com.get(id=self.app_id, unix=self.app_unix)
        else:
            com = self.model(
                name=kwargs['name'],
                connet=kwargs['connet'],
                time_add=TIMEDATES(),
                time_now=TIMEDATES(),
                unix=self.app_unix
            )
            com.save()
            return com
            pass

    def is_valid(self, *args, **kwargs):
        '''
        验证[WareApp|Brand|Scene|Technology|PriceRange|ProductType|Classification|Classification_There]
        Form表单提交数据准确性
        :parameter self.is_valid_error: 返回验证失败表单
        :param args: [Form验证方法: [WareAppModelForm(self.request.POST),] ]
        :param kwargs:
        :return:
        '''
        self.is_valid_error = []
        for i in args:
            if not i.is_valid():
                self.is_valid_error.append(i.verify_info[i.verify[0]])

        if self.is_valid_error or []:
            return False

        return True
        pass

    def post(self, *args, **kwargs):
        name = self.request.POST.get('name')
        money = self.request.POST.get('money')
        connet = self.request.POST.get('connet')
        rate = self.request.POST.get('rate')

        if not rate:
            context = {
                'response': {
                    'code': 400,
                    'state': 'error',
                    'data': {
                        'title': '您有字段未填写哦，请仔细检查后提交！',
                        'content': '央采分类不能为空吗， {}'.format(rate)
                    }
                }
            }
            context.update(self.get_context_data())
            return self.render_to_response(context)

        ModelForm = [
            commodity_from.WareAppModelForm(self.request.POST),
            commodity_from.ClassificationModelForm(self.request.POST),
            commodity_from.Classification_ThereModelForm(self.request.POST),
            commodity_from.BrandModelForm(self.request.POST),
            commodity_from.SceneModelForm(self.request.POST),
            commodity_from.TechnologyModelForm(self.request.POST),
            commodity_from.PriceRangeModelForm(self.request.POST),
            commodity_from.ProductTypeModelForm(self.request.POST)
        ]

        if self.is_valid(*ModelForm):
            brand = models.Brand.objects.get(id=self.request.POST.get('t0'))  # 品牌
            scene = models.Scene.objects.get(id=self.request.POST.get('t3'))  # 使用场景
            technology = models.Technology.objects.get(id=self.request.POST.get('t2'))  # 技术类型
            priceRange = models.PriceRange.objects.get(id=self.request.POST.get('t4'))  # 价格范围
            productType = models.ProductType.objects.get(id=self.request.POST.get('t1'))  # 产品类型
            classify = models.Classification.objects.get(id=self.request.POST.get('classify_id'))
            classifythere = models.Classification_There.objects.get(id=self.request.POST.get('classifytwo_id'))

            rate_models = RateClassgUid.objects.get(uid=rate)

            WareAppPrefix = models.WareAppPrefix.objects.filter(
                wareApp_key=self.ObjectCreateOrUpdata(
                    name=name,
                    money=money,
                    connet=connet,
                )
            )
            if WareAppPrefix.exists():
                WareAppPrefix.update(
                    brand_key=brand,
                    scene_key=scene,
                    technology_key=technology,
                    pricerange_key=priceRange,
                    producttype_key=productType,
                    classify_key=classify,
                    classifythere_key=classifythere,
                    rate_classg_key=rate_models
                )
                logger.i('创建或修改商品成功！！！！！！！！！！！！！')
            else:
                '''
                创建或修改商品失败
                '''
                logger.i('创建或修改商品失败', WareAppPrefix)
                pass
        else:
            '''
            验证失败
            '''
            logger.i('Form表单验证失败', ', '.join(self.is_valid_error))
            context = {
                'response': {
                    'code': 400,
                    'state': 'error',
                    'data': {
                        'title': '您有字段未填写哦，请仔细检查后提交！',
                        'content': ', '.join(self.is_valid_error)
                    }
                }
            }
            context.update(self.get_context_data())
            return self.render_to_response(context)
            pass

        return redirect(reverse('admins:stay'))


class ArticleInfoRelease(TemplateView):
    '''
    商品参数信息
    '''
    template_name = 'defaule/admin/commodity/parameter.html'

    response_info = False
    response_return = False
    response_msg = None

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.app_id = self.kwargs['app_id']
        self.app_unix = self.kwargs['app_unix']
        self.app_there = self.kwargs['app_there']

        if self.request.method == 'POST':
            self.app_file_image = self.request.FILES.getlist('image', None)
            self.app_brands = self.request.POST.get('brands', None)

            self.app_model = self.request.POST.get('model', None)
            self.app_colorType = self.request.POST.get('colorType', None)
            self.app_coverFunction = self.request.POST.get('coverFunction', None)
            self.app_velocityType = self.request.POST.get('velocityType', None)
            self.app_maximumOriginalSize = self.request.POST.get('maximumOriginalSize', None)
            self.app_memory = self.request.POST.get('memory', None)
            self.app_hardDisk = self.request.POST.get('hardDisk', None)
            self.app_forPaperCapacity = self.request.POST.get('forPaperCapacity', None)
            self.app_mediumWeight = self.request.POST.get('mediumWeight', None)
            self.app_materialDescription = self.request.POST.get('materialDescription', None)
            self.app_doubleSidedDevice = self.request.POST.get('doubleSidedDevice', None)
            self.app_automaticDrafts = self.request.POST.get('automaticDrafts', None)
            self.app_networkFunction = self.request.POST.get('networkFunction', None)
            self.app_highestCv = self.request.POST.get('highestCv', None)

            self.app_productType = self.request.POST.get('productType', None)

            '''
            复印功能
            '''
            self.app_photocopyingSpeed = self.request.POST.get('photocopyingSpeed', None)
            self.app_PhotocopyingResolution = self.request.POST.get('PhotocopyingResolution', None)
            self.app_copySize = self.request.POST.get('copySize', None)
            self.app_preheatingTime = self.request.POST.get('preheatingTime', None)
            self.app_copyPhotocopyingPage = self.request.POST.get('copyPhotocopyingPage', None)
            self.app_continuityXeroxPages = self.request.POST.get('continuityXeroxPages', None)
            self.app_zoomRange = self.request.POST.get('zoomRange', None)
            self.app_copyOdds = self.request.POST.get('copyOdds', None)

            '''
            打印功能
            '''
            self.app_printController = self.request.POST.get('printController', None)
            self.app_printingSpeed = self.request.POST.get('printingSpeed', None)
            self.app_printResolution = self.request.POST.get('printResolution', None)
            self.app_printLanguage = self.request.POST.get('printLanguage', None)
            self.app_printingOtherPerformance = self.request.POST.get('printingOtherPerformance', None)

            '''
            扫描功能
            '''
            self.app_scanningController = self.request.POST.get('scanningController', None)
            self.app_scanningResolution = self.request.POST.get('scanningResolution', None)
            self.app_outputFormat = self.request.POST.get('outputFormat', None)
            self.app_scanningOtherPerformance = self.request.POST.get('scanningOtherPerformance', None)

            '''
            传真功能
            '''
            self.app_facsimileController = self.request.POST.get('facsimileController', None)
            self.app_modemSpeed = self.request.POST.get('modemSpeed', None)
            self.app_dataCompressionMethod = self.request.POST.get('dataCompressionMethod', None)
            self.app_faxOtherPerformance = self.request.POST.get('faxOtherPerformance', None)

            '''
            其他特性
            '''
            self.app_display = self.request.POST.get('display', None)
            self.app_mainframeSize = self.request.POST.get('mainframeSize', None)
            self.app_weight = self.request.POST.get('weight', None)
            self.app_otherFeatures = self.request.POST.get('otherFeatures', None)
            self.app_other = self.request.POST.get('other', None)
            self.app_timeMarket = self.request.POST.get('timeMarket', None)

            '''
            复印机附件
            '''
            self.app_optionalAccessories = self.request.POST.get('optionalAccessories', None)

            '''
            保修信息
            '''
            self.app_warrantyTime = self.request.POST.get('warrantyTime', None)
            self.app_customerService = self.request.POST.get('customerService', None)
            self.app_detailedContent = self.request.POST.get('detailedContent', None)
            pass

        return super(ArticleInfoRelease, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        par = None
        try:
            there = models.Classification_There.objects.get(id=self.app_there)
            par = models.WareParProfix.objects.get(key=there)
        except models.WareParProfix.DoesNotExist:
            self.response_info = True
        except models.Classification_There.DoesNotExist as e:
            self.response_return = True
            if self.response_msg:
                self.response_msg = '({}),({})'.format(self.response_msg, e)
            else:
                self.response_msg = e
            pass

        try:
            ware = models.WareApp.objects.get(id=self.app_id, unix=self.app_unix)
        except models.WareApp.DoesNotExist as e:
            self.response_return = True
            ware = None
            if self.response_msg:
                self.response_msg = '({}),({})'.format(self.response_msg, e)
            else:
                self.response_msg = e
            pass

        image = models.images.objects.filter(key=ware)

        content = {
            "id": self.app_id,
            "unix": self.app_unix,
            "par": par,
            "ware": ware,
            'image': image
        }
        kwargs.update(content)
        return kwargs

    def render_to_response(self, context, **response_kwargs):
        if self.response_info:
            return redirect(reverse('admins:setupparameter'))

        if self.response_return:
            context_data = {
                'title': '商品不存在或分类不存在哦！',
                'page': self.response_msg
            }
            return HttpResponseError(self.request, **context_data).HttpResponse_or_404()
        return super(ArticleInfoRelease, self).render_to_response(context, **response_kwargs)

    def post(self, *args, **kwargs):
        info_form_res = False
        image_form_res = False

        context = {}

        info_form = commodity_from.ParameterModelForm(self.request.POST)
        image_form = commodity_from.ImageModelForm(self.request.POST, self.request.FILES)

        if image_form.is_valid():
            for img in self.app_file_image:
                models.images.objects.create(image=img, key_id=self.app_id)
            logger.i('image_form')
            image_form_res = True
            context = {
                'response': {
                    'code': 200,
                    'state': 'success',
                    'data': {
                        'title': '商品首图以保存',
                        'content': '您的商品首图以保存'
                    }
                }
            }

            pass

        if info_form.is_valid():
            logger.i('info_form', info_form.data)
            areap = models.WareAppPrefix.objects.get(wareApp_key_id=self.app_id)
            parameter = models.parameter.objects.filter(key=areap.wareApp_key)

            if not parameter.exists():
                logger.e('未查询到商品参数表，正在创建')
                parameter = models.parameter(key=areap.wareApp_key)
                parameter.save()
                logger.e('商品参数表，以创建')
                pass

            parameter.update(
                productType=areap.classifythere_key.name,
                brands=self.app_brands,
                model=self.app_model,
                colorType=self.app_colorType,
                coverFunction=self.app_coverFunction,
                velocityType=self.app_velocityType,
                maximumOriginalSize=self.app_maximumOriginalSize,
                memory=self.app_memory,
                hardDisk=self.app_hardDisk,
                forPaperCapacity=self.app_forPaperCapacity,
                mediumWeight=self.app_mediumWeight,
                materialDescription=self.app_materialDescription,
                doubleSidedDevice=self.app_doubleSidedDevice,
                automaticDrafts=self.app_automaticDrafts,
                networkFunction=self.app_networkFunction,
                highestCv=self.app_highestCv,
                photocopyingSpeed=self.app_photocopyingSpeed,
                PhotocopyingResolution=self.app_PhotocopyingResolution,
                copySize=self.app_copySize,
                preheatingTime=self.app_preheatingTime,
                copyPhotocopyingPage=self.app_copyPhotocopyingPage,
                continuityXeroxPages=self.app_continuityXeroxPages,
                zoomRange=self.app_zoomRange,
                copyOdds=self.app_copyOdds,
                printController=self.app_printController,
                printingSpeed=self.app_printingSpeed,
                printResolution=self.app_printResolution,
                printLanguage=self.app_printLanguage,
                printingOtherPerformance=self.app_printingOtherPerformance,
                scanningController=self.app_scanningController,
                scanningResolution=self.app_scanningResolution,
                outputFormat=self.app_outputFormat,
                scanningOtherPerformance=self.app_scanningOtherPerformance,
                facsimileController=self.app_facsimileController,
                modemSpeed=self.app_modemSpeed,
                dataCompressionMethod=self.app_dataCompressionMethod,
                faxOtherPerformance=self.app_faxOtherPerformance,
                display=self.app_display,
                mainframeSize=self.app_mainframeSize,
                weight=self.app_weight,
                otherFeatures=self.app_otherFeatures,
                other=self.app_other,
                timeMarket=self.app_timeMarket,
                optionalAccessories=self.app_optionalAccessories,
                warrantyTime=self.app_warrantyTime,
                customerService=self.app_customerService,
                detailedContent=self.app_detailedContent,
            )

            try:
                data = parameter.get(key=areap.wareApp_key).time_now.now()
            except MultipleObjectsReturned:
                data = parameter[0].time_now.now()
                logger.e('商品info存在多个Models对象, 商品为：', areap.wareApp_key.id)
                logger.e('准备清理info所在Models对象：', parameter[1].id)
                parameter[1].delete()
                logger.e('清理info所在Models对象完成！！！！')
                pass

            context = {
                'response': {
                    'code': 200,
                    'state': 'success',
                    'data': {
                        'title': '商品信息以保存',
                        'data': data,
                        'content': '您的商品信息以保存,保存于'
                    }
                }
            }
            info_form_res = True

            pass

        if info_form_res or image_form_res:
            return redirect(reverse('admins:info', args=[self.app_id, self.app_unix, self.app_there]))

        context = {
            'response': {
                'code': 400,
                'state': 'error',
                'data': {
                    'title': '您有字段未填写哦，请仔细检查后提交！',
                    'content': '商品参数信息部分字段未填写哦！'
                }
            }
        }

        context.update(self.get_context_data())
        return self.render_to_response(context)


class ClassZycg(TemplateView):
    template_name = 'defaule/admin/commodity/ClassZycg.html'

    def get_context_data(self, **kwargs):
        rate = RateClassgUid.objects.filter()

        context = {
            'rate': rate
        }

        kwargs.update(context)
        return kwargs


'''获取首页分类列表'''


@_GET
@Web_Maintain
@auth_admin
def get_classModels(request):
    '''
    获取首页分类列表
    :param request:
    :return:
    '''
    classModels = []
    try:
        setl = Setclassify.objects.filter()[:1].get()
        if setl.radio == '2':
            for ify in models.Classification.objects.filter():
                classModelsThere = []
                for ifyThere in models.Classification_There.objects.filter(Classifykey=ify):
                    classModelsThere.append({
                        "n": ifyThere.name,
                        "v": ifyThere.id
                    })
                classModels.append({
                    "n": ify.name,
                    "v": ify.id,
                    "s": classModelsThere
                })

            content = {
                'classModels': classModels,
                'state': 'success',
                'code': '200'
            }
            pass
        else:
            for ify in models.Classification.objects.filter():
                classModelsTwo = []
                for ifyTwo in models.Classification_Two.objects.filter(key=ify):
                    classModelsThere = []
                    for ifyThere in models.Classification_There.objects.filter(key=ifyTwo):
                        classModelsThere.append({
                            "n": ifyThere.name,
                            "v": ifyThere.id
                        })
                    classModelsTwo.append({
                        "n": ifyTwo.subtitle,
                        "v": ifyTwo.id,
                        "s": classModelsThere
                    })
                classModels.append({
                    "n": ify.name,
                    "v": ify.id,
                    "s": classModelsTwo
                })

            content = {
                'classModels': classModels,
                'state': 'success',
                'code': '200'
            }
    except:
        for ify in models.Classification.objects.filter():
            classModelsTwo = []
            for ifyTwo in models.Classification_Two.objects.filter(key=ify):
                classModelsThere = []
                for ifyThere in models.Classification_There.objects.filter(key=ifyTwo):
                    classModelsThere.append({
                        "n": ifyThere.name,
                        "v": ifyThere.id
                    })
                classModelsTwo.append({
                    "n": ifyTwo.subtitle,
                    "v": ifyTwo.id,
                    "s": classModelsThere
                })
            classModels.append({
                "n": ify.name,
                "v": ify.id,
                "s": classModelsTwo
            })

        content = {
            'classModels': classModels,
            'state': 'success',
            'code': '200'
        }

    return HttpResponse(json.dumps(content))
    pass


'''商品-商品管理-创建商品页面-商品参数'''


@_GET
@Web_Maintain
@auth_admin
def parameter(request, unix, id):
    '''
    商品-商品管理-创建商品页面-商品参数
    :param unix:
    :param id:
    :return:
    '''

    Dic = models.WareParProfix.CHOICES
    there_id = request.GET.get('there_id')
    stype = request.GET.get('type')
    there = models.Classification_There.objects.get(id=there_id)

    try:
        Wpf = models.WareParProfix.objects.get(key=there)
    except models.WareParProfix.DoesNotExist:
        return redirect(reverse('admins:setupparameter'))

    parameter = models.parameter.objects.filter(key=models.WareApp.objects.filter(id=id, unix=unix)[0])

    content = {
        "connet": parameter,
        "stype": stype,
        "Dic": Dic,
        "id": id,
        "Wpf": Wpf,
        "unix": unix,
    }
    return render(request, 'defaule/admin/commodity/parameter.html', content)
    pass


'''添加商品参数'''


@_POST
@Web_Maintain
@auth_admin
def add_Parameter(request):
    '''
    添加商品参数
    :param request:
    :param unix:
    :param id:
    :return:
    '''

    stype = request.POST.get('stype')
    unix = request.POST.get('unix')
    id = request.POST.get('id')
    brands = request.POST.get('brands')

    model = request.POST.get('model')
    colorType = request.POST.get('colorType')
    coverFunction = request.POST.get('coverFunction')
    velocityType = request.POST.get('velocityType')
    maximumOriginalSize = request.POST.get('maximumOriginalSize')
    memory = request.POST.get('memory')
    hardDisk = request.POST.get('hardDisk')
    forPaperCapacity = request.POST.get('forPaperCapacity')
    mediumWeight = request.POST.get('mediumWeight')
    materialDescription = request.POST.get('materialDescription')
    doubleSidedDevice = request.POST.get('doubleSidedDevice')
    automaticDrafts = request.POST.get('automaticDrafts')
    networkFunction = request.POST.get('networkFunction')
    highestCv = request.POST.get('highestCv')

    productType = request.POST.get('productType')

    '''
    复印功能
    '''
    photocopyingSpeed = request.POST.get('photocopyingSpeed')
    PhotocopyingResolution = request.POST.get('PhotocopyingResolution')
    copySize = request.POST.get('copySize')
    preheatingTime = request.POST.get('preheatingTime')
    copyPhotocopyingPage = request.POST.get('copyPhotocopyingPage')
    continuityXeroxPages = request.POST.get('continuityXeroxPages')
    zoomRange = request.POST.get('zoomRange')
    copyOdds = request.POST.get('copyOdds')

    '''
    打印功能
    '''
    printController = request.POST.get('printController')
    printingSpeed = request.POST.get('printingSpeed')
    printResolution = request.POST.get('printResolution')
    printLanguage = request.POST.get('printLanguage')
    printingOtherPerformance = request.POST.get('printingOtherPerformance')

    '''
    扫描功能
    '''
    scanningController = request.POST.get('scanningController')
    scanningResolution = request.POST.get('scanningResolution')
    outputFormat = request.POST.get('outputFormat')
    scanningOtherPerformance = request.POST.get('scanningOtherPerformance')

    '''
    传真功能
    '''
    facsimileController = request.POST.get('facsimileController')
    modemSpeed = request.POST.get('modemSpeed')
    dataCompressionMethod = request.POST.get('dataCompressionMethod')
    faxOtherPerformance = request.POST.get('faxOtherPerformance')

    '''
    其他特性
    '''
    display = request.POST.get('display')
    mainframeSize = request.POST.get('mainframeSize')
    weight = request.POST.get('weight')
    otherFeatures = request.POST.get('otherFeatures')
    other = request.POST.get('other')
    print('other', brands)
    timeMarket = request.POST.get('timeMarket')

    '''
    复印机附件
    '''
    optionalAccessories = request.POST.get('optionalAccessories')

    '''
    保修信息
    '''
    warrantyTime = request.POST.get('warrantyTime')
    customerService = request.POST.get('customerService')
    detailedContent = request.POST.get('detailedContent')

    areap = models.WareAppPrefix.objects.get(wareApp_key=models.WareApp.objects.get(id=id))

    try:
        pm = models.parameter.objects.get(key=areap.wareApp_key)
        pm.brands = brands
        pm.model = model
        pm.colorType = colorType
        pm.coverFunction = coverFunction
        pm.velocityType = velocityType
        pm.maximumOriginalSize = maximumOriginalSize
        pm.memory = memory
        pm.hardDisk = hardDisk
        pm.forPaperCapacity = forPaperCapacity
        pm.mediumWeight = mediumWeight
        pm.materialDescription = materialDescription
        pm.doubleSidedDevice = doubleSidedDevice
        pm.automaticDrafts = automaticDrafts
        pm.networkFunction = networkFunction
        pm.highestCv = highestCv
        pm.photocopyingSpeed = photocopyingSpeed
        pm.PhotocopyingResolution = PhotocopyingResolution
        pm.copySize = copySize
        pm.preheatingTime = preheatingTime
        pm.copyPhotocopyingPage = copyPhotocopyingPage
        pm.continuityXeroxPages = continuityXeroxPages
        pm.zoomRange = zoomRange
        pm.copyOdds = copyOdds
        pm.printController = printController
        pm.printingSpeed = printingSpeed
        pm.printResolution = printResolution
        pm.printLanguage = printLanguage
        pm.printingOtherPerformance = printingOtherPerformance
        pm.scanningController = scanningController
        pm.scanningResolution = scanningResolution
        pm.outputFormat = outputFormat
        pm.scanningOtherPerformance = scanningOtherPerformance
        pm.facsimileController = facsimileController
        pm.modemSpeed = modemSpeed
        pm.dataCompressionMethod = dataCompressionMethod
        pm.faxOtherPerformance = faxOtherPerformance
        pm.display = display
        pm.mainframeSize = mainframeSize
        pm.weight = weight
        pm.otherFeatures = otherFeatures
        pm.other = other,
        pm.timeMarket = timeMarket
        pm.optionalAccessories = optionalAccessories
        pm.warrantyTime = warrantyTime
        pm.customerService = customerService
        pm.detailedContent = detailedContent
        pm.save()

        content = {
            'state': 'success',
            'url': '/admin/commodity/',
            'code': '200'
        }
    except:
        models.parameter(
            brands=brands,
            model=model,
            # productType=productType,
            colorType=colorType,
            coverFunction=coverFunction,
            velocityType=velocityType,
            maximumOriginalSize=maximumOriginalSize,
            memory=memory,
            hardDisk=hardDisk,
            forPaperCapacity=forPaperCapacity,
            mediumWeight=mediumWeight,
            materialDescription=materialDescription,
            doubleSidedDevice=doubleSidedDevice,
            automaticDrafts=automaticDrafts,
            networkFunction=networkFunction,
            highestCv=highestCv,
            photocopyingSpeed=photocopyingSpeed,
            PhotocopyingResolution=PhotocopyingResolution,
            copySize=copySize,
            preheatingTime=preheatingTime,
            copyPhotocopyingPage=copyPhotocopyingPage,
            continuityXeroxPages=continuityXeroxPages,
            zoomRange=zoomRange,
            copyOdds=copyOdds,
            printController=printController,
            printingSpeed=printingSpeed,
            printResolution=printResolution,
            printLanguage=printLanguage,
            printingOtherPerformance=printingOtherPerformance,
            scanningController=scanningController,
            scanningResolution=scanningResolution,
            outputFormat=outputFormat,
            scanningOtherPerformance=scanningOtherPerformance,
            facsimileController=facsimileController,
            modemSpeed=modemSpeed,
            dataCompressionMethod=dataCompressionMethod,
            faxOtherPerformance=faxOtherPerformance,
            display=display,
            mainframeSize=mainframeSize,
            weight=weight,
            otherFeatures=otherFeatures,
            other=other,
            timeMarket=timeMarket,
            optionalAccessories=optionalAccessories,
            warrantyTime=warrantyTime,
            customerService=customerService,
            detailedContent=detailedContent,
            key=WAREOBJECTSKEY(id)
        ).save()

        content = {
            'state': 'success',
            'url': '/admin/commodity/online/{}/{}/'.format(unix, id),
            'code': '200'
        }

    return HttpResponse(json.dumps(content))
    pass


'''商品套餐分类'''


@_GET
@Web_Maintain
@auth_admin
def online(request, unix, id):
    '''
    商品套餐分类
    :param request:
    :param unix:
    :param id:
    :return:
    '''
    stype = request.GET.get('type')
    url = request.GET.get('url')

    wareapp = models.WareApp.objects.get(id=id)

    # 租赁Models 配置
    Lease = []
    for q in models.Lease.objects.filter(ware_key=wareapp, select=0):
        Lease.append({
            'id': q.id,
            'name': q.name,
            'defaule': q.defaule,
            'duration': models.Duration.objects.filter(ware_key=wareapp)
        })
        pass

    # 购买Models 配置
    purchase = []
    for q in models.Lease.objects.filter(ware_key=wareapp, select=1):
        purchase.append(q)
        pass

    lease_default = config.AppModels().get_LeaseSelect()

    connet = {
        'lease_default': lease_default,
        'lease': Lease,
        'purchase': purchase,
        'stype': stype,
        'url': '/admin/{}/'.format(url),
        'unix': unix,
        'id': id,
    }

    return render(request, 'defaule/admin/commodity/online.html', connet)


'''商品-商品管理-创建商品-添加商品分类信息-创建分类信息'''


@_POST
@Web_Maintain
@auth_admin
def add_mode(request):
    '''
    商品-商品管理-创建商品-添加商品分类信息-创建分类信息
    :param unix:
    :param id:
    :return:
    '''
    name = request.POST.get('name')
    money = request.POST.get('money')
    defaule = request.POST.get('defaule')
    unix = request.POST.get('unix')
    id = request.POST.get('id')

    if defaule == '0':
        defaule = True
        models.Duration.objects.filter(defaule=True).update(defaule=False)

    else:
        defaule = False

    wareapp = models.WareApp.objects.get(id=id)
    models.Duration(name=name, defaule=defaule, money=money, ware_key=wareapp).save()

    content = {
        'state': 'success',
        'url': '/admin/create/parameter/{}/{}/'.format(unix, id),
        'code': '200'
    }
    return HttpResponse(json.dumps(content))


'''添加商品套餐信息'''


@_POST
@Web_Maintain
@auth_admin
def add_choice(request):
    '''
    添加商品套餐信息
    :return:
    '''
    defaule = request.POST.get('defaule')
    action = request.POST.get('action')
    name = request.POST.get('name')
    money = request.POST.get('money')
    id = request.POST.get('id')

    ware_key = models.WareApp.objects.get(id=id)

    if defaule == '0':
        models.Lease.objects.filter(defaule=True, ware_key=ware_key).update(defaule=False)
        defaule = True
    else:
        defaule = False

    online = online_from.Form_one(request.POST)

    if online.is_valid():
        try:
            models.Lease(name=name, money=money, defaule=defaule, ware_key=ware_key).save()
        # models.Choicetwo(name=p2, defaule=defaule, key=ch[0], ware_key=ware_key[0]).save()
        except ValidationError:
            content = {
                'state': 'error',
                'error': '必须为十进制数字',
                'code': '403'
            }
            return HttpResponse(json.dumps(content))
        except:
            content = {
                'state': 'error',
                'error': '套餐分类或商品为空',
                'code': '403'
            }
            return HttpResponse(json.dumps(content))
            pass

    else:
        content = {
            'state': 'error',
            'error': '缺少提交参数',
            'code': '403'
        }
        return HttpResponse(json.dumps(content))
        pass

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))


'''商品版本发布'''


@_GET
@Web_Maintain
@auth_admin
def release(request, unix, id):
    '''
    商品版本发布
    :param request:
    :param unix:
    :param id:
    :return:
    '''
    state = models.WareApp.objects.get(id=id)
    release = state.release
    release_version = state.release_version
    timedate = state.time_now

    release = {
        'name': state.name,
        'state': release,  # 表示商品未发布
        'version': release_version,
        'timedate': timedate,  # 商品发布时间
    }
    dic = {
        'release': release,
        'unix': unix,
        'id': id,
    }
    return render(request, 'defaule/admin/commodity/release.html', dic)


'''发布商品或下架商品'''


@_POST
@Web_Maintain
@auth_admin
def set_online(request):
    '''
    发布商品或下架商品
    :return:
    '''
    id = request.POST.get('id')
    print(id)
    # state = models.WareAppPrefix.objects.get(id=id)
    state = models.WareApp.objects.get(id=id)
    release = state.release
    if release:
        # us = 'del'
        us = 'update'
        state.release = False
        logger.i('下架商品 -> 主动推送', us)
    else:
        us = 'urls'
        logger.i('发布商品 -> 主动推送', us)
        state.release_version += 1
        state.release = True
        pass

    state.save()
    logger.i(' -> 主动推送', us)
    ActivePush(us=us).Push(date='{}{}'.format(settings.HTTP_HOST, state.get_absolute_url()))

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''删除商品'''


@_POST
@Web_Maintain
@auth_admin
def del_ware(request):
    '''
    删除商品
    :param request:
    :param id:
    :return:
    '''

    stype = request.POST.get('stype')
    lists = request.POST.get('list')
    if stype == 'list':
        for i in str(lists).split('&'):
            w_id = int(str(i).split('=')[1])
            uid = models.WareApp.objects.filter(id=w_id)  # 批量删除
            for ui in uid:
                if ui.release:
                    logger.i('删除商品 -> 主动推送', 'del')
                    ActivePush(us='del').Push(date='{}{}'.format(settings.HTTP_HOST, ui.get_absolute_url()))

                try:
                    controller.DelDate(ui.unix)
                    if ui.id != None:
                        print('Del No')
                        models.parameter.objects.get(key=ui.id).delete()
                except Exception as e:
                    logger.e('except Del No', e.args)
            uid.delete()

            pass
        pass
    else:
        uid = lists
        try:
            uid = models.WareApp.objects.get(id=uid)
            unix = uid.unix
            pid = uid.id
            uid.delete()

            controller.DelDate(unix)
            if pid != None:
                models.parameter.objects.get(key=pid).delete()
        except Exception as e:
            '''
            日志收集
            #raise e
            '''
            pass

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''商品-待发布'''


@_GET
@Web_Maintain
@auth_admin
def stay(request, lend=1):
    '''
    商品-待发布
    :param lend:
    :return:
    '''
    lend = int(lend)
    Front, After = HttpUrl.UrlSection(lend, '/admin/list/')
    war = []

    for i in models.WareApp.objects.filter(release=False):

        try:
            _w = models.WareAppPrefix.objects.get(wareApp_key=i)
            there = _w.classifythere_key.id
            logger.i('classifythere_key', _w.classifythere_key)
        except models.WareAppPrefix.DoesNotExist:
            there = 0
            logger.i('classifythere_key DoesNotExist', )
        except AttributeError:
            there = 0
            logger.i('classifythere_key AttributeError', )

        war.append({
            'id': i.id,
            'name': i.name,
            'release': i.release,
            'money': i.money,
            'connet': i.connet,
            'unix': i.unix,
            'commodity_description': i.commodity_description,
            'characteristic': i.characteristic,
            'release_version': i.release_version,
            'time_now': i.time_now,
            'there_id': there
        })

    leng = len(war)
    war = war[Front:After]

    content = {
        'war': war,
        'leng': leng,
        'Front': Front,
        'After': After,
        'Jumpgo': lend + 1,
        'Jumpre': lend - 1
    }
    return render(request, 'defaule/admin/commodity/stay.html', content)
    pass


def SetupCommod(request):
    return render(request, 'defaule/admin/commodity/setupcommod.html')
    pass


'''创建商品，get搜索页筛选器列表'''


def get_ClassifyTwo(request):
    '''
    创建商品，get搜索页筛选器列表
    :param request:
    :return:
    '''
    id = request.GET.get('id')

    setl = Setclassify.objects.filter()[:1].get()

    key = models.Classification_There.objects.get(id=id)
    waresetup = models.WareSetupPrefix.objects.filter(key=key)

    BrandKey = waresetup.filter(filter_id='0')[:1].get()
    ProductTypeKey = waresetup.filter(filter_id='1')[:1].get()
    TechnologyKey = waresetup.filter(filter_id='2')[:1].get()
    SceneKey = waresetup.filter(filter_id='3')[:1].get()
    PriceRangeKey = waresetup.filter(filter_id='4')[:1].get()

    # log.i(globals(), BrandKey, ProductTypeKey, TechnologyKey, TechnologyKey, SceneKey, PriceRangeKey)
    Brand = []

    t1 = []

    for pre in models.Brand.objects.filter(PrefixKey=BrandKey):
        Brand.append({
            'id': pre.id,
            'name': pre.name
        })
        pass

    t1.append({
        'cid': BrandKey.filter_id,
        'name': BrandKey.t1,
        'filter_id': BrandKey.filter_id,
        'data': Brand
    })

    ProductType = []
    for pre in models.ProductType.objects.filter(PrefixKey=ProductTypeKey):
        ProductType.append({
            'id': pre.id,
            'name': pre.name
        })
        pass

    t1.append({
        'cid': ProductTypeKey.filter_id,
        'name': ProductTypeKey.t2,
        'filter_id': ProductTypeKey.filter_id,
        'data': ProductType
    })

    Technology = []
    for pre in models.Technology.objects.filter(PrefixKey=TechnologyKey):
        Technology.append({
            'id': pre.id,
            'name': pre.name
        })
        pass

    t1.append({
        'cid': TechnologyKey.filter_id,
        'name': TechnologyKey.t3,
        'filter_id': TechnologyKey.filter_id,
        'data': Technology
    })

    Scene = []
    for pre in models.Scene.objects.filter(PrefixKey=SceneKey):
        Scene.append({
            'id': pre.id,
            'name': pre.name
        })
        pass

    t1.append({
        'cid': SceneKey.filter_id,
        'name': SceneKey.t4,
        'filter_id': SceneKey.filter_id,
        'data': Scene
    })

    PriceRange = []
    for pre in models.PriceRange.objects.filter(PrefixKey=PriceRangeKey):
        PriceRange.append({
            'id': pre.id,
            'name': pre.name
        })
        pass

    t1.append({
        'cid': PriceRangeKey.filter_id,
        'name': PriceRangeKey.t5,
        'filter_id': PriceRangeKey.filter_id,
        'data': PriceRange
    })

    content = {
        'state': 'success',
        'data': t1,
        'code': '200'
    }

    logger.i(t1)

    return HttpResponse(json.dumps(content))


class SettupView(TemplateView):
    '''
    未设置商品首图展示
    '''
    template_name = 'defaule/admin/commodity/setup.html'

    def get_context_data(self, **kwargs):
        wareapp = models.WareApp.objects.filter(image__isnull=True, release=True)
        context = {
            'context': wareapp,
            'count': wareapp.count()
        }
        kwargs.update(context)
        return kwargs

    def post(self, request, *args, **kwargs):
        for i in models.WareApp.objects.filter(image__isnull=True):
            image = models.images.objects.filter(key=i)
            if image.exists():
                a = image.get(id=image[0].id)
                logger.i('not image.exists()', a.defaule)
                a.defaule = True
                a.save()
                logger.i('save image.exists()', a.defaule)
            else:
                logger.i('not filt', image)
            pass

        return redirect(reverse("admins:commodity"))
        pass
