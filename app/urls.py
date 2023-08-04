from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import permissions
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Marriage Photo Gallery",
        default_version='v1',
        description="This is an application to upload photos for a Marriage Album",
        contact=openapi.Contact(email="yghorcastello.backend@gmail.com"),
        license=openapi.License(name="Yghor Castello - Dev Backend"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('casamento.urls')),

    path('api/v1/auth/', include('users.urls')), 

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
