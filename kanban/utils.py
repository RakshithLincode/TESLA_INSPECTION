from django.utils import timezone
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
def create_kanban_util(data):
        try:
            kanban_name = data['kanban_name']
        except:
            message = "kanban name not provided"
            status_code = 400
            return message, status_code

        try:
            kanban_description = data['kanban_description']
        except:
            message = "kanban description not provided"
            status_code = 400
            return message, status_code
        
        mp = MongoHelper().getCollection('kanban_collection')

        ### Logic to check if kanban already exists
        if mp.find_one({"$and":[{"kanban_name":kanban_name},{"isdeleted":False}]}):
            status_code = 400
            message = "kanban already exists"
            return message, status_code


        isdeleted = False
        # mp = MongoHelper().getCollection(KANBAN_COLLECTION)
        

        collection_obj = {
       	    'kanban_name' : kanban_name,
       	    'kanban_description' : kanban_description,
       	    'isdeleted' : isdeleted,
       	    'created_at': timezone.now(),
       	    'modified_at': timezone.now()}
       	_id = mp.insert(collection_obj)
       	status_code = 200
       	message = "Added new feature to kanban"
       	return message, status_code


def get_all_kanban_util():
        mp = MongoHelper().getCollection('kanban_collection')
        kanbans = [p for p in mp.find({"isdeleted":False})]
        if kanbans:
            return kanbans
        else:
            return []


def get_single_kanban_util(id):
        kanban_id = id
        _id = ObjectId(kanban_id)
        mp = MongoHelper().getCollection('kanban_collection')
        p = mp.find_one({'_id' : _id})
        
        if p:
            return p
        else:
            return {}


def update_kanban_util(data):
        print(data)
        try:
            kanban_name = data['kanban_name']
        except:
            message = "kanban name not provided"
            status_code = 400
            return message, status_code

        try:
            kanban_description = data['kanban_description']
        except:
            message = "kanban description not provided"
            status_code = 400
            return message, status_code
        
        try:
            kanban_id = data['_id']
        except:
            message = "kanban id not provided"
            status_code = 400
            return message, status_code
        modified_at = timezone.now()
        _id = kanban_id
        mp = MongoHelper().getCollection('kanban_collection')
        kb = mp.find_one({'_id' : ObjectId(_id)})
        kb['kanban_name'] = kanban_name
        kb['kanban_description'] = kanban_description
        kb['modified_at'] = timezone.now()
        mp.update({'_id' : kb['_id']}, {'$set' :  kb})
        status_code = 200
        message = "Success"
        return message, status_code


####DELETE
def delete_kanban_util(kanban_id):
        _id = kanban_id
        mp = MongoHelper().getCollection('kanban_collection')
        kb = mp.find_one({'_id' : ObjectId(_id)})
        isdeleted = kb.get('isdeleted')
        if not isdeleted:
            kb['isdeleted'] = True
        mp.update({'_id' : kb['_id']}, {'$set' :  kb})
        status_code = 200
        message = "Success"
        return message, status_code
