from app import models
from lhwill import settings
from lhwill.util.log import log
from managestage.models import Setclassify

logger = log(globals())

'''
需要重构， 代码待优化，加载速度太慢
'''


def getClassify():
    '''
        页面全部分类数据
        '''
    navigation = models.Navigation.objects.filter()  # 导航
    navigation_Two = models.Navigation_Two.objects.filter()  # 子导航

    setclassifys = None
    connet_bar = []
    classify_assortment = []

    setclassifys = setclassify = Setclassify.objects.filter()
    if setclassifys.exists():
        setclassifys = setclassifys[0]

        if setclassify.radio == '2':
            '''全部分类 二级深度'''
            for line in models.Classification.objects.filter():
                '''
                分类数据
                '''
                connets = []

                for line_2 in models.Classification_There.objects.filter(Classifykey=line.id):
                    ''' 分类数据首图 '''
                    wareFrefix = models.WareAppPrefix.objects.filter(classifythere_key=line_2)
                    image = 'http://i1.mifile.cn/f/i/g/2015/TV4-75.png?width=80&amp;height=80'
                    if wareFrefix.exists():
                        try:
                            image = wareFrefix[0].wareApp_key.get_image_url_64x64()
                        except:
                            pass

                    connets.append(
                        {
                            "title": line_2.name,
                            "image": image,
                            "url": line_2.url
                        }
                    )

                connet_bar = []
                for line_2 in models.Classification_bar.objects.filter(key=line.id):
                    connet_bar.append(
                        {
                            "title": line_2.name,
                            "url": line_2.url
                        }
                    )

                classify_assortment.append(
                    {
                        "title": line.name,
                        "connets": connets,
                        "connet_bar": connet_bar
                    }
                )
                pass



    else:
        '''全部分类 三级深度'''
        for line in models.Classification.objects.filter():
            '''
            分类数据
            '''
            connets = []
            for line_1 in models.Classification_Two.objects.filter(key=line.id):
                connet_list = []
                for line_2 in models.Classification_There.objects.filter(key=line_1.id):
                    ''' 分类数据首图 '''
                    wareFrefix = models.WareAppPrefix.objects.filter(classifythere_key=line_2)
                    image = 'http://i1.mifile.cn/f/i/g/2015/TV4-75.png?width=80&amp;height=80'
                    if wareFrefix.exists():
                        try:
                            image = models.images.objects.filter(key=wareFrefix[0].wareApp_key)[0].image.url_64x64
                        except IndexError:
                            pass

                    connet_list.append(
                        {
                            "title": line_2.name,
                            "image": image,
                            "url": line_2.url
                        }
                    )

                connets.append(
                    {
                        "subtitle": line_1.subtitle,
                        "url": line_1.url,
                        "connets_list": connet_list,
                        "connet_bar": connet_bar
                    }
                )

            connet_bar = []
            for line_2 in models.Classification_bar.objects.filter(key=line.id):
                connet_bar.append(
                    {
                        "title": line_2.name,
                        "url": line_2.url
                    }
                )

            classify_assortment.append(
                {
                    "title": line.name,
                    "connets": connets,
                    "connet_bar": connet_bar
                }
            )
            pass

    context = {
        'navigation': navigation,
        'navigation_two': navigation_Two,
        'classify_assortment': classify_assortment,
        'setclassify': setclassifys,
    }
    return context
