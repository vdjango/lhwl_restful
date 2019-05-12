from django.conf.urls import url, include

from payment.views import recharge, aliapy_back_url

urlpatterns = [
    url(r"^alipay/", recharge),
    url(r"^aliapy_back_url/", aliapy_back_url),
]
