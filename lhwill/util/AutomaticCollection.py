from django.contrib.sitemaps import Sitemap
from app import models
import requests

from lhwill.util.log import log

logger = log(globals())


class ZnanrenSitemaps(Sitemap):
    ''' 网站地图 '''
    changefreq = 'weekly'

    priority = 0.5

    def items(self):
        return models.WareApp.objects.filter(release=True)[:5000000]

    def lastmod(self, obj):
        return obj.time_now.astimezone()


class ActivePush(object):
    '''主动推送'''

    def __init__(self, us='urls', token='q3z85s2X03z96jNI'):
        '''
        初始化推送引擎
        :param us: urls[推送数据] update[更新数据] del[删除数据]
        :param token:
        '''
        self.url = 'http://data.zz.baidu.com/{}?site=https://www.lhwill.com&token={}'.format(us, token)
        self.headers = {"Content-type": "text/plain"}

    def Push(self, date):
        '''
        推送数据 [推送数据 更新数据 删除数据]
        :param date: [推送数据 更新数据 删除数据] 的数据
        :return:
        '''
        html = requests.post(url=self.url, data=str(date), headers=self.headers)

        logger.i('推送数据', date)
        logger.i('推送反馈', html.text)
        pass

    pass
