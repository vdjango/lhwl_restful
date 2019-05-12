from django.db import models

# Create your models here.
from slugify import slugify

from account.models import User
from app.models import Lease, Duration, Classification_There


class Acceptance(models.Model):
    '''
    央采用户验收单
    '''
    state = models.CharField(default=1, max_length=5, choices=(
        (-1, '验收单作废'),
        (0, '以生成验收单'),
        (1, '未生成验收单')
    ), verbose_name='验收单状态')
    ysd_code = models.CharField(max_length=100, verbose_name='验收单号', null=True)
    usercode = models.CharField(max_length=255, verbose_name='', null=True)
    orderid = models.CharField(max_length=30, verbose_name='订单号')

    time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='验收单创建时间')
    pass


class Invoices(models.Model):
    '''发票'''
    stype = models.CharField(max_length=5, default=1, verbose_name='发票类型', choices=(
        (1, '普通发票'),
        (2, '专用发票')
    ))
    content = models.CharField(max_length=5, default=0, verbose_name='', choices=(
        (0, '商品明细'),
        (1, '商品类型')
    ))

    taxpayer = models.CharField(max_length=50, verbose_name='纳税人识别号')
    phone = models.CharField(max_length=15, verbose_name='收票人手机', null=True)
    email = models.EmailField(verbose_name='收票人邮箱', null=True)

    head = models.CharField(max_length=200, verbose_name='抬头', null=True)
    #
    unitName = models.CharField(max_length=255, verbose_name='单位名称', null=True)
    registeredAddress = models.CharField(max_length=255, verbose_name='注册地址', null=True)
    registeredTelephone = models.CharField(max_length=15, verbose_name='注册电话', null=True)
    accountOpening = models.CharField(max_length=255, verbose_name='开户银行', null=True)
    account = models.CharField(max_length=255, verbose_name='银行账户', null=True)
    key = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    '''
    主订单
    @:param ordtype 记录订单发货等信息
    @:param state 记录订单整体状态信息， 比如 订单已完成 【此状态表示 订单已收货，已结账。】
    '''

    stype_choices = (
        (0, '租赁'),
        (1, '购买')
    )

    paymethod_choices = (
        (1, '货到付款-公务卡'),
        (2, '货到付款-支票'),
        (3, '货到付款-转账汇款'),
        (4, '货到付款-现金结算'),
        (5, '在线支付'),
        (9, '账期')
    )

    state_choices = (
        (0, '以完成'),
        # (1, '以收货-待付款'),
        (2, '待收货'),
        # (3, '待评价'),
        # (4, '售后中'),
        (5, '以取消'),
        (-1, '待发货'),
        (-2, '以删除')
    )

    ordispaid = models.IntegerField(default=0, verbose_name='订单是否生成验收单', choices=(
        (0, '未生成验收单'),
        # (1, '以生成未结账验收单'),  # 作废
        (2, '以成验收单'),
        (-1, '验收单作废')
    ))

    ordContract = models.IntegerField(default=1, verbose_name='是否生成了电子合同', choices=(
        (0, '未生成'),
        (1, '以生成'),
        (-1, '以作废'),
        # (2, '以作废')
    ))

    state = models.IntegerField(default=-1, choices=state_choices, verbose_name='交易状态')

    invoice = models.IntegerField(default=0, choices=(
        (0, '不开发票'),
        (1, '普通发票'),
        (2, '增值税发票')
    ), verbose_name='发票类型')

    isgotuaddress = models.BooleanField(default=False, verbose_name='申请取消订单', help_text='以发货订单不可直接取消，申请取消')

    orderid = models.CharField(max_length=30, verbose_name='订单号')
    province = models.CharField(max_length=200, verbose_name='省份简称')
    city = models.CharField(max_length=200, verbose_name='城市简称')
    area = models.CharField(max_length=20, verbose_name='所在地区 详细地址', null=True)

    total = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='订单商品总价')
    linkman = models.CharField(max_length=50, verbose_name='购买人姓名')
    linkmobile = models.CharField(max_length=20, verbose_name='购买人联系方式')
    deliveryaddress = models.CharField(max_length=200, verbose_name='收货地址')
    paymethod = models.IntegerField(default=1, choices=paymethod_choices, verbose_name='付款方式')
    ispaid = models.CharField(max_length=5, default=0, choices=(
        (0, '未结账'),
        (1, '已结账')
    ), verbose_name='是否完成支付')

    remark = models.TextField(verbose_name='订单备注', null=True)
    usercode = models.CharField(max_length=50, verbose_name='采购人唯一识别码[普通用户空]', null=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='订单起草时间')
    url = models.CharField(max_length=255, verbose_name='订单链接', null=True)

    key_inv = models.ForeignKey(Invoices, on_delete=models.SET_NULL, null=True, verbose_name='发票信息 不开票为None')
    key = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='归属用户')
    ordtype = models.IntegerField(default=-1, verbose_name='订单发货状态', choices=(
        (-1, '未发货'),
        (0, '以发货'),
        (1, '以收货')
    ))

    update_time = models.DateTimeField(auto_now=True, verbose_name='订单操作更新时间',
                                       help_text='订单操作更新时间，发货等操作')

    ''' DEL '''
    name = models.CharField(max_length=200, verbose_name='主订单名字', null=True)  # DEL
    money = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='订单商品应付价', null=True)  # DEL
    number = models.IntegerField(verbose_name='商品数量', null=True)  # DEL

    stype = models.CharField(max_length=5, default=1, choices=stype_choices, verbose_name='交易类型[购买/租赁]')
    images = models.CharField(max_length=255, verbose_name='订单首页图片', null=True)  # DEL
    lease_or = models.ForeignKey(Lease, on_delete=models.SET_NULL, null=True, verbose_name='交易套餐[配置/套餐]')
    duration_or = models.ForeignKey(Duration, on_delete=models.SET_NULL, null=True, verbose_name='交易时间[针对租赁]')

    def save(self, *args, **kwargs):
        from django.utils.datetime_safe import datetime
        self.update_time = datetime.utcnow()

        '''
        已发货
        改变state状态为 待收货
        '''
        # if self.ordtype == 0:
        #     self.state = 2
        #     pass
        #
        # '''
        # 已收货
        # 改变state状态为 [已完成]
        # '''
        # if self.ordtype == 1:
        #     self.state = 0
        #super(Order, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-createtime']

    pass


