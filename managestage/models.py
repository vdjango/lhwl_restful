from django.db import models

# Create your models here.

from django.utils import timezone

from api.util.RemoveDisFiles import remove_all
from lhwill import settings


class HTTP_USER_AGENT(models.Model):
    '''记录访问客户端HTTP_USER_AGENT信息'''

    agent = models.TextField(verbose_name='记录访问客户端HTTP_USER_AGENT信息')
    path_info = models.URLField(verbose_name='客户端访问地址', null=True)
    method = models.CharField(max_length=5, verbose_name='REQUEST_METHOD')
    accept = models.TextField(verbose_name='HTTP_ACCEPT')

    time_add = models.DateTimeField(auto_now_add=True, verbose_name='记录访问客户端来访时间')

    def save(self, *args, **kwargs):
        self.time_add = timezone.now()

        return super(HTTP_USER_AGENT, self).save(*args, **kwargs)

    pass


'''站点设置-邮箱设置'''


class systemmail(models.Model):
    '''
    站点设置-邮箱设置
    '''
    host = models.CharField(max_length=300, verbose_name='SMTP地址')
    port = models.CharField(max_length=10, verbose_name='端口')
    user = models.CharField(max_length=300, verbose_name='发信人地址')
    name = models.CharField(max_length=300, verbose_name='验证用户名')
    passwd = models.CharField(max_length=300, verbose_name='验证密码')


'''站点设置 - 站点属性'''


class systemSetup(models.Model):
    '''
    站点设置 - 站点属性
    '''

    site_name = models.CharField(max_length=200, verbose_name='站点标题')
    site_tags = models.CharField(max_length=500, verbose_name='微标描述')
    site_url = models.URLField(verbose_name='站点地址（URL）')
    site_email = models.TextField(verbose_name='管理员邮箱')
    site_icp = models.TextField(verbose_name='ICP 备案信息')

    site_can_register = models.BooleanField(default=True, verbose_name='开放注册')
    site_allow_sending_statistics = models.BooleanField(default=True, verbose_name='开启统计信息')
    site_time_now = models.DateTimeField(auto_now=True, verbose_name='最后一次编辑时间')


class Debug(models.Model):
    state = models.IntegerField(choices=(
        (0, '开启DEBUG'),
        (1, '关闭DEBUG')
    ), unique=True)


'''站点设置-站点维护模式'''


class maintain(models.Model):
    '''
    站点设置-站点维护模式
    '''
    inta_info = models.TextField(verbose_name='本次维护说明')
    inta_datatime = models.DateTimeField(auto_now=False, verbose_name='预计维护结束时间')
    inta_allwo = models.BooleanField(default=False, verbose_name='开启维护模式')
    inta_time_now = models.DateTimeField(auto_now=True, verbose_name='最后一次编辑时间')


class Setclassify(models.Model):
    '''

    '''
    radio = models.CharField(max_length=5, verbose_name='首页分类深度设置', choices=(
        (2, '二级分类深度'),
        (3, '三级分类深度')
    ))

    pass


'''站点设置-第三方登陆'''


class appid(models.Model):
    '''
    站点设置-第三方登陆
    '''
    apptype = models.CharField(max_length=50, choices=(
        ('qq', 'QQ登陆'),
        ('weixin', '微信登陆')
    ), verbose_name='第三方登陆接入方式')
    appid = models.CharField(max_length=100, verbose_name='APPID')
    appkey = models.CharField(max_length=300, verbose_name='APPKEY')

    pass


class seosetup(models.Model):
    stype = models.CharField(max_length=20, choices=(
        ('index', '首页SEO'),
        ('ware', '商品SEO'),
    ), verbose_name='SEO分类')
    title = models.CharField(max_length=500, verbose_name='标题')
    description = models.TextField(verbose_name='描述')
    keywords = models.TextField(verbose_name='关键字')


class SearchStatistics(models.Model):
    '''
    统计用户搜索关键字
    不会重复，计次统计方法。 用户搜索命中后统计记册
    [注意： 程序算法 只保留20个搜索关键字]
    '''
    name = models.CharField(max_length=200, verbose_name='搜索关键字')
    number = models.IntegerField(verbose_name='统计搜索次数')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']

    pass


class ImportFile(models.Model):
    '''
    导入商品压缩包
    分片上传，最后将碎片组合成为一个完整文件
    '''
    file = models.FileField(help_text='文件', upload_to='importfile')
    filename = models.CharField(max_length=256, help_text='文件名')
    relativePath = models.CharField(help_text='文件夹上传的时候文件的相对路径属性', max_length=256)
    identifier = models.CharField(help_text='每个文件的唯一标示', max_length=256)
    totalSize = models.IntegerField(help_text='文件总大小')
    currentChunkSize = models.IntegerField(help_text='当前块的大小，实际大小')
    chunkSize = models.IntegerField(help_text='分块大小，根据 totalSize 和这个值你就可以计算出总共的块数。注意最后一块的大小可能会比这个要大')
    totalChunks = models.IntegerField(help_text='文件被分成块的总数')
    chunkNumber = models.IntegerField(help_text='当前块的次序，第一个块是 1，注意不是从 0 开始的')
    time_add = models.DateTimeField(auto_now_add=True, help_text='上传时间')

    def save(self, *args, **kwargs):
        super(ImportFile, self).save(*args, **kwargs)
        pass


    def delete(self, *args, **kwargs):
        import os
        if os.path.exists(self.file.path):
            os.remove(self.file.path)
            pass

        super(ImportFile, self).delete(*args, **kwargs)

    def __str__(self):
        return self.identifier

    class Meta:
        ordering = ['chunkNumber']


class ImportGoods(models.Model):
    '''
    ImportFile 分片碎片组合成为一个完整文件的存放路径
    '''
    file = models.FileField(help_text='文件路径，由ImportFile分片组合', max_length=256, upload_to='import_success')
    name = models.CharField(help_text='文件名称', max_length=256, blank=True, null=True)
    unix = models.IntegerField(help_text='资源路径')
    status = models.IntegerField(help_text='导入状态', choices=(
        (0, '以导入'),
        (1, '未导入'),
    ), default=1)
    time = models.DateTimeField(help_text='创建时间', auto_now_add=True)
    # https://docs.djangoproject.com/en/2.1/ref/models/fields/#datefield

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name

        super(ImportGoods, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        import os
        if os.path.exists(self.file.path):
            remove_all(self.file.path)
            os.removedirs('{}/media/import_success/{}'.format(settings.BASE_DIR, self.unix))
            pass

        super(ImportGoods, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['-time']
    pass
