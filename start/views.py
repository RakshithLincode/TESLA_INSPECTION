from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from django.http import HttpResponse,StreamingHttpResponse
import json
from common.utils import *

from drf_yasg import openapi
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY
from drf_yasg.utils import swagger_auto_schema


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def start_process_indo(request):
    data = json.loads(request.body)
    from indo.utils import start_indo_process
    print("Inside VIew start_process_indo ")
    resp = start_indo_process(data)
    print(resp)
    return HttpResponse(json.dumps(resp, cls=Encoder), content_type="application/json") 


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def end_process_indo(request):
    data = json.loads(request.body)
    from indo.utils import end_indo_process
    response = end_indo_process(data)
    return HttpResponse(json.dumps(response,cls=Encoder), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_indo_running_process(request):
    from indo.utils import get_indo_running_process
    response = get_indo_running_process()
    return HttpResponse(json.dumps(response,cls=Encoder), content_type="application/json") 


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
def get_camera_feed_urls(request):
    from indo.utils import get_camera_feed_urls_util
    response = get_camera_feed_urls_util()
    return HttpResponse(json.dumps(response,cls=Encoder), content_type="application/json") 


@api_view(['GET'])
@csrf_exempt
def get_redis_stream(request, key):
    from indo.utils import redis_camera
    # key = RedisKeyBuilderServer(wid).get_key(cameraid, 'predicted-frame')
    # print("key:::::::::::::::::::::::::::::",key)
    return StreamingHttpResponse(redis_camera(key), content_type='multipart/x-mixed-replace; boundary=frame')