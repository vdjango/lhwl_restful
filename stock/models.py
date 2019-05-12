from django.db import models

# Create your models here.
from app.models import WareApp


class StockInfo(models.Model):
    '''
    库存信息，商品库存记录
    is_valid 字段会阻止用户操作
    '''
    name = models.TextField(verbose_name='商品名称', help_text='该库存商品名称，字段会被替换为商品名称，无法手动修改', blank=True, null=True)
    number = models.IntegerField(default=0, verbose_name='库存数量', help_text='所关联的商品库存数量信息')
    is_valid = models.BooleanField(default=False, verbose_name='库存状态',
                                   help_text='当库存状态为True的时候，锁定当前关联的商品，阻止下单，添加购物车等操作！'
                                             '对已经下单用户不受影响，对添加购物车用户，受影响！')
    key = models.ForeignKey(WareApp, verbose_name='库存商品', help_text='库存所关联的商品', on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='库存信息创建时间', help_text='库存信息创建的时间，在当前数据生成的时候时间以被创建')
    now_time = models.DateTimeField(auto_now=True, verbose_name='库存修改时间', help_text='库存每次修改的时候会自动更新时间')

    def save(self, *args, **kwargs):
        self.name = self.key.name
        super(StockInfo, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-add_time']

    pass
