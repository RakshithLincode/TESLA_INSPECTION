from common.utils import MongoHelper
from livis.settings import *
from bson import ObjectId
import datetime


def strToDate(time_str):
    time_object = datetime.datetime.strptime(time_str, '%H:%M:%S')
    return time_object

def add_shift(data):
    shift_name = data.get('shift_name')
    start_time = strToDate(data.get('start_time'))
    end_time = strToDate(data.get('end_time'))
    status = data.get('status')


    mp = MongoHelper().getCollection('shifts')
    collection_obj = {
        'shift_name' : shift_name,
        'start_time' : str(start_time.time()),
        'end_time' : str(end_time.time()),
        'is_deleted' : False,
        'status':status
        
    }
    _id = mp.insert(collection_obj)    
    return mp.find_one({'_id' : _id})

def update_shift(data):
    _id = data.get('_id')
    resp = {}
    if _id:
        shift_name = data.get('shift_name')
        start_time = strToDate(data.get('start_time'))
        end_time = strToDate(data.get('end_time'))
        status = data.get('status')
        

        mp = MongoHelper().getCollection('shifts')
        sc = mp.find_one({'_id' : ObjectId(_id)})
        if shift_name:
            sc['shift_name'] = shift_name
        if start_time:
            sc['start_time'] = str(start_time.time())
        if end_time:
            sc['end_time'] = str(end_time.time())
        if status:
            sc['status'] = status

        mp.update({'_id' : sc['_id']}, {'$set' :  sc})
        resp = mp.find_one({'_id' : sc['_id']})
    return resp

def delete_shift(shift_id):  
    _id = shift_id
    resp = {}
    if _id:    
        mp = MongoHelper().getCollection('shifts')
        sc = mp.find_one({'_id' : ObjectId(_id)})
        sc['is_deleted'] = True
        mp.update({'_id' : sc['_id']}, {'$set' :  sc})
        resp =  mp.find_one({'_id' : sc['_id']})
    return resp

def shift_list(skip, limit):
    mp = MongoHelper().getCollection('shifts')
    resp = [p for p in mp.find({"$and" : [{"is_deleted": False}, { "is_deleted" : {"$exists" : True}}]}).skip(skip).limit(limit)]
    print("----resp:",resp)
    return resp

def shift_single(shift_id):
    """
    request:   http://127.0.0.1:8000/livis/v1/shifts/get_shift/5f0e8226578a96b642f556a1
    """
    _id = shift_id
    resp = {}
    if _id:
        _id = ObjectId(_id)
        mp = MongoHelper().getCollection('shifts')
        resp = mp.find_one({'_id' : _id})
    return resp
