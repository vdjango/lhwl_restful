import json
import os
import random

from PIL import ImageFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins, views
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account.util.decorator import auth_admin
from app import models as app
from lhwill import settings
from lhwill.util.log import log
from managestage.utli.wrapper import Web_Maintain

logger = log(globals())


class IndexV1(mixins.ListModelMixin, views.APIView):
    '''
    ## auth:
    * auth-token: 获取Token
    * auth-token-refresh: 刷新Token
    * auth-token-verify: 验证Token

    ## root:
    * model: Models模型数据接口
    * method: 功能相关接口
    * admin: 后台管理相关接口
    '''

    def get(self, request, *args, **kwargs):
        context = {}
        root = {}

        context.update({
            'auth': {
                'authorization': '{}/{}'.format(settings.HTTP_API_HOST, 'authorization/'),
                'authorization-refresh': '{}/{}'.format(settings.HTTP_API_HOST, 'authorization-refresh/'),
                'authorization-verify': '{}/{}'.format(settings.HTTP_API_HOST, 'authorization-verify/'),
            }
        })

        root.update({
            'model': '{}/{}'.format(settings.HTTP_API_HOST, 'v1/'),
            'method': '{}/{}'.format(settings.HTTP_API_HOST, 'v1/logical/')
        })

        if request.user.is_authenticated:
            root.update({
                'admin': '{}/{}'.format(settings.HTTP_API_HOST, 'v1/admin/')
            })

        context.update({
            'root': root
        })

        context.update({
            'novel': '{}/{}'.format(settings.HTTP_API_HOST, 'v2/')
        })

        context.update({
            'version': '0.0.1',
        })
        return Response(context)
    pass


class IndexV2(mixins.ListModelMixin, views.APIView):
    '''
    ## auth:
    * auth-token: 获取Token
    * auth-token-refresh: 刷新Token
    * auth-token-verify: 验证Token

    ## root:
    * model: Models模型数据接口
    * method: 功能相关接口
    * admin: 后台管理相关接口
    '''

    version = '0.2.0'

    def get_host_path(self):
        path = '{}{}'.format(self.request.get_host(), self.request.path)
        host = ''
        if self.request.is_secure():
            host = 'https://{}'.format(path)
        else:
            host = 'http://{}'.format(path)
            pass
        return host

    def get(self, request, *args, **kwargs):
        context = {}
        root = {}
        setting = {}
        context.update({
            'auth': {
                'authorization': '{}{}'.format(self.get_host_path(), 'authorization/'),
                'authorization-refresh': '{}{}'.format(self.get_host_path(), 'authorization-refresh/'),
                'authorization-verify': '{}{}'.format(self.get_host_path(), 'authorization-verify/'),
            }
        })

        root.update({
            'model': {
                'public': '{}{}'.format(self.get_host_path(), 'model-public/'),
                'private': '{}{}'.format(self.get_host_path(), 'model-private/'),
            },
            'method': {
                'public': '{}{}'.format(self.get_host_path(), 'method-public/'),
                'private': '{}{}'.format(self.get_host_path(), 'method-private/'),
            },
            'search': {
                'goods': '{}{}'.format(self.get_host_path(), 'search/')
            }
        })

        setting.update({
            'pagination': {
                'pageSize': settings.PAGE_SIZE,
            },
            'language_code': settings.LANGUAGE_CODE,
            'zones': {
                'TIME_ZONE': settings.TIME_ZONE,
                'USE_I18N': settings.USE_I18N,
                'USE_L10N': settings.USE_L10N,
                'USE_TZ': settings.USE_TZ
            }
        })

        if request.user.is_authenticated:
            root.update({
                'admin': '{}/{}'.format(self.get_host_path(), 'v2/admin/')
            })

        context.update({
            'root': root,
            'setting': setting,
            'version': self.version,
        })

        return Response(context)

    pass


