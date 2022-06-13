from cgitb import lookup
from email.policy import HTTP
from django.shortcuts import render
from rest_framework import generics, status, views
import datetime
from blog.serializers import BlogListSerializer
from blog.models import Blog
from .serializers import (
                        ChangePasswordSerializer,
                        RegisterSerializer,  
                        EmailVerificationSerializer, 
                        LoginSerializer,
                        UserDetailSerializer,
                        UserDetailSerializer,
                        UserSerializer,
                        LogoutSerializer
                        )
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes





class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('authentication:email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Verify your email'
                }

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)
    
user_register_view = RegisterView.as_view()


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

email_verification_view = VerifyEmail.as_view()


class LoginAPIView(generics.GenericAPIView):
    # serializer_class = LoginSerializer

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)


    #     return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='access', value=token, httponly=True)
        response.data = {
            
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
        return response

login_view = LoginAPIView.as_view()




class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    

user_list_view = UserList.as_view()


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    


     
user_detail_view = UserDetail.as_view()


# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer
    
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# user_logout_view = LogoutAPIView.as_view()

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('access')
        response.data = {
            'message': 'success'
        }
        return response
    
user_logout_view = LogoutView.as_view()



class ChangePasswordView(generics.UpdateAPIView):
    
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

change_password_view = ChangePasswordView.as_view()