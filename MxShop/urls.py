"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from django.views.static import serve
from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListViewSet, BannerViewset, IndexCategoryViewset
from rest_framework.documentation import include_docs_urls
from goods.views import GoodsListViewSet,CategoryViewSet
from trade.views import ShoppingCartViewset, OrderViewset, AlipayView
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from users.views import UserViewset
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from users.views import SmsCodeViewset

router = DefaultRouter()

#配置goods的url
router.register(r'goods', GoodsListViewSet)
# 配置Category的url
router.register(r'categorys', CategoryViewSet, base_name="categorys")
# 配置codes的url
router.register(r'code', SmsCodeViewset, base_name="code")

router.register(r'users', UserViewset, base_name="users")

# 配置用户收藏的url
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

# 配置用户留言的url
router.register(r'messages', LeavingMessageViewset, base_name="messages")
# 配置收货地址
router.register(r'address',AddressViewset , base_name="address")

# 配置购物车的url
router.register(r'shopcarts', ShoppingCartViewset, base_name="shopcarts")

# 配置订单的url
router.register(r'orders', OrderViewset, base_name="orders")

# 配置支付宝支付相关接口的url
path('alipay/return/', AlipayView.as_view())

# 配置首页轮播图的url
router.register(r'banners', BannerViewset, base_name="banners")

# 首页系列商品展示url
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [

    path('sentry-debug/', trigger_error),
    re_path('^', include(router.urls)),

    path('xadmin/', xadmin.site.urls),
    path('ueditor/',include('DjangoUeditor.urls' )),
    #文件
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),
    # path('goods/', GoodsListView.as_view(), name='goods-list'),
    path('api-auth/',include('rest_framework.urls')),
    # drf文档，title自定义
    path('docs/', include_docs_urls(title='慕学生鲜')),
    # token
    # path('api-token-auth/', views.obtain_auth_token)

    # jwt的token认证接口
    path('login/', obtain_jwt_token)

]
