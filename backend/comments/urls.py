from django.urls import path
from . import views

urlpatterns = [
    path('comments/<int:pk>/', views.comment_detail_view, name='comments-detail'),
    path('create/', views.comment_create_view, name='create')
]


app_name = 'comments'