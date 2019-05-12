from rest_framework import serializers

from app import models
from lhwill import settings


class GoodsImageList(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, instance):
        return '{}{}'.format(settings.HTTP_HOST, instance.image.url)

    class Meta:
        model = models.images
        fields = '__all__'
    pass
