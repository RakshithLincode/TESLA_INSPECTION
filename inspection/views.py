from json import encoder
import json
from django.http import HttpResponse, response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.decorators import api_view, permission_classes
from common.utils import Encoder
from .utils import *
from rest_framework.permissions import AllowAny
from accounts.views import check_permission
from django.http import HttpResponse, StreamingHttpResponse


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def getDefectList(request, inspectionid):
    # check_permission(request,"can_get_defect_list")
    from inspection.utils import get_defect_list
    response,status_code = get_defect_list(inspectionid)
    # print(data,'defects list....')
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json") 

# @api_view(['GET'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def get_metrics_view(request,inspection_id):
#     from operators.utils import get_metrics_util
#     response,status_code = get_metrics_util(inspection_id)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json") 

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def save_inspection_details_view(request):
    data = request.data
    from inspection.utils import save_inspection_details_util
    response,status_code = save_inspection_details_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json") 



@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def save_inspection_per_view(request):
    data = request.data
    #check_permission(request,"can_save_inspection_results")
    from inspection.utils import save_inspection_per_view
    #topic_detected_labels= str(cameraid)+str("_taco")
    url = save_inspection_per_view(data)
    return HttpResponse(json.dumps({'data': url}), content_type="application/json")


@permission_classes((AllowAny,))
@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))
def get_data_stream(request, cameraid):
    check_permission(request,"can_get_capture_feed_url")
    from inspection.utils import get_data_feed
    #topic_detected_labels = str(cameraid) +str("_taco")
    url = get_data_feed(cameraid)
    return HttpResponse(json.dumps({'data': url}), content_type="application/json")


import os
# @permission_classes((AllowAny,))
@api_view(['GET'])
@csrf_exempt
#@permission_classes((AllowAny,))

# def get_camera_urls(request):
#     # check_permission(request,"can_get_capture_feed_url")
#     url_list = [
#         "http://127.0.0.1:8000/livis/operators/get_redis_image/input_frame/",
# 			CacheHelper().get_json("mask_frame"),
# 			CacheHelper().get_json("measure_frame"),
# 			CacheHelper().get_json("inference_frame"),


#     ]
#     # mp = MongoHelper().getCollection('config')
#     # mp_data = mp.find_one()
#     # rows = mp_data.get('rows')
#     # columns = mp_data.get('columns')

#     # for i in range(1,predicted_frame_length+1):        
#     #     url_list.append(create_urls_from_camera(i, f'http://localhost:{port_number}') )
    
    
    
#     return HttpResponse(json.dumps({'data': url_list}), content_type="application/json")
def get_camera_urls(request):
    # check_permission(request,"can_get_capture_feed_url")
    url_list = [
        "http://127.0.0.1:8000//livis/v1/inspection/get_output_stream/input_frame/",
            CacheHelper().get_json("inference_frame"),
            # CacheHelper().get_json("mask_frame"),
            # CacheHelper().get_json("measure_frame"),
    ]
    # url_list = []
    # for i in range(1,7):
    # 	url_list.append(create_urls_from_camera(i, 'http://localhost:8000') )   
    # for i in range(7,13):
        
    # 	url_list.append(create_urls_from_camera(i, 'http://127.0.0.1:8000') )
    # #for i in range(13,16):  #### 15th view
    # for i in range(13,19):
    # 	url_list.append(create_urls_from_camera(i, 'http://192.168.32.123:8000'))

    # for i in range(19,22):
    # 	url_list.append(create_urls_from_camera(i, 'http://0.0.0.0:8000') )           
    # url_list.append(CacheHelper().get_json("mask_frame"))
    # 	url_list.append(CacheHelper().get_json("measure_frame"))
    # 	url_list.append(CacheHelper().get_json("inference_frame")) 
    print(url_list)

    return HttpResponse(json.dumps({'data': url_list}), content_type="application/json")


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
#@permission_classes((AllowAny,))
def get_running_process_views(request):
    # check_permission(request,"can_get_running_process")
    from inspection.utils import get_running_process_utils
    response, status_code = get_running_process_utils()
    if status_code != 200:
        return HttpResponse({response}, status = status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def camera_health_check_view(request):
    data = CacheHelper().get_json('camera_health_check')
    print(data)
    return HttpResponse(json.dumps({'data': data}), content_type="application/json")


@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def plc_health_check_view(request):
    CacheHelper().set_json({'plc_health_check':False})
    data = CacheHelper().get_json('plc_health_check')
    print(data)
    return HttpResponse(json.dumps({'data': data}), content_type="application/json")    


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def start_process(request):
    # check_permission(request,"can_start_process")
    data = json.loads(request.body)
    response,status_code = start_process_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
# @permission_classes((AllowAny,))
def end_process(request):
    # check_permission(request,"can_end_process")
    data = json.loads(request.body)
    response,status_code = end_process_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type = "application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
@csrf_exempt
@permission_classes((AllowAny,))
def get_output_stream(request,cameraid):
    from inspection.utils import get_inference_feed
    return StreamingHttpResponse(get_inference_feed(cameraid), content_type='multipart/x-mixed-replace; boundary=frame')

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def getRedZoneList(request):
    data = CacheHelper().get_json('redzone_list')
    print(data)
    return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def get_metrics_view(request,inspection_id):
    from inspection.utils import get_metrics_util
    response,status_code = get_metrics_util(inspection_id)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json") 

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def start_inspection_view(request):
    data = json.loads(request.body)
    print(data,'hhhhhhhhhhhhhhhhhhhgbggggggggggggggggggggggggggggggggggggggggg')
    from inspection.utils import start_inspection_util
    response,status_code = start_inspection_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")


@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def set_config(request):
    data = json.loads(request.body)
    from inspection.utils import set_config_util
    response,status_code = set_config_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer,JSONRenderer))
@csrf_exempt
@permission_classes((AllowAny,))
def flag(request):
    data = json.loads(request.body)
    from inspection.utils import flag_util
    response,status_code = flag_util(data)
    if status_code != 200:
        return HttpResponse( {response}, status=status_code)
    else:
        return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")        

# @api_view(['POST'])
# @renderer_classes((TemplateHTMLRenderer,JSONRenderer))
# @csrf_exempt
# @permission_classes((AllowAny,))
# def flag(request):
#     data = json.loads(request.body)
#     from inspection.utils import flag_util
#     response,status_code = flag_util(data)
#     if status_code != 200:
#         return HttpResponse( {response}, status=status_code)
#     else:
#         return HttpResponse(json.dumps(response, cls=Encoder), content_type="application/json")         