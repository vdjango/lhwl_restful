from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from app import models
from lhwill.views import error_
from managestage.utli.wrapper import _GET

'''
二级导航 二级商品首页
二级首页和 首页index布局差不多
'''


class IndexView(TemplateView):

    template_name = 'defaule/plate/index.html'


@_GET
def navaid(request, str_navaid):
    try:

        nav = models.Navaid.objects.get(id=str_navaid)
        image = models.NavaidImages.objects.filter(key=nav)
        navmd = []
        for i in models.NavaidMiddle.objects.filter(key=nav):
            nm = []
            for k in models.NavaidMiddleWareApp.objects.filter(key=i):
                waress = []
                ks = models.WareAppPrefix.objects.filter(
                    Q(classifytheres__contains=k.navaid_Keyword) |
                    Q(classifytwos__contains=k.navaid_Keyword)
                )
                for app in ks:

                    if app.wareApp_key.release == True:
                        print('OK --- ', app.wareApp_key.release)

                        waress.append({
                            'name': app.wareApp_key.name,
                            'money': app.wareApp_key.money,
                            'characteristic': app.wareApp_key.characteristic,
                            'commodity_description': app.wareApp_key.commodity_description,
                            'images': models.images.objects.filter(key=app.wareApp_key)[:1].get(),
                            'unix': app.wareApp_key.unix,
                            'time_add': app.wareApp_key.time_add,
                            'time_now': app.wareApp_key.time_now
                        })
                        print('END --- ', app.wareApp_key.release)

                nm.append({
                    'id': k.id,
                    'navaid_name': k.navaid_name,
                    'navaid_Keyword': k.navaid_Keyword,
                    'navaid_number': k.navaid_number,
                    'wareapp': waress
                })

            navmd.append({
                'navaid_name': i.navaid_name,
                'navaid_urls': i.navaid_urls,
                'navaid_images': i.navaid_images,
                'Keyword': nm
            })

        content = {
            'nav': nav,
            'images': image,
            'navmd': navmd
        }
        return render(request, 'defaule/navaid/index.html', content)
    except:
        return error_(request)
    pass
