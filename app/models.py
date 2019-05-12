# from sorl.thumbnail import ImageField
import imghdr
import os
from io import BytesIO

from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime

from account.models import User
# Create your models here.
from api.util.RemoveDisFiles import remove_all
from lhwill import settings
from lhwill.util.log import log
from managestage.utli.datetimenow import datetimenow
from plate.models import plateModels

logger = log(globals())

imageurl = '图片存储路径'
httpurls = '链接地址'
titleurl = '标题'
time_addurl = '创建时间'
time_nowurl = '更新时间'
userurl = '创建者'

rateUid = [
    {
        'value': 0,
        'label': '其他'
    },
    {
        'value': 1,
        'label': '服务器'
    },
    {
        'value': 2,
        'label': '视频会议系统及会议室音频系统'
    },
    {
        'value': 3,
        'label': '多功能一体机'
    },
    {
        'value': 4,
        'label': '传真机'
    },
    {
        'value': 5,
        'label': '打印设备（针式打印机、条码打印机、标签打印机、支票打印机）'
    },
    {
        'value': 6,
        'label': '扫描设备'
    },
    {
        'value': 7,
        'label': '投影仪及器材'
    },
    {
        'value': 8,
        'label': '电视机'
    }, {
        'value': 9,
        'label': '硬盘保护卡'
    },
    {
        'value': 10,
        'label': '照相机及器材'
    },
    {
        'value': 11,
        'label': '电子白板'
    }, {
        'value': 12,
        'label': '触控一体机'
    },
    {
        'value': 13,
        'label': '碎纸机'
    },
    {
        'value': 14,
        'label': '不间断电源'
    },
    {
        'value': 15,
        'label': '摄像机'
    },
    {
        'value': 16,
        'label': '复印纸（京外单位）'
    },
    {
        'value': 17,
        'label': '通用耗材'
    },
    {
        'value': 18,
        'label': '办公用品'
    }
]


# TOP广告横幅
class BannerAd(models.Model):
    '''
    TOP广告横幅
    '''
    title = models.CharField(max_length=50, verbose_name=titleurl)
    url = models.CharField(max_length=100, verbose_name=httpurls)
    image = models.CharField(max_length=100, verbose_name=imageurl)
    time_add = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='添加时间')  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 更新
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=userurl)

    class Meta:
        ordering = ['time_now']
        verbose_name = '广告横幅'
        verbose_name_plural = '广告横幅-[首页横幅]'

    pass


# 首页导航
class Navigation(models.Model):
    '''
    首页导航
    '''
    name = models.CharField(max_length=50, verbose_name=titleurl)  # 标题
    url = models.CharField(max_length=100, verbose_name=httpurls)  # Url地址
    time_add = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 更新

    class Meta:
        ordering = ['time_add']
        verbose_name = '首页导航'
        verbose_name_plural = '首页导航'


# 二级导航
class Navigation_Two(models.Model):
    '''
    二级导航
    '''
    name = models.CharField(max_length=50, verbose_name=titleurl)  # 标题

    time_add = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 更新

    key = models.ForeignKey(plateModels, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['time_add']
        verbose_name = '二级导航'
        verbose_name_plural = '二级导航'

    def save(self, *args, **kwargs):
        if not self.time_add:
            self.time_add = timezone.now()

        super(Navigation_Two, self).save(*args, **kwargs)


# 添加分类导航
class Classification_bar(models.Model):
    '''
    添加分类导航
    '''
    name = models.CharField(max_length=50, verbose_name=titleurl)  # 标题
    url = models.CharField(max_length=100, verbose_name=httpurls)  # Url地址
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新
    key = models.ForeignKey('Classification', on_delete=models.CASCADE, verbose_name='分类', blank=True)

    class Meta:
        ordering = ['time_add']
        verbose_name = '分类导航'
        verbose_name_plural = '分类导航 -> [首页全部分类子导航]'

    def __str__(self):
        return self.name

    pass


# 全部分类-二级分类
class Classification_Two(models.Model):
    '''
    全部分类-二级分类
    '''
    subtitle = models.CharField(max_length=50, verbose_name=titleurl)  # 标题
    url = models.CharField(max_length=100, verbose_name=httpurls)  # Url地址
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新
    key = models.ForeignKey('Classification', on_delete=models.CASCADE, verbose_name='分类', blank=True)

    class Meta:
        ordering = ['time_add']
        verbose_name = '一级分类'
        verbose_name_plural = '一级分类 -> [首页全部分类]'

    def __str__(self):
        return self.subtitle


# 轮播图片
class Carousel(models.Model):
    '''
    轮播图片
    '''
    name = models.CharField(max_length=50, verbose_name='说明摘要')
    url = models.URLField(verbose_name=httpurls)
    image = models.ImageField(upload_to='carousel', verbose_name='图片')
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新

    class Meta:
        ordering = ['name']
        verbose_name = '首页轮播图'
        verbose_name_plural = '首页轮播图-[首页轮播图]'

        pass

    def __str__(self):
        return self.name


# 条/公告
class Headlines(models.Model):
    '''
    头条/公告
    '''
    title = models.CharField(max_length=50, verbose_name=titleurl)
    url = models.CharField(max_length=100, verbose_name='跳转地址 [文本内容留空]', blank=True, null=True)
    connet = models.TextField(verbose_name='文本内容', blank=True, null=True)
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=userurl)

    class Meta:
        ordering = ['-time_now']
        verbose_name = '头条/公告'
        verbose_name_plural = '头条/公告-[首页头条/公告]'


