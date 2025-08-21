
from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework import routers
router=routers.SimpleRouter()
router.register('categories',CategoryView)
router.register('products',ProductView)
router.register('cart/items',CartItemView)
router.register('cart',CartView)
router.register('orders',OrderView)

urlpatterns = [
    # path('categories',category_list),
    # path('categories',category_detail),
    # path('categories',CategoryView.as_view()),
    # path('categories/<pk>',CategoryView.as_view()),
    
]+router.urls
