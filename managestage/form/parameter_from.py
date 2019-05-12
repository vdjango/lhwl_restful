from django import forms

class Form(forms.Form):
    model = forms.CharField(max_length=200, label='产品型号')
    colorType = forms.CharField(max_length=200, label='颜色类型')
    coverFunction = forms.CharField(max_length=200, label='涵盖功能')
    velocityType = forms.CharField(max_length=200, label='速度类型')
    maximumOriginalSize = forms.CharField(max_length=200, label='最大原稿尺寸')
    memory = forms.CharField(max_length=200, label='内存容量')
    hardDisk = forms.CharField(max_length=200, label='硬盘容量')
    forPaperCapacity = forms.CharField(label='供纸容量', widget=forms.Textarea)
    mediumWeight = forms.CharField(label='介质重量', widget=forms.Textarea)
    materialDescription = forms.CharField(max_length=200, label='材料描述')
    doubleSidedDevice = forms.CharField(max_length=200, label='双面器')
    automaticDrafts = forms.CharField(max_length=200, label='自动输稿器')
    networkFunction = forms.CharField(max_length=200, label='网络功能')
    highestCv = forms.CharField(max_length=200, label='最高月印量')

    '''
    复印功能
    '''
    photocopyingSpeed = forms.CharField(max_length=200, label='复印速度')
    PhotocopyingResolution = forms.CharField(max_length=200, label='复印分辨率')
    copySize = forms.CharField(max_length=200, label='复印尺寸')
    preheatingTime = forms.CharField(max_length=200, label='预热时间')
    copyPhotocopyingPage = forms.CharField(max_length=200, label='首页复印时间')
    continuityXeroxPages = forms.CharField(max_length=200, label='连续复印页数')
    zoomRange = forms.CharField(max_length=200, label='缩放范围')
    copyOdds = forms.CharField(max_length=200, label='复印赔率')

    '''
    打印功能
    '''
    printController = forms.CharField(max_length=200, label='打印控制器')
    printingSpeed = forms.CharField(max_length=200, label='打印速度')
    printResolution = forms.CharField(max_length=200, label='打印分辨率')
    printLanguage = forms.CharField(label='打印语言', widget=forms.Textarea)
    printingOtherPerformance = forms.CharField(label='打印其他性能', widget=forms.Textarea)

    '''
    扫描功能
    '''
    scanningController = forms.CharField(max_length=200, label='扫描控制器')
    scanningResolution = forms.CharField(max_length=200, label='扫描分辨率')
    outputFormat = forms.CharField(max_length=200, label='输出格式')
    scanningOtherPerformance = forms.CharField(label='扫描其他性能', widget=forms.Textarea)

    '''
    传真功能
    '''
    facsimileController = forms.CharField(max_length=200, label='传真控制器')
    modemSpeed = forms.CharField(max_length=200, label='制解调器速度')
    dataCompressionMethod = forms.CharField(max_length=200, label='数据压缩方式')
    faxOtherPerformance = forms.CharField(label='传真其他性能', widget=forms.Textarea)

    '''
    其他特性
    '''
    display = forms.CharField(max_length=200, label='液晶显示屏')
    mainframeSize = forms.CharField(max_length=200, label='主机尺寸')
    weight = forms.CharField(max_length=20, label='重量')
    otherFeatures = forms.CharField(max_length=200, label='其他特点')
    timeMarket = forms.CharField(max_length=200, label='上市时间')

    '''
    复印机附件
    '''
    optionalAccessories = forms.CharField(max_length=200, label='可选配件')

    '''
    保修信息
    '''
    warrantyTime = forms.CharField(max_length=200, label='质保时间')
    customerService = forms.CharField(max_length=200, label='客服电话')
    detailedContent = forms.CharField(label='详细内容', widget=forms.Textarea)
    pass