# 首页今日推荐
class Recommend(models.Model):
    '''
    首页今日推荐
    '''
    title = models.CharField(max_length=50, verbose_name=titleurl)
    image = models.CharField(max_length=100, verbose_name=imageurl)
    url = models.CharField(max_length=100, verbose_name=httpurls)
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=userurl)

    class Meta:
        ordering = ['-time_now']
        verbose_name = '今日推荐'
        verbose_name_plural = '今日推荐 - [首页今日推荐]'


'''商品筛选器结束'''
''''''''''''''''''


# 首页板块
class MiddleTop(models.Model):
    '''
    首页板块
    '''
    name = models.CharField(max_length=50, verbose_name=titleurl)
    temp = models.CharField(max_length=10, verbose_name='请选择模板', choices=[
        (0, '默认'),
        (1, '简约')
    ])
    number = models.IntegerField(verbose_name='展示列数')  # 移动端不使用
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新

    class Meta:
        ordering = ['time_add']
        verbose_name = '首页板块'
        verbose_name_plural = '首页板块 - [首页板块]'

    def __str__(self):
        return self.name

    pass


# 板块标签
class Mid_Search(models.Model):
    '''
    板块标签
    '''
    name = models.CharField(max_length=20, verbose_name='标签')
    url = models.URLField(verbose_name='标签链接地址')
    key = models.ForeignKey(MiddleTop, on_delete=models.CASCADE, verbose_name='板块', related_name='mid_search')
    pass


# 首页板块商品
class commodity(models.Model):
    '''
    首页板块商品
    '''
    title = models.TextField(verbose_name=titleurl)  # 商品名称
    money = models.IntegerField(verbose_name='商品价钱')
    image = models.CharField(max_length=100, verbose_name=imageurl)  # 商品头像
    url = models.CharField(max_length=100, verbose_name='商品地址')
    key = models.ForeignKey(MiddleTop, on_delete=models.CASCADE, verbose_name='首页板块')
    ware_key = models.ForeignKey('WareApp', on_delete=models.CASCADE, verbose_name='产品归类')
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新

    class Meta:
        ordering = ['time_now']
        verbose_name = '板块商品链接'
        verbose_name_plural = '板块商品链接 -> [首页板块商品]'

    pass


'''不知道这是什么东西'''


class CommodityClassification_connet(models.Model):
    subtitle = models.CharField(max_length=50)
    money = models.FloatField()
    imgurl = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='')
    time_add = models.DateTimeField(auto_now=False)  # 创建
    time_now = models.DateTimeField(auto_now=True)  # 更新


# 商品分类信息，包括商品本身
class CommodityClassification(models.Model):
    '''
    商品分类信息，包括商品本身
    '''
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    connet = models.ForeignKey(CommodityClassification_connet, on_delete=models.CASCADE)

    time_add = models.DateTimeField(auto_now=False)  # 创建
    time_now = models.DateTimeField(auto_now=True)  # 更新

    class Meta:
        ordering = ['-time_now']


'''商品详情'''


# 商品详情页-选择颜色
class Choice(models.Model):
    '''
    商品详情页-选择颜色
    '''
    name = models.CharField(max_length=10, verbose_name='选择颜色')
    defaule = models.BooleanField(verbose_name='选择状态默认勾选')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '选择颜色'
        verbose_name_plural = '选择颜色 -> [商品详情页]'


# 租赁配置/ 选择方式等条件 三级分类
class Duration(models.Model):
    '''
    分类信息[二级分类 时间/...]
    '''
    name = models.CharField(max_length=20, verbose_name='时间/...')
    money = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='时长起租价')
    defaule = models.BooleanField(verbose_name='选择状态默认勾选')
    ware_key = models.ForeignKey('WareApp', on_delete=models.CASCADE, verbose_name='商品')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '租赁配置/ 选择方式等条件2'
        verbose_name_plural = '租赁配置/ 选择方式等条件 -> [商品详情页]2'


'''
下面是二级导航urls页面相关
'''


# 二级导航模板页信息
class Navaid(models.Model):
    site_navaid_name = models.CharField(max_length=200, verbose_name='二级导航首页大标题')
    site_navaid_tags = models.CharField(max_length=200, verbose_name='二级导航首页描述', null=True)
    site_navaid_button = models.CharField(default='30秒快速预览商品', max_length=50, verbose_name='二级导航首页按钮名称')
    key = models.ForeignKey(Navigation_Two, on_delete=models.CASCADE, verbose_name='首页二级导航', null=True)
    pass


