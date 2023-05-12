import torch
import numpy as np
import cv2 
import glob
import cv2
import torch
import requests
import time
import numpy as np
# from mongohelper import MongoHelper
import os
import copy
import bson
import gc
import sys
import redis
import pickle
import warnings
warnings.warn('my warning')
from pymongo import MongoClient
from ai_settings import *
sys.path.insert(0,"C:/DEMO/Tesla_Tyre/TESLA_INSPECTION/")
from inference_module import *
from config_module import *
torch.cuda.empty_cache()
gc.collect()
predictor = Inference()

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

def get_cords(img):
    try:
        cords = []
        four_points = []
        results_img = copy.copy(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img_bw = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(img_bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        ref = np.zeros_like(img_bw)
        cv2.drawContours(ref, contours, 0, 255, 1)
        M = cv2.moments(contours[0])
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])
        width = img.shape[1]
        height = img.shape[0]
        N = 20
        for i in range(N):
            tmp = np.zeros_like(img_bw)
            theta = i*(360/N)
            theta *= np.pi/180.0
            cv2.line(tmp, (centroid_x, centroid_y),
                    (int(centroid_x+np.cos(theta)*width),
                        int(centroid_y-np.sin(theta)*height)), 255, 5)
            (row,col) = np.nonzero(np.logical_and(tmp, ref))
            cords.append((col[0],row[0]))
            cv2.line(results_img, (centroid_x, centroid_y), (col[0],row[0]), (0,0,255), 1)
        N = 4
        for i in range(N):
            tmp = np.zeros_like(img_bw)
            theta = i*(360/N)
            theta *= np.pi/180.0
            cv2.line(tmp, (centroid_x, centroid_y),
                    (int(centroid_x+np.cos(theta)*width),
                        int(centroid_y-np.sin(theta)*height)), 255, 5)
            (row,col) = np.nonzero(np.logical_and(tmp, ref))
            four_points.append((col[0],row[0]))    
        return results_img ,cords ,four_points
    except:
        return results_img ,None ,None
        

def get_distance(pts1, pts2, calib_mm_per_pixel):
    dist_pixels = ((pts2[0] - pts1[0])**2 + (pts2[1] - pts1[1])**2)**0.5
    dist_cm = dist_pixels * calib_mm_per_pixel / 5.0
    return dist_cm

def draw_line(original_image,inner_cord,outer_cord):
    try:
        dist = []
        for inner,outter in zip(inner_cord,outer_cord):
            calib_mm_per_pixel = 0.1 
            dist_cm = get_distance(inner, outter, calib_mm_per_pixel)
            # distance = round((get_distance(inner,outter)/10),1)
            dist.append(dist_cm)
        for cord,dis in zip(inner_cord,dist):
            xy = np.array(outer_cord).T
            d = ( (xy[0] - cord[0]) ** 2 + (xy[1] - cord[1]) ** 2) ** 0.5
            closest_idx = np.argmin(d)
            closest = outer_cord[closest_idx]
            cv2.line(original_image, cord, closest, (255, 0, 0), 2)
            dis = str(dis * 10) 
            dis = dis[0:3]
            cv2.putText(original_image, dis +'_cm', closest, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5,(0, 0, 255), 1)
        return original_image 
    except:
        return original_image 

def draw_circle(original_image,outer_four_points,inner_four_points):
    try:
        cx = sum([p[0] for p in outer_four_points]) / len(outer_four_points)
        cy = sum([p[1] for p in outer_four_points]) / len(outer_four_points)
        centroid = (cx, cy)
        distances = [np.sqrt((p[0]-cx)**2 + (p[1]-cy)**2) for p in outer_four_points]
        radius = int(sum(distances) / len(distances))
        cv2.circle(original_image, (int(centroid[0]),int(centroid[1])), radius, (0,255,0), thickness=2)
        cx = sum([p[0] for p in inner_four_points]) / len(inner_four_points)
        cy = sum([p[1] for p in inner_four_points]) / len(inner_four_points)
        centroid = (cx, cy)
        distances = [np.sqrt((p[0]-cx)**2 + (p[1]-cy)**2) for p in inner_four_points]
        radius = int(sum(distances) / len(distances))
        cv2.circle(original_image, (int(centroid[0]),int(centroid[1])), radius, (0,255,0), thickness=2)
        return original_image
    except:
        return original_image 

