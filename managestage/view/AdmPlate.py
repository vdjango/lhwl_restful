from django.views.generic import TemplateView

from lhwill.util.log import log
from plate import models

logger = log(globals())


class IndexView(TemplateView):
    template_name = 'defaule/admin/plate/index.html'

    def get_context_data(self, **kwargs):
        plateContent = models.plateContent.objects.filter()

        Content = []

        for i in models.plateModels.objects.filter():
            Content.append({
                'Models': i,
                'Content': plateContent.filter(key=i),
            })

        context = {
            'Content': Content,
        }
        kwargs.update(context)
        return kwargs