class NavaidImages(models.Model):
    '''
    和上面是一起的
    二级导航模板页信息 图片
    '''
    images = models.ImageField(upload_to='images/Navaid/%Y/%m/%d', default="default.jpg")
    key = models.ForeignKey(Navaid, on_delete=models.CASCADE, verbose_name='二级导航模板页信息')
    pass


# 二级导航页面板块
class NavaidMiddle(models.Model):
    '''二级导航页面板块'''
    navaid_name = models.CharField(max_length=50, verbose_name='板块名称')
    navaid_urls = models.URLField(verbose_name='更多超链接地址')
    navaid_images = models.ImageField(upload_to='images/navaidMiddle/%Y/%m/%d', default="navaid_default.jpg")
    key = models.ForeignKey(Navaid, on_delete=models.CASCADE, verbose_name='二级导航页面')
    pass


# 根据关键字推荐商品到板块上来
class NavaidMiddleWareApp(models.Model):
    '''
    二级导航 根据关键字推荐商品到板块上来
    '''
    navaid_name = models.CharField(max_length=50, verbose_name='商品分类标题')
    navaid_Keyword = models.CharField(max_length=50, verbose_name='搜索关键字', null=True)
    navaid_number = models.IntegerField(default=2, verbose_name='展示行数')
    key = models.ForeignKey(NavaidMiddle, on_delete=models.CASCADE, verbose_name='二级导航页面板块')

    pass


'''
上面方法废弃，请使用下面方法
'''


# 全部分类-一级分类
class Classification(models.Model):
    '''
    全部分类-一级分类
    '''
    name = models.CharField(max_length=50, verbose_name=titleurl)  # 标题
    time_add = models.DateTimeField(auto_now_add=True, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新

    class Meta:
        ordering = ['time_add']
        verbose_name = '全部分类'
        verbose_name_plural = '全部分类-[首页全部分类]'

    def __str__(self):
        return self.name

    pass


# 全部分类-三级分类
class Classification_There(models.Model):
    '''
    全部分类-三级分类
    '''
    name = models.CharField(max_length=50, verbose_name=titleurl)
    url = models.CharField(max_length=100, verbose_name=httpurls)
    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新
    key = models.ForeignKey(Classification_Two, on_delete=models.CASCADE, verbose_name='分类', blank=True, null=True)
    Classifykey = models.ForeignKey(Classification, on_delete=models.CASCADE, verbose_name='分类', blank=True, null=True)

    level = models.IntegerField(default=1000, verbose_name='分类展示优先级[搜索]')

    class Meta:
        ordering = ['time_add']
        verbose_name = '二级分类'
        verbose_name_plural = '二级分类 -> [首页全部分类]'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.level:
            self.level = 1000
            pass

        super(Classification_There, self).save(*args, **kwargs)
        pass


# 存放商品内容等
class WareApp(models.Model):
    '''
    存放商品内容等

    image字段API接口异常
    '''
    image_size = ['64x64', '125x125', '200x200', '400x400', '800x800']

    def user_directory_path(self, filename):
        import os
        filename = '{}.{}'.format(str(datetimenow()).split('+')[0], filename.split('.')[-1])
        path = os.path.join("images", filename)
        return path

    name = models.TextField(verbose_name='商品名称')
    slug = models.SlugField(max_length=255, verbose_name='', null=True, blank=True)
    money = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='商品金额')
    connet = models.TextField(verbose_name='图文描述')

    image = models.ImageField(upload_to="images", verbose_name='首图地址', null=True, blank=True)
    image_64x64 = models.ImageField(upload_to="images", verbose_name='首图地址', null=True, blank=True)
    image_125x125 = models.ImageField(upload_to="images", verbose_name='首图地址', null=True, blank=True)
    image_200x200 = models.ImageField(upload_to="images", verbose_name='首图地址', null=True, blank=True)
    image_400x400 = models.ImageField(upload_to="images", verbose_name='首图地址', null=True, blank=True)
    image_800x800 = models.ImageField(upload_to="images", verbose_name='首图地址', null=True, blank=True)

    characteristic = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='促销价', null=True,
                                         blank=True)  # DEL
    commodity_description = models.TextField(verbose_name='促销详情', null=True, blank=True)  # DEL

    unix = models.CharField(max_length=100, verbose_name='资源路径')

    stock = models.BooleanField(default=False, verbose_name='库存状态',
                                help_text='如果库存为0的时候，此状态为True。True的时候锁定商品，防止其他用户下单操作')

    release = models.BooleanField(default=False, verbose_name='发布状态')
    release_version = models.IntegerField(default=0, verbose_name='发布版本号')
    time_add = models.DateTimeField(auto_now_add=True, verbose_name=time_addurl)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl)  # 更新

    keyword = models.TextField(verbose_name='SEO关键词', null=True, blank=True)
    describe = models.TextField(verbose_name='SEO描述', null=True, blank=True)

    class Meta:
        ordering = ['-time_now']
        verbose_name = '添加商品'
        verbose_name_plural = '添加商品-[发布商品]'
        pass

    def get_absolute_url(self):
        return reverse('app:details', args=[self.id])

    def get_image_url(self):
        if self.image:
            return '/media{}'.format(self.image)
        return ''

    def get_image_url_64x64(self):
        if self.image_64x64:
            return '/media{}'.format(self.image_64x64)
        return ''

    def get_image_url_125x125(self):
        if self.image_125x125:
            return '/media{}'.format(self.image_125x125)
        return ''

    def get_image_url_200x200(self):
        if self.image_200x200:
            return '/media{}'.format(self.image_200x200)
        return ''

    def get_image_url_400x400(self):
        if self.image_400x400:
            return '/media{}'.format(self.image_400x400)
        return ''

    def get_image_url_800x800(self):
        if self.image_800x800:
            return '/media{}'.format(self.image_800x800)
        return ''

    def get_thumbnail(self):
        if not self.image:
            logger.i('get_thumbnail', '字段为空', self.image)
            return
        if self.image == '':
            logger.i('get_thumbnail', '字段为空', self.image)
            return

        if not os.path.exists('{}{}'.format(settings.MEDIA_ROOT, self.image)):
            logger.i('文件不存在', self.image)
            return

        url_list = str(self.image).split('head/')
        url_prefix = url_list[1].split('.')[0]
        url_suffix = url_list[1].split('.')[1]

        _suffix = '{}'

        image = Image.open('{}{}'.format(settings.MEDIA_ROOT, self.image))

        for size in self.image_size:
            _suffix = imghdr.what('{}{}'.format(settings.MEDIA_ROOT, self.image))

            _size_ = [int(size.split('x')[0]), int(size.split('x')[1])]
            path = '{}{}head/{}'.format(settings.MEDIA_ROOT, url_list[0], size)
            url_name = '{}-{}.{}'.format(url_prefix, size, _suffix)
            url_path = '{}/{}'.format(path, url_name)
            url = '{}head/{}/{}'.format(url_list[0], size, url_name)

            if image.mode not in ('L', 'RGB', 'RGBA'):
                image = image.convert('RGB')

            thumbnail = ImageOps.fit(image, _size_, Image.ANTIALIAS)

            io = BytesIO()
            thumbnail.save(io, _suffix)

            if not os.path.exists(path):
                os.makedirs(path)

            Image.open(ContentFile(io.getvalue())).save(url_path)

            if '64x64' in size:
                self.image_64x64 = url

            if '125x125' in size:
                self.image_125x125 = url

            if '200x200' in size:
                self.image_200x200 = url

            if '400x400' in size:
                self.image_400x400 = url

            if '800x800' in size:
                self.image_800x800 = url

            logger.i('url', url)

    def save(self, *args, **kwargs):
        if self.image:
            self.get_thumbnail()
            pass

        super(WareApp, self).save(*args, **kwargs)

        prefix = self.wareappprefix_set.filter()
        if not prefix.exists():
            prefix.create(wareApp_key=self)

        '''
        初始化库存
        '''
        from stock.models import StockInfo
        stock = StockInfo.objects.filter()
        if not stock.exists():
            stock.create(key=self)
            pass

        pass

    def delete(self, *args, **kwargs):
        path = os.path.join('{}/media/images/{}'.format(settings.BASE_DIR, self.unix))
        remove_all(path)
        super(WareApp, self).delete(*args, **kwargs)
        pass

    pass


