from lhwill import settings
from managestage import models

'''全局'''

'''
全局-站点设置-站点属性
'''


class systemsetup(object):
    def __init__(self):
        self.sitesystem = models.systemSetup.objects.filter()
        pass

    def get_sitename(self):
        '''
        站点名称
        :return:
        '''
        if self.sitesystem:
            return self.sitesystem[0].site_name
        return None

    def get_sitetags(self):
        '''
        站点描述[TITLE - TAGS]
        :return:
        '''
        if self.sitesystem:
            return self.sitesystem[0].site_tags
        return None

    def get_url(self):
        '''
        站点地址
        :return:
        '''


        return settings.HTTP_HOST

    def get_email(self):
        '''
        管理员邮箱
        :return:
        '''
        if self.sitesystem:
            return self.sitesystem[0].site_email
        return None

    def get_icp(self):
        '''
        ICP 备案信息
        :return:
        '''
        if self.sitesystem:
            return self.sitesystem[0].site_icp
        return None

    def get_can_register(self):
        '''
        开放注册
        :return:
        '''
        if self.sitesystem:
            return self.sitesystem[0].site_can_register
        return None

    def get_allow_sending_statistics(self):
        '''
        统计信息[发送程序使用情况统计信息以帮助开发]
        :return:
        '''
        if self.sitesystem:
            return self.sitesystem[0].site_allow_sending_statistics
        return None


'''
全局-站点设置-站点维护模式
'''


class MainTain(object):
    '''
    站点维护模式
    '''

    def __init__(self):
        self.tain = models.maintain.objects.filter(inta_allwo=True)
        pass

    def get_tain(self):
        '''
        获取站点维护模式
        :return: T/F
        '''
        if self.tain:
            return True
        return False

    def get_content(self):
        '''
        本次维护说明
        :return:
        '''
        if self.tain:
            return self.tain[0].inta_info
        return None

    def get_datatime(self):
        '''
        预计维护结束时间
        :return:
        '''
        if self.tain:
            return self.tain[0].inta_datatime

    pass
