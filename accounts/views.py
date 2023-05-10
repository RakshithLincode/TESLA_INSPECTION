from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
import json
from django.contrib.auth.models import Group, Permission
from common.utils import Encoder
from rest_framework import status
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_object_or_404
import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from common.utils import MongoHelper

from rest_framework.permissions import AllowAny

from logs.utils import add_logs_util
import tldextract


#############################################################USER CRUDS################################################################


def check_permission(request,perm_name):
    is_perm = False
    role = request.user.role_name
    #print("user issssssssssssssssssssss")
    #print(role)
    mp = MongoHelper().getCollection("permissions")
    p = [i for i in mp.find()]
    try:
        o = p[0][role]
    except:
        #entity name not in db
        raise PermissionDenied
    for key,val in o.items():
        if perm_name in val:
            is_perm = True
            break
  
    if is_perm:
        pass
    else:
        raise PermissionDenied

def throw_permission(role):

    #role = request.user.role_name
    mp = MongoHelper().getCollection("permissions")
    p = [i for i in mp.find()]
    try:
        o = p[0][role]
        return o
    except:
        #entity name not in db
        return []

def group_required(group, login_url=None, raise_exception=True):
    """
    Decorator for views that checks whether a user has a group permission,
    redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group
        # First check if the user has the permission (even anon users)

        if user.groups.filter(name__in=groups).exists():
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)
   
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={

        'username' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz'),
        'first_name' : openapi.Schema(type=openapi.TYPE_STRING, example='x'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='yz'),
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz@xyz.com'),
        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'user_address' : openapi.Schema(type=openapi.TYPE_STRING, example='abc'),
        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'role_name' : openapi.Schema(type=openapi.TYPE_STRING, example='supervisor'),
        'phone_number' : openapi.Schema(type=openapi.TYPE_STRING, example='43283743113'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password')

    }
))
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def add_user_account(request):

    # token_user_id = request.user.user_id
    # operation_type = "accounts"
    # notes = "add user"
    
    # add_logs_util(token_user_id,operation_type,notes)
    
    
    data = json.loads(request.body)
    from accounts.utils import add_user_account_util
    message,status_code = add_user_account_util(data)
    print(message,'sssssssssssssssssssssssssssssssss')
    if status_code == 400:
        return HttpResponse( {message}, status=status_code)
    else:    
        return HttpResponse(json.dumps({'message' : message,'status':status_code}), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_account(request,client_id):

    from accounts.utils import get_user_account_util
    response = get_user_account_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={

        'user_id' : openapi.Schema(type=openapi.TYPE_STRING, example='d92719dd-cd03-4857-bf7f-7b78a68ba888'),
        'first_name' : openapi.Schema(type=openapi.TYPE_STRING, example='x'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='yz'),
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz@xyz.com'),
        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'user_address' : openapi.Schema(type=openapi.TYPE_STRING, example='abc'),
        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'role_name' : openapi.Schema(type=openapi.TYPE_STRING, example='operator'),
        'phone_number' : openapi.Schema(type=openapi.TYPE_STRING, example='43283743113'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password')

    }
))
@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_account(request):

    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update user"
    
    add_logs_util(token_user_id,operation_type,notes)
    
    data = json.loads(request.body)
    from accounts.utils import update_user_account_util
    message,message1 = update_user_account_util(data,request)
    if message1 == "fail":
        return HttpResponse({message}, status=500)
    else:
        return  HttpResponse(json.dumps(message,cls=Encoder), content_type="application/json")
    #return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_account(request, client_id):
    token_user_id = request.user.username
    operation_type = "accounts"
    notes = "delete user"
    print(client_id,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')

    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_account_util
    message = delete_user_account_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_all_user_accounts(request):

    # token_user_id = request.user.user_id
    # token_user_email = request.user.email
    #print("user email:::",token_user_email)
    from accounts.utils import get_all_user_accounts_util
    response = get_all_user_accounts_util()
    return  HttpResponse(json.dumps(response), content_type="application/json")

#########################################################Master CRUDS ############################################################


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_master(request):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add master user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_master_util
    message = add_user_master_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 



@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_master(request):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update master user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_master_util
    message = update_user_master_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_master(request, client_id):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete master user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_master_util
    message = delete_user_master_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_master(request,client_id):

    from accounts.utils import get_user_master_util
    response = get_user_master_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_masters(request):

    from accounts.utils import get_user_masters_util
    response = get_user_masters_util()
    return  HttpResponse(json.dumps(response), content_type="application/json") 
    
    
#########################################################ADMIN CRUDS ############################################################


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_admin(request):
    check_permission(request,"can_add_user_admin")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add admin user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_admin_util
    message = add_user_admin_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 



@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_admin(request):
    check_permission(request,"can_update_user_admin")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update admin user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_admin_util
    message = update_user_admin_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_admin(request, client_id):
    check_permission(request,"can_delete_user_admin")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete admin user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_admin_util
    message = delete_user_admin_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_admin(request,client_id):
    check_permission(request,"can_get_user_admin")
    from accounts.utils import get_user_admin_util
    response = get_user_admin_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_admins(request):
    check_permission(request,"can_get_user_admins")
    from accounts.utils import get_user_admins_util
    response = get_user_admins_util()
    return  HttpResponse(json.dumps(response), content_type="application/json") 
    

#########################################################Business_manager CRUDS ############################################################



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_business_manager(request):
    check_permission(request,"can_add_business_manager")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add business_manager user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_business_manager_util
    message = add_user_business_manager_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 



@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_business_manager(request):
    check_permission(request,"can_update_business_manager")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update business_manager user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_business_manager_util
    message = update_user_business_manager_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_business_manager(request, client_id):
    check_permission(request,"can_delete_business_manager")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete business_manager user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_business_manager_util
    message = delete_user_business_manager_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_business_manager(request,client_id):
    check_permission(request,"can_get_business_manager")
    from accounts.utils import get_user_business_manager_util
    response = get_user_business_manager_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_business_managers(request):
    check_permission(request,"can_get_business_managers")
    from accounts.utils import get_user_business_managers_util
    response = get_user_business_managers_util()
    return  HttpResponse(json.dumps(response), content_type="application/json") 



#########################################################sales_executive CRUDS ############################################################


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_sales_executive(request):

    check_permission(request,"can_add_sales_executive")
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add sales_executive user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_sales_executive_util
    message = add_user_sales_executive_util(data,request)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 



@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_sales_executive(request):
    check_permission(request,"can_update_sales_executive")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update sales_executive user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_sales_executive_util
    message = update_user_sales_executive_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_sales_executive(request, client_id):
    check_permission(request,"can_delete_sales_executive")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete sales_executive user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_sales_executive_util
    message = delete_user_sales_executive_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_sales_executive(request,client_id):
    check_permission(request,"can_get_sales_executive")
    from accounts.utils import get_user_sales_executive_util
    response = get_user_sales_executive_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_sales_executives(request):
    check_permission(request,"can_get_sales_executives")
    from accounts.utils import get_user_sales_executives_util
    response = get_user_sales_executives_util()
    return  HttpResponse(json.dumps(response), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_sales_by_business_manager(request, business_manager_id):
    check_permission(request,"can_get_sales_executives")
    from accounts.utils import get_user_sales_by_business_manager_util
    response = get_user_sales_by_business_manager_util(business_manager_id)
    return  HttpResponse(json.dumps(response), content_type="application/json")


#########################################################USER_SI CRUDS############################################################


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'si_id' : openapi.Schema(type=openapi.TYPE_STRING, example='e396a732-c187-477a-8d94-7a4def2f1678'),
        'username' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz'),
        'first_name' : openapi.Schema(type=openapi.TYPE_STRING, example='x'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='yz'),
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz@xyz.com'),
        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'user_address' : openapi.Schema(type=openapi.TYPE_STRING, example='abc'),
        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'role_name' : openapi.Schema(type=openapi.TYPE_STRING, example='34734'),
        'phone_number' : openapi.Schema(type=openapi.TYPE_STRING, example='43283743113'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password')

    }
))
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def add_user_si(request):
    #print("im hereeeeeeee")

    check_permission(request,"can_add_user_si")
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add si user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_si_util
    message = add_user_si_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'si_id' : openapi.Schema(type=openapi.TYPE_STRING, example='e396a732-c187-477a-8d94-7a4def2f1678'),
        'username' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz'),
        'first_name' : openapi.Schema(type=openapi.TYPE_STRING, example='x'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='yz'),
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz@xyz.com'),
        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'user_address' : openapi.Schema(type=openapi.TYPE_STRING, example='abc'),
        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'role_name' : openapi.Schema(type=openapi.TYPE_STRING, example='34734'),
        'phone_number' : openapi.Schema(type=openapi.TYPE_STRING, example='43283743113'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password')

    }
))
@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_si(request):

    check_permission(request,"can_update_user_si")
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update si user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_si_util
    message = update_user_si_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_si(request, client_id):

    check_permission(request,"can_delete_user_si")
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete si user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_si_util
    message = delete_user_si_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_si(request,client_id):

    check_permission(request,"can_get_user_si")
    
    from accounts.utils import get_user_si_util
    response = get_user_si_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_sis(request):

    check_permission(request,"can_get_user_sis")
    from accounts.utils import get_user_sis_util
    response = get_user_sis_util()
    return  HttpResponse(json.dumps(response), content_type="application/json") 


################################################################USER_CLIENT CRUDS#############################################################

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'client_id' : openapi.Schema(type=openapi.TYPE_STRING, example='e396a732-c187-477a-8d94-7a4def2f1678'),
        'username' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz'),
        'first_name' : openapi.Schema(type=openapi.TYPE_STRING, example='x'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='yz'),
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz@xyz.com'),
        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'user_address' : openapi.Schema(type=openapi.TYPE_STRING, example='abc'),
        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'role_name' : openapi.Schema(type=openapi.TYPE_STRING, example='34734'),
        'phone_number' : openapi.Schema(type=openapi.TYPE_STRING, example='43283743113'),
        'client_user_manager' : openapi.Schema(type=openapi.TYPE_STRING, example='None'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password'),
        'is_client_admin' : openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)

    }
))
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_client(request):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add user client"
    
    add_logs_util(token_user_id,operation_type,notes)
    # data = json.loads(request.body)
    data = json.loads(request.body)
    from accounts.utils import add_user_client_util
    message = add_user_client_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'user_id' : openapi.Schema(type=openapi.TYPE_STRING, example='be5f1c5d-b5aa-457a-8cf9-9112307e9c38'),
        'first_name' : openapi.Schema(type=openapi.TYPE_STRING, example='x'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='yz'),
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='xyz@xyz.com'),
        'is_staff': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'user_address' : openapi.Schema(type=openapi.TYPE_STRING, example='abc'),
        'is_superuser': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
        'role_name' : openapi.Schema(type=openapi.TYPE_STRING, example='supervisor'),
        'phone_number' : openapi.Schema(type=openapi.TYPE_STRING, example='43283743113'),
        'client_user_manager' : openapi.Schema(type=openapi.TYPE_STRING, example='None'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password'),
        'is_client_admin' : openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)

    }
))
@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_client(request):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update user client"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_client_util
    message = update_user_client_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_client(request, client_id):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete user client"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_client_util
    message = delete_user_client_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_client(request,client_id):

    from accounts.utils import get_user_client_util
    response = get_user_client_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 



@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_list_client(request,client_id):

    from accounts.utils import get_list_client_util
    response = get_list_client_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 
    
    
    
    

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_clients(request):

    from accounts.utils import get_user_clients_util
    response = get_user_clients_util()
    return  HttpResponse(json.dumps(response), content_type="application/json") 


################################################################CLIENT CRUDS################################################################


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'client_name' : openapi.Schema(type=openapi.TYPE_STRING, example='Toyoda'),
        'client_license_key' : openapi.Schema(type=openapi.TYPE_STRING, example='dfhiweuf8w'),
        'client_role' : openapi.Schema(type=openapi.TYPE_STRING, example='Role2'),
        'assigned_to': openapi.Schema(type=openapi.TYPE_STRING, example='Client_User3'),
        'client_address' : openapi.Schema(type=openapi.TYPE_STRING, example='Bangalore')
    }
))
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_client_account(request):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add client account"
    
    add_logs_util(token_user_id,operation_type,notes)
    #print(request)
    data = json.loads(request.body)
    from accounts.utils import add_client_account_util
    message = add_client_account_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_client_account(request,client_id):

    from accounts.utils import get_client_account_util
    response = get_client_account_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'client_id' : openapi.Schema(type=openapi.TYPE_STRING, example='96e993fc-3f24-4e06-b2d1-e8736882c27f'),
        'client_name' : openapi.Schema(type=openapi.TYPE_STRING, example='Toyoda'),
        'client_license_key' : openapi.Schema(type=openapi.TYPE_STRING, example='dfhiweuf8w'),
        'client_role' : openapi.Schema(type=openapi.TYPE_STRING, example='Role2'),
        'assigned_to': openapi.Schema(type=openapi.TYPE_STRING, example='Client_User3'),
        'client_address' : openapi.Schema(type=openapi.TYPE_STRING, example='Bangalore')
    }
))
@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_client_account(request):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update client account"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_client_account_util
    message = update_client_account_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_client_account(request, client_id):
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete client account"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_client_account_util
    message = delete_client_account_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_all_client_accounts(request):

    from accounts.utils import get_all_client_accounts_util
    response = get_all_client_accounts_util()
    return  HttpResponse(json.dumps(response), content_type="application/json") 


################################################################SI CRUDS################################################################



#@permission_required('accounts.can_add_si',raise_exception=True)
#@group_required('level0')

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_si_account(request):

    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add si account"
    
    add_logs_util(token_user_id,operation_type,notes)

    data = json.loads(request.body)
    from accounts.utils import add_si_account_util
    message = add_si_account_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 

#@permission_required('accounts.can_get_si',raise_exception=True)
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_si_account(request,client_id):

    
    
    from accounts.utils import get_si_account_util
    response = get_si_account_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


#@permission_required('accounts.can_update_si',raise_exception=True)
@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_si_account(request):

    
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update si account"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_si_account_util
    message = update_si_account_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

#@permission_required('accounts.can_delete_si',raise_exception=True)
@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_si_account(request, client_id):

    

    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete si account"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_si_account_util
    message = delete_si_account_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

#@permission_required('accounts.can_get_sis',raise_exception=True)
#@group_required('dummy1')
@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_all_si_accounts(request):
    

    from accounts.utils import get_all_si_accounts_util
    response = get_all_si_accounts_util()
    return  HttpResponse(json.dumps(response), content_type="application/json") 


##############################################User Authentication APIS##########################################

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='sysadmin_xyz@xyz.com'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password'),
        'workstation_name' : openapi.Schema(type=openapi.TYPE_STRING, example='W_01')
    }
))
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def login_user(request):
    
    data = json.loads(request.body)
    from accounts.utils import login_user_util
    message = login_user_util(data,request)
    if message == "MissingField":
        return HttpResponse( {'Missing fields'}, status=status.HTTP_401_UNAUTHORIZED)
    elif message == "AuthError":
        return HttpResponse({'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
    return  HttpResponse(json.dumps(message,cls=Encoder), content_type="application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def logout_user(request):
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "log out"
    
    add_logs_util(token_user_id,operation_type,notes)
    
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    message = "logout success!"
    return  HttpResponse(json.dumps(message,cls=Encoder), content_type="application/json")
    
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def change_password(request):

    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "change password"
    
    add_logs_util(token_user_id,operation_type,notes)
    
    data = json.loads(request.body)
    from accounts.utils import change_password_util
    message,message1 = change_password_util(data,request)
    if message1 == "fail":
        return HttpResponse({message}, status=500)
    else:
        return  HttpResponse(json.dumps(message,cls=Encoder), content_type="application/json")





@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'email' : openapi.Schema(type=openapi.TYPE_STRING, example='sysadmin_xyz@xyz.com'),
        'password' : openapi.Schema(type=openapi.TYPE_STRING, example='password'),
        'workstation_name' : openapi.Schema(type=openapi.TYPE_STRING, example='W_01')
    }
))
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def login_supervisor(request):
    data = json.loads(request.body)
    from accounts.utils import login_supervisor_util
    message = login_supervisor_util(data)
    if message == "MissingField":
        return HttpResponse( {'Missing fields'}, status=status.HTTP_401_UNAUTHORIZED)
    elif message == "AuthError":
        return HttpResponse({'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
    return  HttpResponse(json.dumps({'message' : message}), content_type="application/json") 






#########################################################user_supervisor CRUDS ############################################################


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_supervisor(request):

    check_permission(request,"can_add_supervisor")
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add supervisor user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_supervisor_util
    message = add_user_supervisor_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 



@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_supervisor(request):
    check_permission(request,"can_update_supervisor")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update supervisor user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_supervisor_util
    message = update_user_supervisor_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_supervisor(request, client_id):
    check_permission(request,"can_delete_supervisor")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete supervisor user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_supervisor_util
    message = delete_user_supervisor_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_supervisor(request,client_id):
    check_permission(request,"can_get_supervisor")
    from accounts.utils import get_user_supervisor_util
    response = get_user_supervisor_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_supervisors(request):
    check_permission(request,"can_get_supervisors")
    from accounts.utils import get_user_supervisors_util
    response = get_user_supervisors_util()
    return  HttpResponse(json.dumps(response), content_type="application/json")
    
    
#########################################################line_manager CRUDS ############################################################


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_line_manager(request):

    check_permission(request,"can_add_line_manager")
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add line_manager user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_line_manager_util
    message = add_user_line_manager_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 



@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_line_manager(request):
    check_permission(request,"can_update_line_manager")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update line_manager user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_line_manager_util
    message = update_user_line_manager_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_line_manager(request, client_id):
    check_permission(request,"can_delete_line_manager")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete line_manager user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_line_manager_util
    message = delete_user_line_manager_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_line_manager(request,client_id):
    check_permission(request,"can_get_line_manager")
    from accounts.utils import get_user_line_manager_util
    response = get_user_line_manager_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_line_managers(request):
    check_permission(request,"can_get_line_managers")
    from accounts.utils import get_user_line_managers_util
    response = get_user_line_managers_util()
    return  HttpResponse(json.dumps(response), content_type="application/json")



    
    
#########################################################operator CRUDS ############################################################


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_user_operator(request):

    check_permission(request,"can_add_operator")
    
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "add operator user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import add_user_operator_util
    message = add_user_operator_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json") 



@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_user_operator(request):
    check_permission(request,"can_update_operator")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "update operator user"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from accounts.utils import update_user_operator_util
    message = update_user_operator_util(data)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_user_operator(request, client_id):
    check_permission(request,"can_delete_operator")
    token_user_id = request.user.user_id
    operation_type = "accounts"
    notes = "delete operator user"
    
    add_logs_util(token_user_id,operation_type,notes)
    from accounts.utils import delete_user_operator_util
    message = delete_user_operator_util(client_id)
    return HttpResponse(json.dumps({'message' : message}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_operator(request,client_id):
    check_permission(request,"can_get_operator")
    from accounts.utils import get_user_operator_util
    response = get_user_operator_util(client_id)
    return HttpResponse(json.dumps(response), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_operators(request):
    check_permission(request,"can_get_operators")
    from accounts.utils import get_user_operators_util
    response = get_user_operators_util()
    return  HttpResponse(json.dumps(response), content_type="application/json")


