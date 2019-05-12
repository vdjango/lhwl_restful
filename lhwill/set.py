from managestage import models


class qq(object):
    def __init__(self):
        self.qq = models.appid.objects.filter(apptype='qq')
        pass

    def get_appid(self):
        q = self.qq
        try:
            id = q[0].appid
        except Exception as e:
            id = None
            pass
        return id
        pass

    def get_appkey(self):
        q = self.qq
        try:
            id = q[0].appkey
        except Exception as e:
            id = None
            pass
        return id
        pass


class weixin(object):
    def __init__(self):
        self.weixin = models.appid.objects.filter(apptype='weixin')
        pass

    def get_appid(self):
        weixi = self.weixin
        try:
            id = weixi[0].appid
        except Exception as e:
            id = ''
            pass
        return id
        pass


    def get_appkey(self):
        weixi = self.weixin
        try:
            key = weixi[0].appkey
        except Exception as e:
            key = ''
            pass
        return key
        pass




