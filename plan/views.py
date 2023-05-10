import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from common.utils import Encoder

from logs.utils import add_logs_util

from accounts.views import check_permission

from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'start_time' : openapi.Schema(type=openapi.TYPE_STRING, example='2020-10-02'),
        'end_time' : openapi.Schema(type=openapi.TYPE_STRING, example='2020-10-05'),
        'part_number': openapi.Schema(type=openapi.TYPE_STRING, example='aaserer3423'),
        'planned_production_count': openapi.Schema(type=openapi.TYPE_INTEGER, example=100)
    }
))
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_plan(request):
    check_permission(request,"can_add_plan")
    token_user_id = request.user.user_id
    operation_type = "plan"
    notes = "add plan"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from plan.utils import add_plan
    response = add_plan(data)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@swagger_auto_schema(method='patch', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        '_id' : openapi.Schema(type=openapi.TYPE_STRING, example='5f2d3183bdcd9e81e1690f3f'),
        'planned_production_count': openapi.Schema(type=openapi.TYPE_INTEGER, example=100)
    }
))    
@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_plan(request):
    check_permission(request,"can_update_plan")
    token_user_id = request.user.user_id
    operation_type = "plan"
    notes = "update plan"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    from plan.utils import update_plan
    response = update_plan(data)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def delete_plan(request, plan_id):
    check_permission(request,"can_delete_plan")
    token_user_id = request.user.user_id
    operation_type = "plan"
    notes = "delete plan"
    
    add_logs_util(token_user_id,operation_type,notes)
    from plan.utils import delete_plan
    response = delete_plan(plan_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def plan_list(request):
    check_permission(request,"can_plan_list")
    token_user_id = request.user.user_id
    operation_type = "plan"
    notes = "plan list"
    
    add_logs_util(token_user_id,operation_type,notes)
    skip = request.GET.get('skip', 0)
    limit = request.GET.get('limit', 100)
    from plan.utils import plan_list
    response = plan_list(skip, limit)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def plan_single(request,plan_id):  
    check_permission(request,"can_plan_single")
    token_user_id = request.user.user_id
    operation_type = "plan"
    notes = "single plan"
    
    add_logs_util(token_user_id,operation_type,notes) 
    from plan.utils import plan_single
    response = plan_single(plan_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_todays_planned_production(request,part_id):
    check_permission(request,"can_get_todays_planned_production")
    token_user_id = request.user.user_id
    operation_type = "plan"
    notes = "todays plan production"
    
    add_logs_util(token_user_id,operation_type,notes)
    from plan.utils import get_todays_planned_production_util
    response = get_todays_planned_production_util(part_id)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

    
