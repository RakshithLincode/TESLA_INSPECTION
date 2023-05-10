from kafka.errors import QuotaViolationError
from common.utils import CacheHelper
from django.http import response
import numpy as np
import cv2 
from kafka import KafkaConsumer , TopicPartition
from numpy import array
import json
import base64
import multiprocessing
from kafka import *
import sys
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from livis import settings as settings
from livis.settings import BASE_URL
import os
from common.utils import *

rch = CacheHelper()


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class MongoHelper:
    client = None
    def __init__(self):
        if not self.client:
            self.client = MongoClient(host='localhost', port=27017)

        self.db = self.client[settings.MONGO_DB]
        if settings.DEBUG:
            self.db.set_profiling_level(2)
        # placeholder for filter
    """
    def getDatabase(self):
        return self.db
    """

    def getCollection(self, cname, create=False, codec_options=None):
        _DB = "LIVIS"
        DB = self.client[_DB]
        return DB[cname]


def check_kanban(raw_data, part):
    quick_report = {'reason'  : [], 'defect_camera_index':[]}
    all_detections = []
    #for topic in raw_data:
        #all_detections.extend(raw_data[topic])
    
    mp = MongoHelper().getCollection('kanban')
    kanban = mp.find_one()
    if not kanban:
        kanban = {
        "M5" : {"Good" : ['Screw_Presence', 'M5', 'Screw_Presence', 'A1_220V_50Hz_A2', 'M5', 'Good_Wiring', 'Good_Solder', 'Proper_Bending', 'Proper_Bending', 'Good_Solder', 'Good_Wiring'],
                "Bad" : ["Full_Solder","Improper_Bending","Screw_Absence","Screw_Absence","Plastic_Burnt",
                "Improper_Solder","Extra_Wire","No_Solder","Improper_ocr","Improper_M5", "Wire_Protrusion"]},
        "B5" : {"Good" : ["Good_Winding", "A1_24V_50Hz_A2","Good_Wiring","Proper_Bending","Proper_Solder",
                            "B5","B5","Good_Solder","Good_Wiring","Proper_Bending","Screw_Presence"],
                "Bad" : ["Improper_B5","Improper_OCR","Screw_Absence", "Wire_Protrusion"]},
        "M7" : {"Good" : ["Good_Winding", "A1_220V_50_60Hz_A2","Good_Wiring","Proper_Bending","Proper_Solder","M7","M7","Good_Solder","Good_Wiring","Proper_Bending","Screw_Presence"],
                "Bad" : ["Improper_M7","Improper_OCR","Screw_Absence", "Wire_Protrusion"]},
        }
    counters = {"Good" : 0, "Bad" : 0}
    print("Current PArt: : : : ", part)
    print("FOund classes : : : ",all_detections)

    for topic in raw_data:
        #all_detections.extend(raw_data[topic])
        all_detections = raw_data[topic]
        #print("*******ad"+str(ad))

        for ad in all_detections:
            if ad in kanban[part]["Good"]:
                counters["Good"]+=1
            if ad in kanban[part]['Bad']:
                counters["Bad"] +=1
                quick_report['reason'].append(ad)
                quick_report['status'] = 'Rejected'
                quick_report["defect_camera_index"].append(topic)
            if ad not in kanban[part]["Good"] and ad not in kanban[part]['Bad']:
                quick_report['reason'].append(ad)
                quick_report['status'] = 'Rejected'
                quick_report["defect_camera_index"].append(topic)

    if len(quick_report['reason']) > 0:
        quick_report['status'] = 'Rejected'
        
    else:
        quick_report['status'] = 'Accepted'
    
    return quick_report


