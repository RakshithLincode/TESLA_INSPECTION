from django.contrib import admin
from django.urls import path, re_path
from django.urls import path,re_path
from django.conf.urls import url
from inspection import views

urlpatterns = [
    re_path(r'^get_capture_feed_url/$', views.get_camera_urls),
    # re_path(r'^save_results/$', views.save_inspection_results),
    re_path(r'^save_results_per_view/$', views.save_inspection_per_view),
    re_path(r'^get_running_process/$', views.get_running_process_views),
    re_path(r'^start_process/$', views.start_process),
    re_path(r'^end_process/$', views.end_process),
    re_path(r'^getDefectList/(?P<inspectionid>[A-Za-z0-9-._]+)/$', views.getDefectList),
    re_path(r'^get_data_stream/(?P<cameraid>[A-Za-z0-9-._]+)/$', views.get_data_stream),
    re_path(r'^get_output_stream/(?P<cameraid>[A-Za-z0-9-._]+)/$', views.get_output_stream),
    re_path(r'^getRedZoneList/', views.getRedZoneList),
    re_path(r'^camera_health_check_view/', views.camera_health_check_view),
    re_path(r'^plc_health_check_view/', views.plc_health_check_view),
    re_path(r'^flag/$', views.flag),


    ###################
    re_path(r'^save_inspection_details/$', views.save_inspection_details_view),
    re_path(r'^get_metrics/(?P<inspection_id>[A-Za-z0-9-_]+)', views.get_metrics_view),
    # re_path(r'^start_inspection/$', views.start_inspection_view),
    re_path(r'^get_ui_trigger/$', views.start_inspection_view),
    re_path(r'^set_config/$', views.set_config),



]

