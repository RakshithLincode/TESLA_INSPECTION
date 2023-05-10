import json
import logging
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
import datetime
from livis import settings as s
import pickle
import redis
import cv2
import os
import sys
import argparse
import shutil
import redis
import pickle
import datetime
from livis.settings import PARTS_COLLECTION
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import random 
from sklearn.model_selection import train_test_split
from cryptography.fernet import Fernet



#if (os.getcwd().split('/')[-1]) == "livis":
    #from livis.settings import REDIS_CLIENT_HOST
    #from livis.settings import REDIS_CLIENT_PORT
#else:
    #sys.path.insert(0,"../livis/")
    #from settings import REDIS_CLIENT_HOST
    #from settings import REDIS_CLIENT_PORT


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
        self.db = self.client[s.MONGO_DB]

    def getDatabase(self):
        return self.db

    def getCollection(self, cname, create=False, codec_options=None):
        _DB = s.MONGO_DB
        DB = self.client[_DB]
        if cname in s.MONGO_COLLECTIONS:
            if codec_options:
                return DB.get_collection(s.MONGO_COLLECTIONS[cname], codec_options=codec_options)
            return DB[s.MONGO_COLLECTIONS[cname]]
        else:
            return DB[cname]


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj


def getMachine_addr():
    """ Find OS and run appropriate read mobo serial num command"""
    os_type = sys.platform.lower()

    if "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    elif "win" in os_type:
        command = "wmic bios get serialnumber"
    elif "linux" in os_type:
        command = "cat /sys/devices/virtual/dmi/id/product_uuid"
    return os.popen(command).read().replace("\n", "").replace("  ", "").replace(" ", "")

def get_workstation_by_id(wid):
    mp = MongoHelper().getCollection("workstations")
    pp = mp.find_one({'_id' : ObjectId(wid)})
    return pp


@singleton
class CacheHelper():
    def __init__(self):
        # self.redis_cache = redis.StrictRedis(host="164.52.194.78", port="8080", db=0, socket_timeout=1)
        self.redis_cache = redis.StrictRedis(host=s.REDIS_CLIENT_HOST, port=s.REDIS_CLIENT_PORT, db=0, socket_timeout=1)
        s.REDIS_CLIENT_HOST
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
            #print(temp)
            if temp:
                try:
                    temp= pickle.loads(temp)
                except:
                    temp = json.loads(temp.decode())
            return temp
        except redis.ConnectionError:
            return None
        return None

    def execute_pipe_commands(self, commands):
        #TBD to increase efficiency can chain commands for getting cache in one go
        return None

#Key Builder
def read_json_file(json_file):
    with open(json_file,'r') as f:
        data = json.load(f)
        f.close()
        return data

def get_workstation_id(json_file):
    workstation_dict = read_json_file(json_file)
    workstation_id = workstation_dict['wid']
    return workstation_id

data = {
        "active": True,
        "_id": "5ebb930e4c2ee3532862454b",
        "workstation_name": "WS-01",
        "workstation_ip":'localhost',#"192.168.0.2"
        "client_port" : '6379',#"6379"
        "camera_config": {
            "cameras": [
                {
                    "camera_name": "default",
                    "camera_id": 0
                }
                ]}
}




@singleton    
class RedisKeyBuilderWorkstation():
    def __init__(self):
        #self.wid = get_workstation_id('livis//workstation_settings//settings_workstation.json')
        self.wid = "5ebb930e4c2ee3532862454b"
        self.workstation_info = data
    
    def get_key(self, camera_id, identifier):
        return "{}_{}_{}".format(self.workstation_info["workstation_name"], str(camera_id), identifier)



class RedisKeyBuilderServer():
    def __init__(self, wid):
    
        self.workstation_info = get_workstation_by_id(wid)
    
    def get_key(self, camera_id, identifier):
        
        return "{}_{}_{}".format(self.workstation_info["workstation_name"], str(camera_id), identifier)


