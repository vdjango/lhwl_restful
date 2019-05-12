


class AppModels(object):

    def __init__(self):
        self.lease_select = [
	        {
		        'id': 1,
		        'name': '购买'
	        },
            {
                'id': 0,
                'name': '租赁'

            }
        ]

    def get_LeaseSelect(self):
        '''
        后台-商品-添加套餐选择方式
        :return:
        '''
        return self.lease_select
        pass