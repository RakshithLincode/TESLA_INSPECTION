from common.utils import *
#from django.utils import timezone
import datetime
from bson import ObjectId
# from indo.kanban import static_kanban
from livis.settings import *
# from plan.utils import *
import cv2
from accounts.utils import get_user_account_util
# from indo.common_utils import *
from dateutil import tz


def create_process_collection(c_name):
    pc = MongoHelper().createCollection(c_name)
    print("Process collection >>>>>>",pc)
    return pc
"""
{
    "user_id":"user_1"
    "shift":"shift_1"
    "workstation_id":"12423"
}
"""
def start_indo_process(data):
    # part_number = data.get('part_number',None)
    user_id = data.get('user_id')
    shift = data.get('shift')
    workstation_id = data.get('workstation_id')
    # user = { "user_id": user_id,
    #             "role": user_details['role_name'],
    #             "name": (user_details['first_name']+" "+user_details['last_name'])
    #         }
    #print("user:::: ",user)
    createdAt = str(datetime.datetime.now(tz=tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S"))#datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    mp = MongoHelper().getCollection('inspection_summary')
    print(mp , "inside  start indo processs!!!!!")
    obj = {
        'start_time' : createdAt,
        'user_id' : user_id,
        "workstation_id" : workstation_id,
        "status" : "started",
        "end_time" : "",
        "total_accepted_parts": 0,
        "total_rejected_parts": 0,
        "total_parts": 0,
        "shift" : shift
    }
    # set_kanban_on_redis(workstation_id, short_number) 
    _id = mp.insert(obj)
    print(_id ,obj)
    try:
        # my_col = mp[(str(_id))]
        my_col = create_process_collection(str(_id))
        print("collection create",str(_id) , my_col)
    except Exception as e:
        print(e)
        pass
    resp = mp.find_one({"_id" : _id})
    return resp


def end_indo_process(data):
    # part_number = data.get('part_number',None)
    mp = MongoHelper().getCollection('inspection_summary')
    run_process = mp.find_one({"status" : "started"})

    _id = run_process["_id"]
    
    pr = mp.find_one({"_id" : ObjectId(_id)})
    print(run_process , _id ,"inside end_indo_process!!")
    metrics = get_metrics_util(inspection_id = str(_id))
    print(metrics)
    # for i in pr :
    #     print(i)
    completedAt = str(datetime.datetime.now(tz=tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S"))#datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    if bool(pr):
        pr["end_time"] = completedAt
        pr["status"] = "completed"
        pr["total_accepted_parts"] = metrics["accepted"]
        pr["total_rejected_parts"] = metrics["rejected"]
        pr["total_parts"] = metrics["total"]
        # obj = {
        #     'start_time' : createdAt,
        #     'user_id' : user_id,
        #     "workstation_id" : workstation_id,
        #     "status" : completed,
        #     "end_time" : "",
        #     "total_accepted_parts": 0,
        #     "total_rejected_parts": 0,
        #     "total_parts": 0,
        #     "shift" : shift
        # }
        # set_kanban_on_redis(workstation_id, short_number) 
        # _id = mp.insert(obj)
        mp.update({'_id' : pr['_id']}, {'$set' : pr})
        resp = mp.find_one({"_id" : _id})
        if resp:
            return resp
    else:
        return {}

"""
{"inspection_id" : "6073f41fd02caf270a168cc3"}
"""
def get_metrics_util(inspection_id):
    print("inside get_metric" ,inspection_id)
    # inspection_id = data.get("inspection_id")
    mp = MongoHelper().getCollection(INSPECTION_DATA_COLLECTION)
    pr = mp.find_one({"_id" : ObjectId(inspection_id)})
    print(pr)
    if pr:

        inspection = MongoHelper().getCollection(inspection_id)
        total = inspection.count()
        total_accepted = inspection.find({'is_accepted' : True}).count()
        total_rejected = inspection.find({'is_accepted' : False}).count()#total - total_accepted
        # qc_inspection = get_inspection_qc_list(inspection_id)
        print(f"total : {total} ,total_accepted :{total_accepted}, total_rejected :{total_rejected}")
        resp = {
            "accepted" : total_accepted,
            "rejected" : total_rejected,
            "total" : total,

        }
        return resp

    else:
        return {}

def get_indo_running_process():
    mp = MongoHelper().getCollection('inspection_summary')
    run_process = mp.find_one({"status" : "started"})

    resp = run_process
    if resp :
        return resp
    else :
        {}

def get_workstation_details():
    mp = MongoHelper().getCollection('workstation')
    resp = mp.find_one({"workstation_name" : "WS_01"})
    print(resp)
    return resp

def get_camera_details():
    w = get_workstation_details()
    camera_details = w["cameras"]
    return camera_details

def get_camera_feed_urls_util():
    feed_urls = []
    # workstation_info = RedisKeyBuilderServer(workstation_id).workstation_info
    camera_info = get_camera_details()
    for camera in camera_info:
        url = "http://localhost:8000/livis/v1/indo/stream/{}/".format("WS_01"+"_"+str(camera['camera_id'])+"_predicted_frame")
        feed_urls.append(url)
    return feed_urls

def redis_camera(key):
    rch = CacheHelper()
    while True:
        frame1 = rch.get_json(key)
        # print("KEY :      : :: :  : : : : :" , key )
        # print(frame1.shape)
        ret, jpeg = cv2.imencode('.jpg', frame1)
        frame =  jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')