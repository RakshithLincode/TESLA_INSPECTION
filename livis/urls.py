"""livis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,re_path,include

from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('livis/v1/admin', admin.site.urls),
    re_path(r'livis/v1/accounts/', include("accounts.urls")),
    re_path(r'livis/v1/parts/', include("parts.urls")),
    re_path(r'livis/v1/capture/', include("capture.urls")),
    re_path(r'livis/v1/shifts/', include("shifts.urls")),
    re_path(r'livis/v1/reports/', include("reports.urls")),
    re_path(r'livis/v1/report/', include("reports.urls")),
    re_path(r'livis/v1/workstations/', include("workstations.urls")),
    re_path(r'livis/v1/plan/', include("plan.urls")),
    re_path(r'livis/v1/logs/', include("logs.urls")),
    re_path(r'livis/v1/assects/', include("assects.urls")), 
    re_path(r'livis/v1/preprocess/', include("preprocess.urls")),
    re_path(r'livis/v1/kanban/', include("kanban.urls")),
    re_path(r'livis/v1/inspection/', include("inspection.urls")),
    re_path(r'livis/v1/dashboards/', include("dashboards.urls"))
]