@api_view(['GET'])
def indexApiRoot(request):
    """
    ## auth:
    * auth-token: 获取Token
    * auth-token-refresh: 刷新Token
    * auth-token-verify: 验证Token

    ## root:
    * model: Models模型数据接口
    * method: 功能相关接口
    * admin: 后台管理相关接口

    """
    context = {}
    root = {}

    context.update({
        'auth': {
            'auth-token': '{}/{}'.format(settings.HTTP_API_HOST, 'auth-token/'),
            'auth-token-refresh': '{}/{}'.format(settings.HTTP_API_HOST, 'auth-token-refresh/'),
            'auth-token-verify': '{}/{}'.format(settings.HTTP_API_HOST, 'auth-token-verify/'),
        }
    })

    root.update({
        'model': '{}/{}'.format(settings.HTTP_API_HOST, 'v1/'),
        'method': '{}/{}'.format(settings.HTTP_API_HOST, 'v1/logical/'),
    })

    if request.user.is_authenticated:
        root.update({
            'admin': '{}/{}'.format(settings.HTTP_API_HOST, 'v1/admin/')
        })

    context.update({
        'root': root
    })

    context.update({
        'novel': '{}/{}'.format(settings.HTTP_API_HOST, 'v2/')
    })

    context.update({
        'version': '0.0.1',
    })

    """
    asdasd
    """

    return Response(context)


def get_Choice(request):
    id = request.POST.get('id')
    print(id)
    choice = []
    try:
        wareapp = app.WareApp.objects.get(id=id)
    except:
        content = {
            'state': 'error',
            'error': '商品不存在',
            'code': '400'
        }
        return HttpResponse(json.dumps(content))

    for i in app.Choice.objects.filter():
        a = []
        for q in app.Lease.objects.filter(ware_key=wareapp):
            b = []
            for w in app.Lease.objects.filter(ware_key=wareapp):
                b.append({
                    'id': w.id,
                    'name': w.name,
                    'defaule': w.defaule
                })

            a.append({
                'id': q.id,
                'name': q.name,
                'defaule': q.defaule,
                'icetwo': b
            })

        choice.append({
            'id': i.id,
            'name': i.name,
            'iceone': a,
        })

    print(choice)

    content = {
        'state': 'success',
        'data': choice,
        'code': '200'
    }
    return HttpResponse(json.dumps(content))


@csrf_exempt
@Web_Maintain
@auth_admin
def imageUp(request):
    unix = request.GET.get('unix')
    stype = request.GET.get('type')
    pathimgae = request.GET.get('path')
    create = request.GET.get('create')
    image = request.FILES.get('upfile')
    url = '/media/images/{}'.format(unix)
    name = buildFileName(image.name)

    if pathimgae:
        path = '{}{}/{}'.format(settings.BASE_DIR, url, pathimgae)
        save_path = '{}/{}'.format(path, name)
        url = '{}/{}/{}'.format(url, pathimgae, name)
    else:
        path = '{}{}'.format(settings.BASE_DIR, url)
        save_path = '{}/{}'.format(path, name)
        url = '{}/{}'.format(url, name)

    if not os.path.isdir(path):
        os.makedirs(path)
        pass

    parser = ImageFile.Parser()
    for chunk in image.chunks():
        parser.feed(chunk)
    img = parser.close()
    img.save(save_path)

    if create == 'wareapp':
        try:
            logger.i('Api WareApp', '获取到UNIX')
            app.images(
                image=url,
                key=app.WareApp.objects.get(unix=unix)
            ).save()
        except:
            content = {
                'originalName': '',
                'name': name,
                'url': url,
                'size': '',
                'type': stype,
                'state': 'ERROR',
                'code': 500
            }
            print('RETURN', content)
            return HttpResponse(json.dumps(content))

            pass
        pass

    print(request.GET)
    content = {
        'originalName': '',
        'name': name,
        'url': url,
        'size': '',
        'type': stype,
        'state': 'SUCCESS',
        'code': 200
    }
    return HttpResponse(json.dumps(content))
    pass


def buildFileName(filename):
    from managestage.utli.datetimenow import datetimenow
    dt = datetimenow()
    name, ext = os.path.splitext(filename)

    return "%s" % (dt.strftime("%Y-%m-%d-%M-%H-%S-{0}{1}".format(random.randint(1, 999999), ext)))