class Contracts(models.Model):
    '''
    电子合同
    '''

    stype = models.IntegerField(default=0, verbose_name='合同状态', choices=(
        (0, '正式'),
        (1, '转正')
    ))
    username = models.CharField(max_length=50, verbose_name='收货人')
    phlone = models.CharField(max_length=20, verbose_name='电话号')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='订单创建时间')

    usercode = models.CharField(max_length=50, verbose_name='采购人唯一识别码')
    orderid = models.CharField(max_length=50, verbose_name='合同编号')
    Acceptance = models.CharField(max_length=50, verbose_name='验收单编号', null=True)
    Invoice = models.CharField(max_length=50, verbose_name='发票编号', null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='合计[商品总价]')
    DAXTOTAL = models.CharField(max_length=100, verbose_name='大写金额：合计[商品总价]')
    DeliveryTime = models.CharField(max_length=20, verbose_name='送货时间[这个时间前到达目的地]')
    DeliverylaceP = models.CharField(max_length=255, verbose_name='送货地点')
    price = models.CharField(max_length=10, verbose_name='商品单价成交价')
    service = models.CharField(max_length=10, verbose_name='服务费')
    number = models.CharField(max_length=10, verbose_name='数量')

    name = models.CharField(max_length=200, verbose_name='产品名称[商品名称]')
    brands = models.CharField(max_length=100, verbose_name='品牌')
    model = models.CharField(max_length=200, verbose_name='产品型号')
    content = models.TextField(verbose_name='技术规格合主要配置')
    unit = models.CharField(max_length=255, verbose_name='单位')

    images = models.CharField(max_length=255, verbose_name='订单首页图片', null=True)

    url = models.CharField(max_length=255, verbose_name='订单链接', null=True)

    time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='合同创建时间')

    key_order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    key = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['time']

    pass


class Suborderlist(models.Model):
    '''
    子订单
    '''
    suborderid = models.CharField(max_length=200, verbose_name='子订单ID')
    url = models.CharField(max_length=200, verbose_name='子订单url', null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='子订单总金额')
    key = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='')
    pass


'''商品18类分类ID 对接央采'''


class Gusid(models.Model):
    '''
    商品18类分类ID 对接央采
    优惠率报价
    '''
    name = models.CharField(max_length=100, verbose_name='商品类别名')
    guid = models.IntegerField(verbose_name='商品目录ID 枚举值对照表')

    a1 = models.DecimalField(default=2.0, max_digits=9, decimal_places=2, verbose_name='10万元（含）以下')
    a2 = models.DecimalField(default=2.2, max_digits=9, decimal_places=2, verbose_name='10万元至30万元（含）')
    a3 = models.DecimalField(default=2.4, max_digits=9, decimal_places=2, verbose_name='30万元至60万元（含）')
    a4 = models.DecimalField(default=2.7, max_digits=9, decimal_places=2, verbose_name='60万元至100万元（含）')

    key = models.ForeignKey(Classification_There, on_delete=models.CASCADE)
    pass


