from django.views import generic

from lhwill.util.log import log
from managestage import models
logger = log(globals())


class AppTemplateView(generic.TemplateView):
    '''手机端视图'''

    # 移动端HTML模板
    template_mobile_name = None
    app_mobile = False

    def dispatch(self, request, *args, **kwargs):
        # self.app_mobile = self.get_mobile()
        self.request = request
        return super(AppTemplateView, self).dispatch(request, *args, **kwargs)

    def get_mobile(self):
        '''
        用于获取用户访问的浏览器标识
        True 移动
        Fale PC
        :return:
        '''

        logger.i('HTTP_USER_AGENT', self.request.META)
        models.HTTP_USER_AGENT.objects.create(
            agent=self.request.META['HTTP_USER_AGENT'],
            path_info=self.request.META['PATH_INFO'],
            method=self.request.META['REQUEST_METHOD'],
            accept=self.request.META['HTTP_ACCEPT']
        )

        if self.template_mobile_name:
            if not 'Windows' in self.request.META['HTTP_USER_AGENT']:
                self.template_name = self.template_mobile_name
                logger.i('HTTP_USER_AGENT', 'not Windows')
            pass

        return self.app_mobile

    pass
