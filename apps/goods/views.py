from django.shortcuts import render

'''
# Create your views here.
from rest_framework.views import APIView
from goods.serializers import GoodsSerializer
from .models import Goods
from rest_framework.response import Response


class GoodsListView(APIView):
 
    def get(self,request,format=None):
        goods = Goods.objects.all()
        goods_serialzer = GoodsSerializer(goods,many=True)
        return Response(goods_serialzer.data)
'''


from goods.serializers import GoodsSerializer,CategorySerializer
from .models import Goods,GoodsCategory
from rest_framework.response import Response
from rest_framework import mixins, viewsets
from rest_framework import generics

'''
class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
    '商品列表页'
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
'''

from rest_framework.pagination import PageNumberPagination

class GoodsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    #默认每页显示的个数
    page_size = 10
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100

from .filters import GoodsFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class GoodsListViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '商品列表页'

    #这里必须要定义一个默认的排序,否则会报错
    queryset = Goods.objects.all().order_by('id')
    # 分页
    pagination_class = GoodsPagination
    #序列化
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)

    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # 搜索,=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('name', 'goods_brief','goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''

    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
