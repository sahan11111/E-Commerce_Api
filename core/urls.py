from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework import routers
router=routers.SimpleRouter()
router.register('user',UserView)
# router.register('products',ProductView)

urlpatterns = [
    
    
    ]+router.urls