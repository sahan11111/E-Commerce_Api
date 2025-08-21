from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'qty', 'category',)
    search_fields=('name','price')
    list_filter=['category']
    list_per_page=10
    
    
@admin.register(Customer)
class  CustomerAdmin(admin.ModelAdmin):
      list_display = ['first_name','last_name','shipping_address','middle_name']
      search_fields=('first_name','last_name')   
      list_filter=['first_name','last_name']
      list_per_page=5
      
      

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer']
    list_per_page=5
    search_fields=('id',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'qty']
    search_fields=('product','cart')  
    list_per_page=5
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['payment_mode', 'status', 'customer', 'place', 'is_paid']
    list_per_page=20
    readonly_fields = ("pk",)
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'qty', 'price']
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'comment', 'rating']
    search_fields = ['customer', 'comment',]
