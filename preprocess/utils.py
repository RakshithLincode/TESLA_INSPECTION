#from common.utils import MongoHelper, run_in_background
from common.utils import MongoHelper
from common.utils import RedisKeyBuilderServer,CacheHelper
#from preprocess.constants import *
from bson import ObjectId
from zipfile import ZipFile
import os
import json
import uuid
import cv2
import datetime
from copy import deepcopy
import xml.etree.cElementTree as ET
from lxml import etree
import csv
from livis.constants import *
import shutil
import imutils
import random
from django.conf import settings
import base64
import numpy as np




def set_policy_util(data):

    message = None
    status_code = None
    regions = []

    brightness = 0
    hue = None
    contrast = 0
    saturation = None


   
    try:
        regions = data['regions']
    except:
        pass
        
    try:
        brightness = data['brightness']
    except:
        pass
        
    try:
        hue = data['hue']
    except:
        pass  

    try:
        contrast = data['contrast']
    except:
        pass
        
    try:
        saturation = data['saturation']
    except:
        pass 
    


          
    camera_id = data['camera_id']
    
    

    try:
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    part_id =  data['part_id']
    if part_id is None:
        message = "part id not provided"
        status_code = 400
        return message,status_code

    try:
        dataset = mp.find_one({'_id' : ObjectId(part_id)})
        if dataset is None:
            message = "Part not found in Parts collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid PartId"
        status_code = 400
        return message,status_code
       
       
    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    workstation_id =  data['workstation_id']
    if workstation_id is None:
        message = "workstation_id not provided"
        status_code = 400
        return message,status_code

    try:
        dataset = mp.find_one({'_id' : ObjectId(workstation_id)})
        if dataset is None:
            message = "workstation not found in workstation collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid workstationid "
        status_code = 400
        return message,status_code 
        
    preprocessing_coll = str(part_id)+"_preprocessingpolicy"
    mp = MongoHelper().getCollection(preprocessing_coll)
    
    rp = [p for p in mp.find(  {"$and" : [ {"workstation_id": workstation_id }, { "camera_id" : str(camera_id) } ] } )]
    print(rp)
    
    if len(rp) == 0:
        #record not found - insert
        #if regions is not None and regions != '' and len(regions) > 0:
        sc = {"workstation_id": workstation_id, "camera_id" : str(camera_id) , "policy": {"crop":regions,"brightness":brightness,"contrast":contrast} }
        _id = mp.insert(sc)
        print("inserted")
        print(_id)

    else:

        #record dound - update
        _id = rp[0]['_id']
        #if regions is not None:
            #print()
        sc = {"workstation_id": workstation_id, "camera_id" : str(camera_id) , "policy": {"crop":regions,"brightness":brightness,"contrast":contrast} }
        mp.update({'_id' : ObjectId(_id)}, {'$set' :  sc})    
        print("updated")

    return sc,200 
        

    

def get_policy_util(data):

    message = None
    status_code = None
    regions = None
    brightness = None
    hue = None

   
    try:
        part_id_json = data['part_id']
    except:
        message = "part id not provided"
        status_code = 400
        return message, status_code

    try:
        workstation_id = data['workstation_id']
    except:
        message = "workstation id not provided"
        status_code = 400
        return message, status_code

    try:
        camera_id = data['camera_id']
    except:
        message = "camera_id not provided"
        status_code = 400
        return message, status_code



    try:
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    part_id =  data['part_id']
    if part_id is None:
        message = "part id not provided"
        status_code = 400
        return message,status_code

    try:
        dataset = mp.find_one({'_id' : ObjectId(part_id)})
        if dataset is None:
            message = "Part not found in Parts collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid PartId"
        status_code = 400
        return message,status_code
       
       
    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    workstation_id =  data['workstation_id']
    if workstation_id is None:
        message = "workstation_id not provided"
        status_code = 400
        return message,status_code

    try:
        dataset = mp.find_one({'_id' : ObjectId(workstation_id)})
        if dataset is None:
            message = "workstation not found in workstation collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid workstationid "
        status_code = 400
        return message,status_code 
        
    preprocessing_coll = str(part_id)+"_preprocessingpolicy"
    mp = MongoHelper().getCollection(preprocessing_coll)
    
    rp = [p for p in mp.find(  {"$and" : [ {"workstation_id": workstation_id }, { "camera_id" : camera_id } ] } )]
    
    """
    if len(rp) == 0:
        #record not found - insert
        if regions is not None:
            sc = {"workstation_id": workstation_id, "camera_id" : camera_id , "policy": {"crop":regions} }
            _id = mp.insert(sc)

         
    else:

        #record dound - update
        _id = rp[0]['_id']
        if regions is not None:
            sc = {"workstation_id": workstation_id, "camera_id" : camera_id , "policy": {"crop":regions} }
            mp.update({'_id' : rp[0]['_id']}, {'$set' :  sc})    
    """
    
    return rp,200 




