"""
URL configuration for REMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Real Estate Management System API",
      default_version='v1',
      description="API for Real Estate Management System",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="support@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('MBP.urls')),
    path('', include('Accounting.urls')),
    path('', include('booking.urls')),
    path('', include('crm_engagement.urls')),
    path('', include('investment_trends.urls')),
    path('', include('property.urls')),
    path('', include('Support_legal.urls')),
]

urlpatterns += [
     # Swagger & Redoc URLs
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns += [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += path('ckeditor/', include('ckeditor_uploader.urls')),
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api/auth/', include('dj_rest_auth.urls')),  # login/logout/token verify
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),  # signup
    path('api/auth/social/', include('allauth.socialaccount.urls')),  # social callback
]