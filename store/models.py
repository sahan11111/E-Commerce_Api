from decimal import Decimal
from django.db import models
from  django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
        ordering=("-id",)


class Category(BaseModel):
    name=models.CharField(max_length=40)
    
    def  __str__(self):
        return self.name
    
class Product(BaseModel):
    name=models.CharField(max_length=20)
    qty=models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    @property
    def price_with_tax(self):
        # django ma add subtract garna same data type huna parxa so decimal ma convert gareko
        tax_price = self.price*(Decimal(0.13))
        return self.price + tax_price    
    
    def  __str__(self):
        return f"{self.name} ({self.category})"
    
    
class Customer(BaseModel):
    first_name=models.CharField(max_length=30)
    middle_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=30)
    shipping_address=models.TextField()
    user=models.OneToOneField(User, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f'{self.firstName} {self.middleName}{self.lastName}'
    


class Cart(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.id)
    @property
    # cart ma vako items ko sum nikalni
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    # cart ma vako items ko tax_price ko sum nikalni
    def total_price_with_tax(self):
        return sum(item.total_price_with_tax for item in self.items.all())

class CartItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    
    @property
    def total_price(self):
        return self.quantity * self.product.price
    
    @property
    def total_price_with_tax(self):
        return self.quantity * self.product.price_with_tax
    
    def __str__(self):
        return f"{self.pk} ({self.product})"   

    def __str__(self):
        return str(self.product)

class Order(BaseModel):
    CASH_CHOICE = 'C'
    KHALTI_CHOICE = 'K'
    PENDING_PAYMENT_CHOICE = 'P'
    
    PAYMENT_MODE_CHOICES = [
        (PENDING_PAYMENT_CHOICE, 'PENDING'),
        (CASH_CHOICE, 'CASH'),
        (KHALTI_CHOICE, 'KHALTI'),
    ]
    
    PENDING_CHOICE = 'P'
    CONFIRM_CHOICE = 'CF'
    REJECTED_CHOICE = 'R'
    CANCELLED_CHOICE = 'C'
    
    STATUS_CHOICES = [
        (PENDING_CHOICE, 'PENDING'),
        (CONFIRM_CHOICE, 'CONFIRM'),
        (REJECTED_CHOICE, 'REJECTED'),
        (CANCELLED_CHOICE, 'CANCELLED'),        
    ]
    status=models.BooleanField(max_length=2,choices=STATUS_CHOICES,default=PENDING_CHOICE) 
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    delivery_address = models.CharField(max_length=255, null=True)
    place = models.DateTimeField(auto_now_add=True)
    payment_mode = models.CharField(max_length=1, choices=PAYMENT_MODE_CHOICES, default=PENDING_PAYMENT_CHOICE)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order No{self.pk} ({self.customer})"

class OrderItem(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=1000, decimal_places=2)

    def __str__(self):
        return f"Order No{self.pk} ({self.order.customer})"

class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    comment = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.product.name}-{self.customer}({self.rating}/5)"
