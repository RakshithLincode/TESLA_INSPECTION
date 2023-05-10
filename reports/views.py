from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse
import json
from common.utils import *
from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema
from accounts.views import check_permission
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def edit_remark(request):
    #check_permission(request,"can_edit_remark")
    from reports.utils import edit_remark_util
    data = json.loads(request.body)
    response = edit_remark_util(data)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def set_flag(request):
    #check_permission(request,"can_set_flag")
    from reports.utils import set_flag_util
    data = json.loads(request.body)
    response = set_flag_util(data)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))

# def get_mega_report(request):
#     # check_permission(request,"can_get_mega_report")
#     from reports.utils import get_megareport_util
#     data = json.loads(request.body)
#     response = get_megareport_util(data)
#     return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_mega_report(request):
    data = json.loads(request.body)
    from reports.utils import get_mega_report_util
    response,status_code = get_mega_report_util(data)
    if status_code != 200:
        return HttpResponse(response, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")    
         

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def export_report(request):
    check_permission(request,"can_get_mega_report")
    from reports.utils import export_csv_util
    data = json.loads(request.body)
    response = export_csv_util(data)
    return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")
    
