'''
Models模型相关接口
私有访问权限
'''

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response

from account.models import User
from api.serializers import SerializersModel
from api.util.ModelViewUtil import ModelViewSet, ModelPrivateWriteViewSet
from app import models as AppModels
from home import models as HomeModels
from lhwill.util.log import log

logger = log(globals())


class ModelPrivateViewSet(ModelViewSet):
    permission_pubilc_write = False


class UserViewSet(ModelPrivateWriteViewSet):
    """
    用户API，有关于记录用户账号密码以及基本信息
    """
    queryset = User.objects.filter().order_by('-date_joined')
    serializer_class = SerializersModel.UserSerializer
    permission_pubilc_write = False
    SAFE_METHODS = ('HEAD', 'OPTIONS')

    def perform_create(self, serializer):
        serializer.save()
        u = User.objects.get(username=serializer.data['username'])
        u.set_password(serializer.data['password'])
        u.save()
        return u.password

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = self.perform_create(serializer)
        context = serializer.data
        context['password'] = password

        headers = self.get_success_headers(context)
        return Response(context, status=status.HTTP_201_CREATED, headers=headers)



class InvoicesViewSet(ModelPrivateViewSet):
    """发票信息Models"""
    queryset = HomeModels.Invoices.objects.filter()
    serializer_class = SerializersModel.InvoicesSerializer

    def create(self, request, *args, **kwargs):
        model_queryset = self.queryset.filter(key_id=request.data['key'])
        if model_queryset.exists():
            return Response({}, status=403)
        return super(InvoicesViewSet, self).create(request, *args, **kwargs)

    pass


class AddressViewSet(ModelPrivateViewSet):
    """收货地址Models"""
    queryset = HomeModels.Address.objects.filter()
    serializer_class = SerializersModel.AddressSerializer


class RateDisplayViewSet(ModelPrivateViewSet):
    """
    > 获取央采18类各类商品

    添加<code>?rate=rate</code> 获取18类的商品
    """

    queryset = AppModels.RateClassgUid.objects.filter()
    serializer_class = SerializersModel.RateDisplaySerializer
    user_key = None

    def dispatch(self, request, *args, **kwargs):
        self.uid = request.GET.get('rate')
        return super(RateDisplayViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        logger.i('RateDisplayViewSet', self.__class__.__name__)

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance_ = self.get_object()
        if self.uid == 'rate':

            instance = self.filter_queryset(instance_.wareappprefix_set.filter(wareApp_key__release=True))

            data = []
            for i in instance:
                logger.i('there', i.id, )
                data.append({
                    "id": instance_.id,
                    "ther_id": i.id,
                    "classify_key": {
                        "id": i.classify_key.id,
                        "name": i.classify_key.name
                    },
                    "classifythere_key": {
                        "id": i.classifythere_key.id,
                        "name": i.classifythere_key.name
                    },
                    "rate_classg_key": {
                        "id": i.rate_classg_key.id,
                        "uid": i.rate_classg_key.uid,
                        "a1": i.rate_classg_key.a1,
                        "a2": i.rate_classg_key.a2,
                        "a3": i.rate_classg_key.a3,
                        "a4": i.rate_classg_key.a4,
                        "defaule": i.rate_classg_key.defaule
                    },
                    "wareApp_key": {
                        'id': i.wareApp_key.id,
                        'name': i.wareApp_key.name,
                        'slug': i.wareApp_key.slug,
                        'money': i.wareApp_key.money,
                        'image': i.wareApp_key.get_image_url(),
                        'unix': i.wareApp_key.unix,
                        'release': i.wareApp_key.release,
                        'release_version': i.wareApp_key.release_version
                    }
                })

            return Response(data)
            pass
        else:
            serializer = self.get_serializer(instance_)

        return Response(serializer.data)
