from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
from assects.utils import *
import json
from common.utils import *

from logs.utils import add_logs_util

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from accounts.views import check_permission


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def add_assects(request):
    check_permission(request,"can_add_asset")
    token_user_id = request.user.user_id
    operation_type = "asset"
    notes = "add assets"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    response,status_code = add_assects_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

        

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def update_assect(request):
    check_permission(request,"can_update_asset")
    token_user_id = request.user.user_id
    operation_type = "asset"
    notes = "update asset"
    
    add_logs_util(token_user_id,operation_type,notes)
    data = json.loads(request.body)
    response,status_code = update_assect_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_assect(request):
    #check_permission(request,"can_get_asset")
    #token_user_id = request.user.user_id
    #operation_type = "asset"
    #notes = "get asset"
    
    #add_logs_util(token_user_id,operation_type,notes)
    #data = json.loads(request.body)
    
    
    response,status_code = get_assect_util()
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def validate(request):
    #check_permission(request,"can_validate")
    response,status_code = get_validation()
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
