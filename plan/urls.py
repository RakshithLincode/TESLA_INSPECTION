from django.urls import path,re_path
from django.conf.urls import url
from plan import views

urlpatterns = [
               url(r'^add_plan/$', views.add_plan), 
               url(r'^update_plan/$', views.update_plan), 
               url(r'^delete_plan/(?P<plan_id>[A-Za-z0-9-_]+)$', views.delete_plan), 
               url(r'^get_plans/$', views.plan_list), 
               url(r'^get_plan/(?P<plan_id>[A-Za-z0-9-_]+)$', views.plan_single), 
               url(r'^get_todays_planned_production/(?P<part_id>[A-Za-z0-9-_]+)$', views.get_todays_planned_production), 
]
