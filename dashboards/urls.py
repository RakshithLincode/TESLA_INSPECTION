from django.urls import path, re_path
from dashboards import views

urlpatterns = [
    re_path(r'^total_production/$', views.total_production),
    re_path(r'^production_yield/$', views.production_yield),
    re_path(r'^production_rate/$', views.production_rate),
    re_path(r'^defect_count/$', views.defect_count),
    re_path(r'^production_weekly/$', views.production_weekly),
    re_path(r'^production_hourly/$', views.production_hourly),
    re_path(r'^production_monthly/$', views.production_monthly)
]
