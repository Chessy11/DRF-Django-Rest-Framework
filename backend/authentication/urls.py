from django.urls import path 
from . import views
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', views.user_register_view, name='register'),
    path('login/', views.login_view, name='login'),

    path('email-verify/', views.email_verification_view, name='email-verify'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.user_list_view, name='users'),
    # path('users/<int:pk>/', views.user_detail_view, name='user'),
    path('logout/', views.user_logout_view, name='logout'),
    path('change_password/<int:pk>/', views.change_password_view, name='change_password')

]


app_name = 'authentication'
