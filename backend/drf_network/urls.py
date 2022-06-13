from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="DRF-NETWORK API",
      default_version='v1',
      description="DRF description",
      terms_of_service="https://www.drfapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@drf.local"),
      license=openapi.License(name="DRF License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include('api.urls')),
    path("api/blog/", include('blog.urls')),
    path("api/comments/", include('comments.urls')),
    path('api/authentication/', include('authentication.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('social_auth/', include('social_auth.urls'), name='social_auth')
]
