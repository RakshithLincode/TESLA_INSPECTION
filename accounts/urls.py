from django.urls import path,re_path
from accounts import views

urlpatterns = [
    re_path(r'^add_user_account/$', views.add_user_account),
    re_path(r'^get_user_account/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_account),
    re_path(r'^update_user_account/$', views.update_user_account),
    re_path(r'^delete_user_account/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_account),
    re_path(r'^user_accounts/$', views.get_all_user_accounts),

    re_path(r'^add_user_master/$', views.add_user_master),
    re_path(r'^get_user_master/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_master),
    re_path(r'^update_user_master/$', views.update_user_master),
    re_path(r'^delete_user_master/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_master),
    re_path(r'^get_user_masters/$', views.get_user_masters),
    
    re_path(r'^add_user_admin/$', views.add_user_admin),
    re_path(r'^get_user_admin/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_admin),
    re_path(r'^update_user_admin/$', views.update_user_admin),
    re_path(r'^delete_user_admin/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_admin),
    re_path(r'^get_user_admins/$', views.get_user_admins),

    re_path(r'^add_user_business_manager/$', views.add_user_business_manager),
    re_path(r'^get_user_business_manager/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_business_manager),
    re_path(r'^update_user_business_manager/$', views.update_user_business_manager),
    re_path(r'^delete_user_business_manager/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_business_manager),
    re_path(r'^get_user_business_managers/$', views.get_user_business_managers),

    re_path(r'^add_user_sales_executive/$', views.add_user_sales_executive),
    re_path(r'^get_user_sales_executive/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_sales_executive),
    re_path(r'^update_user_sales_executive/$', views.update_user_sales_executive),
    re_path(r'^delete_user_sales_executive/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_sales_executive),
    re_path(r'^get_user_sales_executives/$', views.get_user_sales_executives),
    re_path(r'^get_user_sales_by_business_manager/(?P<business_manager_id>[A-Za-z0-9-_]+)$',
            views.get_user_sales_by_business_manager),
    
    re_path(r'^add_user_client/$', views.add_user_client),
    re_path(r'^get_user_client/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_client),
    re_path(r'^get_list_client/(?P<client_id>[A-Za-z0-9-_]+)', views.get_list_client),
    re_path(r'^update_user_client/$', views.update_user_client),
    re_path(r'^delete_user_client/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_client),
    re_path(r'^get_user_clients/$', views.get_user_clients),

    re_path(r'^add_user_si/$', views.add_user_si),
    re_path(r'^get_user_si/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_si),
    re_path(r'^update_user_si/$', views.update_user_si),
    re_path(r'^delete_user_si/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_si),
    re_path(r'^get_user_sis/$', views.get_user_sis),

    re_path(r'^add_client_account/$', views.add_client_account),
    re_path(r'^get_client_account/(?P<client_id>[A-Za-z0-9-_]+)', views.get_client_account),
    re_path(r'^update_client_account/$', views.update_client_account),
    re_path(r'^delete_client_account/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_client_account),
    re_path(r'^client_accounts/$', views.get_all_client_accounts),

    re_path(r'^add_si_account/$', views.add_si_account),
    re_path(r'^get_si_account/(?P<client_id>[A-Za-z0-9-_]+)', views.get_si_account),
    re_path(r'^update_si_account/$', views.update_si_account),
    re_path(r'^delete_si_account/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_si_account),
    re_path(r'^si_accounts/$', views.get_all_si_accounts),
    
    
    
    
    re_path(r'^add_user_supervisor/$', views.add_user_supervisor),
    re_path(r'^get_user_supervisor/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_supervisor),
    re_path(r'^update_user_supervisor/$', views.update_user_supervisor),
    re_path(r'^delete_user_supervisor/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_supervisor),
    re_path(r'^get_user_supervisors/$', views.get_user_supervisors),

    re_path(r'^add_user_line_manager/$', views.add_user_line_manager),
    re_path(r'^get_user_line_manager/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_line_manager),
    re_path(r'^update_user_line_manager/$', views.update_user_line_manager),
    re_path(r'^delete_user_line_manager/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_line_manager),
    re_path(r'^get_user_line_managers/$', views.get_user_line_managers),

    re_path(r'^add_user_operator/$', views.add_user_operator),
    re_path(r'^get_user_operator/(?P<client_id>[A-Za-z0-9-_]+)', views.get_user_operator),
    re_path(r'^update_user_operator/$', views.update_user_operator),
    re_path(r'^delete_user_operator/(?P<client_id>[A-Za-z0-9-_]+)$', views.delete_user_operator),
    re_path(r'^get_user_operators/$', views.get_user_operators),
    
    
    

    re_path(r'^login/$', views.login_user),
    re_path(r'^login_supervisor/$', views.login_supervisor),
    re_path(r'^logout/$', views.logout_user),
    re_path(r'^change_password/$', views.change_password),
    
    ]
