from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from apps.user.api.views.views_login import Login, Logout

schema_view = get_schema_view(
    openapi.Info(
        title="Documentacion de API",
        default_version='v1',
        description="Documentacion de las rutas del proyecto de grado",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Login
    path('login/', Login.as_view(), name='login'),
    # Logout
    path('logout/', Logout.as_view(), name='logout'),
    # Admin
    path('admin/', admin.site.urls),
    # Swagger
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    # Users
    path('user/', include('apps.user.api.routers.routers')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