# 商品图片
class images(models.Model):
    '''
    商品图片
    '''

    def user_directory_path(self, filename):
        import os
        filename = '{}.{}'.format(str(datetimenow()).split('+')[0], filename.split('.')[-1])
        path = os.path.join("images", self.key.unix, "head", filename)
        logger.i('os.path.join  ', path)
        return path

    image = models.ImageField(
        upload_to=user_directory_path,
    )

    defaule = models.BooleanField(default=False, verbose_name='默认首图')
    key = models.ForeignKey(WareApp, on_delete=models.CASCADE, verbose_name='所属商品')

    def save(self, *args, **kwargs):
        if self.defaule:
            images.objects.filter(key=self.key).update(defaule=False)
            self.key.image = self.image
            self.key.save()
            pass
        super(images, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        remove_all(self.image.path)
        super(images, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        if 'http' in self.image.url:
            return self.image.url

        if '/media/' in self.image.name:
            # logger.i('SAVE 准备替换首图不规范路径', self.image.url)
            image = str(self.image.url).replace('/media/', '/')
            logger.i('SAVE 替换首图不规范路径未： ', str(self.image.name).replace('/media/', '/'))
            self.image.name = image
            self.save()

        # logger.i('self.image.path', '{}{}'.format(settings.HTTP_HOST, self.image.url))
        return '{}{}'.format(settings.HTTP_HOST, self.image.url)
        pass

    def __str__(self):
        if self.image:
            return self.image
        return None


# 商品搜索筛选器
class WareSetupPrefix(models.Model):
    '''

    '''
    t1 = models.CharField(max_length=20, verbose_name='商品品牌', null=True)
    t2 = models.CharField(max_length=20, verbose_name='产品类型', null=True)
    t3 = models.CharField(max_length=20, verbose_name='技术类型', null=True)
    t4 = models.CharField(max_length=20, verbose_name='使用场景', null=True)
    t5 = models.CharField(max_length=20, verbose_name='价格范围', null=True)
    filter_id = models.CharField(max_length=5, verbose_name='分类类型', choices=(
        (0, '商品品牌'),
        (1, '产品类型'),
        (2, '技术类型'),
        (3, '使用场景'),
        (4, '价格范围'),
    ))
    key = models.ForeignKey(Classification_There, on_delete=models.SET_NULL, null=True)
    pass


class Brand(models.Model):
    '''
    商品品牌 [0]
    '''
    name = models.CharField(max_length=200, verbose_name='品牌')
    key = models.ForeignKey(Classification_There, on_delete=models.CASCADE, verbose_name='品牌归属')
    PrefixKey = models.ForeignKey(WareSetupPrefix, on_delete=models.CASCADE, verbose_name='筛选器', null=True)

    def __str__(self):
        if self.name:
            return self.name
        return None

    pass


class ProductType(models.Model):
    '''
    产品类型 [1]
    '''
    name = models.CharField(max_length=200, verbose_name='产品类型')
    key = models.ForeignKey(Classification_There, on_delete=models.CASCADE, verbose_name='品牌归属')
    PrefixKey = models.ForeignKey(WareSetupPrefix, on_delete=models.CASCADE, verbose_name='筛选器', null=True)

    def __str__(self):
        if self.name:
            return self.name
        return None

    pass


class Technology(models.Model):
    '''
    技术类型 [2]
    '''
    name = models.CharField(max_length=200, verbose_name='技术类型')
    key = models.ForeignKey(Classification_There, on_delete=models.CASCADE, verbose_name='品牌归属')
    PrefixKey = models.ForeignKey(WareSetupPrefix, on_delete=models.CASCADE, verbose_name='筛选器', null=True)

    def __str__(self):
        if self.name:
            return self.name
        return None

    pass


class Scene(models.Model):
    '''
    使用场景 [3]
    '''
    name = models.CharField(max_length=200, verbose_name='使用场景')
    key = models.ForeignKey(Classification_There, on_delete=models.CASCADE, verbose_name='品牌归属')
    PrefixKey = models.ForeignKey(WareSetupPrefix, on_delete=models.CASCADE, verbose_name='筛选器', null=True)

    def __str__(self):
        if self.name:
            return self.name
        return None

    pass


class PriceRange(models.Model):
    '''
    价格范围 [4]
    '''
    name = models.CharField(max_length=200, verbose_name='使用场景')
    key = models.ForeignKey(Classification_There, on_delete=models.CASCADE, verbose_name='品牌归属')
    PrefixKey = models.ForeignKey(WareSetupPrefix, on_delete=models.CASCADE, verbose_name='筛选器', null=True)

    def __str__(self):
        if self.name:
            return self.name
        return None

    pass


class RateClassgUid(models.Model):
    '''
    央采18类ID
    : 优惠率报价
    '''

    uid_choices = (
        (1, '服务器 '),
        (2, '视频会议系统及会议室音频系统'),
        (3, '多功能一体机'),
        (4, '传真机'),
        (5, '打印设备（针式打印机、条码打印机、标签打印机、支票打印机）'),
        (6, '扫描设备'),
        (7, '投影仪及器材'),
        (8, '电视机'),
        (9, '硬盘保护卡'),
        (10, '照相机及器材'),
        (11, '电子白板'),
        (12, '触控一体机'),
        (13, '碎纸机'),
        (14, '不间断电源'),
        (15, '摄像机'),
        (16, '复印纸（京外单位）'),
        (17, '通用耗材'),
        (18, '办公用品'),
        (0, '其他')
    )

    uid = models.IntegerField(unique=True, default=0, choices=uid_choices, verbose_name='中央采购18类ID')

    a1 = models.DecimalField(default=2.0, max_digits=9, decimal_places=2, verbose_name='10万元（含）以下')
    a2 = models.DecimalField(default=2.2, max_digits=9, decimal_places=2, verbose_name='10万元至30万元（含）')
    a3 = models.DecimalField(default=2.4, max_digits=9, decimal_places=2, verbose_name='30万元至60万元（含）')
    a4 = models.DecimalField(default=2.7, max_digits=9, decimal_places=2, verbose_name='60万元至100万元（含）')
    defaule = models.BooleanField(default=True, verbose_name='是否为国采优惠率', blank=True)  # TODO 状态废弃，新版本不引入

    def get_absolute_url(self):
        '''
        获取当前ModelsView视图Url
        generic：success_url =
        :return:
        '''
        return reverse('admins:discount')

    def save(self, *args, **kwargs):
        # self.get_uid_display() (x, y) = y
        super(RateClassgUid, self).save(*args, **kwargs)
        pass

    pass


class WareAppPrefix(models.Model):
    '''
    商品搜索表[搜索页面点击不同的类型，都在这里查询] - 商品搜索器
    TODO(job@6box.net): del 即将弃用
    '''
    classifys = models.CharField(max_length=100, verbose_name='首页一级分类', null=True)  # TODO 弃用
    classifytwos = models.CharField(max_length=100, verbose_name='首页二级分类', null=True)  # TODO 弃用
    classifytheres = models.CharField(max_length=100, verbose_name='首页三级分类', null=True)  # TODO 弃用
    priceranges = models.CharField(max_length=100, verbose_name='价格范围')  # TODO 弃用
    producttypes = models.CharField(max_length=100, verbose_name='产品类型')  # TODO 弃用
    technologys = models.CharField(max_length=100, verbose_name='技术类型')  # TODO 弃用
    scenes = models.CharField(max_length=100, verbose_name='使用场景')  # TODO 弃用
    brands = models.CharField(max_length=100, verbose_name='品牌')  # TODO 弃用
    classifytwo_key = models.ForeignKey(Classification_Two, on_delete=models.SET_NULL, verbose_name='首页二级分类',
                                        null=True)  # TODO 弃用

    classify_key = models.ForeignKey(Classification, on_delete=models.SET_NULL, verbose_name='首页一级分类', null=True)
    classifythere_key = models.ForeignKey(Classification_There, on_delete=models.SET_NULL, verbose_name='首页三级分类',
                                          null=True)
    pricerange_key = models.ForeignKey(PriceRange, on_delete=models.SET_NULL, null=True, verbose_name='价格范围')
    producttype_key = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, verbose_name='产品类型')
    technology_key = models.ForeignKey(Technology, on_delete=models.SET_NULL, null=True, verbose_name='技术类型')
    scene_key = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, verbose_name='使用场景')
    brand_key = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name='品牌')
    wareApp_key = models.ForeignKey(WareApp, on_delete=models.CASCADE, verbose_name='商品')

    rate_classg_key = models.ForeignKey(RateClassgUid, on_delete=models.SET_NULL, verbose_name='央采18类ID', null=True)

    time_add = models.DateTimeField(auto_now=True, verbose_name='创建时间', null=True)

    class Meta:
        ordering = ['-time_add']
        verbose_name = '商品搜索器'
        verbose_name_plural = '商品搜索器'
        pass

    def save(self, *args, **kwargs):
        if not self.time_add:
            self.time_add = datetimenow()

        super(WareAppPrefix, self).save(*args, **kwargs)

        info = self.wareApp_key.parameter_set.filter()
        if info.exists():
            info = info.get(key=self.wareApp_key)
            info.productType = self.classifythere_key.name
            info.save()
        else:
            parameter.objects.create(key=self.wareApp_key)

        # try:
        #     self.wareApp_key.parameter_set.filter()
        # except parameter.DoesNotExist:
        #     parameter.objects.create(key=self.wareApp_key)
        # except Exception as e:
        #     logger.e('WareAppPrefix save', e.args)

        pass

    pass