#API to save inspection from all cameras.
def save_inspection(data):
    inspection_id = data.get('inspection_id',None)
    coil_number = data.get('coil_number',None)
    config_f = data.get('config', None)
    cwd = "/home/se/DetzoCoil/republic/backend/LIVIS/livis"
    config = json.load(open(os.path.join(cwd,"inspection",config_f)))
    print("Config being used for this request : : : : ", config_f)
    topics = []
    for cam in config['camera_info']:
       topics.append(str(cam['camera_id']))

    mp = MongoHelper().getCollection('inspection')
    pr = mp.find_one({'_id' : ObjectId(inspection_id)})
    part_name = "M5"
    if pr:
        part_name = pr['part_name'] if 'part_name' in pr else "M7"

    if part_name == None:
        part_name = "M5"
    quick_report = {}
    raw_data = {}
    qr_code = ""
    for topic in topics:
        res = get_data_feed(topic)
        raw_data[topic] = res
        print("GOT DATA FOR TOPIC : ", res)
        for i in res:
             if i.find("qr_code:")>-1:
                 key_ = i
                 code = key_.split(":")
                 original = code[0]
                 qr_code = code[1]
                 res.remove(key_)
                 res.append(qr_code)
    quick_report = check_kanban(raw_data, part_name)
    ps = MongoHelper().getCollection(str(inspection_id))
    print("-----------------Save inspection ID--------------------------",str(inspection_id))
    quick_report['time_stamp'] = str(datetime.datetime.now().replace(microsecond=0))
    #save images
    quick_report["inspection_id"] = inspection_id
    quick_report['inference_images'] = []
    quick_report['coil_number'] = coil_number
    quick_report['remark'] = ""
    quick_report['qr_code'] = qr_code
    for topic in topics:
        print("LOOKING FOR TOPIC : : ", topic)
        print(quick_report)
        imgs = get_single_frame(topic)
        print('**********************TOPIC:',topic,'\tImage Shape:',imgs.shape)
        fname = "/home/se/DetzoCoil/republic/backend/LIVIS/livis/data/" + str(ObjectId())+'.jpg'
        print("Writing imgae ,",fname, cv2.imwrite(fname, imgs))
        quick_report['inference_images'].append("http://127.0.0.1:8000/livis/data/" + str(ObjectId())+'.jpg')
    mongo_id = ps.insert_one(quick_report)
    quick_report['_id'] = str(quick_report['_id'])
    print("quick_report-----------------",quick_report)
    print("Sub inspection ID", str(mongo_id.inserted_id))
    CacheHelper().set_json({"detzo" : str(mongo_id.inserted_id)})
    return quick_report


def get_data_feed(topic):
    print("Topic : : ", topic, "_____ ")
    topic= str(topic)+str("_taco")
    b= CacheHelper().get_json(topic)
    result = b
    return result


