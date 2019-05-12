from django.db import models


# 搜索引擎


class GoodsLabelInfo(models.Model):
    '''
    商品标签信息 用于辅助搜索引擎搜索商品
    为商品打标签
    '''
    label = models.CharField(max_length=25, verbose_name='商品标签',
                             help_text='商品标签，每个商品拥有不同的标签。用于定位或标记商品本身')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', help_text='标签创建时间')
    now_time = models.DateTimeField(auto_now=True, verbose_name='标签更新时间', help_text='标签更新时间')
    key = models.ForeignKey('app.WareApp', verbose_name='关联商品', help_text='关联商品', on_delete=models.CASCADE)

    class Meta:
        ordering = ['add_time']

class GoodsPrefixInfo(models.Model):
    '''
    商品更多聚集信息 包含了商品品牌，商品参数，商品型号等信息
    用于辅助搜索引擎搜索商品
    '''

    key = models.ForeignKey('app.WareApp', verbose_name='关联商品', help_text='关联商品', on_delete=models.CASCADE)




