# coding=utf-8
from lhwill.util.log import log

logger = log(globals())


class Duplicate(object):
    '''
    筛选重复List[Dict]
    '''

    def __init__(self, resource_list):
        self.resource_list = resource_list

    def isRemoval(self):
        '''
        筛选List[Dict]
        :return:  没有重复的List[Dict]
        '''
        allResource = []
        if self.resource_list:
            allResource.append(self.resource_list[0])
            for dict in self.resource_list:
                k = 0
                for item in allResource:
                    # print 'item'
                    if dict['id'] != item['id']:
                        k = k + 1
                    # continue
                    else:
                        break
                    if k == len(allResource):
                        allResource.append(dict)
                        pass
                    pass
                pass

        return allResource

    def isDictRemoval(self):
        '''
        筛选Dict
        :param self:
        :return: 没有重复的List[Dict]
        '''
        allResource = []
        allResource.append(self.resource_list)
        for dict in self.resource_list:
            k = 0
            for item in allResource:
                # print 'item'
                if dict['id'] != item['id']:
                    k = k + 1
                # continue
                else:
                    break
                if k == len(allResource):
                    allResource.append(dict)
                    pass
                pass
            pass
        return allResource