def get_single_frame(topic):
    topic_inference_feed = str(topic)+str("_inference")
    frame = CacheHelper().get_json(topic)
    frame = frame['frame']
    im_b64 = bytes(frame[2:], 'utf-8')
    im_binary = base64.b64decode(im_b64)
    im_arr = np.frombuffer(im_binary, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    print("GOT IMAGE OF SHAPE : ", img.shape)
    return img


def create_urls_from_camera(camera_id, BASE_URL):
    fmt_url = BASE_URL + '/livis/v1/inspection/get_output_stream/{}/' 
    return fmt_url.format(camera_id)


def get_running_process_utils():
    mp = MongoHelper().getCollection('inspection')
    insp_coll = [i for i in mp.find({"status":"started"})]
    inspection_id = ""
    response = {}
    if len(insp_coll) > 0:
        res = insp_coll[-1]
        response["inspection_id"] = str(res['_id'])
        response["part_name"] = res["part_name"]
        response["part_id"] = res["part_id"]
        print("*****************Running process inspection_id*********************",inspection_id)
    return response,200


def start_process_util(data):
    part_id = data.get('part_id',None)
    part_name = data.get('part_name',None)
    operator_id = data.get('operator_id')
    
    mp = MongoHelper().getCollection('shifts')
    import time
    #import datetime
    time_now = str(datetime.datetime.now().time()).split('.')[0]
    shift_coll = [i for i in mp.find({ "$and" : [ {"status": True}, { "status" : {"$exists" : True}}\
    ,{"start_time": {"$lte": time_now}}, {"end_time": {"$gte": time_now}} ] })]
    if len(shift_coll) == 0:
        return "no shift at this time of the day, please come back during inspection time",400
    shift_id = str(shift_coll[0]["_id"])
    mp = MongoHelper().getCollection('inspection')
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    createdAt = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    coll = {
    "part_id":part_id,
    "part_name":part_name,
    "start_time":createdAt,
    "end_time":"",
    "shift_id":shift_id,
    "operator_id":operator_id,
    "produced_on":current_date,
    "status":"started",
    }
    curr_insp_id = mp.insert_one(coll)
    bb = MongoHelper().getCollection('current_inspection')
    ps = bb.find_one()
    if ps is None:
        bb.insert_one({'current_inspection_id' : curr_insp_id.inserted_id})
    else:
        ps['current_inspection_id'] = curr_insp_id.inserted_id
        bb.update({"_id" : ps['_id']}, {"$set" : ps})
    print("curr_insp_id.inserted_id",curr_insp_id.inserted_id)
    return "Success" ,200


def end_process_util(data):
    inspection_id  = data.get('inspection_id', None)
    if inspection_id is None:
        return "Failed", 200
    mp = MongoHelper().getCollection('inspection')
    ps = mp.find_one({'_id' : ObjectId(inspection_id)})
    current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ending = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    ps["end_time"] = ending
    ps["status"] = "completed"

    mp.update({'_id' : ps['_id']}, {"$set" : ps})

    bb = MongoHelper().getCollection('current_inspection')
    ps = bb.find_one()
    if ps is None:
        bb.insert_one({'current_inspection_id' : None})
    else:
        ps['current_inspection_id'] = None
        bb.update({"_id" : ps['_id']}, {"$set" : ps})
    return "Success" ,200


def get_defect_list(inspectionid):
    mp = MongoHelper().getCollection(inspectionid)
    list_ = [i for i in mp.find()]
    
    result =  { "quick_report" : {
            "coil_1" : {
                "total" : 0,
                "accepted" : 0,
                "rejected" : 0

            },
            "coil_2" : {
                "total" : 0,
                "accepted" : 0,
                "rejected" : 0

            },},

        "current_inspection_report" : 
            {
                "coil_1" : {
                    "_id" : 1,
                    "status" :"", 
                    "reason" : ["string1", "string2"]
                },
                "coil_2" : {
                    "_id" : 1, 
                    "status" : "",
                    "reason" : ["string1", "string2"]
                },
        
            }
    }
    last_coil_1 = None
    last_coil_2 = None
    for p in list_:
        if p['coil_number'] == "1":
            last_coil_1 = p
            if p['status'] == 'Accepted':
                result["quick_report"]['coil_1']['accepted']+=1
            if p['status'] == 'Rejected':
                result["quick_report"]['coil_1']['rejected']+=1
            if not p['status']:
                result["quick_report"]['coil_1']['total']+=0
            else:
                result["quick_report"]['coil_1']['total']+=1
            reasons = ""
            for i in p['reason']:
                reasons = reasons +str(i)+" , "
            p['reason'] = reasons
            last_coil_1 = p
            

        elif p['coil_number'] == "2":
            last_coil_2 = p
            if p['status'] == 'Accepted':
                result["quick_report"]['coil_2']['accepted']+=1
            if p['status'] == 'Rejected':
                result["quick_report"]['coil_2']['rejected']+=1
            if not p['status']:
                result["quick_report"]['coil_2']['total']+=0
            else:
                result["quick_report"]['coil_2']['total']+=1
            reasons = ""
            for i in p['reason']:
                reasons = reasons +str(i)+" , "
            p['reason'] = reasons
            last_coil_2 = p

    if last_coil_1:
        last_coil_1["_id"] = str(last_coil_1["_id"])
        last_coil_1['time_stamp'] = str(last_coil_1['time_stamp'])
    if last_coil_2:
        last_coil_2["_id"] = str(last_coil_2["_id"])
        last_coil_2['time_stamp'] = str(last_coil_2['time_stamp'])

    result["current_inspection_report"]["coil_1"] = last_coil_1
    result["current_inspection_report"]["coil_2"] = last_coil_2
    return result

def get_inference_feed(topic):
    topic_inference_feed = str(topic)+str("_inference")
    consumer = KafkaConsumer(bootstrap_servers="127.0.0.1:9092")
    tp = TopicPartition(topic_inference_feed,0)
    consumer.assign([tp])
    consumer.seek_to_end(tp)
    last_offset = consumer.position(tp)
    while True:
    
        v = CacheHelper().get_json(topic_inference_feed)
        im_b64_str = v["frame"]
        im_b64 = bytes(im_b64_str[2:], 'utf-8')
        
        im_binary = base64.b64decode(im_b64)
        

        im_arr = np.frombuffer(im_binary, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
           

        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: i
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')