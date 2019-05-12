# Create your views here.
from django.http import HttpResponse

from app.models import WareAppPrefix
from app.util.classify import getClassify
from lhwill.util.log import log
from lhwill.view import AppGenric
from lhwill.view.HttpCodeError import get_object_or_404
from plate import models

logger = log(globals())


class IndexView(AppGenric.AppTemplateView):
    template_name = 'defaule/plate/index.html'
    template_mobile_name = 'defaule/m/plate/index.html'

    _context_data = True
    _context_data_response = None

    def get_context_data(self, **kwargs):

        plat = get_object_or_404(self.request, models.plateModels, id=kwargs['id'], slug=kwargs['slug'])
        if type(plat) == HttpResponse:
            self._context_data = False
            self._context_data_response = plat
        else:
            kwargs['Content'] = models.plateContent.objects.filter(key=plat)
            kwargs['Models'] = plat
            kwargs.update(getClassify())

        return kwargs

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)

        if not self._context_data:
            logger.i(self._context_data_response)
            return self._context_data_response

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

    pass
