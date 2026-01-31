"""
URL configuration for soc_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from alerts.views import AlertViewSet, AlertCommentViewSet
from playbooks.views import PlaybookViewSet, PlaybookExecutionViewSet
from incidents.views import IncidentViewSet
from analytics.views import DailyMetricsViewSet, DashboardStatsView

# API Router
router = DefaultRouter()
router.register(r'alerts', AlertViewSet)
router.register(r'alert-comments', AlertCommentViewSet)
router.register(r'playbooks', PlaybookViewSet)
router.register(r'playbook-executions', PlaybookExecutionViewSet)
router.register(r'incidents', IncidentViewSet)
router.register(r'metrics', DailyMetricsViewSet)

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="SOC Automation Platform API",
        default_version='v1',
        description="Multi-Framework SOC Automation Platform API",
        contact=openapi.Contact(email="admin@socplatform.local"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include(router.urls)),
    path('api/dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    
    # Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]