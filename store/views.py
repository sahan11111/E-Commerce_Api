from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework import viewsets
from .paginations import ProductPageNumberPagination
from django_filters import rest_framework as filters
from .filters import *
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch
# from rest_framework.pagination import PageNumberPagination


class CategoryView(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.select_related('category').all()
    serializer_class=ProductSerializer
    pagination_class=ProductPageNumberPagination
    filter_backends=(filters.DjangoFilterBackend,SearchFilter,OrderingFilter)
    # filterset_fields=('category',)
    filterset_class=ProductFilter
    search_fields=('name',)
    ordering_fields=('qty','price',)
    
class CartView(viewsets.GenericViewSet, ListModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.prefetch_related('items').filter(customer__user=user)
    
    def list(self, request, *args, **kwargs):
        cart = Cart.objects.prefetch_related('items').filter(customer__user=self.request.user).first()
        serializer = CartSerializer(cart)
        return Response(serializer.data)     
    
class CartItemView(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = AddToCartItemSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__customer__user=user)
    
    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT':
            return UpdateCartItemSerializer
        elif method == 'POST':
            return AddToCartItemSerializer
        return CartItemSerializer
    
class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        Prefetch(
            # related_name linxa first ma i.e. lookup field
            'order_items',
            
            # 'order_items' ka bata aauni ho ta vanera vanna parxa
            queryset = OrderItem.objects.all(),
            
            # related_name="order_items" xa ni teslai 'items' ma convert gardinxa
            to_attr='items',    
        ) 
    ) \
    .all()
    
    permission_classes = [
        IsAuthenticated
    ]
    
    http_method_names=[
        'get','post','patch'
    ]
    
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        # yesle k garxa vanda jun user login xa ni tyo user ko matra order items dekhauxa
        
        return self.queryset.filter(user=user)
    
    def get_serializer_class(self):
        method = self.request.method
        if method == 'GET':
            return OrderSerializer
        
        if method == 'POST':
            
            return PlaceOrderSerializer
        return CancelOrderSerializer
  


# # Create your views here.
# class CategoryList(GenericAPIView,ListModelMixin,CreateModelMixin):
#     queryset=Category.objects.all()
#     serializer_class=CategorySerializer
#     def get(self,request,*args, **kwargs):
#         return self.list(request,args,kwargs)
#         # categories=Category.objects.all()
#         # serializer=CategorySerializer(categories,many=True)
#         # return Response(serializer.data)
#     def post(self,request):
#         return self.create(request)
#         # serializer=CategorySerializer(data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()
    
#         # return Response(
#         # serializer.data,
#         #     status=status.HTTP_201_CREATED
#         # )
# class CategoryDetail(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
#     def get(self,request,pk):
#         return  self.retrieve(request,pk)
#         # category=get_object_or_404(Category,pk=pk)
#         # serializer=CategorySerializer(category)
#         # return Response(serializer.data)
#     def put(self,request,pk):
#         # category=get_object_or_404(Category,pk=pk)
#         # serializer=CategorySerializer(category,data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         # return Response(serializer.data)
#         return self.update(request,pk)
#     def delete(self,request,pk):
#         # category=get_object_or_404(Category,pk=pk)
#         # category.delete()
#         # return Response(status=status.HTTP_204_NO_CONTENT)
#         return self.destroy(request,pk)
        
            
# @api_view(['GET','POST'])
# def category_list(request):
#     if request.method=='POST':
#         serializer=CategorySerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
    
#         return Response(
#         serializer.data,
#             status=status.HTTP_201_CREATED
#         )
    
    
#     categories=Category.objects.all()
#     serializer=CategorySerializer(categories,many=True)
    
#     return Response(
#         serializer.data
#     )
# @api_view(['GET','PUT','DELETE'])
# def category_detail(request,pk):
#     category=get_object_or_404(Category,pk)
        
    
        
#     # try:
#     # except Category.DoesNotExist:
#     #     return Response(
#     #         {'error':'Category not found'},
#     #         status=status.HTTP_404_NOT_FOUND
#     #     )
#     if request.method =='GET':
                
#                 serializer=CategorySerializer(category)
#                 return Response(serializer.data)
#     elif request.method=='PUT':
#                 serializer=CategorySerializer(instance=category,data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#                 return Response(serializer.data)
#     elif request.method=='DELETE':
#                 category.delete()
                
#                 return Response(status=status.HTTP_204_NO_CONTENT)