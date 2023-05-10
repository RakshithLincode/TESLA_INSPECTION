from regex import P
from common.utils import *
from bson import ObjectId
from livis.settings import *
from django.utils import timezone
from pymongo import MongoClient
from csv import DictWriter
from datetime import date, datetime


class Encoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ObjectId):
			return str(obj)
		if isinstance(obj, datetime.datetime):
			return obj.isoformat()
		else:
			return obj


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
		_DB = "DEMO"
		DB = self.client[_DB]
		return DB[cname]


def sort_time(val):
	return sorted(val,key=lambda k: k['time_stamp'])

def convert_dict(dict):
	dict['reject_reason'] = {"defects":dict['defects'],
	"features":dict['feature_mismatch'],
	"angle":dict['label_angle']}
	dict['inference_start_time'] = dict['time_stamp']
	dict['captured_inference_frame'] = dict['inference_frame']
	dict['captured_original_frame'] = dict['input_frame']
	# dict['captured_mask_frame'] = dict['mask_frame']
	# dict['captured_measure_frame'] = dict['measure_frame']
	if dict.get('part_name'):
		mp = MongoHelper().getCollection("parts")
		for x in mp.find():
			if x['select_model'] == dict.get('part_name'):
				dict['feature_list'] = x.get('features')
				dict['defect_list'] = x.get('defeats')
	if dict.get("inference_start_time"):
		dict.pop("inference_start_time")
	if dict.get("inference_frame"):
		dict.pop("inference_frame")
	if dict.get("input_frame"):
		dict.pop("input_frame")
	# if dict.get("mask_frame"):
	# 	dict.pop("mask_frame")
	# if dict.get("measure_frame"):
	# 	dict.pop("measure_frame")    
	if dict.get("time_stamp"):
		dict.pop("time_stamp")
	# if dict.get("ocr_barcode_mismatch"):
	# 	dict.pop("ocr_barcode_mismatch")
	if dict.get("label_angle"):
		dict.pop("label_angle")
	# if dict.get("label_to_sealent_measurment"):
	# 	dict.pop("label_to_sealent_measurment")
	if dict.get("status") == 'Rejected':
		dict['isAccepted'] = False
	else:
		dict['isAccepted'] = True
	return dict

