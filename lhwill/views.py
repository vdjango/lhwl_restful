import json
import os
import pathlib
import random
import shutil

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.template import Context
from django.views import View
from haystack.forms import SearchForm

from app import models
from lhwill.settings import BASE_DIR
from lhwill.util import log
from managestage.utli import datetimenow

ListModels = []


class ImportWareApp(object):

    def __init__(self, url, unix):
        self.url = url
        self.unix = unix
        self.name = ''
        self.images = None
        self.money = 0
        self.HeadList = []
        self.ConList = []
        self.content = []
        self.log_ware = []
        pass

    def get_absloute_url(self, *args):
        return os.path.join(*args).replace('\\', '/')

    def dirContent(self, dirc, disUrl):
        '''
        商品详情页
        :param url:
        :param dirc:
        :return:
        '''
        urls = self.get_absloute_url(self.url, dirc)
        if os.path.exists(urls):
            for dircs in os.listdir(urls):
                if not 'Thumbs.db' in dircs:
                    a = self.get_absloute_url(BASE_DIR, self.url, dirc, dircs)
                    if os.path.isdir(a):
                        for root, dirnames, filenames in os.walk(a):
                            for filepath in filenames:

                                name = ''
                                for i in '{}-{}.{}'.format(
                                        str(datetimenow.datetimenow()).split('.')[0],
                                        random.randint(1000, 9000),
                                        str(filepath).split('.')[1]
                                ).split(':'):
                                    name += i
                                    pass

                                b = self.get_absloute_url(disUrl, name)

                                self.ConList.append(
                                    (filepath.split('.')[0], self.get_absloute_url('/', b)))
                                self.ConList.sort(key=lambda k: k[0])
                                log.i(globals(), 'ConList', self.ConList)

                                b = self.get_absloute_url(BASE_DIR, b)
                                shutil.copyfile(self.get_absloute_url(a, filepath), b)

                            # log.i(globals(), '商品详情页：  ', os.path.join(a, filepath), '->', b)
                            pass
                        pass
                    else:
                        name = ''
                        for i in '{}-{}.{}'.format(
                                str(datetimenow.datetimenow()).split('.')[0],
                                random.randint(1000, 9000),
                                str(dircs).split('.')[1]
                        ).split(':'):
                            name += i
                            pass

                        b = self.get_absloute_url(disUrl, name)
                        self.ConList.append((dircs.split('.')[0], self.get_absloute_url('/', b)))
                        self.ConList.sort(key=lambda k: k[0])
                        log.i(globals(), 'ConList', self.ConList)
                        b = self.get_absloute_url(BASE_DIR, b)
                        shutil.copyfile(a, b)
                        log.i(globals(), '商品详情页：  ', a, '->', b)
                    pass
                pass
            pass
        pass

    def dirHead(self, dirc, disUrl, path_image):

        '''
        商品展示图
        :param url:
        :param dirc:
        :return:
        '''

        name = ''
        for i in '{}-{}.{}'.format(
                str(datetimenow.datetimenow()).split('.')[0],
                random.randint(1000, 9000),
                str(dirc).split('.')[1]
        ).split(':'):
            name += i
            pass

        a = self.get_absloute_url(BASE_DIR, self.url, dirc)
        b = self.get_absloute_url(disUrl, 'head', name)

        path_image_b = self.get_absloute_url(path_image, 'head', name)

        log.i(globals(), '商品展示图：  ', dirc.split('.')[0], '->', path_image_b)

        if not self.images:
            self.images = self.get_absloute_url('/', path_image_b)
            print('商品展示图 self.images', self.images)

        self.HeadList.append((dirc.split('.')[0], self.get_absloute_url('/', path_image_b)))

        self.HeadList.sort(key=lambda k: k[0])
        log.i(globals(), 'HeadList', self.HeadList)

        b = self.get_absloute_url(BASE_DIR, b)

        shutil.copyfile(a, b)

        pass

    def addModelsObjects(self):
        c = self.content
        for i in c:
            head = i['a']
            cont = i['b']
            name = i['n']
            money = i['m']
            unix = i['u']

            text = ''
            for i in cont:
                text += '''
				<p>
				    <img src="{}"/>
				</p>
				'''.format(i[1])
                log.i(globals(), '类型cont', i, i[1], unix, text)
                pass

            t = datetimenow.datetimenow()
            ware = models.WareApp(
                name=name,
                money=money,
                connet=text,
                image=self.images,
                unix=unix,
                time_add=t,
                time_now=t
            )
            ware.save()

            for image in head:
                log.i(globals(), '类型head', image, image[1])
                models.images(
                    image=image[1],
                    key=ware
                ).save()

            models.parameter(
                model=name,
                key=ware
            ).save()

        pass

    def dirList(self):

        dirHeadList = []
        dirContentList = []
        log.i(globals(), '--------------------------------Start--------------------------------')
        if os.path.exists(self.url):
            dirs = os.listdir(self.url)
            print('sort', dirs.sort())

            for dis in dirs:
                url = self.get_absloute_url(self.url, dis)
                disUrl = self.get_absloute_url('media', 'images', ''.join(self.unix))

                path_image = self.get_absloute_url('images', ''.join(self.unix))

                Urls = self.get_absloute_url(BASE_DIR, disUrl)
                if not 'Thumbs.db' in dis:
                    h, c = None, None

                    if not pathlib.Path(Urls).exists():
                        os.makedirs(Urls)

                    if not pathlib.Path(self.get_absloute_url(Urls, 'head')).exists():
                        os.makedirs(self.get_absloute_url(Urls, 'head'))

                    if os.path.isfile(url):
                        self.dirHead(dis, disUrl, path_image)  # 商品展示图

                    elif os.path.isdir(url):
                        self.dirContent(dis, disUrl)  # 商品详情页
                        self.name = dis
                    else:
                        log.i(globals(), '导入商品失败', url)
                        self.log_ware.append({
                            'url': url,
                            'name': self.name
                        })
                        pass

                    self.log_ware.append({
                        'name': '商品导入成功    {}'.format(Urls)
                    })

                    pass

            self.content.append({
                'a': self.HeadList,
                'b': self.ConList,
                'u': self.unix,
                'n': self.name,
                'm': 0
            })

            log.i(globals(), self.content)

    def getLog_ware(self):
        '''
        获取上传日志
        :return:
        '''
        return self.log_ware
        pass


