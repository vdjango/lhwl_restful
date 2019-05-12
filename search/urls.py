from django.urls import path, include
from rest_framework import routers

from search.views import RestfulSearchView

router = routers.DefaultRouter()
router.register('search', RestfulSearchView, base_name='search')

urlpatterns = [
    path('', include(router.urls)),
]