def get_mega_report_util(data):

	try:
		from_date = data.get('from_date')
		to_date = data.get('to_date')
		operator_id = data.get('operator_id',None)
		status = data.get('status',None) #pass / fail
		shift_id = data.get('shift_id',None)
		skip = data.get('skip',None)
		limit = data.get('limit',None)
		model = data.get('model',None)
		workstation_id = data.get('workstation_id',None)

		print(from_date,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(to_date,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(operator_id,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(status,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(shift_id,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(skip,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(limit,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(workstation_id,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print(model,'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
		print('hhhhhhhhhhhhhhhhhhhhgggggggggggggggggggggggggfffffffffffffffffffffffffffffffff')

		query = []

		if workstation_id:
			query.append({'workstation_id': workstation_id})
		if operator_id:
			query.append({'operator_id': operator_id })
		if shift_id:
			query.append({'shift_id': shift_id })
		if from_date:
			query.append({'start_time': {"$gte":from_date}})#,"$lte":to_date
		if to_date:
			query.append({'end_time': {"$lte":to_date}})
		if model:
			query.append({'part_name': {"$lte":model}})		
		print('')
		if bool(query):
			inspectionid_collection = MongoHelper().getCollection('inspection')
			print(inspectionid_collection)
			objs = [i for i in inspectionid_collection.find({"$and":query}).sort([( '$natural', -1)]) ]
		else:
			inspectionid_collection = MongoHelper().getCollection('inspection')
			objs = [i for i in inspectionid_collection.find().sort([( '$natural', -1)])]
		p = []
		for ins in objs:
			inspection_id = str(ins['_id'])
			log_coll = MongoHelper().getCollection(str(inspection_id)+"_results")
			if status == "Accepted" or status == "Rejected":
				for i in log_coll.find({'status':status}).sort([( 'time_stamp', -1)]):
					if len(i) == 0:
						pass
					else:
						pr = [convert_dict(i)]
						p.extend(pr) 
			else:
				for i in log_coll.find().sort([( 'time_stamp', -1)]):
					if len(i) == 0:
						pass
					else:
						pr = [convert_dict(i)]
						p.extend(pr) 
		q = []
		if skip is not None and limit is not None:
			for items in p[skip:skip+limit]:
				q.append(items)
		else:
			q = p.copy()
		coll={
			"data":q,
			"total":len(p)
		}
		print(coll,'gggggggggggggggggggggggggggggggh')
		return coll,200
	except Exception as e:
		print(e)
		return "nodata",400    


def set_flag_util(data):
	master_obj_id = data['master_obj_id']
	slave_obj_id = data['slave_obj_id']
	remark = data['remark']

	mp = MongoHelper().getCollection(master_obj_id+"_results")

	process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})

	process_attributes['remark']= remark
	process_attributes['flagged']= True
	#print(process_attributes)
	mp.update({'_id' : ObjectId(slave_obj_id) }, {'$set' :  process_attributes})
	# process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})
	
	#goto annotation and set as untagged
	# part_id = process_attributes['part_id']
	# captured_original_frame_http = process_attributes['captured_original_frame_http']
	# captured_original_frame = process_attributes['captured_original_frame']
	
	# mp = MongoHelper().getCollection(str(part_id)+"_dataset")
	
	# capture_doc = {
	#                     "file_path": captured_original_frame,
	#                     "file_url": captured_original_frame_http,
	#                     "state": "untagged",
	#                     "annotation_detection": [],
	#                     "annotation_detection_history": [],
	#                     "annotation_classification": "",
	#                     "annotation_classification_history": [],
	#                     "annotator": "",
	#                     "date_added":timezone.now()}
	# mp.insert(capture_doc)
	return "success"



def edit_remark_util(data):
	master_obj_id = data['master_obj_id']
	slave_obj_id = data['slave_obj_id']
	remark = data['remarks']

	mp = MongoHelper().getCollection(master_obj_id)

	process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})

	process_attributes['remarks']= remark
	#print(process_attributes)
	mp.update({'_id' : ObjectId(slave_obj_id) }, {'$set' :  process_attributes})
	process_attributes = mp.find_one({'_id' : ObjectId(slave_obj_id)})
	return "success"

def export_csv_util(data):
	from_date = data.get('from_date', None)
	to_date = data.get('to_date', None)
	status = data.get('status',None)
	part_name = data.get('part_name',None)
	
	query = []
	if from_date:
		query.append({'start_time': {"$gte":from_date}})
	if to_date:   
		query.append({'end_time': {"$lte":to_date}})
	if part_name:   
		query.append({'part_name': part_name})
	

#print(query)

	if bool(query):
		inspectionid_collection = MongoHelper().getCollection('inspection')
		objs = [i for i in inspectionid_collection.find({"$and":query}).sort([( '$natural', -1)]) ]
		#print("----------------*******------------",objs)
	else:
		inspectionid_collection = MongoHelper().getCollection('inspection')
		objs = [i for i in inspectionid_collection.find().sort([( '$natural', -1)])]
		print(objs)
		#print("----------------else------------",objs)

	p = []
	pr = []
	total_length = 0
	for ins in objs:
		model_selected = ins['part_name']
		inspection_id = str(ins['_id'])
		log_coll = MongoHelper().getCollection(str(inspection_id)+"_results")
		# for i in log_coll.find({'status':status}):
		#     total_length = total_length + len(i)
		#     print(total_length)
		if status:
			pr = [i for i in log_coll.find({'status':status})]
			total_length = total_length + len(pr)
		else:
			pr = [i for i in log_coll.find()]
			total_length = total_length + len(pr)
		for i in pr:
			i["model_selected"] = model_selected

		p.extend(pr)
	
	for items in p:
		#items["model_selected"] = model_selected
		if items.get("inference_frame"):
			items.pop("inference_frame")
		if items.get("input_frame"):
			items.pop("input_frame")
		if items.get("mask_frame"):
			items.pop("mask_frame")   
		if items.get("measure_frame"):
			items.pop("measure_frame")     
		if items.get("model_selected"):
			items.pop("model_selected")

	import bson
	bsf = str(bson.ObjectId())
	file_name = 'D:/Stamping tool/DEMO/datadrive/'+bsf
	print("value of the list object",p)
	# file_name = "/home/mim/Main/dataimages/reports/"+str(datetime.now())
	if 'remark' in p[0].keys() and 'flagged' in p[0].keys():
		list_dict = p
	if 'remark' not in p[0].keys():
		list_dict = p
		list_dict[0]["remark"]= ""
	if 'flagged' not in p[0].keys():
		list_dict = p
		list_dict[0]["flagged"]= False
	print("list of dictttttttttttttttttttt",list_dict[0])
	# ordered_list=list(list_dict[0].keys())
	# list_dict = p
	if list_dict:
		ordered_list=list(list_dict[0].keys())
	# print("data++++++++++!!!!!!!!!!",list_dict)
	#print(len(ordered_list))
		with open(file_name + '.csv','a',newline='') as outfile:
			writer = DictWriter(outfile, tuple(ordered_list))
			writer.writeheader()
			writer.writerows(list_dict)
	fn = file_name + '.csv'
	fn = fn.replace("D:/Stamping tool/DEMO/datadrive/","http://localhost:3306")
	file_w = fn
	# return file_w
	# return "http://0.0.0.0:3306/reports/results.csv"
	return "http://localhost:3306/"+bsf+".csv" 
	# return "http://0.0.0.0:3306/reports/"+ fn




