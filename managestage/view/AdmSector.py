'''板块'''

import json

from PIL import Image
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views import generic

from account.util.decorator import auth_admin
from app import models
from app.models import RateClassgUid
from home.models import Goodslist, Discount, Gusid
from lhwill import settings
from lhwill.util.log import log
from lhwill.views import JsonView
from managestage.form import AdmSector_from
from managestage.models import Setclassify
from managestage.utli.datetimenow import datetime_unix, datetimenow
from managestage.utli.wrapper import _POST, Web_Maintain, _GET
from managestage.views import TIMEDATES
from plate import models as plateModels

'''板块-板块管理-添加板块'''

logger = log(globals())


@_POST
@Web_Maintain
@auth_admin
def add_sector(request):
    '''
    板块-板块管理-添加板块
    :return:
    '''
    name = request.POST.get('name')
    temp = request.POST.get('temp')
    number = request.POST.get('number')

    models.MiddleTop(
        name=name,
        temp=temp,
        number=number,
        time_add=TIMEDATES(),
        time_now=TIMEDATES()
    ).save()
    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))


'''修改板块名称'''


@_POST
@Web_Maintain
@auth_admin
def set_brock(request):
    '''
    修改板块名称
    :return:
    '''
    id = request.POST.get('id')
    name = request.POST.get('name')
    temp = request.POST.get('temp')
    number = request.POST.get('number')

    Mi = models.MiddleTop.objects.get(id=id)
    Mi.name = name
    Mi.temp = temp
    Mi.number = int(number)
    Mi.save()

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))
    pass


'''修改板块标签'''


@_POST
@Web_Maintain
@auth_admin
def set_label(request):
    '''
    修改板块标签[首页板块下方的导航]
    :return:
    '''
    id = request.POST.get('id')
    name = request.POST.get('name')

    lab = models.Mid_Search.objects.get(id=id)
    lab.name = name
    lab.save()

    content = {
        'state': 'success',
        'code': '200'
    }
    return HttpResponse(json.dumps(content))

    pass


'''获取板块标签'''


@_GET
@Web_Maintain
@auth_admin
def get_label(request):
    '''
    获取板块标签
    :return:
    '''
    id = request.GET.get('id')
    lab = []
    Mii = models.MiddleTop.objects.get(id=id)
    for i in models.Mid_Search.objects.filter(key=Mii):
        lab.append({
            'id': i.id,
            'name': i.name,
            'url': i.url
        })

    content = {
        'state': 'success',
        'data': lab,
        'code': '200'
    }

    logger.i(content)

    return HttpResponse(json.dumps(content))


'''商品-板块管理-添加商品'''


@_POST
@Web_Maintain
@auth_admin
def set_addSector(request):
    '''
    商品-板块管理-添加商品
    :return:
    '''
    ware_id = request.POST.get('ware_id')
    temp_id = request.POST.get('temp')
    url = ''  # request.POST.get('url')

    ware = models.WareApp.objects.get(id=ware_id)

    Mt = models.MiddleTop.objects.get(id=temp_id)
    images = '/static/ware/ware-404.jpg'
    try:
        image = models.images.objects.filter(key=ware)[:1].get()
        images = '{}'.format(image.image)
    except:
        images = '/static/ware/ware-404.jpg'
        pass

    if models.commodity.objects.filter(title=ware.name, money=ware.money):
        content = {
            'state': 'warning',
            'warning': '商品以在其他板块添加',
            'code': '200'
        }
        pass
    else:

        models.commodity(
            title=ware.name,
            money=ware.money,
            image=images,
            url=url,
            ware_key=ware,
            key=Mt,
            time_add=datetimenow()
        ).save()

        content = {
            'state': 'success',
            'code': '200'
        }
    return HttpResponse(json.dumps(content))
    pass


'''添加板块标签'''


@_POST
@Web_Maintain
@auth_admin
def add_label(request):
    '''
    添加板块标签
    :return:
    '''
    name = request.POST.get('name')
    temp = request.POST.get('temp')
    url = request.POST.get('url')

    models.Mid_Search(
        name=name,
        url=url,
        key=models.MiddleTop.objects.get(id=temp)
    ).save()

    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))

    pass


'''删除板块'''


@_POST
@Web_Maintain
@auth_admin
def del_brock(request):
    '''
    删除板块
    :return:
    '''
    id = request.POST.get('id')
    models.MiddleTop.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''获取商品列表'''


@_GET
@Web_Maintain
@auth_admin
def get_ware(request):
    '''
    获取商品列表
    :return:
    '''

    id = request.GET.get('id')
    if id:
        Wapp = models.WareApp.objects.filter(id=id)
    else:
        Wapp = models.WareApp.objects.filter()[:20]

    print(Wapp)

    Wapp = serializers.serialize("json", Wapp)

    print(Wapp)

    content = {
        'state': 'success',
        'data': Wapp,
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''板块-板块管理-板块数据-推荐商品[添加推荐商品到板块]'''


