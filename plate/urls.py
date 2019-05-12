from django.urls import path, re_path
from plate.views import IndexView

app_name = 'plate'

urlpatterns = [
    path('<int:id>/<str:slug>/', IndexView.as_view(), name='index')
]
