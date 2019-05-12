# Create your views here.
from rest_framework.viewsets import ViewSet

from app.models import WareApp
from search.serializers import GoodsImageList
from search.viewsets import RestSearchView


class RestfulSearchView(ViewSet, RestSearchView):
    '''
    搜索商品
    '''
    def get_content_results(self):
        results = []
        r = super(RestfulSearchView, self).get_content_results()
        for item in r:
            results.append({
                **item,
                'image': GoodsImageList(WareApp.objects.get(id=item['id']).images_set.filter(), many=True).data
            })
            pass
        return results
    pass
