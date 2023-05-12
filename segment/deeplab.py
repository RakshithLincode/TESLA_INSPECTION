import torch
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
import segmentation_models_pytorch as smp
import albumentations as album
from torch.utils.data import DataLoader
import torch.nn as nn
import torch
import os
import numpy as np
import warnings
warnings.filterwarnings("ignore")
sys.path.insert(0,"C:/DEMO/Tesla_Tyre/TESLA_INSPECTION/")
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

class_dict = {
    'background': [0, 0, 0],
    'gap': [255, 255, 255]
}

class_names = list(class_dict.keys())
class_rgb_values = list(class_dict.values())

print('All dataset classes and their corresponding RGB values in labels:')
print('Class Names: ', class_names)
print('Class RGB values: ', class_rgb_values)

select_classes = ['background', 'gap']

select_class_indices = [class_names.index(
    cls.lower()) for cls in select_classes]
select_class_rgb_values = np.array(class_rgb_values)[select_class_indices]

print('Selected classes and their corresponding RGB values in labels:')
print('Class Names: ', select_classes)
print('Class RGB values: ', select_class_rgb_values)

def one_hot_encode(label, label_values):
    semantic_map = []
    for colour in label_values:
        equality = np.equal(label, colour)
        class_map = np.all(equality, axis=-1)
        semantic_map.append(class_map)
    semantic_map = np.stack(semantic_map, axis=-1)
    return semantic_map

def reverse_one_hot(image):
    x = np.argmax(image, axis=-1)
    return x

def colour_code_segmentation(image, label_values):
    colour_codes = np.array(label_values)
    x = colour_codes[image.astype(int)]
    return x

def get_training_augmentation():
    train_transform = [
        album.Resize(height=544, width=960, always_apply=True),
        album.OneOf(
            [
                # album.HorizontalFlip(p=1),
                # album.VerticalFlip(p=1),
                # album.RandomRotate90(p=1),
            ],
            p=0.75,
        ),
    ]
    return album.Compose(train_transform)

def get_validation_augmentation():
    test_transform = [
        album.Resize(height=544, width=960, always_apply=True),
    ]
    return album.Compose(test_transform)

def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype('float32')

def get_preprocessing(preprocessing_fn=None):
    _transform = []
    if preprocessing_fn:
        _transform.append(album.Lambda(image=preprocessing_fn))
    _transform.append(album.Lambda(image=to_tensor, mask=to_tensor))
    return album.Compose(_transform)


ENCODER = 'resnet50'
ENCODER_WEIGHTS = 'imagenet'
CLASSES = class_names
ACTIVATION = 'sigmoid'

model = smp.DeepLabV3Plus(
    encoder_name=ENCODER,
    encoder_weights=ENCODER_WEIGHTS,
    classes=len(CLASSES),
    activation=ACTIVATION,
)

preprocessing_fn = smp.encoders.get_preprocessing_fn(ENCODER, ENCODER_WEIGHTS)

def get_validation_augmentation():
    test_transform = [
        album.Resize(height=544, width=960, always_apply=True),
    ]
    return album.Compose(test_transform)

def builddataset(images, augmentation=None, preprocessing=None):
    image = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
    if augmentation:
        sample = augmentation(image=image)
        image = sample['image']
    if preprocessing:
        sample = preprocessing(image=image)
        image = sample['image']
    return image

def get_measurment(point):
	calibration_mm = 6.5
	calibration_px = 7.0
	pts1 = point[0]  
	pts2 = point[1]  
	calibration_mm_per_px = calibration_mm / calibration_px
	result = ((pts2[0] - pts1[0])**2 + (pts2[1] - pts1[1])**2)**0.5
	dis = result*calibration_mm_per_px
	dis = str(dis)[0:3]
	print(result , 'resulsssssssssssssssssssssssssssssssss')
	print(result*calibration_mm_per_px , 'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
	return dis

# def get_measurment(point):
#     pixel_to_mm = 0.1 
#     point1 = point[0]  
#     point2 = point[1]  
#     point1_mm = (point1[0] * pixel_to_mm, point1[1] * pixel_to_mm)
#     point2_mm = (point2[0] * pixel_to_mm, point2[1] * pixel_to_mm)
#     distance_mm = ((point2_mm[0] - point1_mm[0])**2 + (point2_mm[1] - point1_mm[1])**2)**0.5
#     mm = str(distance_mm)[0:3]
#     return mm

def get_width_measure(original , img):
    try:
        values = []
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
        contours,hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
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
                values.append(mm)
                cv2.putText(original,str(mm + '_mm'), (right_px + 10,row_num), font, fontScale,fontColor,lineType)
        min_mm = min(values)
        max_mm = max(values) 
        cv2.putText(original, "Min Value length : "+str(min_mm) + '_mm', (50,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
        cv2.putText(original,  "Max Value length : "+str(max_mm) + '_mm', (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)       
        return original
    except Exception as e:
        print(e,'errorrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        return original
    
def model_predict(image):
    import time
    worker_start = time.time()
    h,w,c =image.shape
    image = builddataset(image, augmentation=get_validation_augmentation(), preprocessing=get_preprocessing(preprocessing_fn))
    x_tensor = torch.from_numpy(image).to(DEVICE).unsqueeze(0)
    pred_mask = best_model(x_tensor)
    pred_mask = pred_mask.detach().squeeze().cpu().numpy()
    pred_mask = np.transpose(pred_mask, (1, 2, 0))
    pred_building_heatmap = pred_mask[:, :, select_classes.index('gap')]
    pred_mask = colour_code_segmentation(
        reverse_one_hot(pred_mask), select_class_rgb_values)
    print((pred_mask.shape))
    pred_mask = np.clip(pred_mask, 0, 255)
    pred_mask = pred_mask.astype(np.uint8)
    pred_mask = cv2.resize(pred_mask,(w,h))  
    cv2.imwrite('image.png',pred_mask)    
    print("TIME TAKEN BY MODEL TO PREDICT MASK :::::::::::::::::::::::::::::::::::::::::::::",time.time() - worker_start)    
    return pred_mask    

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
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    best_model = torch.load('C:/DEMO/Tesla_Tyre/TESLA_INSPECTION/segment/deeplabv3.pth', map_location=DEVICE)
    print('Loaded DeepLabV3+ model from this run.')
    predict()