@_POST
@Web_Maintain
@auth_admin
def add_WareAppBrock(request):
    '''
    板块-板块管理-板块数据-推送商品[添加推荐商品到板块]
    :return:
    '''
    middleTop_id = request.POST.get('middleTop_id')
    ware_id = request.POST.get('ware_id')
    mid = models.MiddleTop.objects.get(id=middleTop_id)
    war = models.WareApp.objects.get(id=ware_id)
    image = models.images.objects.filter(key=war)[1]
    image = '/media/images/{}/head/{}'.format(
        war.unix,
        image.image
    )
    models.commodity(
        title=war.name,
        money=war.money,
        image=image,
        url='',
        key=mid,
        ware_key=war,
        time_add=TIMEDATES(),
        time_now=TIMEDATES()
    ).save()

    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''板块-板块管理-板块数据[删除板块数据]'''


@_POST
@Web_Maintain
@auth_admin
def del_WareAppBrock(request):
    '''
    板块-板块管理-板块数据[删除板块推送商品]
    :return:
    '''
    id = request.POST.get('id')
    models.commodity.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''板块-全部分类'''

decorators = [Web_Maintain, auth_admin]


@method_decorator(decorators, name='dispatch')
class classify(TemplateView):
    '''
    板块-全部分类
    '''
    template_name = 'defaule/admin/sector/classify.html'

    def get_context_data(self, **kwargs):
        ify = models.Classification.objects.filter()
        ify_bar = models.Classification_bar.objects.filter()
        ify_two = models.Classification_Two.objects.filter()
        ify_There = models.Classification_There.objects.filter()

        try:
            setl = Setclassify.objects.filter()[:1].get()
        except:
            setl = 3
            pass

        ex_content = []
        aaa = []

        for i in ify:
            ex_content.append({
                'Classification': {
                    'obj': i,
                    'Navigation_There': ify_There.filter(Classifykey=i)
                },
            })

        logger.i(ex_content)

        content = {
            'setclassify': setl,
            'classify': ify,
            'classify_bar': ify_bar,
            'classify_two': ify_two,
            'classify_there': ify_There,
            **kwargs,
            'content': ex_content
        }
        return content
        pass

    pass


'''板块-全部分类-添加分类'''


@_POST
@Web_Maintain
@auth_admin
def add_classify(request):
    '''
    板块-全部分类-添加分类
    :return:
    '''
    name = request.POST.get('name')
    models.Classification(
        name=name,
        time_now=TIMEDATES(),
        time_add=TIMEDATES()
    ).save()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''添加分类导航'''


@_POST
@Web_Maintain
@auth_admin
def add_classifyLabel(request):
    '''
    添加分类导航
    :return:
    '''
    name = request.POST.get('name')
    url = request.POST.get('url')
    id = request.POST.get('id')

    key = models.Classification.objects.get(id=id)
    models.Classification_bar(
        key=key,
        name=name,
        url=url,
        time_add=TIMEDATES(),
        time_now=TIMEDATES()
    ).save()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''获取全部分类列表'''


@_GET
@Web_Maintain
@auth_admin
def get_classify(request):
    '''
    获取全部分类列表
    :return:
    '''
    id = request.GET.get('id')
    if id:
        classifys = models.Classification.objects.filter(id=id)
    else:
        classifys = models.Classification.objects.filter()

    classify = []
    for i in classifys:
        classify.append({
            'id': i.id,
            'name': i.name
        })

    content = {
        'state': 'success',
        'data': classify,
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''修改分类名称'''


@_POST
@Web_Maintain
@auth_admin
def set_classify(request):
    '''
    修改分类名称
    :return:
    '''
    id = request.POST.get('id')
    name = request.POST.get('name')
    ify = models.Classification.objects.get(id=id)
    ify.name = name
    ify.save()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''删除首页分类'''


@_POST
@Web_Maintain
@auth_admin
def del_classify(request):
    '''
    删除首页分类
    :return:
    '''
    id = request.POST.get('id')
    models.Classification.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''获取分类导航列表'''


@_GET
@Web_Maintain
@auth_admin
def get_classifyLabel(request):
    '''
    获取分类导航列表
    :return:
    '''
    id = request.GET.get('id')
    if id:
        classify = models.Classification_bar.objects.filter(id=id)
    else:
        classify = models.Classification_bar.objects.filter()

    classify = serializers.serialize("json", classify)

    content = {
        'state': 'success',
        'data': classify,
        'code': '200'
    }

    return HttpResponse(json.dumps(content))


'''修改分类导航名称'''


@_POST
@Web_Maintain
@auth_admin
def set_classifyLabel(request):
    '''
    修改分类导航名称
    :return:
    '''
    id = request.POST.get('id')
    name = request.POST.get('name')
    ify = models.Classification_bar.objects.get(id=id)
    ify.name = name
    ify.save()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''删除分类导航'''


@_POST
@Web_Maintain
@auth_admin
def del_classifyLabel(request):
    '''
    删除分类导航
    :return:
    '''
    id = request.POST.get('id')
    models.Classification_bar.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))