def set_cam_part_util(data):
    workstation_id = data['workstation_id']
    camera_id = data['camera_id']
    part_id = data['part_id']
    
    mp = MongoHelper().getCollection("cam_to_part")
    
    rp = [p for p in mp.find()]
    
    rp = rp[0]
    _id = rp['_id']
    
    
    rp['camera_id'] = camera_id
    rp['part_id'] = part_id
    
    
    mp.update({'_id' : ObjectId(_id)}, {'$set' :  rp})
    
    return "success",200
    
    
  


#just a util for crop/padding to 600x600 for ssd mobilenet - used in final_capture_util
def resize_pad(crop_img):

    h,w,c = crop_img.shape
    if h>600 and w>600:
        crop_img = cv2.resize(crop_img,(600,600))
    else:
        ww = 600
        hh = 600
        color = (0,0,0)
        result = np.full((hh,ww,cc), color, dtype=np.uint8)

        # compute center offset
        xx = (ww - wd) // 2
        yy = (hh - ht) // 2

        # copy img image into center of result image
        result[yy:yy+ht, xx:xx+wd] = crop_img
    
    return crop_img

#fetch all camera urls to display as streaming response on ui
def get_camera_feed_urls():

    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code


    p = [p for p in mp.find()]

    p=p[0]

    workstation_id = p['_id']

    feed_urls = {}
    workstation_info = RedisKeyBuilderServer(workstation_id).workstation_info
    print(workstation_info)
    cam=workstation_info['camera_config']
    print(cam)
    for camera_info in cam['cameras']:
        url = "http://127.0.0.1:8000/livis/v1/preprocess/stream/{}/{}/".format(workstation_id,camera_info['camera_id'])

        feed_urls[camera_info['camera_name']] = url
    if feed_urls:
        return feed_urls
    else:
        return {}

