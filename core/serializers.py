from rest_framework import serializers
from django.contrib.auth import get_user_model
from store.models import *
from django.db import transaction
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
    confirm_password = serializers.CharField(max_length=255, write_only=True)
    first_name=models.CharField(max_length=30)
    middle_name=models.CharField(max_length=30,null=True,blank=True)
    last_name=models.CharField(max_length=30)
    shipping_address=models.TextField()
    
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'shipping_address',
            'email',
            'password',
            'confirm_password',   
        )
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match'
            })
        return super().validate(attrs)
        
        
       
    
    
    @transaction.atomic
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        # middle_name=validate_data.get('middle_name')
        
        customer={
            'first_name': validated_data.pop('first_name'),
            'middle_name': validated_data.pop('middle_name'),
            'last_name': validated_data.pop('last_name'),
            'shipping_address': validated_data.pop('shipping_address'),
        }
        
        user = User.objects.create_user(
            **validated_data
        )
        
        # yesle chai user lai active huna dina hunna. 
        # By default user chai 'is_active=True' hunxa
        user.is_active = False
        
        # OTP ta random integer hunxa ni tye vayera 'randint' use gareko. 
        # Hamle 'OTP=charfield' garaxam so 'str' use gareko
        user.otp = str(randint(0000,9999))
        user.save()            

        customer.update({
            'user_id':user.pk,
        })
            
        Customer.objects.create(
            **customer,
        )
            
        # mail send garda yo chai lekhnai parxa    
        send_mail(
            subject='User activation',
            message=f'Your otp is {user.otp} for {user.email}',
            from_email=settings.SENDER_EMAIL_USER,
            recipient_list=[
                user.email
            ]
        )
        
        for key,value in customer.items():
            setattr(user, key, value)
        
        return user
    
# This is for User Verification   
class UserVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    
    def update(self, user, validated_data):
        otp = validated_data.get('otp')
        email = validated_data.get('email')
        
        if otp == user.otp and email == user.email:
            user.is_active = True
            user.otp = None
            user.save()
        else:
            raise serializers.ValidationError({
                'otp': 'Invalid otp or email'
            })

        return user

# This is for Forgot Password
class UserForgotPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

# This is for Updating Forgot Password
class UpdateUserForgotPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=255)
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs.get('password')!= attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match'
            })
        return super().validate(attrs)
    
    def update(self, user, validated_data):
        otp = validated_data.get('otp')
        email = validated_data.get('email')
        
        if otp == user.otp and email == user.email:
            # make_password rakhena vani validation ma error aauxa ra hamle manager banauda password hash ma store hunxa so hash ma ja rakhna parxa otherwise error aauxa login garda
            user.password = make_password(validated_data.get('password'))
            
            # 'OTP=none' le chai ekchoti pathako OTP, ekchoti matra use garna milxa
            user.otp = None
            user.save()
        else:
            raise serializers.ValidationError({
                'otp': 'Invalid OTP.'
            })
            
        return user

# This is for User Login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)