def error_(request, code=404, error=None, title=None, page=None, content=None):
    if not content:
        if code == 404:
            page = 'page not found'
            title = '对不起，您查找的页面不存在！'
            content = '当您看到这个页面,表示您的访问出错,这个错误是您打开的页面不存在,请确认您输入的地址是正确的,如果是在本站点击后出现这个页面,请联系站长进行处理,或者请通过下边的搜索重新查找资源!'

        if code == 403:
            page = 'prohibition of access'
            title = '对不起，您查找的页面被禁止访问！'
            content = '当您看到这个页面,表示您的访问出错,这个错误是您打开的页面访问被拒绝,请确认您输入的地址是正确的,如果是在本站点击后出现这个页面,请联系站长进行处理,或者请通过下边的搜索重新查找资源!'

    connet = {
        'error': error,
        'code': code,
        'page': page,
        'title': title,
        'content': content,
    }
    return render_to_response('defaule/error/index.html', context=connet, status=404)


def query(request):
    return render(request, 'defaule/app/search-text.html')


def full_search(request):
    sform = SearchForm(request.GET)

    posts = sform.search()
    template = 'defaule/app/search-text.html'
    c = Context({'posts': posts})
    return render_to_response(template, c)


class JsonView(View):

    def extra_context(self, **kwargs):
        return {**kwargs}

    def get_context_data(self, **kwargs):
        extra_context = self.extra_context()
        if 'view' not in kwargs:
            kwargs['view'] = self
        if extra_context is not None:
            kwargs.update(extra_context)
        return kwargs

    def json_to_response(self, context):
        return HttpResponse(json.dumps(context))
        pass

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        return self.json_to_response(context)

    pass