class GetLabelData():

    def __init__(self, part_id):
        self.part_id = part_id
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
        self.part_id_collection = mp.find_one({'_id' : ObjectId(part_id)})
        _id = str(self.part_id_collection['_id'])
        mp = MongoHelper().getCollection(str(self.part_id_collection['_id'])+"_dataset")
        self.p = [i for i in mp.find()]


    def get_metrics(self):

        data = {}
        data['total_images'] = len(self.p)
        data['total_labeled_images'] = 0
        data['total_unlabeled_images'] = 0
        #data['label_info'] = []
        classifier_labels = []
        detector_labels = []

        def getDuplicatesWithCount(listOfElems):
    
            dictOfElems = dict()     
            for elem in listOfElems:         
                if elem in dictOfElems:
                    dictOfElems[elem] += 1
                else:
                    dictOfElems[elem] = 1    
                 
            #dictOfElems = { key:value for key, value in dictOfElems.items() if value > 1}

            return dictOfElems

        for i in self.p:
            if i['state'] == 'tagged' or i['state'] == 'semi-tagged':
                data['total_labeled_images'] += 1
            elif i['state'] == 'untagged':
                data['total_unlabeled_images'] += 1
        

            if i['annotation_classification'] != "":
                classifier_labels.append(i['annotation_classification'])

            
            if i['annotation_detection'] !=[] :
                for j in i['annotation_detection']:
                    detector_labels.append(j["cls"])

        classifier_label_obj = getDuplicatesWithCount(classifier_labels)
        detector_label_obj = getDuplicatesWithCount(detector_labels)

        data["classifier_label_data"] = classifier_label_obj
        data["detector_label_data"] = detector_label_obj

        return data



class ExperimentDataset():

    def __init__(self, part_id, experiment_id):
        self.part_id = ObjectId(part_id)
        self.experiment_id = ObjectId(experiment_id)
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
        self.part_id_collection = mp.find_one({'_id' : ObjectId(part_id)})

        _id = str(self.part_id_collection['_id'])

        mp = MongoHelper().getCollection(str(self.part_id_collection['_id']))
        self.entire_parts_object = [i for i in mp.find()]

        #print(type(self.entire_parts_object))
        #print(len(self.entire_parts_object))

        self.part_id_experiments = str(self.part_id)+"_"+"experiment"
        mp = MongoHelper().getCollection(self.part_id_experiments)

        self.dataset_of_exp = mp.find_one({'_id' : ObjectId(self.experiment_id)})

        self.labels_selected = self.dataset_of_exp["label_list"]
        #print(self.labels_selected)


    def to_csv(self,type_of_export):
        random.shuffle(self.entire_parts_object)
        #print(self.entire_parts_object)

        def xml_to_csv(split_val,labels_sel):
            xml_list = []
            for i in split_val:

                img_file_path = i['file_path']
                head_tail = os.path.split(img_file_path)
                name_of_img = head_tail[1]
                
                state = i['state']
                regions = i['regions']
                im = cv2.imread(img_file_path)
                height,width,depth = im.shape

                if regions!=[]:
                    if state == "tagged" or state == "updated":

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
                            if labels_sel:
                                if label in labels_sel:

                                    value = (str(name_of_img),
                                            int(width),
                                            int(height),
                                            str(label),
                                            int(x0),
                                            int(y0),
                                            int(x1),
                                            int(y1)
                                            )
                                    xml_list.append(value)
                            else:
                                value = (str(name_of_img),
                                        int(width),
                                        int(height),
                                        str(label),
                                        int(x0),
                                        int(y0),
                                        int(x1),
                                        int(y1)
                                        )
                                xml_list.append(value)


            column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
            xml_df = pd.DataFrame(xml_list, columns=column_name)
            return xml_df

        def xml_to_classification(split_val,labels_sel):
            xml_list = []
            for i in split_val:
                img_file_path = i['file_path']
                head_tail = os.path.split(img_file_path)
                name_of_img = head_tail[1]
                classifier_label = i['classifier_label']
                state = i['state']
                regions = i['regions']

                if classifier_label!= "":
                    if state == "tagged" or state == "updated":
                        if labels_sel:
                            if classifier_label in labels_sel:

                                value = (str(name_of_img),
                                        str(classifier_label)
                                        )
                                xml_list.append(value)
                        else:
                            value = (str(name_of_img),
                                     str(classifier_label)
                                     )
                            xml_list.append(value)

            column_name = ['filename', 'class']
            xml_df = pd.DataFrame(xml_list, columns=column_name)
            return xml_df



        if type_of_export == "classification":
            train_df = xml_to_classification(self.entire_parts_object,self.labels_selected)
            test_df = pd.DataFrame()
            return train_df,test_df
        elif type_of_export == "detection":
            training_dataset,test_dataset  = train_test_split(self.entire_parts_object, train_size=.8, test_size=.2)
            train_df = xml_to_csv(training_dataset,self.labels_selected)
            test_df = xml_to_csv(test_dataset,self.labels_selected)
            return train_df,test_df




    #detector - default split 80/20 gen csv


        

