from django.urls import path,re_path
from django.conf.urls import url
from training import views

urlpatterns = [

               url(r'^deploy_experiment/$', views.deploy_experiment),
               url(r'^set_threshold/$', views.set_threshold),
               url(r'^create_experiment/$', views.create_experiment_modified),
               url(r'^interrupt_training/$', views.interrupt_training),
               url(r'^create_retrain_experiment/$', views.create_retrain_experiment),
               url(r'^get_model_data/(?P<experiment_type>[A-Za-z0-9-_]+)$', views.get_model_data),
              # url(r'^get_deployment_list/$', views.get_deployment_list),
               # url(r'^get_deployment_list/$', views.get_deployment_list_updated),
               url(r'^get_deployment_list/$', views.deployment_list_filter),
            #    url(r'^get_all_running_experiments/$', views.get_all_running_experiments),
               url(r'^get_all_running_experiments/$', views.all_experiments_filter), 
               #url(r'^get_running_experiment/(?P<part_id>[A-Za-z0-9-_]+)$', views.get_running_experiment), 
               url(r'^experiment_status/(?P<part_id>[A-Za-z0-9-_]+)/(?P<experiment_id>[A-Za-z0-9-_]+)$', views.get_experiment_status),
               
               #url(r'^deploy_experiment/$', views.deploy_experiment)

               #static exp crud api
               url(r'^get_model_static/(?P<experiment_static_id>[A-Za-z0-9-_]+)$', views.get_model_static), #experiment_settings
               url(r'^create_model_static/$', views.create_model_static),
               #url(r'^delete_model_static/$', views.delete_model_static),

]
