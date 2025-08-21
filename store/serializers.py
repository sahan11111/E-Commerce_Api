from rest_framework import serializers
from .models import *
from decimal import Decimal
from django.db import transaction

# class CategorySerializer(serializers.Serializer):
#     id=serializers.IntegerField()
#     name=serializers.CharField(max_length=40)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        # fields=['id','name']
        fields='__all__'
# def create(self, validated_data):
#     category=Category.objects.create(
#         **validated_data
#         )
#     return category

# def update(self,category:Category, validated_data):
#     category.name=validated_data.get('name')
#     category.save()
#     return category

# def delete(self,category:Category):
#     category.delete()
#     return category

class ProductSerializer(serializers.ModelSerializer):
    category_id=serializers.PrimaryKeyRelatedField(
    queryset=Category.objects.all(),
    source="category"
    )
    category=serializers.StringRelatedField()
    price_with_tax=serializers.SerializerMethodField()
    class Meta:
        model=Product
        # fields=['id','name','price','category']
        fields=[
            'id','name','category_id','category','price','qty','price_with_tax'
        ]
    
    def get_price_with_tax(self,product:Product):
        thirteen_percent_of_product=(product.price*Decimal(0.13))
        return   thirteen_percent_of_product + product.price 


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# For showing cart items information
class AddToCartItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = 'product'        
    )
    qty = serializers.IntegerField(allow_null=True)
    class Meta:
        model = CartItem
        fields = [
            'id',
            'user',
            'product_id',
            'qty',
        ]
    @transaction.atomic 
    def create(self, validated_data):
        user = validated_data.pop('user')
        product = validated_data['product']
        cart,_ = Cart.objects.get_or_create(user=user)
        validated_data.update({
            'cart_id': cart.pk
        })
        qty=validated_data.get('qty')
        try:
            cart_item = CartItem.objects.get(cart__user=user, product=product)
            cart_item.qty += 1 if qty is None else qty
            cart_item.save()
            
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(**validated_data)
            
        return cart_item

# For updating cart items in add to cart
class UpdateCartItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = CartItem
        fields = [
            'id',
            'user',
            'qty',
        ]
        
class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        source = 'product',
    )
    user = serializers.StringRelatedField()
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        fields=[
            'id',
            'user',
            'product_id',
            'product',
            'qty',
            'total_price',
            'total_price_with_tax',
        ]
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'items',
            'total_price',
            'total_price_with_tax',
        ]
        
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'       
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        
class PlaceOrderSerializer(serializers.ModelSerializer):
    delivery_address = serializers.CharField(max_length=255)
    class Meta:
        model = Order
        fields = [
            'delivery_address',
        ]
        
    @transaction.atomic
    def create(self, validated_data):
        
        user = self.context['request'].user
        items = CartItem.objects.filter(cart__user=user)
        
        # order create hunxa
        order = Order.objects.create(
            user = user,
            delivery_address = validated_data.get('delivery_address'),
        )
        
        order_item_objects = [
            OrderItem(
                order = order,
                product = item.product,
                qty = item.qty,
                price = item.product.price,                    
            )
            for item in items
        ]
        
        OrderItem.objects.bulk_create(
            order_item_objects,
        )
        
        return order


class CancelOrderSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)