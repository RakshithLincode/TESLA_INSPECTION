from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from common.utils import Encoder,RedisKeyBuilderServer,CacheHelper
import json
from django.http import HttpResponse,StreamingHttpResponse


from accounts.views import check_permission



@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@check_group(['admin'])
def set_policy(data):
    check_permission(data,"can_set_policy")
    data = json.loads(data.body)
    from preprocess.utils import set_policy_util
    message,status_code = set_policy_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)
        
        
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@check_group(['admin'])
def get_policy(data):
    check_permission(data,"can_get_policy")
    data = json.loads(data.body)
    from preprocess.utils import get_policy_util
    message,status_code = get_policy_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)
              
        
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@check_group(['admin'])
def set_cam_part(data):
    check_permission(data,"can_set_cam_part")
    data = json.loads(data.body)
    from preprocess.utils import set_cam_part_util
    message,status_code = set_cam_part_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code) 

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
#@check_group(['admin'])
def set_crop(data):
    check_permission(data,"can_set_crop")
    data = json.loads(data.body)
    from preprocess.utils import set_crop_util
    message,status_code = set_crop_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

@api_view(['GET'])
@csrf_exempt
def get_capture_feed_url(request):
    check_permission(request,"can_get_capture_feed_url")
    from preprocess.utils import get_camera_feed_urls
    url = get_camera_feed_urls()
    return HttpResponse(json.dumps( {'capture_url' : url} , cls=Encoder), content_type="application/json")


@api_view(['POST'])
@csrf_exempt
def initial_capture(request):
    check_permission(request,"can_initial_capture")
    data = json.loads(request.body)
    from preprocess.utils import initial_capture_util
    message,status_code = initial_capture_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)


@api_view(['POST'])
@csrf_exempt
def set_init_regions(request):
    check_permission(request,"can_set_init_regions")
    data = json.loads(request.body)
    from preprocess.utils import set_init_regions_util
    message,status_code = set_init_regions_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

@api_view(['POST'])
@csrf_exempt
def capture_util(request):
    check_permission(request,"can_capture")
    data = json.loads(request.body)
    from preprocess.utils import capture_util
    message,status_code = capture_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

@api_view(['POST'])
@csrf_exempt
def final_capture(request):
    check_permission(request,"can_final_capture")
    data = json.loads(request.body)
    from preprocess.utils import final_capture_util
    message,status_code = final_capture_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

@api_view(['GET'])
@csrf_exempt
def show_captured_img(request):
    check_permission(request,"can_get_captured_img")
    data = json.loads(request.body)
    from preprocess.utils import show_captured_img_util
    message,status_code = show_captured_img_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

@api_view(['GET'])
@csrf_exempt
def change_img(request):
    check_permission(request,"can_change_img")
    data = json.loads(request.body)
    from preprocess.utils import change_img_util
    message,status_code = change_img_util(data)
    if status_code == 200:
        return HttpResponse(json.dumps({'Message' : 'Success!', 'data' : message}, cls=Encoder), content_type="application/json")
    else:
        return HttpResponse( {message}, status=status_code)

@api_view(['GET'])
@csrf_exempt
def get_camera_stream(request, wid, cameraid):
    check_permission(request,"can_get_camera_stream")
    from preprocess.utils import redis_camera
    key = RedisKeyBuilderServer(wid).get_key(cameraid, 'original-frame')
    print(key)
    return StreamingHttpResponse(redis_camera(key), content_type='multipart/x-mixed-replace; boundary=frame')


@api_view(['GET'])
@csrf_exempt
def get_redis_stream(request, key):
    check_permission(request,"can_get_redis_stream")
    from preprocess.utils import redis_camera
    #key = RedisKeyBuilderServer(wid).get_key(cameraid, 'predicted-frame')
    #print(key)
    return StreamingHttpResponse(redis_camera(key), content_type='multipart/x-mixed-replace; boundary=frame')