def generate_xml(exp_id,part_id,list_of_selected_lables,export_type):

    try:
        mp = MongoHelper().getCollection(PARTS_COLLECTION)
    except Exception as e:
        print(e)
        message = "Cannot connect to db"
        status_code = 500
        return message,status_code
    


    dataset = mp.find_one({'_id' : ObjectId(part_id)})
    _id = str(dataset['_id'])

    mp = MongoHelper().getCollection(str(dataset['_id']))
    p = [i for i in mp.find()]
    xml_file_path = None

    


    if export_type == "xml":

        for i in p:

            img_file_path = i['file_path']
            curr_annotation = i['detector_annotation']
            state = i['state']
            regions = i['regions']
            
            head_tail = os.path.split(img_file_path)

            #xml_file_path = head_tail[0]
            extract_loc = os.path.join("/livis/annotate/annotations/",str(exp_id))
            os.makedirs(extract_loc)
            xml_file_path = extract_loc
            name_of_img = head_tail[1]
            name_of_xml = str(name_of_img.split('.')[0]) +".xml"
            full_path_of_xml = os.path.join(xml_file_path,name_of_xml)


            folder_name = os.path.basename(xml_file_path)
            im = cv2.imread(img_file_path)
            height,width,depth = im.shape

            if len(curr_annotation) != 0:  
                if curr_annotation != []:
                    if curr_annotation != [[]]:
                        if state == 'updated' or state == 'tagged':

                            annotation = ET.Element('annotation')
                            ET.SubElement(annotation, 'folder').text = str(folder_name)
                            ET.SubElement(annotation, 'filename').text = str(name_of_img)
                            ET.SubElement(annotation, 'path').text = str(img_file_path)


                            size = ET.SubElement(annotation, 'size')
                            ET.SubElement(size, 'width').text = str(width)
                            ET.SubElement(size, 'height').text = str(height)
                            ET.SubElement(size, 'depth').text = str(depth)

                            ET.SubElement(annotation, 'segmented').text = '0'
                            
                            
                    
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

                                if label in list_of_selected_lables:

                                    ob = ET.SubElement(annotation, 'object')
                                    ET.SubElement(ob, 'name').text = str(label)
                                    ET.SubElement(ob, 'pose').text = 'Unspecified'
                                    ET.SubElement(ob, 'truncated').text = '1'
                                    ET.SubElement(ob, 'difficult').text = '0'

                                    bbox = ET.SubElement(ob, 'bndbox')
                                    ET.SubElement(bbox, 'xmin').text = str(x0)
                                    ET.SubElement(bbox, 'ymin').text = str(y0)
                                    ET.SubElement(bbox, 'xmax').text = str(x1)
                                    ET.SubElement(bbox, 'ymax').text = str(y1)

                            
                                    tree = ET.ElementTree(annotation) 

                                    with open(full_path_of_xml, "wb") as files : 
                                        tree.write(files)
        
    return xml_file_path


from livis.settings import *
def get_file(files):
    tup = ()
    if str(files).startswith('http'): #starts with
        f_name = str(files).split('/')[-1]
        #download wget -O /var/cache/foobar/stackexchange-site-list.txt http://url.to/stackexchange-site-list.txt
        cmd = 'wget -P '+ TRAIN_DATA_STATIC + ' ' + str(files)
        os.system(cmd)
        #return the absolute path with servable path
        abs_pth = os.path.join(TRAIN_DATA_STATIC,f_name)
        ser_pth = os.path.join('http://0.0.0.0:3306/'+f_name)
        return (abs_pth,ser_pth)
    else:
        abs_pth = os.path.join(TRAIN_DATA_STATIC,files)
        ser_pth = os.path.join('http://0.0.0.0:3306/'+files)
        return (abs_pth,ser_pth)
    #tup = (abs_pth,ser_pth)
    #return tup
