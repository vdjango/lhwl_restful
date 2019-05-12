import json
import os

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse


from account.util.decorator import auth_admin
from app import models
from managestage.form import page_From
from managestage.utli.wrapper import _GET, Web_Maintain



def ImageSave(dest, reqfile):
    if os.path.exists(dest):
        os.remove(dest)
    with open(dest, "wb+") as destination:
        for chunk in reqfile.chunks():
            destination.write(chunk)
    return dest

@Web_Maintain
@auth_admin
def Page_createView(request):
    if request.method == 'GET':
        s = models.Navaid.objects.filter()
        a = []
        for ks in models.Navigation_Two.objects.filter():
            if len(s) > 1:
                for i in models.Navaid.objects.filter():
                    if i.key_id != ks.id:
                        a.append({
                            'id': ks.id,
                            'name': ks.name,
                            'url': ks.url
                        })
            else:
                a.append({
                    'id': ks.id,
                    'name': ks.name,
                    'url': ks.url
                })
            pass

        content = {
            'nav': a
        }
        return render(request, 'defaule/admin/page/create.html', content)

    if request.method == 'POST':
        nav_id = request.POST.get('nav_id')
        name = request.POST.get('site_navaid_name')
        tags = request.POST.get('site_navaid_tags')
        images = request.FILES.getlist('site_navaid_images')

        button = request.POST.get('site_navaid_button')

        page = page_From.pageFrom(request.POST)
        pageImage = page_From.pageImageForm(request.FILES)

        if page.is_valid() and pageImage.is_valid():
            k = models.Navigation_Two.objects.get(id=nav_id)
            if not name:
                name = k.name

            if not button:
                button = '30秒快速预览商品'

            if models.Navaid.objects.filter(key=k):
                k = models.Navigation_Two.objects.filter()
                content = {
                    'nav': k,
                    'error': '页面已存在，每个对象只允许一个页面'
                }
                return render(request, 'defaule/admin/page/create.html', content)

            nav = models.Navaid(
                site_navaid_name=name,
                site_navaid_tags=tags,
                site_navaid_button=button,
                key=k
            )

            nav.save()


            print(images)

            for i in images:
                models.NavaidImages(
                    images=i,
                    key=nav
                ).save()
                file_content = ContentFile(i.read())
        else:
            k = models.Navigation_Two.objects.filter()
            content = {
                'nav': k,
                'error': page.errors
            }
            return render(request, 'defaule/admin/page/create.html', content)

        return redirect(reverse('admins:page_create'))
    pass


@Web_Maintain
@auth_admin
def Page_NavPlate(request):
    if request.method == 'GET':
        page = models.Navaid.objects.filter()

        content = {
            'page': page,
            '': '',
        }
        return render(request, 'defaule/admin/page/nav_plate.html', content)

    if request.method == 'POST':
        nav_id = request.POST.get('nav_id')
        navaid_name = request.POST.get('navaid_name')
        navaid_urls = request.POST.get('navaid_urls')
        navaid_images = request.FILES.get('navaid_images')

        pageNav = page_From.pageNavPlateForm(request.POST, request.FILES)
        if pageNav.is_valid():
            print('ok')
            k = models.Navaid.objects.get(id=nav_id)

            models.NavaidMiddle(
                navaid_name=navaid_name,
                navaid_urls=navaid_urls,
                navaid_images=navaid_images,
                key=k
            ).save()
            file_content = ContentFile(navaid_images.read())
        else:
            page = models.Navaid.objects.filter()
            content = {
                'page': page,
                'error': pageNav.errors
            }
            print('no')
            return render(request, 'defaule/admin/page/nav_plate.html', content)

        return redirect(reverse('admins:navplate'))
        pass


@Web_Maintain

def Page_NavWareAppKeyword(request):
    if request.method == 'GET':
        nav = models.Navaid.objects.filter()
        content = {
            'nav': nav
        }
        return render(request, 'defaule/admin/page/navkeyword.html', content)

    if request.method == 'POST':
        navm_id = request.POST.get('navm_id')
        navaid_name = request.POST.get('navaid_name')
        navaid_Keyword = request.POST.get('navaid_Keyword')
        navaid_number = request.POST.get('navaid_number')

        forms = page_From.pageNavWareAppeForm(request.POST)
        if forms.is_valid():
            k = models.NavaidMiddle.objects.get(id=navm_id)
            models.NavaidMiddleWareApp(
                navaid_name=navaid_name,
                navaid_Keyword=navaid_Keyword,
                navaid_number=navaid_number,
                key=k
            ).save()
            pass
        else:
            nav = models.Navaid.objects.filter()
            content = {
                'nav': nav,
                'error': forms.errors
            }
            return render(request, 'defaule/admin/page/navkeyword.html', content)

        return redirect(reverse('admins:navkeyword'))
        pass
    pass



@_GET
@Web_Maintain
@auth_admin
def get_navaid(request):
    id = request.GET.get('id')
    nav = []
    try:
        i = models.Navaid.objects.get(id=id)
        for i in models.NavaidMiddle.objects.filter(key=i):
            nav.append({
                'id': i.id,
                'name': i.navaid_name
            })

        content = {
            'code': 202,
            'data': nav
        }
        return HttpResponse(json.dumps(content))
    except:
        content = {
            'state': 'error',
            'error': '未获取到相关页面信息',
            'code': 404
        }
        return HttpResponse(json.dumps(content), status=404)























