# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

from managestage.utli.datetimenow import datetimenow


class UserVipGroup(models.Model):
    '''
    用户的VIP，根据不同消费情况晋升不同等级
    需要预先设置
    '''
    level = models.IntegerField(default=0, verbose_name='用户VIP多级')
    money = models.IntegerField(default=10000, verbose_name='消费晋级')

from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, blank=True)
    nickname = models.CharField(max_length=50, unique=True, blank=True)
    usercode = models.CharField(max_length=100, unique=True, verbose_name='唯一的用户ID', null=True)
    update_time = models.DateTimeField(auto_now=True)
    state = models.CharField(default='0', max_length=10, verbose_name='用户状态', choices=(
        (-2, "被封禁"),
        (-1, "未激活"),
        (0, "站点"),
        (1, "国采第三方登录")
    ))
    key = models.ForeignKey(UserVipGroup, on_delete=models.SET_NULL, null=True)

    class Meta(AbstractUser.Meta):
        unique_together = ('email', 'username', 'nickname',)
        pass


class UserProfix(models.Model):
    username = models.CharField(max_length=100, verbose_name='用户名')
    email = models.EmailField(max_length=100, verbose_name="邮箱")
    code = models.CharField(max_length=300, verbose_name="验证码", null=True)
    code_default = models.BooleanField(default=False, verbose_name='是否完成找回密码')
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10, choices=(
        ("register", "注册"),
        ("retrieve", "找回密码")
    ))
    defaule = models.BooleanField(default=False, verbose_name='账号可用验证状态[注册账号邮箱验证]')
    timedate = models.DateTimeField(null=True, auto_now=True, verbose_name='验证通过时间')
    addtime = models.DateTimeField(auto_now=True, verbose_name='验证码创建时间')
    oneKey = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='关联用户')

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class UserProhibit(models.Model):
    '''
    用户是否被禁止登陆
    [prohibit_time_one - prohibit_time_tow]
    '''
    prohibit = models.BooleanField(default=False, verbose_name='用户是否被禁止登陆')
    prohibit_text = models.TextField(verbose_name='禁止原因')
    prohibit_time_one = models.DateTimeField(verbose_name='封禁时间[小时]-开始时间')
    prohibit_time_two = models.DateTimeField(verbose_name='封禁时间[小时]-结束时间')
    time_add = models.DateTimeField(auto_now=False, verbose_name='创建')  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name='更新')  # 更新
    key = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='')


class Md5Salt(models.Model):
    email = models.EmailField(verbose_name='用户邮箱')
    salt = models.TextField(verbose_name='Md5加密salt值')
    time_add = models.DateTimeField(auto_now=False, verbose_name='')  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name='')  # 更新
    key = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='')
    pass


class UserInfo(models.Model):
    email = models.EmailField(verbose_name='邮箱', null=True)
    name = models.CharField(max_length=50, verbose_name='真实姓名', null=True)
    qq = models.CharField(max_length=25, verbose_name='QQ', null=True)
    sex = models.CharField(max_length=5, verbose_name='性别', null=True)
    phone = models.CharField(max_length=30, verbose_name='电话', null=True)
    birthday = models.CharField(max_length=50, verbose_name='出生日期', null=True)
    fax = models.CharField(max_length=50, verbose_name='传真', null=True)
    job = models.CharField(max_length=100, verbose_name='职务', null=True)
    datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True)
    userlevel = models.IntegerField(verbose_name='用户级别 0主 1从', null=True)
    usercode = models.CharField(max_length=100, verbose_name='唯一的用户ID')
    key = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.datetime = datetimenow()
        super(UserInfo, self).save(*args, **kwargs)

    pass


class UnitInfo(models.Model):
    usercode = models.CharField(max_length=100, verbose_name='唯一的用户ID')

    name = models.CharField(max_length=200, verbose_name='单位名称', null=True)
    shortname = models.TextField(verbose_name='单位简称', null=True)
    orgcode = models.CharField(max_length=100, verbose_name='组织机构代码或统一社会信用代码', null=True)
    detailaddress = models.TextField(verbose_name='单位地址', null=True)
    postalcode = models.CharField(max_length=10, verbose_name='邮编', null=True)
    website = models.URLField(verbose_name='网址', null=True)
    telephone = models.CharField(max_length=20, verbose_name='电话', null=True)
    fax = models.CharField(max_length=20, verbose_name='传真', null=True)
    description = models.TextField(verbose_name='单位描述', null=True)
    datetime = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True)
    istopunit = models.IntegerField(verbose_name='是否顶级单位:1 是', null=True)
    province = models.CharField(max_length=100, verbose_name='省', null=True)
    city = models.CharField(max_length=100, verbose_name='市', null=True)
    remark = models.TextField(verbose_name='备注', null=True)
    topunitname = models.CharField(max_length=200, verbose_name='部委（归口）单位名称', null=True)
    topunitcode = models.CharField(max_length=200, verbose_name='部委（归口）单位唯一编号', null=True)
    unitcode = models.CharField(max_length=100, verbose_name='单位唯一编号', null=True)
    hyxt1 = models.CharField(max_length=200, verbose_name='行业系统1', null=True)
    hyxt2 = models.CharField(max_length=200, verbose_name='行业系统2', null=True)
    key = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    pass
