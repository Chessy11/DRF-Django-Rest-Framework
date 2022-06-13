from django.urls import path
from .import views


urlpatterns = [
    path("<int:pk>/", views.blog_detail_view, name='detail'),
    path("create/", views.blog_create_view),
    path('<int:pk>/update/', views.blog_update_view),
    # path('<int:pk>/delete/', views.blog_delete_view),
    path("", views.blog_listing_view),

]


app_name = "blog"