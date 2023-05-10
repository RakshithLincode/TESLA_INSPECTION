from common.utils import MongoHelper
from livis import settings
from bson import ObjectId
import datetime


def strToDate(date_str):
    date_object =  datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    return date_object

def add_plan(data):
    """
    Input
        {
        "start_time" : "1997-12-02",
        "end_time" : "1998-01-02",
        "part_number" : "aaserer3423",
        "planned_production_count" : 100 
        }    
    """
    try:
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        part_number = data.get('part_number')
        part_id = data.get('part_id')

        planned_production_count = data.get('planned_production_count')
        is_deleted = False

        mp = MongoHelper().getCollection(settings.PLAN_COLLECTION)

        collection_obj = {
            'start_time' : start_time,
            'end_time' : end_time,
            'part_number' : part_number,
            'part_id':part_id,
            'is_deleted' : is_deleted,
            'planned_production_count' : planned_production_count
        }

        _id = mp.insert(collection_obj)    
        return mp.find_one({'_id' : _id})
    except Exception as e:
        return "Could not add plan: "+str(e)

def update_plan(data):
    """
    Input
        {
        "_id":"5f2d3183bdcd9e81e1690f3f",
        "planned_production_count" : 10532 
        }    
    """
    _id = data.get('_id')
    if _id:
        mp = MongoHelper().getCollection(settings.PLAN_COLLECTION)
        sc = mp.find_one({'_id' : ObjectId(_id)})
        if sc:
            sc['planned_production_count'] = data.get('planned_production_count')
            mp.update({'_id' : sc['_id']}, {'$set' :  sc})
            resp = mp.find_one({'_id' : sc['_id']})
            return resp
        else:
            return {"message" : "Plan not found"}
    else:
        return {"message" : "Please enter the plan ID."}


def delete_plan(plan_id):  
    """
    method: http://localhost:8000/livis/v1/plan/delete_plan/5f2d3183bdcd9e81e1690f3f
    """
    _id = plan_id
    if _id:    
        mp = MongoHelper().getCollection(settings.PLAN_COLLECTION)
        sc = mp.find_one({'_id' : ObjectId(_id)})
        if sc:
            sc['is_deleted'] = True
            mp.update({'_id' : sc['_id']}, {'$set' :  sc})
            resp =  mp.find_one({'_id' : sc['_id']})
            return resp
        else:
            return {"message" : "Plan not found"}
    else:
        return {"message" : "Please enter the plan ID."}


def plan_list(skip, limit):
    mp = MongoHelper().getCollection(settings.PLAN_COLLECTION)
    resp = [p for p in mp.find({"$and" : [{"is_deleted": False}, { "is_deleted" : {"$exists" : True}}]}).skip(skip).limit(limit)]
    #if len(resp)>0:

    #    for r in resp:
    #        mp = MongoHelper().getCollection(settings.PARTS_COLLECTION)
    #        part_id = r['part_number']

    #        res = [p for p in mp.find({'part_id':part_id}) ]
    #        part_number = res['part_number']
    
    if resp:
        return resp
    else:
        return []
        

def plan_single(plan_id):
    _id = plan_id
    resp = {}
    if _id:
        _id = ObjectId(_id)
        mp = MongoHelper().getCollection(settings.PLAN_COLLECTION)
        resp = mp.find_one({'_id' : _id})
        if resp:
            return resp
        else:
            return {"message" : "Plan not found"}
    else:
        return {"message" : "Please enter the plan ID."}


def get_todays_planned_production_util(part_id):
    current_date = str(datetime.date.today())
    mp = MongoHelper().getCollection(settings.PLAN_COLLECTION)
    obj = mp.find_one({"$and" : [{"part_number": part_id}, {"start_time": {"$lte": current_date}}, {"end_time": {"$gte": current_date}}]})
    if obj:
        resp = obj
        return resp
    else:
        resp = {"message" : "Today's planned production details not found."}
        return resp

