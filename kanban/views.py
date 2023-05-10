from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from django.http import HttpResponse
import json
from common.utils import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from kanban.utils import *
from bson.json_util import dumps
from bson.objectid import ObjectId

from accounts.views import check_permission


@api_view(['PATCH'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def update_kanban(request):
    check_permission(request,"can_update_kanban")
    data = json.loads(request.body)
    message, status_code = update_kanban_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")


@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
# def delete_kanban(request, id):
#     data = json.loads(request.body)
#     message, status_code = delete_kanban_util(id)
#     if status_code == 200:
#         return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
#     else:
#         return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")


def delete_kanban(request, id):
    check_permission(request,"can_delete_kanban")
    # data = json.loads(request.body)
    message, status_code = delete_kanban_util(id)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")        


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def create_kanban(request):
    check_permission(request,"can_create_kanban")
    data = json.loads(request.body)
    message, status_code = create_kanban_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message': 'Success!', 'data': message}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'Message': 'fail!', 'data': message}), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_all_kanban(request):
    check_permission(request,"can_get_all_kanban")
    kanban_list = get_all_kanban_util()
    print(kanban_list)
    # val = json.loads(kanban_list)
    return HttpResponse(json.dumps( kanban_list , cls=Encoder), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_single_kanban(request, id):
    check_permission(request,"can_get_single_kanban")
    kanban_list = get_single_kanban_util(id)
    return HttpResponse(json.dumps( kanban_list , cls=Encoder), content_type="application/json")