#actual camera stream as a http stream
def redis_camera(key):
    rch = CacheHelper()
    while True:
        #key = str(key)+"_small"
        frame = rch.get_json(key)
        #frame1 = base64.b64decode(frame1)
        #frame1 = np.frombuffer(frame1, dtype=np.uint8)
        #frame1 = cv2.imdecode(frame1, flags=1)
        
        
        #print("KEY :      : :: :  : : : : :" , key)
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame =  jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#to capture 5 images and store in local and db
def initial_capture_util(data):
    message = None
    status_code = None


    try:
        mp = MongoHelper().getCollection(JIG_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    jig_id =  data['jig_id']
    if jig_id is None:
        message = "jig id not provided"
        status_code = 400
        return message,status_code

    try:
        dataset = mp.find_one({'_id' : ObjectId(jig_id)})
        if dataset is None:
            message = "Jig not found in Jig collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid jigID"
        status_code = 400
        return message,status_code
    

    oem_number = dataset['oem_number']
    jig_type = dataset['jig_type']

    rch = CacheHelper()
    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    p = [p for p in mp.find()]

    workstation_det = p[0]['camera_config']['cameras']
    workstation_name = p[0]['workstation_name']


    cam_name = []
    cam_id = []

    for indexes in workstation_det:
        cam_id.append(indexes['camera_id'])
        cam_name.append(indexes['camera_name'])

    redis_key_list = []

    for actual_idx in cam_id:
        redis_key_list.append(str(workstation_name)+'_'+str(actual_idx)+'_'+'original-frame')

    #import pwd
    #my_home_pth = str(pwd.getpwuid(os.getuid()).pw_dir)
    base_path =  os.path.join('/critical_data/')
    if oem_number is None:
        this_model_pth = str(jig_type)
    else:
        this_model_pth = str(jig_type) + str(oem_number)

    dir_path = os.path.join(base_path,this_model_pth)

    dir_init_img_path = os.path.join(dir_path,'full_image_before_preprocess')


    #clear out local storage and create same path
    import shutil
    shutil.rmtree(dir_init_img_path,ignore_errors=True)
    os.makedirs(dir_init_img_path, exist_ok=True)

    #clear out db 
    #jig collection in that {full_img :[ {cam1 : path}, {cam2 : path}, {cam3 : path} ] }


    ############# find the specific jig in jig collection
    try:
        mp = MongoHelper().getCollection(JIG_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code


    collection_obj = {'full_img':""}


    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' :  collection_obj})


    img_name_list = []

    for red_key in redis_key_list:
        frame1  = rch.get_json(red_key)
        frame1 = base64.b64decode(frame1)
        frame1 = np.frombuffer(frame1, dtype=np.uint8)
        frame = cv2.imdecode(frame1, flags=1)
        
        img_name = os.path.join(dir_init_img_path,str(red_key)+".png")
        img_name_list.append(img_name)
        cv2.imwrite(img_name,frame)

    cam_path_dict = {}
    pic_det = []

    for img,cam in zip(img_name_list,cam_name):
        print(img,cam)
        img_url = str(img).replace('/critical_data','http://127.0.0.1:3306/')
        pic_det.append({'cam_name':cam,'img_pth':img,'img_url':img_url})
    

    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' :  {'full_img':pic_det}})

    message = pic_det
    status_code = 200

    return message,status_code

#display all 5 images once its captured to ui
def show_captured_img_util(data):
    message = None
    status_code = None

    try:
        mp = MongoHelper().getCollection(JIG_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    jig_id =  data['jig_id']
    if jig_id is None:
        message = "jig id not provided"
        status_code = 400
        return message,status_code
    

    try:
        dataset = mp.find_one({'_id' : ObjectId(jig_id)})
        if dataset is None:
            message = "Jig not found in Jig collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid jigID"
        status_code = 400
        return message,status_code
    try:
        message=dataset['full_img']
        status_code = 200
    except:
        message="error retriving images"
        status_code=400


    return message,status_code

#next and prev 5 images along with the regions if any
def change_img_util(data):

    message = None
    status_code = None

    jig_id = data['jig_id']
    current_cam_name = data['cam_name']
    position = data['position']

    if jig_id is None:
        message = "jig_id not provided"
        status_code = 400
        return message,status_code

    
    try:
        mp = MongoHelper().getCollection(JIG_COLLECTION)
    except:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    try:
        dataset = mp.find_one({'_id' : ObjectId(jig_id)})
        if dataset is None:
            message = "jig not found in jig collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid jig_id"
        status_code = 400
        return message,status_code

    full_img=dataset['full_img']
    print(full_img)

    if position == 'next':


        if current_cam_name == 'extreme_left_camera':
            return full_img[1],200
        elif current_cam_name == 'left_camera':
            return full_img[2],200
        elif current_cam_name == 'middle_camera':
            return full_img[3],200
        elif current_cam_name == 'right_camera':
            return full_img[4],200
        elif current_cam_name == 'extreme_right_camera':
            return full_img[4],200
    else:

        if current_cam_name == 'extreme_left_camera':
            return full_img[0],200
        elif current_cam_name == 'left_camera':
            return full_img[0],200
        elif current_cam_name == 'middle_camera':
            return full_img[1],200
        elif current_cam_name == 'right_camera':
            return full_img[2],200
        elif current_cam_name == 'extreme_right_camera':
            return full_img[3],200

#set the bounding box regions got from ui to full_img obj
def set_init_regions_util(data):

    message = None
    status_code = None

    jig_id =  data['jig_id']

    if jig_id is None:
        message = "jig type not provided"
        status_code = 400
        return message,status_code

    regions =  data['regions']
    if regions is None:
        message = "regions not provided"
        status_code = 400
        return message,status_code

    #img_url =  data['src']
    #if img_url is None:
    #    message = "img_url not provided"
    #    status_code = 400
    #    return message,status_code

    camera_name =  data['cam_name']
    if camera_name is None:
        message = "camera_name not provided"
        status_code = 400
        return message,status_code 

    #img_pth =  data['img_pth']
    #if img_pth is None:
    #    message = "img_pth not provided"
    #    status_code = 400
    #    return message,status_code 

    try:
        mp = MongoHelper().getCollection(JIG_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code
    
    try:
        dataset = mp.find_one({'_id' : ObjectId(jig_id)})
        if dataset is None:
            message = "Jig not found in Jig collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid jigID"
        status_code = 400
        return message,status_code
        
    rch = CacheHelper()
    oem_number = dataset['oem_number']
    jig_type = dataset['jig_type']

    base_path =  os.path.join('/critical_data/')
    if oem_number is None:
        this_model_pth = str(jig_type)
    else:
        this_model_pth = str(jig_type) + str(oem_number)

    model_complete_name_pth = os.path.join(base_path,this_model_pth)


    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    p = [p for p in mp.find()]

    workstation_det = p[0]['camera_config']['cameras']
    workstation_name = p[0]['workstation_name']


    cam_name = []
    cam_id = []

    for indexes in workstation_det:
        cam_id.append(indexes['camera_id'])
        cam_name.append(indexes['camera_name'])

    redis_key_list = []

    for actual_idx in cam_id:
        redis_key_list.append(str(workstation_name)+'_'+str(actual_idx)+'_'+'original-frame')

    #var = str(ObjectId(dataset['_id'])) + "_full_img"
    #full_img = rch.get_json(var)
    #print("$$$$$$$$")
    
    from os import path
    import json 
    if path.exists('/critical_data/regions/'+str(ObjectId(dataset['_id'])) + "_full_img"+".json"):
        f = open ('/critical_data/regions/'+str(ObjectId(dataset['_id'])) + "_full_img"+".json", "r")
        a = json.loads(f.read())
        full_img = a['full_img']
        f.close()
    else:
        full_img = None
        
    print(full_img)
    print("eeeeeee")
    
    if full_img is None:
        full_img=dataset['full_img']


    index = 0
    for ind in full_img:
        if ind['cam_name'] == camera_name:
            new_dict = {'cam_name':camera_name,'regions':regions}
            full_img[index] = new_dict
            break
        index = index + 1
    
    
    #print("here")
    #full_img = {'cam_name':camera_name,'regions':regions}
    #print(full_img)
    
    full_img1  = {}
    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' : {'full_img':[]}})
    
    mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' : {'full_img':full_img}})
    print(full_img)
    
    #var = str(ObjectId(dataset['_id'])) + "_full_img"
    #rch.set_json({var:full_img})
    #full_img = rch.get_json(var)
    data_of_full = {'full_img':full_img}
    with open('/critical_data/regions/'+str(ObjectId(dataset['_id'])) + "_full_img"+".json", 'w') as outfile:
        json.dump(data_of_full, outfile)
    
    print("#########")
    print(full_img)

    #full_img = dataset['full_img']
    #sometimes regions might not be defined - error handle that (regions would be none - ask fe to send that)
    #region annotation key should be unique within an image
    

    #img_fill_tmp = cv2.imread(img_pth)
    #height,width,channel = img_fill_tmp.shape
    #model_complete_name_pth = os.path.join(str(img_pth).split('/')[1] , str(img_pth).split('/')[2])
    #model_complete_name_pth = "/" + str(model_complete_name_pth)
    #print(model_complete_name_pth)

    # height and width ()





    idx = None
    print(cam_name)

    cam_name =  data['cam_name']
    regions =  data['regions']
    #img_pth =  data['img_pth']



    for indexes in workstation_det:
        if indexes['camera_name'] == cam_name:
            idx = indexes['camera_id']
            break

    redis_key = None
    frame = None

    if idx is None:
        return "problem with camera_idx",400
    else:
        redis_key = str(workstation_name)+'_'+str(idx)+'_'+'original-frame'
        frame  = rch.get_json(redis_key)
        #frame1 = base64.b64decode(frame1)
        #frame1 = np.frombuffer(frame1, dtype=np.uint8)
        #frame = cv2.imdecode(frame1, flags=1)
        height,width,channel = frame.shape
    
    crop_save_pth =  os.path.join(model_complete_name_pth,'crops')
    if not os.path.exists(crop_save_pth):
        os.makedirs(crop_save_pth)


    if redis_key is None:
        return "problem with redis key string",400
    else:

        policy_crop = []

        for j in regions:

            x = j["x"]
            y = j["y"]
            w = j["w"]
            h = j["h"]

            x0 = x * width
            y0 = y * height
            x1 = ((x+w) * width)
            y1 = ((y+h) * height)

            label = j["cls"]
            cords = [x0,y0,x1,y1]

            policy_crop.append({label:cords})



        for pol in policy_crop:
            cords=pol.values()
            for i in cords:
                x0 = int(i[0])
                y0 = int(i[1])
                x1 = int(i[2])
                y1 = int(i[3])

                crop = frame[y0:y1,x0:x1].copy()
                
                #crop = resize_pad(crop)
                id_uuid = str(uuid.uuid4())+'.png'

                crop_img_pth = os.path.join(crop_save_pth,id_uuid)


                crop_img_url = str(os.path.join(crop_save_pth,id_uuid)).replace('/critical_data','http://127.0.0.1:3306/')
                # store on local dsk
                #cv2.imwrite(crop_img_pth,crop)

                # store in db
                _id = str(dataset['_id'])
                mp = MongoHelper().getCollection(str(dataset['_id']))


                collection_obj = {
                    'file_path' : crop_img_pth,
                    'file_url' : crop_img_url,
                    'state' : 'untagged',
                    'regions' : [],
                    'regions_history' : [],
                    'classifier_label' : "",
                    'classifier_label_history' : [],
                    'annotator' : ''
                }

                #mp.insert(collection_obj)



    message = 'success'
    status_code = 200
  
    return message,status_code

#final capture capture crops according to region policy and 
def final_capture_util(data):
    message = None
    status_code = None

    #ui will send jig_id
    #iterate inside full_img inside that regions (get xywh)
    #open redis using cap index, iterate through regions and crop save in local as well as new collection _id(refer zip upload api for fields)
    message = None
    status_code = None

    jig_id =  data['jig_id']
    if jig_id is None:
        message = "jig type not provided"
        status_code = 400
        return message,status_code

    rch = CacheHelper()
    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    p = [p for p in mp.find()]

    workstation_det = p[0]['camera_config']['cameras']
    workstation_name = p[0]['workstation_name']


    cam_name = []
    cam_id = []

    for indexes in workstation_det:
        cam_id.append(indexes['camera_id'])
        cam_name.append(indexes['camera_name'])

    redis_key_list = []

    for actual_idx in cam_id:
        redis_key_list.append(str(workstation_name)+'_'+str(actual_idx)+'_'+'original-frame')

    try:
        mp = MongoHelper().getCollection(JIG_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code
    
    try:
        dataset = mp.find_one({'_id' : ObjectId(jig_id)})
        if dataset is None:
            message = "Jig not found in Jig collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid jigID"
        status_code = 400
        return message,status_code

    
    full_img = dataset['full_img']
    #sometimes regions might not be defined - error handle that (regions would be none - ask fe to send that)
    #region annotation key should be unique within an image
    for f_img in full_img:
        cam_name = f_img['cam_name']
        regions = f_img['regions']
        img_pth = f_img['img_pth']
        model_complete_name_pth = os.path.join(str(img_pth).split('/')[1] , str(img_pth).split('/')[2])

        idx = None
        
        for indexes in workstation_det:
            if indexes['camera_name'] == cam_name:
                idx = indexes['camera_id']
                break

        redis_key = None
        frame = None

        if idx is None:
            return "problem with camera_idx",400
        else:
            redis_key = str(workstation_name)+'_'+str(idx)+'_'+'original-frame'
            frame1  = rch.get_json(redis_key)
            frame1 = base64.b64decode(frame1)
            frame1 = np.frombuffer(frame1, dtype=np.uint8)
            frame = cv2.imdecode(frame1, flags=1)
        
        crop_save_pth =  os.path.join(model_complete_name_pth,'crops')


        if redis_key is None:
            return "problem with redis key string",400
        else:

            policy_crop = []

            for j in regions:

                x = j["x"]
                y = j["y"]
                w = j["w"]
                h = j["h"]

                x0 = x * width
                y0 = y * height
                x1 = ((x+w) * width)
                y1 = ((y+h) * height)

                label = j["cls"]
                cords = [x0,y0,x1,y1]

                policy_crop.append({label:cords})



            for pol in policy_crop:
                cords=pol.values()
                for i in cords:
                    x0 = i[0]
                    y0 = i[1]
                    x1 = i[2]
                    y1 = i[3]

                    crop = frame[y0:y1,x0:x1].copy()
                    #crop = resize_pad(crop)
                    id_uuid = str(uuid.uuid4())+'.png'

                    crop_img_pth = os.path.join(crop_save_pth,id_uuid)
                    crop_img_url = str(os.path.join(crop_save_pth,id_uuid)).replace('/critical_data','http://127.0.0.1:3306/')
                    # store on local dsk
                    cv2.imwrite(crop_img_pth,crop)

                    # store in db
                    _id = str(dataset['_id'])
                    mp = MongoHelper().getCollection(str(dataset['_id']))


                    collection_obj = {
                        'file_path' : crop_img_pth,
                        'file_url' : crop_img_url,
                        'state' : 'untagged',
                        'regions' : [],
                        'regions_history' : [],
                        'classifier_label' : "",
                        'classifier_label_history' : [],
                        'annotator' : ''
                    }

                    mp.insert(collection_obj)



    message = 'success'
    status_code = 200
  
    return message,status_code


def capture_util(data):


    message = None
    status_code = None

    jig_id =  data['jig_id']

    if jig_id is None:
        message = "jig type not provided"
        status_code = 400
        return message,status_code

    regions =  data['regions']
    if regions is None:
        message = "regions not provided"
        status_code = 400
        return message,status_code

    #img_url =  data['src']
    #if img_url is None:
    #    message = "img_url not provided"
    #    status_code = 400
    #    return message,status_code

    camera_name =  data['cam_name']
    if camera_name is None:
        message = "camera_name not provided"
        status_code = 400
        return message,status_code 

    #img_pth =  data['img_pth']
    #if img_pth is None:
    #    message = "img_pth not provided"
    #    status_code = 400
    #    return message,status_code 

    try:
        mp = MongoHelper().getCollection(JIG_COLLECTION)
    except Exception as e:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code
    
    try:
        dataset = mp.find_one({'_id' : ObjectId(jig_id)})
        if dataset is None:
            message = "Jig not found in Jig collection"
            status_code = 404
            return message,status_code

    except Exception as e:
        message = "Invalid jigID"
        status_code = 400
        return message,status_code
        
    rch = CacheHelper()
    oem_number = dataset['oem_number']
    jig_type = dataset['jig_type']

    base_path =  os.path.join('/home/schneider/Documents/critical_data/annotation')
    if oem_number is None:
        this_model_pth = str(jig_type)
    else:
        this_model_pth = str(jig_type) + str(oem_number)

    model_complete_name_pth = os.path.join(base_path,this_model_pth)


    try:
        mp = MongoHelper().getCollection(WORKSTATION_COLLECTION)
    except:
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code

    p = [p for p in mp.find()]

    workstation_det = p[0]['camera_config']['cameras']
    workstation_name = p[0]['workstation_name']


    cam_name = []
    cam_id = []

    for indexes in workstation_det:
        cam_id.append(indexes['camera_id'])
        cam_name.append(indexes['camera_name'])

    redis_key_list = []

    for actual_idx in cam_id:
        redis_key_list.append(str(workstation_name)+'_'+str(actual_idx)+'_'+'original-frame')

    #var = str(ObjectId(dataset['_id'])) + "_full_img"
    #full_img = rch.get_json(var)
    #print("$$$$$$$$")
    
    from os import path
    import json 
    if path.exists('/critical_data/regions/'+str(ObjectId(dataset['_id'])) + "_full_img"+".json"):
        f = open ('/critical_data/regions/'+str(ObjectId(dataset['_id'])) + "_full_img"+".json", "r")
        a = json.loads(f.read())
        full_img = a['full_img']
        f.close()
    else:
        full_img = None
        
    print(full_img)
    print("eeeeeee")
    
    if full_img is None:
        full_img=dataset['full_img']


    index = 0
    for ind in full_img:
        if ind['cam_name'] == camera_name:
            new_dict = {'cam_name':camera_name,'regions':regions}
            full_img[index] = new_dict
            break
        index = index + 1
    
    
    #print("here")
    #full_img = {'cam_name':camera_name,'regions':regions}
    #print(full_img)
    
    full_img1  = {}
    #mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' : {'full_img':[]}})
    
    #mp.update({'_id' : ObjectId(dataset['_id'])}, {'$set' : {'full_img':full_img}})
    print(full_img)
    
    #var = str(ObjectId(dataset['_id'])) + "_full_img"
    #rch.set_json({var:full_img})
    #full_img = rch.get_json(var)
    data_of_full = {'full_img':full_img}
    #with open('/critical_data/regions/'+str(ObjectId(dataset['_id'])) + "_full_img"+".json", 'w') as outfile:
    #    json.dump(data_of_full, outfile)
    
    print("#########")
    print(full_img)

    #full_img = dataset['full_img']
    #sometimes regions might not be defined - error handle that (regions would be none - ask fe to send that)
    #region annotation key should be unique within an image
    

    #img_fill_tmp = cv2.imread(img_pth)
    #height,width,channel = img_fill_tmp.shape
    #model_complete_name_pth = os.path.join(str(img_pth).split('/')[1] , str(img_pth).split('/')[2])
    #model_complete_name_pth = "/" + str(model_complete_name_pth)
    #print(model_complete_name_pth)

    # height and width ()





    idx = None
    print(cam_name)

    cam_name =  data['cam_name']
    regions =  data['regions']
    #img_pth =  data['img_pth']



    for indexes in workstation_det:
        if indexes['camera_name'] == cam_name:
            idx = indexes['camera_id']
            break

    redis_key = None
    frame = None

    if idx is None:
        return "problem with camera_idx",400
    else:
        redis_key = str(workstation_name)+'_'+str(idx)+'_'+'original-frame'
        frame  = rch.get_json(redis_key)
        #frame1 = base64.b64decode(frame1)
        #frame1 = np.frombuffer(frame1, dtype=np.uint8)
        #frame = cv2.imdecode(frame1, flags=1)
        height,width,channel = frame.shape
    
    crop_save_pth =  os.path.join(model_complete_name_pth,'crops')
    if not os.path.exists(crop_save_pth):
        os.makedirs(crop_save_pth)


    if redis_key is None:
        return "problem with redis key string",400
    else:

        policy_crop = []

        for j in regions:

            x = j["x"]
            y = j["y"]
            w = j["w"]
            h = j["h"]

            x0 = x * width
            y0 = y * height
            x1 = ((x+w) * width)
            y1 = ((y+h) * height)

            label = j["cls"]
            cords = [x0,y0,x1,y1]

            policy_crop.append({label:cords})



        for pol in policy_crop:
            cords=pol.values()
            for i in cords:
                x0 = int(i[0])
                y0 = int(i[1])
                x1 = int(i[2])
                y1 = int(i[3])

                crop = frame[y0:y1,x0:x1].copy()
                
                #crop = resize_pad(crop)
                id_uuid = str(uuid.uuid4())+'.png'

                crop_img_pth = os.path.join(crop_save_pth,id_uuid)


                crop_img_url = str(os.path.join(crop_save_pth,id_uuid)).replace('/home/schneider/Documents/critical_data/annotation/','http://0.0.0.0:3306/')
                #crop_img_url = "http://127.0.0.1:3306/" + str(crop_img_url)
                # store on local dsk
                cv2.imwrite(crop_img_pth,crop)

                # store in db
                _id = str(dataset['_id'])
                mp = MongoHelper().getCollection(str(dataset['_id']))


                collection_obj = {
                    'file_path' : crop_img_pth,
                    'file_url' : crop_img_url,
                    'state' : 'untagged',
                    'regions' : [],
                    'regions_history' : [],
                    'classifier_label' : "",
                    'classifier_label_history' : [],
                    'annotator' : ''
                }

                mp.insert(collection_obj)



    message = 'success'
    status_code = 200
  
    return message,status_code
