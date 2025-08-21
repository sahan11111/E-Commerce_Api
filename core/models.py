from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.

# Create custome user
class User(AbstractUser):
    email=models.EmailField(unique=True)
    otp = models.CharField(max_length=255, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    
    objects=UserManager()

    

