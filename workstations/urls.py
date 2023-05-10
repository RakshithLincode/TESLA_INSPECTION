from django.urls import path,re_path
from workstations import views

urlpatterns = [
    re_path(r'^add_workstation/$', views.add_workstation),
    re_path(r'^delete_workstation/(?P<wid>[A-Za-z0-9-_]+)$', views.delete_workstation),
    re_path(r'^update_workstation/$', views.update_workstation),
    re_path(r'^get_workstations/$', views.get_workstations),
    re_path(r'^workstation/(?P<workstationid>[A-Za-z0-9-_]+)', views.get_workstation_config),
    re_path(r'^get_restart_alert/$', views.get_restart_alert)

]
