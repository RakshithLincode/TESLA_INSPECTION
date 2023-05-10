from django.urls import path,re_path

from indo import views



urlpatterns = [
    # path('', views.index, name='index'),

    re_path(r'^start_process/$', views.start_process_indo),#To create the process collection
    re_path(r'^end_process/$', views.end_process_indo),# To end the process
    re_path(r'^get_running_process/$', views.get_indo_running_process),
    re_path(r'^get_camera_feed_urls/$', views.get_camera_feed_urls),
    re_path(r'^stream/(?P<key>[A-Za-z0-9-_.]+)/$', views.get_redis_stream), 
    # TO DO camera feed urls
]