'''添加二级分类'''


@_POST
@Web_Maintain
@auth_admin
def add_classify_two(request):
    '''
    添加二级分类
    :return:
    '''
    id = request.POST.get('id')
    url = request.POST.get('url')
    name = request.POST.get('name')
    ify = models.Classification.objects.get(id=id)
    models.Classification_Two(
        key=ify,
        url=url,
        subtitle=name,
        time_add=TIMEDATES(),
        time_now=TIMEDATES()
    ).save()

    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''获取二级分类'''


@_GET
@Web_Maintain
@auth_admin
def get_classifytwo(request):
    '''
    获取二级分类 【Setclassify = 2 获取三级分类】
    :return:
    '''
    id = request.GET.get('id')
    setl = Setclassify.objects.filter()[:1].get()
    if setl.radio == '2':
        ify = models.Classification.objects.get(id=id)
        iftwos = models.Classification_There.objects.filter(Classifykey=ify)

        iftwo = []
        for i in iftwos:
            iftwo.append({
                'id': i.id,
                'name': i.name,
                'url': i.url
            })
    else:
        ify = models.Classification.objects.get(id=id)
        iftwos = models.Classification_Two.objects.filter(key=ify)

        iftwo = []
        for i in iftwos:
            iftwo.append({
                'id': i.id,
                'name': i.subtitle,
                'url': i.url
            })
        pass

    content = {
        'state': 'success',
        'data': iftwo,
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''获取三级分类'''


