# -*- coding: utf-8 -*-
#
# @Time     : 2018/11/24 17:02
# @Author   : Merrill
# @Contact  : merrill@vdjango.com
# @File     : UnzipFileutils.py
# @Date     : 2018/11/24
# @Software : PyCharm
# @Desc     : 解压缩包工具类

import os
import zipfile

from api.util.RemoveDisFiles import remove_all
from lhwill.util.log import log

logger = log(globals())


class xzipfile(object):

    def __init__(self, path):
        '''
        self.name 解压文件夹名字
        self.out 解压目标存放位置
        self.pathOut 压缩包解压位置
        :param path: 压缩包路径
        '''
        self.azip = zipfile.ZipFile(os.path.join(path), 'r')
        self.path = os.path.join(path)
        self.out = self.getPath()
        self.name = self.getName()
        self.pathOut = '{}/{}'.format(self.out, self.name)
        pass

    def getUrl(self):
        import platform
        if 'windows' in platform.system().lower():
            url = self.path.split('\\')
        else:
            url = str(self.path).split('/')
            pass

        return url

    def getPath(self):
        url = self.getUrl()
        return '/'.join(url[0:-1])
        pass

    def getName(self):
        url = self.getUrl()
        return '.'.join(str(url[-1]).split('.')[0:-1])
        pass

    def endecode(self, path):
        pass

    def garcode(self, path):
        '''
        编码转换，解决Windows打包压缩包解压中文乱码
        :param path:
        :return:
        '''
        for dir in os.listdir(path):
            url = '{}/{}'.format(path, dir)
            if os.path.isdir(url):
                nurl = '{}/{}'.format(path, dir.encode('cp437').decode("gbk"))
                logger.i('nurl', nurl)
                try:
                    os.rename(url, nurl)
                except FileExistsError as e:
                    e.args
                    remove_all(nurl)
                    remove_all(url)
                    return False, '文件已存在的时候不能替换目录[编码转换]，以删除，请重试'
                    pass

                for file in os.listdir(nurl):
                    filurl = '{}/{}'.format(nurl, file)
                    if os.path.isfile(filurl):
                        filnurl = '{}/{}'.format(nurl, file.encode('cp437').decode("gbk"))
                        os.rename(filurl, filnurl)
                        pass
                    pass

                self.garcode(nurl)
                if self.pathOut != nurl:
                    self.pathOut = nurl
                pass
            pass

        return True, None
        pass

    def Unzip(self):
        '''
        解压Zip压缩包
        :return:
        '''
        zip_list = self.azip.namelist()

        for zip_file in zip_list:
            self.azip.extract(zip_file, self.out)
            pass

        try:
            _code, _mess = self.garcode(self.out)
            if not _code:
                return False, _mess
        except Exception as e:
            self.close()
            return False, '{}'.format(e.args[1])

        return True, None

    def close(self):
        self.azip.close()