# 商品筛选器结束


class WareParProfix(models.Model):
    '''
    商品参数信息，关于商品的参数有很多。这里定义了需要哪些参数
    然后去获取 app.parameter 模型字段
    '''
    from lhwill.field.SelectField import SelectField

    CHOICES = (
        ('brands', '品牌'),
        ('model', '产品型号'),
        ('productType', '产品类型'),
        ('colorType', '颜色类型'),
        ('coverFunction', '涵盖功能'),
        ('velocityType', '速度类型'),
        ('maximumOriginalSize', '最大原稿尺寸'),
        ('memory', '内存容量'),
        ('hardDisk', '硬盘容量'),
        ('forPaperCapacity', '供纸容量'),
        ('mediumWeight', '介质重量'),
        ('materialDescription', '材料描述'),
        ('doubleSidedDevice', '双面器'),
        ('automaticDrafts', '自动输稿器'),
        ('networkFunction', '网络功能'),
        ('highestCv', '最高月印量'),
        ('falsrom', '其他容量'),
        ('other', '适用机型'),
        ('photocopyingSpeed', '复印速度'),
        ('PhotocopyingResolution', '复印分辨率'),
        ('copySize', '复印尺寸'),
        ('preheatingTime', '预热时间'),
        ('copyPhotocopyingPage', '首页复印时间'),
        ('continuityXeroxPages', '连续复印页数'),
        ('zoomRange', '缩放范围'),
        ('copyOdds', '复印赔率'),
        ('printController', '打印控制器'),
        ('printingSpeed', '打印速度'),
        ('printResolution', '打印分辨率'),
        ('printLanguage', '打印语言'),
        ('printingOtherPerformance', '打印其他性能'),
        ('scanningController', '扫描控制器'),
        ('scanningResolution', '扫描分辨率'),
        ('outputFormat', '输出格式'),
        ('scanningOtherPerformance', '扫描其他性能'),
        ('facsimileController', '传真控制器'),
        ('modemSpeed', '制解调器速度'),
        ('dataCompressionMethod', '数据压缩方式'),
        ('faxOtherPerformance', '传真其他性能'),
        ('display', '液晶显示屏'),
        ('mainframeSize', '主机尺寸'),
        ('weight', '重量'),
        ('otherFeatures', '其他特点'),
        ('timeMarket', '上市时间'),
        ('optionalAccessories', '可选配件'),
        ('warrantyTime', '质保时间'),
        ('customerService', '客服电话'),
        ('detailedContent', '详细内容'),
    )

    Dis_CHOICES = {
        'brands': '品牌',
        'model': '产品型号',
        'productType': '产品类型',
        'colorType': '颜色类型',
        'coverFunction': '涵盖功能',
        'velocityType': '速度类型',
        'maximumOriginalSize': '最大原稿尺寸',
        'memory': '内存容量',
        'hardDisk': '硬盘容量',
        'forPaperCapacity': '供纸容量',
        'mediumWeight': '介质重量',
        'materialDescription': '材料描述',
        'doubleSidedDevice': '双面器',
        'automaticDrafts': '自动输稿器',
        'networkFunction': '网络功能',
        'highestCv': '最高月印量',
        'falsrom': '其他容量',
        'other': '适用机型',
        'photocopyingSpeed': '复印速度',
        'PhotocopyingResolution': '复印分辨率',
        'copySize': '复印尺寸',
        'preheatingTime': '预热时间',
        'copyPhotocopyingPage': '首页复印时间',
        'continuityXeroxPages': '连续复印页数',
        'zoomRange': '缩放范围',
        'copyOdds': '复印赔率',
        'printController': '打印控制器',
        'printingSpeed': '打印速度',
        'printResolution': '打印分辨率',
        'printLanguage': '打印语言',
        'printingOtherPerformance': '打印其他性能',
        'scanningController': '扫描控制器',
        'scanningResolution': '扫描分辨率',
        'outputFormat': '输出格式',
        'scanningOtherPerformance': '扫描其他性能',
        'facsimileController': '传真控制器',
        'modemSpeed': '制解调器速度',
        'dataCompressionMethod': '数据压缩方式',
        'faxOtherPerformance': '传真其他性能',
        'display': '液晶显示屏',
        'mainframeSize': '主机尺寸',
        'weight': '重量',
        'otherFeatures': '其他特点',
        'timeMarket': '上市时间',
        'optionalAccessories': '可选配件',
        'warrantyTime': '质保时间',
        'customerService': '客服电话',
        'detailedContent': '详细内容',
    }

    filter_name = SelectField()
    key = models.ForeignKey(Classification_There, on_delete=models.SET_NULL, verbose_name='商品参数关联对象', null=True)

    pass


