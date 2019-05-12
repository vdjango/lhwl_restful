from django.contrib.auth.models import AnonymousUser

from account import models
from lhwill.settings import HTTP_HOST

from lhwill.util import complete
from lhwill.util.log import log
from managestage.models import SearchStatistics

logger = log(globals())


def template_defaule(request):
    '''
    模板全局变量
    :param request:
    :return:
    '''

    from django.contrib.sites.models import Site

    url = '{}'.format(HTTP_HOST.split('//')[1])
    try:
        s = Site.objects.get(pk=1)
        if s.name != url:
            s.name = url
            s.domain = url
            s.save()
            logger.i('save', s.name)
            pass
        logger.i('ok ', s.name)
    except:
        Site.objects.create(pk=1, domain=url, name=url)
        logger.i('create', s.name)

    user = request.user

    if not user.is_authenticated:
        user = None

    sysup = complete.systemsetup()

    search_filter = SearchStatistics.objects.filter()[:10]


    context = {
        'user': user,  # 新
        'site_name': sysup.get_sitename(),
        'site_tags': sysup.get_sitetags(),
        'site_icp': sysup.get_icp(),
        'site_url': sysup.get_url(),
        'description': '',
        'keywords': '',

        'search_filter': search_filter,
    }

    return context
