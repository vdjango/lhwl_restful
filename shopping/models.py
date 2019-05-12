from django.db import models
from account.models import User

from app.models import WareApp, Lease, WareAppPrefix

# Create your models here.
from managestage.utli.datetimenow import datetimenow


class Cart(models.Model):
    '''
    购物车
    : 央采用户默认按照优惠率计算总金额
    : 普通用户按照单价计算总金额
    '''
    name = models.CharField(max_length=200, verbose_name='商品名称')
    image = models.URLField(verbose_name='首图url')
    numb = models.IntegerField(verbose_name='商品数量')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='商品单价')
    money = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='商品总金额')
    meal = models.TextField(verbose_name='套餐分类', null=True)  # 目前只有购买，没有租赁
    time = models.DateTimeField(auto_now_add=True, verbose_name='添加到购物车时间')

    rate = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='优惠率')
    yc_price = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='央采优惠商品单价', null=True)
    yc_money = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='央采优惠商品总金额', null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户')
    key = models.ForeignKey(WareApp, on_delete=models.CASCADE, null=True, verbose_name='关联商品')
    key_meal = models.ForeignKey(Lease, on_delete=models.CASCADE, null=True, verbose_name='套餐类型')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.time is not None:
            self.time = datetimenow()


        super(Cart, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-time']

    pass