# 商品的详细配置参数
class parameter(models.Model):
    '''
    基本参数
    复合机一体机，墨盒股份等
    通用配置参数
    '''

    brands = models.CharField(max_length=200, verbose_name='品牌', null=True)  #
    model = models.CharField(max_length=200, verbose_name='产品型号', null=True)  #
    productType = models.CharField(max_length=200, verbose_name='产品类型', null=True)  #
    colorType = models.CharField(max_length=200, verbose_name='颜色类型', null=True)  #
    coverFunction = models.CharField(max_length=200, verbose_name='涵盖功能', null=True)
    velocityType = models.CharField(max_length=200, verbose_name='速度类型', null=True)
    maximumOriginalSize = models.CharField(max_length=200, verbose_name='最大原稿尺寸', null=True)
    memory = models.CharField(max_length=200, verbose_name='内存容量', null=True)
    hardDisk = models.CharField(max_length=200, verbose_name='硬盘容量', null=True)
    forPaperCapacity = models.TextField(verbose_name='供纸容量', null=True)
    mediumWeight = models.TextField(verbose_name='介质重量', null=True)
    materialDescription = models.CharField(max_length=200, verbose_name='材料描述', null=True)
    doubleSidedDevice = models.CharField(max_length=200, verbose_name='双面器', null=True)
    automaticDrafts = models.CharField(max_length=200, verbose_name='自动输稿器', null=True)
    networkFunction = models.CharField(max_length=200, verbose_name='网络功能', null=True)
    highestCv = models.CharField(max_length=200, verbose_name='最高月印量', null=True)
    falsrom = models.CharField(max_length=50, verbose_name='其他容量', null=True)
    other = models.CharField(max_length=200, verbose_name='适用机型', null=True)

    '''
    复印功能
    '''
    photocopyingSpeed = models.CharField(max_length=200, verbose_name='复印速度', null=True)
    PhotocopyingResolution = models.CharField(max_length=200, verbose_name='复印分辨率', null=True)
    copySize = models.CharField(max_length=200, verbose_name='复印尺寸', null=True)
    preheatingTime = models.CharField(max_length=200, verbose_name='预热时间', null=True)
    copyPhotocopyingPage = models.CharField(max_length=200, verbose_name='首页复印时间', null=True)
    continuityXeroxPages = models.CharField(max_length=200, verbose_name='连续复印页数', null=True)
    zoomRange = models.CharField(max_length=200, verbose_name='缩放范围', null=True)
    copyOdds = models.CharField(max_length=200, verbose_name='复印赔率', null=True)

    '''
    打印功能
    '''
    printController = models.CharField(max_length=200, verbose_name='打印控制器', null=True)
    printingSpeed = models.CharField(max_length=200, verbose_name='打印速度', null=True)
    printResolution = models.CharField(max_length=200, verbose_name='打印分辨率', null=True)
    printLanguage = models.TextField(verbose_name='打印语言', null=True)
    printingOtherPerformance = models.TextField(verbose_name='打印其他性能', null=True)

    '''
    扫描功能
    '''
    scanningController = models.CharField(max_length=200, verbose_name='扫描控制器', null=True)
    scanningResolution = models.CharField(max_length=200, verbose_name='扫描分辨率', null=True)
    outputFormat = models.CharField(max_length=200, verbose_name='输出格式', null=True)
    scanningOtherPerformance = models.TextField(verbose_name='扫描其他性能', null=True)

    '''
    传真功能
    '''
    facsimileController = models.CharField(max_length=200, verbose_name='传真控制器', null=True)
    modemSpeed = models.CharField(max_length=200, verbose_name='制解调器速度', null=True)
    dataCompressionMethod = models.CharField(max_length=200, verbose_name='数据压缩方式', null=True)
    faxOtherPerformance = models.TextField(verbose_name='传真其他性能', null=True)

    '''
    其他特性
    '''
    display = models.CharField(max_length=200, verbose_name='液晶显示屏', null=True)
    mainframeSize = models.CharField(max_length=200, verbose_name='主机尺寸', null=True)
    weight = models.CharField(max_length=20, verbose_name='重量', null=True)
    otherFeatures = models.CharField(max_length=200, verbose_name='其他特点', null=True)
    timeMarket = models.CharField(max_length=200, verbose_name='上市时间', null=True)

    '''
    复印机附件
    '''
    optionalAccessories = models.CharField(max_length=200, verbose_name='可选配件', null=True)

    '''
    保修信息
    '''
    warrantyTime = models.CharField(max_length=200, verbose_name='质保时间', null=True)
    customerService = models.CharField(max_length=200, verbose_name='客服电话', null=True)
    detailedContent = models.TextField(verbose_name='详细内容', null=True)

    time_add = models.DateTimeField(auto_now=False, verbose_name=time_addurl, null=True)  # 创建
    time_now = models.DateTimeField(auto_now=True, verbose_name=time_nowurl, null=True)  # 更新

    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, verbose_name='品牌', null=True)
    key = models.ForeignKey(WareApp, on_delete=models.CASCADE, verbose_name='隶属于商品')

    class Meta:
        ordering = ['-time_now']
        verbose_name = '商品参数'
        verbose_name_plural = '商品参数'
        pass

    def save(self, *args, **kwargs):

        warePrefix = self.key.wareappprefix_set.get()
        try:
            self.productType = warePrefix.classifythere_key.name
        except AttributeError:
            self.productType = ''

        logger.i('productType', self.productType)

        if not self.time_add:
            self.time_add = datetimenow()
            pass

        super(parameter, self).save(*args, **kwargs)
        pass

    pass


