from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
from logs.utils import *
import json
from common.utils import *

from accounts.views import check_permission


from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'short_number' : openapi.Schema(type=openapi.TYPE_STRING, example='sht11'),
        'model_number' : openapi.Schema(type=openapi.TYPE_STRING, example='md11'),
        'part_number': openapi.Schema(type=openapi.TYPE_STRING, example='pt11'),
        'planned_production' : openapi.Schema(type=openapi.TYPE_STRING, example='100'),
        'part_description': openapi.Schema(type=openapi.TYPE_STRING, example='fjjff'),
        'edit_part_data' : openapi.Schema(type=openapi.TYPE_BOOLEAN, example='true')
    }
))

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_logs(request):
    check_permission(request,"can_add_logs")
    data = json.loads(request.body)
    add_logs_util(request.user.user_id,"test","this is test message")
    return HttpResponse(json.dumps({'data' : 'Logs added Successfully!'}, cls=Encoder), content_type="application/json")



@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def test_logs(request):
    check_permission(request,"can_test_logs")
    # from parts.utils import get_short_numbers_list_util 
    # skip = request.GET.get('skip', 0)
    # limit = request.GET.get('limit' , 10)
    # response = get_short_numbers_list_util(skip, limit)
    return HttpResponse(json.dumps(['test logs api'], cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_user_list(request,user_type):
    check_permission(request,"can_get_user_list")
    #data = json.loads(request.body)
    message,status_code=get_user_list_util(user_type)
    if status_code == 200:
        return HttpResponse(json.dumps({'message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)
    
    

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_access_log_report(request):
    check_permission(request,"can_get_access_log_report")
    # from reports.utils import get_defect_list_report_util
    data = json.loads(request.body)
    total,current,limit,message,status_code = get_access_log_report_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'message' : 'Success!', 'data' : message,'total' : total,'current' : current,'limit' : limit}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)
        
    #return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")4
    

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def export_logs(request):
    check_permission(request,"can_export_logs")
    data = json.loads(request.body)
    message,status_code=export_logs_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)
    
    
    