def draw_ellipse(original_image,outer_four_points,inner_four_points):
    cx = sum([p[0] for p in outer_four_points]) / len(outer_four_points)
    cy = sum([p[1] for p in outer_four_points]) / len(outer_four_points)
    centroid = (cx, cy)
    distances = [np.sqrt((p[0]-cx)**2 + (p[1]-cy)**2) for p in outer_four_points]
    major_axis = max(distances)
    minor_axis = min(distances)
    color = (0,255,0)
    thickness = 2
    angle = 0
    startAngle = 0
    endAngle = 360
    axes = (int(major_axis), int(minor_axis))
    cv2.ellipse(original_image, (int(centroid[0]),int(centroid[1])), axes, angle, startAngle, endAngle, color, thickness)
    cx = sum([p[0] for p in inner_four_points]) / len(inner_four_points)
    cy = sum([p[1] for p in inner_four_points]) / len(inner_four_points)
    centroid = (cx, cy)
    distances = [np.sqrt((p[0]-cx)**2 + (p[1]-cy)**2) for p in inner_four_points]
    major_axis = max(distances)
    minor_axis = min(distances)
    axes = (int(major_axis), int(minor_axis))
    cv2.ellipse(original_image, (int(centroid[0]),int(centroid[1])), axes, angle, startAngle, endAngle, color, thickness)
    return original_image


def pre_process(original_image,mask):
    try:
        mask_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        h,w,c = mask_image.shape
        gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
        contours, hier = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
        largest_item= sorted_contours[0]
        sorted_contours= sorted(contours, key=cv2.contourArea, reverse= False)
        smallest_item= sorted_contours[0]
        outer_line = np.ones((h,w,3), np.uint8)
        inner_line = np.ones((h,w,3), np.uint8) 
        if cv2.contourArea(largest_item) > 50000 and cv2.contourArea(largest_item) > 50000 :
            x,y,w,h = cv2.boundingRect(smallest_item)
            cv2.polylines(original_image, [largest_item],True, (0,255,0), 2)
            cv2.polylines(original_image, [smallest_item],True, (0,255,0), 2)
            cv2.polylines(outer_line, [largest_item],True, (255,255,255), 1)
            cv2.polylines(inner_line, [smallest_item],True, (255,255,255), 1)
        outer_line,outer_cord,outer_four_points = get_cords(outer_line)
        inner_line,inner_cord,inner_four_points = get_cords(inner_line)
        # original_image = draw_circle(original_image,outer_four_points,inner_four_points)
        cv2.imwrite('image.png',original_image)    
        original_image = draw_line(original_image,inner_cord,outer_cord)
        return original_image
    except:
        return original_image


# vid = cv2.VideoCapture('lf.mp4')
# while(True):
#     ret, frame = vid.read()
#     mask_input_frame = copy.copy(frame)
#     input_frmae = copy.copy(frame)
#     predictor.mask_input_frame  = mask_input_frame
#     masks = predictor.mask_dummy()
#     worker_start = time.time()
#     original_image = pre_process(mask_input_frame,masks)
#     original_image = cv2.resize(original_image,(640,480))
#     input_frame_resize = cv2.resize(frame,(640,480))
#     print("TIME TAKEN BY WORKER  :::::::::::::::::::::::::::::::::::::::::::::",time.time() - worker_start)    
#     cv2.imshow('original',input_frame_resize)
#     cv2.imshow('original_image', original_image)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
  
# vid.release()
# cv2.destroyAllWindows()

def predict():
        while 1:
            vid = cv2.VideoCapture(0)        
            while(True):
                ret, frame = vid.read()
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
                # print(trigger)
                # if trigger == True:
                worker_start = time.time()
                select_model = CacheHelper().get_json('current_part_name')
                print(select_model,'select_model..................................................................')
                part_name = select_model
                mask_input_frame = copy.copy(frame)
                input_frmae = copy.copy(frame)
                predictor.mask_input_frame  = mask_input_frame
                masks = predictor.mask_dummy()
                worker_start = time.time()
                original_image = pre_process(mask_input_frame,masks)      
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