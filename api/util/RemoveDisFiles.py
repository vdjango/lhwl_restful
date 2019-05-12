# -*- coding: utf-8 -*-
#
# @Time     : 2018/11/26 11:05
# @Author   : Merrill
# @Contact  : merrill@vdjango.com
# @File     : RemoveDisFiles.py
# @Date     : 2018/11/26
# @Software : PyCharm
# @Desc     : 文件删除工具类
#
import os


def remove_all(path):
    '''
    Delete directories and files
    :param path: Deleted directory path
    :return:
    '''
    if not os.path.exists(path):
        return

    if os.path.isfile(path):
        os.remove(path)
        return

    for dir in os.listdir(path):
        url = '{}/{}'.format(path, dir)
        if os.path.isdir(url):
            remove_all(url)
        else:
            os.remove(url)
            pass
        pass

    if os.path.exists(path):
        os.removedirs(path)
    pass
