# -*- coding: utf-8 -*-
#
# @Time     : 2018/11/24 17:50
# @Author   : Merrill
# @Contact  : merrill@vdjango.com
# @File     : ImportGoodsutils.py
# @Date     : 2018/11/24
# @Software : PyCharm
# @Desc     : 商品导入工具类
#
import os
import shutil

from app.models import WareApp, images
from lhwill import settings
from lhwill.util.log import log
from managestage.models import ImportGoods

logger = log(globals())


class ImportGoodsmodel(object):
    html_image = '<img src="{}{}" class="html-images"/>'.format(settings.HTTP_HOST, '{}')

    def __init__(self, pk, path_out):
        self.model = WareApp
        self.model_images = images
        self.model_import = ImportGoods.objects.get(pk=pk)
        self.path = path_out
        self.url = '/images/{}'

        self.path_graphic = None

        self.first = []
        self.graphic = []

        self._first = []
        self._graphic = []

        pass

    def remove_all(self, path):
        '''
        Delete directories and files
        :param path: Deleted directory path
        :return:
        '''
        for dir in os.listdir(path):
            url = '{}/{}'.format(path, dir)
            if os.path.isdir(url):
                self.remove_all(url)
            else:
                os.remove(url)
                pass
            pass

        if os.path.exists(path):
            os.removedirs(path)
        pass

    def sortitems(self, sort):
        '''
        Dict sorting
        :param sort:
        :return:
        '''
        _dis_ = {}
        for value in list(sort):
            v_id = int(str(value).split('.')[0:-1][0])
            v_suffix = str(value).split('.')[-1]
            _dis_.update({
                v_id: v_suffix
            })
            pass
        return sorted(_dis_.items(), key=lambda d: d[0], reverse=False)

    def _getfirst(self):
        '''
        Here is the big picture of the goods
        :return:
        '''
        for dir in os.listdir(self.path):
            url = '{}/{}'.format(self.path, dir)
            if os.path.isfile(url) and 'Thumbs.db' not in dir:
                self.first.append(dir)
                pass
            pass

        if self.first is not None:
            self.first = self.sortitems(self.first)
            pass

        # for i in self.first:
        #     logger.i('html first', i)

        pass

    def _getgraphic(self):
        '''
        Graphic details
        :return:
        '''

        for dir in os.listdir(self.path):
            url = '{}/{}'.format(self.path, dir)
            if os.path.isdir(url):

                for vdir in os.listdir(url):
                    path = '{}/{}'.format(url, vdir)
                    if os.path.isfile(path) and 'Thumbs.db' not in vdir:
                        if self.path_graphic is None:
                            self.path_graphic = url
                            pass
                        self.graphic.append(vdir)
                        pass
                    pass

                pass
            pass

        if self.graphic is not None:
            self.graphic = self.sortitems(self.graphic)
            pass
        pass

    def getheadurl(self, first):
        '''
        Gets the first graph path
        :param first:
        :return:
        '''
        head = []
        for i in first:
            head.append('{}/head/{}'.format(self.url.format(self.model_import.unix), '{}.{}'.format(i[0], i[-1])))
        return head
        pass

    def getbodyurl(self, graphic):
        '''
        Get the image and text details url
        :param graphic:
        :return:
        '''
        body = []
        for i in graphic:
            body.append('{}/{}'.format(self.url.format(self.model_import.unix), '{}.{}'.format(i[0], i[-1])))
        return body

    def gethtml(self, graphic):
        '''
        Generate graphic and text detail HTML text
        :param graphic:
        :return:
        '''
        html = []
        for i in self.getbodyurl(graphic):
            html.append('{}'.format(self.html_image.format('/media{}'.format(i))))
            pass

        return ' '.join(html)

    def objects(self):
        '''
        Import commodity data
        :return:
        '''
        app = self.model.objects.create(
            name=str(self.model_import.name).split('.zip')[0],
            connet=self.gethtml(self.graphic),
            image=self.getheadurl(self.first)[0],
            unix=self.model_import.unix
        )
        for image in self.getheadurl(self.first):
            self.model_images.objects.create(
                key=app,
                image=image
            )
        pass

    def copy(self):
        '''
        Copy the file
        :return:
        '''
        for first in self.first:
            self._first.append('{}/{}'.format(self.path, '{}.{}'.format(first[0], first[1])))
            pass

        for graphic in self.graphic:
            self._graphic.append('{}/{}'.format(self.path_graphic, '{}.{}'.format(graphic[0], graphic[1])))
            pass

        newurl = '{}/media/images/{}/head'.format(settings.BASE_DIR, self.model_import.unix)

        if os.path.exists(newurl):
            return False

        os.makedirs(newurl)

        for first in self._first:
            shutil.copy(os.path.join(first), os.path.join(newurl))
            pass

        newurl = '{}/media/images/{}'.format(settings.BASE_DIR, self.model_import.unix)

        for graphic in self._graphic:
            shutil.copy(os.path.join(graphic), os.path.join(newurl))
            pass

        return True

    def introduction(self):
        '''

        :return:
        '''

        try:
            self._getfirst()
            self._getgraphic()
        except ValueError:
            return False, '压缩包格式错误，可能存在非数字命名'

        if not self.copy():
            return False, '商品已经被导入过了，无需导入'

        self.objects()

        self.remove_all(self.path)

        self.model_import.status = 0
        self.model_import.save()
        return True, '商品以导入'
        pass

    pass
