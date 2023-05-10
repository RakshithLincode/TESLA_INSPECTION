from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
import json
from common.utils import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from logs.utils import add_logs_util
#from accounts.views import check_permission

from accounts.views import check_permission

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'id' : openapi.Schema(type=openapi.TYPE_STRING, example='5f080781e987304f98e77d38'),
        'workstation_name' : openapi.Schema(type=openapi.TYPE_STRING, example='XYZ'),
        'workstation_ip': openapi.Schema(type=openapi.TYPE_STRING, example='1.1.1.1'),
        'workstation_port' : openapi.Schema(type=openapi.TYPE_STRING, example='8888'),
        'workstation_status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example='true'),
        'cameras' : openapi.Schema(type=openapi.TYPE_OBJECT, example=[{'camera_id' : '0','camera_name' : 'hey'},\
                                                                      {'camera_id' : '1','camera_name' : 'hi'}]),
        'isdeleted' : openapi.Schema(type=openapi.TYPE_BOOLEAN, example='true')
    }
))


@api_view(['POST'])
@csrf_exempt
#@permission_classes((AllowAny,))
def add_workstation(request):
    check_permission(request,"can_add_workstation")
    token_user_id = request.user.user_id
    operation_type = "workstation"
    notes = "add workstation"
    
    add_logs_util(token_user_id,operation_type,notes)
    
    data = json.loads(request.body)
    from workstations.utils import add_workstation_task
    added_workstation_id = add_workstation_task(data)
    return HttpResponse(json.dumps({'message' : 'Workstation added Successfully!', 'added_workstation_id' : \
        added_workstation_id}, cls=Encoder), content_type="application/json")


@api_view(['DELETE'])
@csrf_exempt
#@permission_classes((AllowAny,))
def delete_workstation(request, wid):
    check_permission(request,"can_delete_workstation")

    token_user_id = request.user.user_id
    operation_type = "workstation"
    notes = "delete workstation"
    
    add_logs_util(token_user_id,operation_type,notes)
    from workstations.utils import delete_workstation_task
    deleted_workstation_id = delete_workstation_task(wid)
    return HttpResponse(json.dumps({'message' : 'Workstation deleted Successfully!', 'deleted_workstation_id' : \
        deleted_workstation_id}, cls=Encoder), content_type="application/json")


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'id' : openapi.Schema(type=openapi.TYPE_STRING, example='5f080781e987304f98e77d38'),
        'edit_workstation_name' : openapi.Schema(type=openapi.TYPE_STRING, example='XYZ'),
        'edit_workstation_ip': openapi.Schema(type=openapi.TYPE_STRING, example='1.1.1.1'),
        'edit_workstation_port' : openapi.Schema(type=openapi.TYPE_STRING, example='8888'),
        'edit_workstation_status': openapi.Schema(type=openapi.TYPE_BOOLEAN, example='true'),
        'camerasEdit' : openapi.Schema(type=openapi.TYPE_OBJECT, example=[{'edit_camera_id' : '0','edit_camera_name' : 'cam1'},{'edit_camera_id' : '1','edit_camera_name' : 'hi'}])
    }
))


@api_view(['PATCH'])
@csrf_exempt
#@permission_classes((AllowAny,))
def update_workstation(request):
    check_permission(request,"can_update_workstation")
    
    token_user_id = request.user.user_id
    operation_type = "workstation"
    notes = "update workstation"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from workstations.utils import update_workstation_task
    updated_workstation_id = update_workstation_task(data)
    return HttpResponse(json.dumps({'message' : 'Workstation updated Successfully!', 'updated_workstation_id' : updated_workstation_id}, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_workstation_config(request, workstationid):
    check_permission(request,"can_get_workstation_config")
    token_user_id = request.user.user_id
    operation_type = "workstation"
    notes = "get workstation config"
    
    add_logs_util(token_user_id,operation_type,notes)
    from workstations.utils import get_workstation_config_task
    response = get_workstation_config_task(workstationid)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_workstations(request):
    check_permission(request,"can_get_workstations")
    #token_user_id = request.user.user_id
    #operation_type = "workstation"
    #notes = "get all workstations"
    
    #add_logs_util(token_user_id,operation_type,notes)
    from workstations.utils import get_workstations_task 
    skip = request.GET.get('skip', 0)
    limit = request.GET.get('limit' , 100)
    response = get_workstations_task(skip, limit)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_restart_alert(request):
    from workstations.utils import get_restart_alert_util
    response = get_restart_alert_util()
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
    
