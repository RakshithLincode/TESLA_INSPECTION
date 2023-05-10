from django.urls import path,re_path
from reports import views

urlpatterns = [
    re_path(r'^getMegaReport/$', views.get_mega_report),
    re_path(r'^edit_remark/$', views.edit_remark),
    re_path(r'^set_flag/$', views.set_flag),
    re_path(r'^exportCSV/$', views.export_report)
]