@_GET
@Web_Maintain
@auth_admin
def get_classifythere(request):
    '''
    获取三级分类
    :return:
    '''
    id = request.GET.get('id')
    iftwo = []
    there = models.Classification_There.objects.filter(id=id)
    for i in there:
        try:
            duton = Discount.objects.get(classif_there=i)
            if duton:
                print('duton', duton.defaule)
                iftwo.append({
                    'id': i.id,
                    'name': i.name,
                    'url': i.url,
                    'time': str(i.time_now.astimezone()).split('+')[0],
                    'a1': str(duton.a1),
                    'a2': str(duton.a2),
                    'a3': str(duton.a3),
                    'a4': str(duton.a4),
                    'defaule': duton.defaule
                })
            else:
                iftwo.append({
                    'id': i.id,
                    'name': i.name,
                    'url': i.url,
                    'time': str(i.time_now.astimezone()).split('+')[0],
                    'defaule': False
                })
        except:
            iftwo.append({
                'id': i.id,
                'name': i.name,
                'url': i.url,
                'time': str(i.time_now.astimezone()).split('+')[0],
                'defaule': False
            })

    logger.i(iftwo)

    content = {
        'state': 'success',
        'data': iftwo,
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''添加三级分类'''


@_POST
@Web_Maintain
@auth_admin
def add_classifyThere(request):
    '''
    添加三级分类
    :return:
    '''
    name = request.POST.get('name')
    url = request.POST.get('url')
    id = request.POST.get('id')

    setl = Setclassify.objects.filter()[:1].get()
    if setl.radio == '2':
        iftwo = models.Classification.objects.get(id=id)
        models.Classification_There(
            name=name,
            url=url,
            Classifykey=iftwo,
            time_now=TIMEDATES(),
            time_add=TIMEDATES()
        ).save()
    else:
        iftwo = models.Classification_Two.objects.get(id=id)
        models.Classification_There(
            name=name,
            url=url,
            key=iftwo,
            time_now=TIMEDATES(),
            time_add=TIMEDATES()
        ).save()

    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''修改二级分类'''


@_POST
@Web_Maintain
@auth_admin
def set_classifyTwo(request):
    '''
    修改二级分类
    :return:
    '''
    name = request.POST.get('name')
    url = request.POST.get('url')
    id = request.POST.get('id')
    Two = models.Classification_Two.objects.get(id=id)
    if url:
        Two.url = url

    if name:
        Two.subtitle = name

    Two.save()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''修改三级分类'''


@_POST
@Web_Maintain
@auth_admin
def set_classifyThere(request):
    '''
    修改三级分类
    :return:
    '''
    name = request.POST.get('name')
    url = request.POST.get('url')
    id = request.POST.get('id')
    There = models.Classification_There.objects.get(id=id)
    if url:
        There.url = url

    if name:
        There.name = name

    There.save()
    print('There', There.name)
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''删除二级分类'''


@_POST
@Web_Maintain
@auth_admin
def del_classifyTwo(request):
    '''
    删除二级分类
    :return:
    '''
    id = request.POST.get('id')
    models.Classification_Two.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''删除三级分类[商品分类]'''


@_POST
@Web_Maintain
@auth_admin
def del_classifyThere(request):
    '''
    删除三级分类[商品分类]
    :return:
    '''
    id = request.POST.get('id')
    models.Classification_There.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''板块-首页导航'''


@_GET
@Web_Maintain
@auth_admin
def navigation(request):
    '''
    板块-首页导航
    :param request:
    :return:
    '''
    naviga = models.Navigation.objects.filter()
    naviga_two = models.Navigation_Two.objects.filter()
    page = models.Navaid.objects.filter()

    context = {
        'naviga': naviga,
        'naviga_two': naviga_two,
        'page': page
    }
    return render(request, 'defaule/admin/sector/navigation.html', context)
    pass


'''添加首页导航'''


@_POST
@Web_Maintain
@auth_admin
def add_Navigation(request):
    '''
    添加首页导航
    :param request:
    :return:
    '''
    stype = request.POST.get('stype')
    name = request.POST.get('name')
    url = request.POST.get('url')
    if stype == 'default':
        page_id = request.POST.get('page_id')
        url = '/app/navaid/{}/'.format(page_id)

    print('url--------', stype)

    models.Navigation(
        name=name,
        url=url,
        time_add=TIMEDATES(),
        time_now=TIMEDATES()
    ).save()

    return redirect(reverse('admins:navigation'))
    pass


'''添加二级导航'''


@_POST
@Web_Maintain
@auth_admin
def add_NavigationTwo(request):
    '''
    添加二级导航
    :param request:
    :return:
    '''
    stype = request.POST.get('stype')
    name = request.POST.get('name')
    url = request.POST.get('url')
    if stype == 'default':
        page_id = request.POST.get('page_id')
        url = '/app/navaid/{}/'.format(page_id)

    plate = plateModels.plateModels(
        name=name
    )
    plate.save()
    models.Navigation_Two(
        name=name,
        key=plate
    ).save()

    return redirect(reverse('admins:navigation'))
    pass


'''修改首页导航'''


@_POST
@Web_Maintain
@auth_admin
def set_Navigation(request):
    '''
    修改首页导航
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    name = request.POST.get('name')
    url = request.POST.get('url')

    stype = request.POST.get('stype')

    if stype == 'default':
        page_id = request.POST.get('page_id')
        url = '/app/navaid/{}/'.format(page_id)

    Nav = models.Navigation.objects.get(id=id)
    if name:
        Nav.name = name

    if url:
        Nav.url = url
    Nav.save()

    return redirect(reverse('admins:navigation'))
    pass


'''修改二级导航'''


@_POST
@_POST
@Web_Maintain
@auth_admin
def set_NavigationTwo(request):
    '''修改二级导航'''
    id = request.POST.get('id')
    name = request.POST.get('name')
    url = request.POST.get('url')

    stype = request.POST.get('stype')

    if stype == 'default':
        page_id = request.POST.get('page_id')
        url = '/app/navaid/{}/'.format(page_id)

    print('id------', id)

    Nav = models.Navigation_Two.objects.get(id=id)
    if name:
        Nav.name = name
        Nav.key.name = name
        Nav.key.save()
        Nav.save()

    Nav.save()

    return redirect(reverse('admins:navigation'))
    pass


'''删除首页导航'''


@_POST
@Web_Maintain
@auth_admin
def del_Navigation(request):
    '''
    删除首页导航
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    models.Navigation.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''删除二级导航'''


@_POST
@Web_Maintain
@auth_admin
def del_NavigationTwo(request):
    '''
    删除二级导航
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    print('asdasda', id)
    nav = models.Navigation_Two.objects.get(id=id)
    nav.key.delete()
    nav.delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''首页轮播图管理'''


@_GET
@Web_Maintain
@auth_admin
def broadcast(request):
    '''
    首页轮播图管理
    :param request:
    :return:
    '''
    wapp = models.WareApp.objects.filter()[:20]
    car = models.Carousel.objects.filter()
    content = {
        'wareapp': wapp,
        'car': car
    }
    return render(request, 'defaule/admin/sector/broadcast.html', content)
    pass


'''参加添加轮播图'''


@_POST
@Web_Maintain
@auth_admin
def _add_broadcast(request):
    '''
    参加添加轮播图
    :param request:
    :return:
    '''
    action = request.POST.get('action')
    id = request.POST.get('id')
    url = request.POST.get('url')
    name = request.POST.get('name')
    images = request.FILES.get('image')
    str_images = '{}.{}'.format(datetime_unix(), str(images.name).split('.')[1])

    if action == 'WareApp':
        url = '/app/details/{}/?m=1F'.format(models.WareApp.objects.get(id=id).id)
        models.Carousel(
            name=name,
            image=str_images,
            time_add=TIMEDATES(),
            time_now=TIMEDATES(),
            url=url
        ).save()
        print('WareApp')
        pass

    if action == 'custom':
        models.Carousel(
            name=name,
            image=str_images,
            time_add=TIMEDATES(),
            time_now=TIMEDATES(),
            url=url
        ).save()
        print('custom')
        pass

    from PIL import Image
    from lhwill import settings

    print('images.name', settings.MEDIA_ROOT + '/' + str_images)
    if images:
        img = Image.open(images)
        img.save(settings.MEDIA_ROOT + '/carousel/' + str_images)

    # return HttpResponsePermanentRedirect('/admin/sector/broadcast/')
    return redirect(reverse('admins:broadcast'))
    pass


'''修改轮播图'''


@_POST
@Web_Maintain
@auth_admin
def _set_broadcast(request):
    '''
    修改轮播图
    :param request:
    :return:
    '''
    action = request.POST.get('action')
    id = request.POST.get('id')
    car_id = request.POST.get('car_id')
    url = request.POST.get('url')
    name = request.POST.get('name')
    images = request.FILES.get('image')

    if action == 'WareApp' and id != '-1':
        url = '/app/details/{}/'.format(models.WareApp.objects.get(id=id).id)
        pass

    car = models.Carousel.objects.get(id=car_id)
    if name:
        car.name = name

    if images:
        str_images = '{}.{}'.format(datetime_unix(), str(images.name).split('.')[1])
        car.image = str_images
        print('images.name', settings.MEDIA_ROOT + '/' + str_images)
        img = Image.open(images)
        img.save(settings.MEDIA_ROOT + '/carousel/' + str_images)

    if url and id != '-1':
        car.url = url

    car.save()

    # return HttpResponsePermanentRedirect('/admin/sector/broadcast/')
    return redirect(reverse('admins:broadcast'))
    pass


'''删除轮播图'''


@_POST
@Web_Maintain
@auth_admin
def del_broadcast(request):
    '''
    删除轮播图
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    models.Carousel.objects.get(id=id).delete()
    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


'''商品筛选器'''


@_GET
@Web_Maintain
@auth_admin
def SetupSearch(request):
    '''
    板块-商品筛选器
    :param request:
    :return:
    '''
    classify = models.Classification.objects.filter()
    try:
        setl = Setclassify.objects.filter()[:1].get()
    except:
        setl = None
        pass

    content = {
        'classify': classify,
        'setclassify': setl
    }
    return render(request, 'defaule/admin/sector/setupSearch.html', content)
    pass


def get_WareSetupPrefix(request):
    id = request.GET.get('id')
    There = models.Classification_There.objects.get(id=id)
    setupprefix = []
    for i in models.WareSetupPrefix.objects.filter(key=There):
        if i.t1:
            setupprefix.append({
                'id': i.id,
                'name': i.t1,
                'filter_id': i.filter_id
            })
            pass
        if i.t2:
            setupprefix.append({
                'id': i.id,
                'name': i.t2,
                'filter_id': i.filter_id
            })
            pass
        if i.t3:
            setupprefix.append({
                'id': i.id,
                'name': i.t3,
                'filter_id': i.filter_id
            })
            pass
        if i.t4:
            setupprefix.append({
                'id': i.id,
                'name': i.t4,
                'filter_id': i.filter_id
            })
            pass
        if i.t5:
            setupprefix.append({
                'id': i.id,
                'name': i.t5,
                'filter_id': i.filter_id
            })
            pass

    content = {
        'state': 'success',
        'code': '200',
        'data': setupprefix
    }

    return HttpResponse(json.dumps(content))


'''添加筛选器名称'''


def SetupPrefix(request):
    '''
    添加筛选器名称
    :param request:
    :return:
    '''
    there_id = request.POST.get('there_id')
    t1 = request.POST.get('t1')
    t2 = request.POST.get('t2')
    t3 = request.POST.get('t3')
    t4 = request.POST.get('t4')
    t5 = request.POST.get('t5')

    there = models.Classification_There.objects.get(id=there_id)
    models.WareSetupPrefix(
        t1=t1,
        filter_id=0,
        key=there
    ).save()
    models.WareSetupPrefix(
        t2=t2,
        filter_id=1,
        key=there
    ).save()
    models.WareSetupPrefix(
        t3=t3,
        filter_id=2,
        key=there
    ).save()
    models.WareSetupPrefix(
        t4=t4,
        filter_id=3,
        key=there
    ).save()
    models.WareSetupPrefix(
        t5=t5,
        filter_id=4,
        key=there
    ).save()

    return redirect(reverse('admins:setupsearch'))
    pass


'''添加筛选器'''


@_POST
@Web_Maintain
@auth_admin
def add_filter(request):
    '''
    添加筛选器
    :param request:
    :return:
    '''
    id = request.POST.get('id')
    logger.i(id)

    classifyThere_id = request.POST.get('classifyThere_id')
    name = request.POST.get('name')

    sid = str(id).split(',')[0]
    filter_id = str(id).split(',')[1]

    classify = models.Classification_There.objects.get(id=classifyThere_id)
    WareSetupPrefix = models.WareSetupPrefix.objects.get(id=sid)

    if filter_id == '0':
        models.Brand(
            name=name,
            key=classify,
            PrefixKey=WareSetupPrefix
        ).save()
        pass
    elif filter_id == '1':
        models.ProductType(
            name=name,
            key=classify,
            PrefixKey=WareSetupPrefix
        ).save()
        pass
    elif filter_id == '2':
        models.Technology(
            name=name,
            key=classify,
            PrefixKey=WareSetupPrefix
        ).save()
        pass
    elif filter_id == '3':
        models.Scene(
            name=name,
            key=classify,
            PrefixKey=WareSetupPrefix
        ).save()
        pass
    elif filter_id == '4':
        models.PriceRange(
            name=name,
            key=classify,
            PrefixKey=WareSetupPrefix
        ).save()
    else:
        content = {
            'state': 'error',
            'error': 'filter_id invalid',
            'code': '400'
        }

        return HttpResponse(json.dumps(content))
        pass

    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


@Web_Maintain
@auth_admin
def setupParameterView(request):
    '''
    添加参数信息
    商品详情页的参数
    :param request:
    :return:
    '''
    if request.method == 'GET':
        classifyThere = models.Classification_There.objects.filter()
        WareParProfix = models.WareParProfix.objects.filter()

        content = {
            'classifyThere': classifyThere,
            'wareParProfix': WareParProfix,
            'CHOICES': WareParProfix.model.CHOICES
        }
        return render(request, 'defaule/admin/sector/setupParameter.html', content)
        pass

    if request.method == 'POST':
        There_id = request.POST.get('There_id')

        brand = request.POST.get('brands')  # 品牌
        model = request.POST.get('model')  # 产品型号
        productType = request.POST.get('productType')  # 产品类型
        colorType = request.POST.get('colorType')  # 颜色类型
        coverFunction = request.POST.get('coverFunction')  # 涵盖功能
        velocityType = request.POST.get('velocityType')  # 速度类型
        maximumOriginalSize = request.POST.get('maximumOriginalSize')  # 最大原稿尺寸
        memory = request.POST.get('memory')  # 内存容量
        hardDisk = request.POST.get('hardDisk')  # 硬盘容量
        forPaperCapacity = request.POST.get('forPaperCapacity')  # 供纸容量
        mediumWeight = request.POST.get('mediumWeight')  # 介质重量
        materialDescription = request.POST.get('materialDescription')  # 材料描述
        doubleSidedDevice = request.POST.get('doubleSidedDevice')  # 双面器
        automaticDrafts = request.POST.get('automaticDrafts')  # 自动输稿器
        networkFunction = request.POST.get('networkFunction')  # 网络功能
        highestCv = request.POST.get('highestCv')  # 最高月印量
        falsrom = request.POST.get('falsrom')  # 其他容量
        other = request.POST.get('other')  # 适用机型
        photocopyingSpeed = request.POST.get('photocopyingSpeed')  # 复印速度
        PhotocopyingResolution = request.POST.get('PhotocopyingResolution')  # 复印分辨率
        copySize = request.POST.get('copySize')  # 复印尺寸
        preheatingTime = request.POST.get('preheatingTime')  # 预热时间
        copyPhotocopyingPage = request.POST.get('copyPhotocopyingPage')  # 首页复印时间
        continuityXeroxPages = request.POST.get('continuityXeroxPages')  # 连续复印页数
        zoomRange = request.POST.get('zoomRange')  # 缩放范围
        copyOdds = request.POST.get('copyOdds')  # 复印赔率
        printController = request.POST.get('printController')  # 打印控制器
        printingSpeed = request.POST.get('printingSpeed')  # 打印速度
        printResolution = request.POST.get('printResolution')  # 打印分辨率
        printLanguage = request.POST.get('printLanguage')  # 打印语言
        printingOtherPerformance = request.POST.get('printingOtherPerformance')  # 打印其他性能
        scanningController = request.POST.get('scanningController')  # 扫描控制器
        scanningResolution = request.POST.get('scanningResolution')  # 扫描分辨率
        outputFormat = request.POST.get('outputFormat')  # 输出格式
        scanningOtherPerformance = request.POST.get('scanningOtherPerformance')  # 扫描其他性能
        facsimileController = request.POST.get('facsimileController')  # 传真控制器
        modemSpeed = request.POST.get('modemSpeed')  # 制解调器速度
        dataCompressionMethod = request.POST.get('dataCompressionMethod')  # 数据压缩方式
        faxOtherPerformance = request.POST.get('faxOtherPerformance')  # 传真其他性能
        display = request.POST.get('display')  # 液晶显示屏
        mainframeSize = request.POST.get('mainframeSize')  # 主机尺寸
        weight = request.POST.get('weight')  # 重量
        otherFeatures = request.POST.get('otherFeatures')  # 其他特点
        timeMarket = request.POST.get('timeMarket')  # 上市时间
        optionalAccessories = request.POST.get('optionalAccessories')  # 可选配件
        warrantyTime = request.POST.get('warrantyTime')  # 质保时间
        customerService = request.POST.get('customerService')  # 客服电话
        detailedContent = request.POST.get('detailedContent')  # 详细内容

        content = []
        content.append(['brands', brand, True])
        content.append(['model', model, True])
        content.append(['productType', productType, False])
        content.append(['colorType', colorType, True])
        content.append(['coverFunction', coverFunction, True])
        content.append(['velocityType', velocityType, True])
        content.append(['maximumOriginalSize', maximumOriginalSize, True])
        content.append(['memory', memory, True])
        content.append(['hardDisk', hardDisk, True])
        content.append(['forPaperCapacity', forPaperCapacity, True])
        content.append(['mediumWeight', mediumWeight, True])
        content.append(['materialDescription', materialDescription, True])
        content.append(['doubleSidedDevice', doubleSidedDevice, True])
        content.append(['automaticDrafts', automaticDrafts, True])
        content.append(['networkFunction', networkFunction, True])
        content.append(['highestCv', highestCv, True])
        content.append(['falsrom', falsrom, True])
        content.append(['other', other, True])
        content.append(['photocopyingSpeed', photocopyingSpeed, True])
        content.append(['PhotocopyingResolution', PhotocopyingResolution, True])
        content.append(['copySize', copySize])
        content.append(['preheatingTime', preheatingTime, True])
        content.append(['copyPhotocopyingPage', copyPhotocopyingPage, True])
        content.append(['continuityXeroxPages', continuityXeroxPages, True])
        content.append(['zoomRange', zoomRange, True])
        content.append(['copyOdds', copyOdds, True])
        content.append(['printController', printController, True])
        content.append(['printingSpeed', printingSpeed, True])
        content.append(['printResolution', printResolution, True])
        content.append(['printLanguage', printLanguage, True])
        content.append(['printingOtherPerformance', printingOtherPerformance, True])
        content.append(['scanningController', scanningController, True])
        content.append(['scanningResolution', scanningResolution, True])
        content.append(['outputFormat', outputFormat, True])
        content.append(['scanningOtherPerformance', scanningOtherPerformance, True])
        content.append(['facsimileController', facsimileController, True])
        content.append(['modemSpeed', modemSpeed, True])
        content.append(['dataCompressionMethod', dataCompressionMethod, True])
        content.append(['faxOtherPerformance', faxOtherPerformance, True])
        content.append(['display', display, True])
        content.append(['mainframeSize', mainframeSize, True])
        content.append(['weight', weight, True])
        content.append(['otherFeatures', otherFeatures, True])
        content.append(['timeMarket', timeMarket, True])
        content.append(['optionalAccessories', optionalAccessories, True])
        content.append(['warrantyTime', warrantyTime, True])
        content.append(['customerService', customerService, True])
        content.append(['detailedContent', detailedContent, True])

        content_app = []
        for i in content:
            b = i[1]
            if b:
                content_app.append(i)
            pass

        logger.i('content_app', content_app)

        try:
            k = models.Classification_There.objects.get(id=There_id)
            wpf = models.WareParProfix.objects.get(key=k)
            wpf.filter_name = content_app
            wpf.save()
        except:
            models.WareParProfix(
                filter_name=content_app,
                key=k
            ).save()

        return redirect(reverse('admins:setupparameter'))

        pass
    pass


def get_wareparCHOICES(request):
    CHOICES = []
    for v, x in models.WareParProfix.CHOICES:
        CHOICES.append([v, x])
        pass

    content = {
        'code': 200,
        'data': CHOICES
    }
    return HttpResponse(json.dumps(content))


def get_parter(request):
    id = request.GET.get('id')

    k = models.Classification_There.objects.get(id=id)

    WareParProfix = []

    try:
        wp = models.WareParProfix.objects.get(key=k)
        for l in wp.filter_name:
            logger.i('get_parter', l)
            WareParProfix.append([l[0], l[1], l[2]])
    except:
        pass

    content = {
        'code': 200,
        'data': WareParProfix
    }
    return HttpResponse(json.dumps(content))
    pass


def add_Brand(request):
    name = request.POST.get('name')
    classify = request.POST.get('classify_id')

    models.Brand(
        name=name,
        key=models.Classification.objects.get(id=classify)
    ).save()

    content = {
        'code': 200,
        'data': ''
    }
    return HttpResponse(json.dumps(content))
    pass


class DiscountView(generic.CreateView):
    template_name = 'defaule/admin/sector/Discount.html'



    model = RateClassgUid
    fields = '__all__'

    def get_context_data(self, **kwargs):
        rate = RateClassgUid.objects.filter()
        ware_rate = models.WareAppPrefix.objects.filter(rate_classg_key__isnull=True, wareApp_key__release=True)

        paginator = Paginator(ware_rate, settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        page = self.request.GET.get("page")

        try:
            current_page = paginator.page(page)
        except PageNotAnInteger:  # 页码不是整数
            current_page = paginator.page(1)
        except EmptyPage:  # 页码空或者NUll
            current_page = paginator.page(paginator.num_pages)
            pass

        context = {
            'page': current_page,
            'paginator': paginator,
            'uid_choices': RateClassgUid.uid_choices,
            'rate': rate
        }
        kwargs.update(context)
        return kwargs

    def get_success_url(self):
        return super(DiscountView, self).get_success_url()



def getDiscount(request):
    id = request.POST.get('id')
    dis = []
    for i in models.Classification_There.objects.filter(key=id):
        duton = Discount.objects.get(classif_there=i)

        if duton:
            print('duton', duton.defaule)
            dis.append({
                'id': i.id,
                'name': i.name,
                'url': i.url,
                'time': str(i.time_now.astimezone()).split('+')[0],
                'a1': str(duton.a1),
                'a2': str(duton.a2),
                'a3': str(duton.a3),
                'a4': str(duton.a4),
                'defaule': duton.defaule
            })
        else:
            dis.append({
                'id': i.id,
                'name': i.name,
                'url': i.url,
                'time': str(i.time_now.astimezone()).split('+')[0],
                'defaule': False
            })

    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


@_POST
@Web_Maintain
@auth_admin
def addDiscount(request):
    '''商品分类优惠率设置'''
    create_id = request.POST.get('create_id')
    r1 = request.POST.get('r1')
    a1 = request.POST.get('a1')
    a2 = request.POST.get('a2')
    a3 = request.POST.get('a3')
    a4 = request.POST.get('a4')

    guid = request.POST.get('guid')

    there = models.Classification_There.objects.get(id=create_id)

    if r1 == '0':
        defaule = True
    else:
        defaule = False

    Discount.objects.filter(classif_there=there).delete()

    Discount(
        a1=a1,
        a2=a2,
        a3=a3,
        a4=a4,
        defaule=defaule,
        classif_there=there
    ).save()

    Gusid.objects.filter(key=there).delete()

    Gusid(
        name=there.name,
        guid=guid,
        key=there
    ).save()

    content = {
        'state': 'success',
        'code': '200'
    }

    return HttpResponse(json.dumps(content))
    pass


class searchLevel(JsonView):
    id = None

    def get_models(self):
        try:
            if not self.id:
                self.id = self.request.GET.get('id')
        except AttributeError:
            pass

        logger.i("self.request.GET.get('id')", self.id)
        return models.Classification_There.objects.get(id=self.id)

    def get_context_data(self, **kwargs):
        logger.i(self.get_models().level)
        content = {
            'level': self.get_models().level,
            'code:': 200,
            'state': 'success'
        }
        content.update(kwargs)
        return content
        pass

    def post(self, request, *args, **kwargs):
        id = self.request.POST.get('id')
        level = self.request.POST.get('level')
        logger.i("self.request.POST.get('id')", id)
        a = models.Classification_There.objects.get(id=id)
        a.level = level
        a.save()
        logger.i("self.request.POST.get('level')", level)
        context = {
            'id': id,
            'data': level,
            'code:': 200,
            'state': 'success'
        }
        return self.json_to_response(context)

    pass
