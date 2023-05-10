from django.urls import path,re_path
from django.conf.urls import url
from shifts import views

urlpatterns = [
               url(r'^add_shift/$', views.add_shift), 
               url(r'^update_shift/$', views.update_shift), 
               url(r'^delete_shift/(?P<shift_id>[A-Za-z0-9-_]+)$', views.delete_shift), 
               url(r'^get_shifts/$', views.shift_list), 
               url(r'^get_shift/(?P<shift_id>[A-Za-z0-9-_]+)$', views.shift_single), 
]
