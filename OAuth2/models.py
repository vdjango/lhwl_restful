from django.db import models

# Create your models here.
from account.models import User
from managestage.utli.datetimenow import datetimenow


class UserToken(models.Model):
    '''
    央采登录，存储用户Token，根据IP地址来注册用户
    '''
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', null=True)
    usercode = models.CharField(max_length=200, verbose_name='唯一ID')
    token = models.CharField(max_length=50, verbose_name='Token', null=True)
    time_add = models.DateTimeField(auto_now=True, verbose_name='创建')  # 创建

    def save(self, *args, **kwargs):
        if not self.time_add:
            self.time_add = datetimenow()
        super(UserToken, self).save(*args, **kwargs)

    pass


class RegisterState(models.Model):
    '''
    央采用户登录生成的state
    用于检测是否为跨站请求(CSRF)
    验证是否本本人操作等
    : 5分钟后过期，将会被删除
    '''

    state_code = models.CharField(max_length=20, verbose_name='准入ID', null=True)
    code = models.CharField(max_length=20, verbose_name='央采验证码', null=True)
    state = models.CharField(max_length=20, verbose_name='唯一的state值')
    time_add = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.time_add:
            self.time_add = datetimenow()
        super(RegisterState, self).save(*args, **kwargs)

    pass
