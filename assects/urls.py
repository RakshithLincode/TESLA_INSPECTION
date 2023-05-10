from django.urls import path,re_path
from assects import views


urlpatterns = [
    # re_path(r'^testLogs/$', views.test_logs),
    re_path(r'^add_assects/$', views.add_assects),
    re_path(r'^update_assect/$', views.update_assect),
    re_path(r'^get_assect/$', views.get_assect),
    re_path(r'^validate/$', views.validate),
]
