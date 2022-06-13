from django.urls import path
from . import views

urlpatterns = [
    path('google/', views.GoogleSocialAuthView.as_view())
]
