from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.settings import api_settings


class ListMethodMixin(mixins.ListModelMixin):
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        return super(ListMethodMixin, self).list(request, *args, **kwargs)


class CreateMethodMixin(mixins.CreateModelMixin):
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        return super(CreateMethodMixin, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class RetrieveMethodMixin(mixins.RetrieveModelMixin):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        return super(RetrieveMethodMixin, self).retrieve(request, *args, **kwargs)


class UpdateMethodMixin(mixins.UpdateModelMixin):
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        return super(UpdateMethodMixin, self).update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyMethodMixin(mixins.DestroyModelMixin):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        return super(DestroyMethodMixin, self).destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