# 商品详情页- 商品套餐
class Lease(models.Model):
    '''
    商品详情页- 商品套餐
    '''
    sel = (
        (0, '租赁'),
        (1, '购买')
    )
    name = models.CharField(max_length=255, verbose_name='选择配置')
    money = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='套餐价')
    defaule = models.BooleanField(verbose_name='选择状态默认勾选')
    select = models.CharField(max_length=20, default=1, verbose_name='[租赁/购买]', choices=(
        (0, '租赁'),
        (1, '购买')
    ))
    ware_key = models.ForeignKey(WareApp, on_delete=models.CASCADE, verbose_name='商品')
    time_add = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.defaule:
            self.ware_key.money = self.money
            self.ware_key.save()
            self.ware_key.lease_set.update(defaule=False)

        super(Lease, self).save(*args, **kwargs)


    class Meta:
        verbose_name = '选择配置'
        verbose_name_plural = '选择配置 -> [商品详情页]'
        ordering = ['-time_add']

class WheelModel(models.Model):
    def user_directory_path(self, filename):
        import os
        filename = '{}.{}'.format(str(datetimenow()).split('+')[0].split('.')[0], filename.split('.')[-1])
        path = os.path.join("wheel-image", filename)
        return path

    image = models.ImageField(verbose_name='首页轮播图', upload_to=user_directory_path)
    time_add = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
    time_now = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    pass


class SectorModel(models.Model):
    '''
    首页下半部分商品板块展示栏目
    '''
    name = models.CharField(verbose_name='板块名称', help_text='首页板块名称', max_length=50, null=True, unique=True)
    number = models.IntegerField(verbose_name='板块条目', help_text='板块展示数据条目倍数[步进4]')
    key = models.ForeignKey(Classification_There, verbose_name='数据源', help_text='展示数据源', on_delete=models.CASCADE)
    time_add = models.DateTimeField(auto_now_add=True, verbose_name='添加时间', help_text='板块栏目创建时间')
    time_now = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    def save(self, *args, **kwargs):
        self.name = self.key.name
        super(SectorModel, self).save(*args, **kwargs)



