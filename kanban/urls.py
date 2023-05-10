from django.urls import path,re_path
from kanban import views


urlpatterns = [
	re_path(r'^update_kanban/$', views.update_kanban),
	re_path(r'^get_all_kanban/$', views.get_all_kanban),
	re_path(r'^get_single_kanban/(?P<id>[A-Za-z0-9-_]+)/$', views.get_single_kanban),
	re_path(r'^create_kanban/$', views.create_kanban),
	re_path(r'^delete_kanban/(?P<id>[A-Za-z0-9-_]+)/$', views.delete_kanban)
]
