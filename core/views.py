from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,DestroyModelMixin
from django.contrib.auth import get_user_model,authenticate
from .serializers import *
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
User = get_user_model()

# Create your views here.
class UserView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    
    # This view is for user verification
    @swagger_auto_schema(
        methods=['put'],
        request_body=UserVerificationSerializer
    )
    
    @action(methods=['put'],detail=False)
    def verification(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        serializer = UserVerificationSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'details':'User has been successfully verified.'
        })
    
    # This view is for Forgot Password
    @swagger_auto_schema(
        methods=['post'],
        request_body=UserForgotPasswordEmailSerializer
    )
    @action(methods=['post'],detail=False)
    def send_otp_forgot_password(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        serializer = UserForgotPasswordEmailSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user.otp = str(randint(0000,9999))
        user.save()
        
        send_mail(
            subject='Forgot Password OTP',
            message=f'Your otp is {user.otp} for {user.email}',
            from_email=settings.SENDER_EMAIL_USER,
            recipient_list=[
                user.email
            ]
        )
        return Response({
            'details':f'OTP has been successfully sent to {user.email}.'
        })
        
    # This view is for Update Forgot Password 
    @swagger_auto_schema(
        methods=['put'],
        request_body=UpdateUserForgotPasswordEmailSerializer
    )
    @action(methods=['put'],detail=False)
    def update_forgot_password(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        serializer = UpdateUserForgotPasswordEmailSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'details':f'Password has been successfully updated for {user.email}'
        })
        
    # This is for Login User
    @swagger_auto_schema(
        methods=['post'],
        request_body=UserLoginSerializer
    )
    @action(methods=['post'],detail=False)
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(username=email,password=password)
        
        if user:
            # get_or_create le k garxa vanda: if token pailai xa vani get garxa ra yedi xaina vani create garxa. 'create' matra garyo vani tesle harek time create garxa so we use get_or_create
            token,_ = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.pk,
                'token': token.key,
                'user': user.email,
            })
        
        return Response({
            'details':'Invalid email or password.'
        })
        
    