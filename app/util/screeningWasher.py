from app import models
from lhwill.util.log import log

logger = log(globals())


class modelsObjectsfilter(object):
    '''
    实现商品搜索筛选器功能
    '''

    def __init__(self, search, modrls, *args, **kwargs):
        self.search = search
        self.modrls = modrls
        self.args = args
        self.kwargs = kwargs
        try:
            if self.kwargs['method'] == 'jieba':
                self.jiebaFilter()
        except KeyError:
            self.gain()
        pass

    def gain(self):
        '''
        全部分类 筛选
        :return:
        '''
        A1 = self.kwargs['a1']
        A2 = self.kwargs['a2']
        A3 = self.kwargs['a3']
        A4 = self.kwargs['a4']
        A5 = self.kwargs['a5']

        logger.i('', self.kwargs)

        fil = {}

        if A1:
            fil_A1 = {
                'brand_key_id': A1,
            }
            fil.update(fil_A1)
        if A2:
            fil_A2 = {
                'producttype_key': A2,
            }
            fil.update(fil_A2)
        if A3:
            fil_A3 = {
                'technology_key': A3,
            }
            fil.update(fil_A3)
        if A4:
            fil_A4 = {
                'scene_key': A4,
            }
            fil.update(fil_A4)
        if A5:
            fil_A5 = {
                'pricerange_key': A5
            }
            fil.update(fil_A5)
            pass

        if fil:
            fil = {
                'classifythere_key__name': self.search,
                **fil
            }
            self.modrls = self.modrls.filter(**fil)
        pass

    def jiebaFilter(self):
        '''
        商品搜索 筛选
        :return:
        '''

        A1 = self.kwargs['a1']
        A2 = self.kwargs['a2']
        A3 = self.kwargs['a3']
        A4 = self.kwargs['a4']
        A5 = self.kwargs['a5']

        fil = {}

        if A1:
            fil_A1 = {
                'brand_key_id': A1,
            }
            fil.update(fil_A1)
            pass
        if A2:
            fil_A2 = {
                'producttype_key': A2,
            }
            fil.update(fil_A2)
            pass
        if A3:
            fil_A3 = {
                'technology_key': A3,
            }
            fil.update(fil_A3)
            pass
        if A4:
            fil_A4 = {
                'scene_key': A4,
            }
            fil.update(fil_A4)
            pass
        if A5:
            fil_A5 = {
                'pricerange_key': A5
            }
            fil.update(fil_A5)
            pass

        models_id = []
        for i in self.modrls:
            logger.i('搜索    ', i.object)
            models_id.append(i.object.id)
            pass

        WareAppPrefix = models.WareAppPrefix.objects.filter(id__in=models_id, wareApp_key__release=True)

        if fil:
            self.modrls = WareAppPrefix.filter(**fil).order_by('brand_key__key__level')
        else:
            self.modrls = WareAppPrefix

    def get_objects_pull(self):
        return self.modrls

    pass


