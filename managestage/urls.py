"""Retailers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.urls import path

from managestage import views
from managestage.view import AdmUser, AdmComplete, AdmCommodity, AdmSector, AdmPage, AdmOrder, AdmPlate

app_name = 'admins'

urlpatterns = [
    # 全局-站点设置
    url(r'^complete/$', views.plate.AdmComplete, name='complete'),
    url(r'^complete/set_system/$', AdmComplete.set_system, name='set_system'),
    url(r'^complete/set_maintain/$', AdmComplete.set_maintain, name='set_maintain'),
    url(r'^complete/seosetup/$', AdmComplete.seosetup, name='seosetup'),
    url(r'^complete/set_mailsmtp/$', AdmComplete.set_mailsmtp, name='set_mailsmtp'),
    url(r'^complete/send_email/$', AdmComplete.send_email, name='send_email'),
    url(r'^complete/set_appid/$', AdmComplete.set_appid, name='set_appid'),
    url(r'^complete/partysetup/$', AdmComplete.partysetup, name='partysetup'),
    url(r'^complete/setclassify_orthere/$', AdmComplete.setclassify_orthere, name='setclassify_orthere'),

    # 用户-用户管理
    path('user/', views.UserView.as_view(), name='user'),
    url(r'^user/get_username/$', AdmUser.get_username, name='get_username'),
    url(r'^user/del_user/$', AdmUser.del_user, name='del_user'),
    url(r'^user/set_email/$', AdmUser.set_email, name='set_email'),
    url(r'^user/set_username/$', AdmUser.set_username, name='set_username'),
    url(r'^user/set_password/$', AdmUser.set_password, name='set_password'),
    url(r'^user/add_user/$', AdmUser.add_user, name='add_user'),
    url(r'^user/set_admin/$', AdmUser.set_admin, name='set_admin'),
    url(r'^user/examine/$', AdmUser.examine, name='examine'),
    url(r'^user/set_examine/$', AdmUser.set_examine, name='set_examine'),

    # 商品
    url(r'^commodity/$', views.plate.AdmCommodity, name='commodity'),
    url(r'^commodity/(\d+)/$', views.plate.AdmCommodity, name='commodity'),

    path('commodity/create/', AdmCommodity.ArticleRelease.as_view(), name='ware'),
    path('commodity/create/<int:app_id>/<int:app_unix>/', AdmCommodity.ArticleRelease.as_view(), name='ware'),
    path('commodity/create/info/<int:app_id>/<int:app_unix>/<int:app_there>/',
         AdmCommodity.ArticleInfoRelease.as_view(), name='info'),

    url(r'^commodity/create/parameter/(\d+)/(\d+)/$', AdmCommodity.parameter, name='parameter'),

    url(r'^commodity/create/createParameter/$', AdmCommodity.add_Parameter, name='createParameter'),  # aaaaa
    url(r'^commodity/online/(\d+)/(\d+)/$', AdmCommodity.online, name='online'),
    url(r'^commodity/add_mode/$', AdmCommodity.add_mode, name='addmode'),
    url(r'^commodity/add_choice/$', AdmCommodity.add_choice, name='add_choice'),
    url(r'^commodity/release/(\d+)/(\d+)/$', AdmCommodity.release, name='release'),
    url(r'^commodity/set_online/$', AdmCommodity.set_online, name='set_online'),
    url(r'^commodity/deletle/$', AdmCommodity.del_ware, name='del_ware'),
    url(r'^commodity/deletle/(\d+)/$', AdmCommodity.del_ware, name='del_ware'),
    url(r'^commodity/stay/$', AdmCommodity.stay, name='stay'),
    url(r'^commodity/stay/(\d+)$', AdmCommodity.stay, name='stay'),
    url(r'^commodity/import/$', AdmCommodity.import_Wareapp, name='import'),

    path('commodity/ClassZycg/', AdmCommodity.ClassZycg.as_view(), name='ClassZycg'),
    path('commodity/SettupView/', AdmCommodity.SettupView.as_view(), name='SettupView'),
    path('Initialization/', AdmCommodity.Initialization.as_view(), name='Initialization'),

    url(r'^importfile/$', AdmCommodity.importfile, name='importfile'),

    url(r'^commodity/setupcommod/$', AdmCommodity.SetupCommod, name='setupcommod'),
    url(r'^get_classModels/$', AdmCommodity.get_classModels, name='get_classModels'),
    url(r'^get_ClassifyTwo/$', AdmCommodity.get_ClassifyTwo, name='get_classifyTwo'),

    # 板块
    url(r'^sector/$', views.plate.AdmSector, name='sector'),
    url(r'^sector/get_ware/$', AdmSector.get_ware, name='get_ware'),
    url(r'^sector/add_sector/$', AdmSector.add_sector, name='add_sector'),
    url(r'^sector/set_addSector/$', AdmSector.set_addSector, name='set_addSector'),
    url(r'^sector/set_brock/$', AdmSector.set_brock, name='set_brock'),
    url(r'^sector/add_label/$', AdmSector.add_label, name='add_label'),
    url(r'^sector/get_label/$', AdmSector.get_label, name='get_label'),
    url(r'^sector/set_label/$', AdmSector.set_label, name='set_label'),
    url(r'^sector/del_brock/$', AdmSector.del_brock, name='del_brock'),
    url(r'^sector/add_WareAppBrock/$', AdmSector.add_WareAppBrock, name='add_WareAppBrock'),
    url(r'^sector/del_WareAppBrock/$', AdmSector.del_WareAppBrock, name='del_WareAppBrock'),
    url(r'^sector/classify/$', AdmSector.classify.as_view(), name='classify'),
    url(r'^sector/add_classify/$', AdmSector.add_classify, name='add_classify'),
    url(r'^sector/del_classify/$', AdmSector.del_classify, name='del_classify'),
    url(r'^sector/add_classifyLabel/$', AdmSector.add_classifyLabel, name='add_classifyLabel'),
    url(r'^sector/get_classify/$', AdmSector.get_classify, name='get_classify'),
    url(r'^sector/set_classify/$', AdmSector.set_classify, name='set_classify'),
    url(r'^sector/get_classifyLabel/$', AdmSector.get_classifyLabel, name='get_classifyLabel'),
    url(r'^sector/set_classifyLabel/$', AdmSector.set_classifyLabel, name='set_classifyLabel'),
    url(r'^sector/del_classifyLabel/$', AdmSector.del_classifyLabel, name='del_classifyLabel'),
    url(r'^sector/add_classify_two/$', AdmSector.add_classify_two, name='add_classify_two'),
    url(r'^sector/get_classifytwo/$', AdmSector.get_classifytwo, name='get_classifytwo'),
    url(r'^sector/get_classifythere/$', AdmSector.get_classifythere, name='get_classifythere'),
    url(r'^sector/add_classifythere/$', AdmSector.add_classifyThere, name='add_classifyThere'),
    url(r'^sector/set_classifytwo/$', AdmSector.set_classifyTwo, name='set_classifyTwo'),
    url(r'^sector/set_classifythere/$', AdmSector.set_classifyThere, name='set_classifyThere'),
    url(r'^sector/del_classifytwo/$', AdmSector.del_classifyTwo, name='del_classifyTwo'),
    url(r'^sector/del_classifythere/$', AdmSector.del_classifyThere, name='del_classifyThere'),
    url(r'^sector/navigation/$', AdmSector.navigation, name='navigation'),
    url(r'^sector/add_navigation/$', AdmSector.add_Navigation, name='add_navigation'),
    url(r'^sector/add_navigationtwo/$', AdmSector.add_NavigationTwo, name='add_navigationtwo'),
    url(r'^sector/set_navigation/$', AdmSector.set_Navigation, name='set_navigation'),
    url(r'^sector/set_navigationtwo/$', AdmSector.set_NavigationTwo, name='set_navigationtwo'),
    url(r'^sector/del_navigation/$', AdmSector.del_Navigation, name='del_navigation'),
    url(r'^sector/del_navigationTwo/$', AdmSector.del_NavigationTwo, name='del_navigationtwo'),
    url(r'^sector/broadcast/$', AdmSector.broadcast, name='broadcast'),
    url(r'^sector/_add_broadcast/$', AdmSector._add_broadcast, name='_add_broadcast'),
    url(r'^sector/_set_broadcast/$', AdmSector._set_broadcast, name='_set_broadcast'),
    url(r'^sector/del_broadcast/$', AdmSector.del_broadcast, name='del_broadcast'),
    url(r'^sector/setupsearch/$', AdmSector.SetupSearch, name='setupsearch'),
    url(r'^sector/setupparameter/$', AdmSector.setupParameterView, name='setupparameter'),
    url(r'^sector/add_Brand/$', AdmSector.add_Brand, name='add_brand'),
    # ---
    url(r'^sector/add_filter/$', AdmSector.add_filter, name='add_filter'),
    url(r'^sector/parter/$', AdmSector.get_parter, name='get_parter'),
    url(r'^sector/wareparCHOICES/$', AdmSector.get_wareparCHOICES, name='warechoices'),
    path('sector/DiscountView/', AdmSector.DiscountView.as_view(), name='discount'),
    url(r'^sector/adddiscount/$', AdmSector.addDiscount, name='adddiscount'),
    url(r'^sector/getDiscount/$', AdmSector.getDiscount, name='getDiscount'),

    path('sector/searchlevel/', AdmSector.searchLevel.as_view(), name='searchLevel'),

    url(r'^sector/setupprefix/$', AdmSector.SetupPrefix, name='setupprefix'),
    url(r'^get_WareSetupPrefix/$', AdmSector.get_WareSetupPrefix, name='get_WareSetupPrefix'),

    # 订单部分
    url(r'^order/$', views.AdmOrder.as_view(), name='order'),
    url(r'^order/userorder/$', AdmOrder.UserOrder, name='userorder'),
    url(r'^order/setonorder/$', AdmOrder.setOnOrder, name='setonorder'),
    url(r'^order/setAddesOrder/$', AdmOrder.setAddesOrder, name='setaddesorder'),
    url(r'^order/getOrderAcceptanceCheck/$', AdmOrder.getOrderAcceptanceCheck, name='getOrderAcceptanceCheck'),
    url(r'^order/setOrderIspaid$', AdmOrder.setOrderIspaid, name='setOrderIspaid'),
    url(r'^order/contract/$', AdmOrder.ContractView, name='contract'),
    url(r'^order/acceptances/$', AdmOrder.Acceptances, name='acceptances'),
    url(r'^order/delacceptances/$', AdmOrder.delAcceptances, name='delacceptances'),
    url(r'^order/Approval/$', AdmOrder.Approval, name='Approval'),
    url(r'^order/orderCartWare/$', AdmOrder.orderCartWare.as_view(), name='orderCartWare'),

    #
    url(r'^page/$', views.plate.Page, name='page'),
    url(r'^page/create/$', AdmPage.Page_createView, name='page_create'),
    url(r'^page/navplate/$', AdmPage.Page_NavPlate, name='navplate'),
    url(r'^page/navkeyword/$', AdmPage.Page_NavWareAppKeyword, name='navkeyword'),
    url(r'^page/get_navaid/$', AdmPage.get_navaid, name='get_navaid'),

    path('plate/', AdmPlate.IndexView.as_view(), name='AdmPlate')

]
