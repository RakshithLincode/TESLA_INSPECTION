import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.decorators import api_view
from common.utils import Encoder
from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from logs.utils import add_logs_util
from accounts.views import check_permission

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'start_time' : openapi.Schema(type=openapi.TYPE_STRING, example='11:16:45'),
        'end_time': openapi.Schema(type=openapi.TYPE_STRING, example='12:16:45'),
        'shift_name' : openapi.Schema(type=openapi.TYPE_STRING, example='Morning'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, example='Active')
    }
))

@api_view(['POST'])
@csrf_exempt
def add_shift(request):
    check_permission(request,"can_add_shift")
    # token_user_id = request.user.user_id
    operation_type = "shifts"
    notes = "add shift"
    
    # add_logs_util(token_user_id,operation_type,notes)
    
    data = json.loads(request.body)
    from shifts.utils import add_shift
    response = add_shift(data)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        '_id' : openapi.Schema(type=openapi.TYPE_STRING, example='5f3264a2abb1d860718dba01'),
        'shift_name': openapi.Schema(type=openapi.TYPE_STRING, example='Morning_shift1'),
        'start_time' : openapi.Schema(type=openapi.TYPE_STRING, example='10:16:45'),
        'end_time': openapi.Schema(type=openapi.TYPE_STRING, example='11:16:45'),
        'status': openapi.Schema(type=openapi.TYPE_STRING, example='Active')
    }
))


@api_view(['PATCH'])
@csrf_exempt
def update_shift(request):
    check_permission(request,"can_update_shift")
    # token_user_id = request.user.user_id
    operation_type = "shifts"
    notes = "update shift"
    
    # add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from shifts.utils import update_shift
    response = update_shift(data)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['DELETE'])
@csrf_exempt
def delete_shift(request, shift_id):
    check_permission(request,"can_delete_shift")
    # token_user_id = request.user.user_id
    operation_type = "shifts"
    notes = "delete shift"
    
    # add_logs_util(token_user_id,operation_type,notes)
    from shifts.utils import delete_shift
    response = delete_shift(shift_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
def shift_list(request):
    check_permission(request,"can_get_shift_list")
    # token_user_id = request.user.user_id
    operation_type = "shifts"
    notes = "get all shifts"
    
    # add_logs_util(token_user_id,operation_type,notes)
    skip = request.GET.get('skip', 0)
    limit = request.GET.get('limit', 100)
    from shifts.utils import shift_list
    response = shift_list(skip, limit)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@csrf_exempt
def shift_single(request,shift_id):
    check_permission(request,"can_get_shift_single")
    # token_user_id = request.user.user_id
    operation_type = "shifts"
    notes = "get single shift"
    # add_logs_util(token_user_id,operation_type,notes)
    from shifts.utils import shift_single
    response = shift_single(shift_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

    
