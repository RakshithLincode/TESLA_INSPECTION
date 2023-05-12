import numpy as np
import cv2 
import requests
import time
import copy
import bson
import gc
import sys
import redis
import pickle
from pymongo import MongoClient
from ai_settings import *
import numpy as np
import warnings
import numpy as np
import paddle
from paddleseg.cvlibs import manager, Config, SegBuilder
from paddleseg.utils import get_sys_env 
from paddleseg import utils
from paddleseg.core import infer
import time
from paddleseg import utils
from paddleseg.core import infer
from paddleseg.utils import logger, progbar, visualize
from PIL import Image
import os
warnings.filterwarnings("ignore")
gc.collect()

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class CacheHelper():
    def __init__(self):
        self.redis_cache = redis.StrictRedis(host='localhost', port=6379, db=0, socket_timeout=1)
        print("REDIS CACHE UP!")

    def get_redis_pipeline(self):
        return self.redis_cache.pipeline()
    
    def set_json(self, dict_obj):
        try:
            k, v = list(dict_obj.items())[0]
            v = pickle.dumps(v)
            return self.redis_cache.set(k, v)
        except redis.ConnectionError:
            return None

    def get_json(self, key):
        try:
            temp = self.redis_cache.get(key)
            #print(temp)\
            if temp:
                temp= pickle.loads(temp)
            return temp
        except redis.ConnectionError:
            return None
        return None

    def execute_pipe_commands(self, commands):
        #TBD to increase efficiency can chain commands for getting cache in one go
        return None

@singleton
class MongoHelper:
    try:
        client = None
        def __init__(self):
            if not self.client:
                self.client = MongoClient(host=MONGO_SERVER_HOST, port=MONGO_SERVER_PORT)
            self.db = self.client[MONGO_DB]

        def getDatabase(self):
            return self.db

        def getCollection(self, cname, create=False, codec_options=None):
            _DB = MONGO_DB
            DB = self.client[_DB]
            if cname in MONGO_COLLECTIONS:
                if codec_options:
                    return DB.get_collection(MONGO_COLLECTIONS[cname], codec_options=codec_options)
                return DB[MONGO_COLLECTIONS[cname]]
            else:
                return DB[cname]
    except:
        pass      

rch = CacheHelper()

def mkdir(path):
    sub_dir = os.path.dirname(path)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

def paddle_predict(img, 
            model, 
            model_path,
            transforms, 
            scales=1.0, 
            is_slide=False,
            stride=None,
            crop_size=None):
    
    utils.utils.load_entire_model(model, model_path)
    model.eval()
    
    with paddle.no_grad():
        timer1 = time.time()
        ori_shape = img.shape[:2]
        data = {}
        data['img'] = img
        data = transforms(data)
        data['img'] = data['img'][np.newaxis, ...]
        data['img'] = paddle.to_tensor(data['img'])
        pred, _ = infer.inference(
                    model,
                    data['img'],
                    trans_info=data['trans_info'],
                    is_slide=is_slide,
                    stride=stride,
                    crop_size=crop_size)
        pred = paddle.squeeze(pred)
        pred = pred.numpy().astype('uint8')
        cv2.imwrite('image_pre.png',pred)
        custom_color = [0, 0, 0, 255, 255, 255]
        color_map = visualize.get_color_map_list(256, custom_color=custom_color)
        color_map = [color_map[i:i + 3] for i in range(0, len(color_map), 3)]
        color_map = np.array(color_map).astype("uint8")
        c1 = cv2.LUT(pred, color_map[:, 0])
        c2 = cv2.LUT(pred, color_map[:, 1])
        c3 = cv2.LUT(pred, color_map[:, 2])
        pred = np.dstack((c3, c2, c1))
        timer2 = time.time()
        print("elapsed inf time: ", timer2 - timer1)
        return pred

def get_measurment(point):
    pixel_to_mm = 0.1 
    point1 = point[0]  
    point2 = point[1]  
    point1_mm = (point1[0] * pixel_to_mm, point1[1] * pixel_to_mm)
    point2_mm = (point2[0] * pixel_to_mm, point2[1] * pixel_to_mm)
    distance_mm = ((point2_mm[0] - point1_mm[0])**2 + (point2_mm[1] - point1_mm[1])**2)**0.5
    mm = str(distance_mm)[0:3]
    return mm

