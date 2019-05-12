'''
功能相关接口
公共访问权限
'''
from django.db.models import Sum
from rest_framework import views, status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin, ViewSet, GenericViewSet, ReadOnlyModelViewSet

from api.serializers.SerializersAppMethod import IndexSerializer, WheelSerializer, SectorSerializer
from api.serializers.SerializersMethodl import SearchingList, _SearchingListWareApp
from api.serializers.SerializersModel import SubCategory, Category
from api.util.LimitOffsetPagination import Pagination, PaginationObject
from api.util.ModelViewUtil import ModelViewSet
from lhwill.util.log import log
from app import models as App

logger = log(globals())


class ModelPublicViewSet(ModelViewSet):
    '''
    公共权限，允许公共读，写需要权限验证，
    添加数据，修改验证用户数据
    '''
    permission_pubilc_write = True

# class IndexViewSet(GenericViewSet):
#     serializers_list = [
#         {
#             'serializers': IndexSerializer,
#             'models': App.Classification.objects.prefetch_related(None).filter()
#         }
#     ]
#
#     def exserializer(self):
#         content = {}
#         for item in self.serializers_list:
#             content.update({
#                 item['serializers']().__class__.Meta.serializers_label_name: item['serializers'](self.filter_queryset(item['models']), many=True).data
#             })
#             pass
#         return content
#
#     def get_content(self, **kwargs):
#         kwargs.update(self.exserializer())
#         return kwargs
#
#     def list(self, resquest, *args, **kwargs):
#         return Response(self.get_content(), status=status.HTTP_200_OK)
#
#     pass


class IndexViewSet(ReadOnlyModelViewSet):
    '''
    首页梯级分类 序列化
    首页分类，子分类
    '''
    serializer_class = IndexSerializer
    queryset = App.Classification.objects.prefetch_related(None).filter()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            self.serializer_class.Meta.serializers_label_name: serializer.data
        })
    pass

class IndexSectorViewSet(GenericViewSet):
    '''
    首页板块栏目，板块类别 展示商品
    '''
    serializer_class = SectorSerializer
    queryset = App.SectorModel.objects.prefetch_related(None).filter()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            self.serializer_class.Meta.serializers_label_name: serializer.data
        })
    pass

class IndexWheelViewSet(GenericViewSet):
    '''
    首页轮播图
    '''
    serializer_class = WheelSerializer
    queryset = App.WheelModel.objects.prefetch_related(None).filter()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            self.serializer_class.Meta.serializers_label_name: serializer.data
        })
    pass

class IndexSearchingList(ModelPublicViewSet):
    serializer_class = SearchingList
    queryset = App.Classification_There.objects.prefetch_related(None).filter()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        queryset_search = instance.wareappprefix_set.filter()

        page = PaginationObject()
        page_roles = page.paginate_queryset(queryset=queryset_search, request=request, view=self)
        search = _SearchingListWareApp(page_roles, many=True).data

        context = {}
        context.update(serializer.data)
        context.update({
            'search': page.get_paginated_response(search)
        })

        return Response(context)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    pass

from haystack.views import SearchView

class SearchViewSet(GenericViewSet):
    def list(self, request):
        SearchView()
        return Response({})
    pass