class Goodslist(models.Model):
    '''
    订单商品
    '''
    goodsclassguid_choices = (
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
    goodsname = models.CharField(max_length=200, verbose_name='商品名称')
    goodsid = models.CharField(max_length=50, verbose_name='商品在订单中的唯一ID')
    spu = models.SlugField(max_length=255, verbose_name='细化到商品 商品唯一识别码[商品名称，规格，价钱等]', null=True, blank=True)
    sku = models.SlugField(max_length=255, verbose_name='细化到规格、型号、颜色等', null=True, blank=True)

    model = models.CharField(max_length=200, verbose_name='商品型号、规格')

    taoc = models.CharField(max_length=200, verbose_name='商品套餐信息')

    goodsclassguid = models.CharField(max_length=5, choices=goodsclassguid_choices, verbose_name='商品目录ID')
    goodsclassname = models.CharField(max_length=200, verbose_name='商品类别名')
    goodsbrandname = models.CharField(max_length=200, verbose_name='品牌名称')

    qty = models.IntegerField(verbose_name='购买商品数量')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='购买商品总价')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='购买商品单价')
    originalprice = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='商品在卖场的原单价')
    imgurl = models.CharField(max_length=200, verbose_name='图片地址')
    goodsurl = models.CharField(max_length=200, verbose_name='商品地址')
    key = models.ForeignKey(Suborderlist, blank=True, on_delete=models.CASCADE, verbose_name='')

    def save(self, *args, **kwargs):
        # if self.spu:
        #     self.spu = slugify(self.spu)
        #     pass
        # if self.sku:
        #     self.sku = slugify(self.sku)
        #     pass
        super(Goodslist, self).save(*args, **kwargs)

    def get_image_url(self):
        return self.imgurl

    pass


class Discount(models.Model):
    '''
    优惠率报价
    '''
    a1 = models.DecimalField(default=2.0, max_digits=9, decimal_places=2, verbose_name='10万元（含）以下')
    a2 = models.DecimalField(default=2.2, max_digits=9, decimal_places=2, verbose_name='10万元至30万元（含）')
    a3 = models.DecimalField(default=2.4, max_digits=9, decimal_places=2, verbose_name='30万元至60万元（含）')
    a4 = models.DecimalField(default=2.7, max_digits=9, decimal_places=2, verbose_name='60万元至100万元（含）')
    defaule = models.BooleanField(default=True, verbose_name='是否为国采优惠率')
    classif_there = models.ForeignKey(Classification_There, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.a1:
            self.a1 = 0
            self.a2 = 0
            self.a3 = 0
            self.a4 = 0
        super(Discount, self).save(*args, **kwargs)
        pass

    pass


class Logistics(models.Model):
    '''
    物流信息
    '''
    info = models.TextField(verbose_name='操作信息')
    time = models.DateTimeField(auto_now=True, verbose_name='操作时间')
    username = models.CharField(max_length=15, verbose_name='操作人')
    key = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, verbose_name='关联订单号')

    class Meta:
        ordering = ['time']

    pass


class Address(models.Model):
    '''
    用户收货地址
    '''
    defaule = models.BooleanField(default=False, verbose_name='默认地址')
    consigneeName = models.CharField(max_length=20, verbose_name='收货人')
    province = models.CharField(max_length=20, verbose_name='所在地区')
    city = models.CharField(max_length=20, verbose_name='所在地区')
    area = models.CharField(max_length=20, verbose_name='所在地区', null=True)
    consigneeAddress = models.CharField(max_length=255, verbose_name='详细地址')
    consigneeMobile = models.CharField(max_length=255, verbose_name='手机号码')
    email = models.EmailField(verbose_name='邮箱', null=True)
    key = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')

    def save(self, *args, **kwargs):
        # 实其default默认地址一个用户只有一个默认开关
        Address.objects.filter(key=self.key).update(defaule=False)
        return super(Address, self).save(*args, **kwargs)

    class Meta:
        ordering = ['defaule']


class Error_Order(models.Model):
    '''国采订单接口推送错误日志'''
    info = models.CharField(max_length=5, verbose_name='订单提交失败原因', choices=(
        (0, '订单提交'),
        (1, '订单更新'),
        (2, '订单物流')
    ))
    mess = models.TextField(verbose_name='错误信息')
    time = models.DateTimeField(auto_now_add=True, verbose_name='发生时间')
    key = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    pass