def get_width_measure(original , img):
    try:
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,500)
        fontScale = .25
        fontColor = (0,0,255)
        lineType = 1
        gray = img
        blur=cv2.GaussianBlur(gray, (7, 7), 0)
        flag, thresh = cv2.threshold(blur,100,255 , cv2.THRESH_BINARY)
        edged=cv2.Canny(thresh,50,100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        imm = cv2.inRange(edged, (0), (49))
        kernel = np.ones((5, 5), np.uint8)
        gradient = cv2.morphologyEx(imm, cv2.MORPH_GRADIENT, kernel)
        il = cv2.dilate(gradient, kernel, iterations=7)
        ol = cv2.erode(il, kernel, iterations=7)
        contours, hei = cv2.findContours(
            ol, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c=max(contours,key=cv2.contourArea)
        contours_only = np.zeros_like(img)
        cv2.drawContours(contours_only, [c], 0, (0,255,0), 1)
        gray = cv2.cvtColor(contours_only, cv2.COLOR_BGR2GRAY)
        start, end = [], []
        cv2.drawContours(original, [c], 0, (0,255,0), 2)
        for row_num in range(img.shape[0]-1):
            row = gray[row_num: row_num + 1, :]
            left_px = np.argmax(row)
            row = np.flip(row)
            right_px = img.shape[1] - np.argmax(row)
            if row_num%15 == 0 and left_px != 0 and right_px != 0 :
                cv2.line(original, (left_px, row_num), (right_px, row_num), (255,0,0), 1)
                point = [(left_px,row_num),(right_px,row_num)]
                mm = get_measurment(point)
                cv2.putText(original,str(mm + '_mm'), (right_px + 10,row_num), font, fontScale,fontColor,lineType)
        return original
    except Exception as e:
        print(e,'errorrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        return original
    
def model_predict(img):
    import time
    worker_start = time.time()
    env_info = get_sys_env()
    place = 'gpu' if env_info['Paddle compiled with cuda'] and env_info[
        'GPUs used'] else 'cpu'
    paddle.set_device(place)
    cfg = Config('pp_liteseg_optic_disc_512x512_1k.yml')
    builder = SegBuilder(cfg)
    model_path = './iter_1500/model.pdparams'
    pred_mask = paddle_predict(img, builder.model, model_path=model_path, transforms=builder.val_dataset.transforms)
    cv2.imwrite('image.png',pred_mask)    
    print("TIME TAKEN BY MODEL TO PREDICT MASK :::::::::::::::::::::::::::::::::::::::::::::",time.time() - worker_start)    
    return pred_mask    

def predict():
        while 1:
            vid = cv2.VideoCapture(0)
            vid.set(3,1920)   
            vid.set(4,1080)       
            while(True):
                ret, frame = vid.read()
                print(frame)
                if not ret:
                    break
                if frame is None:
                    continue
                rch.set_json({'input_frame':frame})
                mp = MongoHelper().getCollection("current_inspection")
                data = mp.find_one()
                try:
                    current_inspection_id = data.get('current_inspection_id')
                    print(current_inspection_id)
                    if current_inspection_id is None:
                        continue
                except:
                    pass  
                trigger = CacheHelper().get_json('inspection_trigger')
                print(trigger)
                if trigger == True:
                    worker_start = time.time()
                    select_model = CacheHelper().get_json('current_part_name')
                    print(select_model,'select_model..................................................................')
                    part_name = select_model
                    mask_input_frame = copy.copy(frame)
                    input_frmae = copy.copy(frame)
                    masks = model_predict(mask_input_frame)
                    worker_start = time.time()
                    original_image = get_width_measure(mask_input_frame,masks)      
                    is_accepted = 'Accepted'
                    x = bson.ObjectId()
                    cv2.imwrite(datadrive_path+str(x)+'_ip.jpg',input_frmae)
                    cv2.imwrite(datadrive_path+str(x)+'_pf.jpg',original_image)
                    input_frame_path = 'http://localhost:3306/'+str(x)+'_ip.jpg'
                    predicted_frame_path = 'http://localhost:3306/'+str(x)+'_pf.jpg'
                    print(input_frame_path)
                    rch.set_json({"input_frame_path":input_frame_path})
                    rch.set_json({"right_length":str('0')})
                    rch.set_json({"left_length":str('0')})
                    rch.set_json({"inference_frame":predicted_frame_path})
                    rch.set_json({"feature_mismatch":'features'})
                    rch.set_json({"defects":"0"})
                    rch.set_json({"left_radius":str(int(0))})
                    rch.set_json({"right_radius":str(int(0))})
                    rch.set_json({"radius_defect_value":"0"})
                    rch.set_json({"status":"Accepted"})
                    # else:
                    #     rch.set_json({"status":is_accepted})
                    #     rch.set_json({"defects":position[0]})
                    #     rch.set_json({"left_radius":str(int(radius[0]))})
                    #     rch.set_json({"right_radius":str(int(radius[1]))})
                    #     rch.set_json({"radius_defect_value":value_mis[0]})      
                    data = {'current_inspection_id':str(current_inspection_id)}#,'raw_frame':input_frame_path,'inference_frame':inference_frame_path,'status':is_accepted,'defect_list':conf.defects,'feature_list':conf.feature,'features':[],'defects':defect_list}
                    requests.post(url = 'http://localhost:8000/livis/v1/inspection/save_inspection_details/', data = data)
                    CacheHelper().set_json({'inspection_trigger':False})
                    print("Worker_Time_Taken",time.time() - worker_start)
                    if cv2.waitKey(1) == 27: 
                        break  
                cv2.destroyAllWindows()
        
if __name__ == "__main__":
    start = time.time()
    datadrive_path = "C:/DEMO/Tesla_Tyre/TESLA_DATADRIVE/"
    print("load architecture",time.time() - start)
    predict()