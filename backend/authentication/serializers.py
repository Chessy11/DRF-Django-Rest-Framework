from requests import Response
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from blog.models import Blog

from blog.serializers import BlogDetailSerializer, BlogForUsersSerializer, BlogListSerializer
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username', 
            'password', 
            'password2', 
            'email', 
            'first_name', 
            'last_name'
            ]
        
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],

        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         max_length=60, 
#         min_length=6, 
#         write_only=True
#         )
#     confirm_password = serializers.CharField(max_length=60, min_length=6, write_only=True)

#     def validate(self, data):
#         if not data.get('first_name') or not data.get('last_name'):
#             raise serializers.ValidationError('Credentials missing')
#         if not data.get('password') or not data.get('confirm_password'):
#             raise serializers.ValidationError("Please enter a password and "
#             "confirm it.")
#         if data.get('password') != data.get('confirm_password'):
#             raise serializers.ValidationError("Those passwords don't match.")
#         return data



#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'email',
#             'password',
#             'confirm_password'
#             ]
        
#     def validate(self, attrs):
#         email=attrs.get('email', '')
#         username = attrs.get('username', '')
        
#         if not username.isalnum():
#             raise serializers.ValidationError('The username must contain alphanumeric characters')
#         return attrs
    
#     def get_confirm_password(self, obj):
#         return obj.confirm_password

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)
    
user_url = HyperlinkedIdentityField(
        view_name='authentication:user',
    )



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
        
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']


    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        
 

        # return super().validate(attrs)
    

        
class UserDetailSerializer(serializers.ModelSerializer):
    blogs = BlogForUsersSerializer(many=True)
      

    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'blogs', 
        ]
        
        
        



        
class UserSerializer(serializers.ModelSerializer):
    user_detail = user_url
    
    class Meta:
        model = User
        fields = [
            'user_detail',
            'id', 
            'username', 
        ]
        

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_messages = {
        'bad_token': {'Token is expired or invalid'}
    }
    
    def validate(self, attrs):
        self.token=attrs['refresh']
        return attrs
    
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
            
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'old_password', 
            'password', 
            'password2', 
         
            ]

    def validate_old_password(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return attrs

        

    def update(self, user, validated_data):
        
        user.set_password(validated_data['password'])
        user.save()

        return user

