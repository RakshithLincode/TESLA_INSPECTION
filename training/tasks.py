#from fastai.vision import *
#from fastai.metrics import *
#from constants import *
from sklearn.metrics import classification_report
from common.utils import MongoHelper, ExperimentDataset
from bson import ObjectId
from livis.celery import app
from pathlib import Path
import numpy as np
#from django.conf import settings
from livis import settings 
import os
import pandas as pd
from celery import shared_task
from bson import ObjectId
#from fastai.basics import *
#from fastai.vision.all import *
#from fastai.callback.all import *
#from fastai.vision import *
from livis.settings import *
import datetime
import re
import json
#MODEL_MAP = {"resnet34" : models.resnet34}

def create_model_collections():
    json_file_path = os.path.join(os.getcwd(),"training","pipeline.json")
    parameter_path = os.path.join(os.getcwd(),"training","parameter.json")
    with open(json_file_path) as f:
        data = json.load(f)
    with open(parameter_path) as f1:
        para_data = json.load(f1)

    mp = MongoHelper().getCollection("model_collections")
    collection_object = {
    "checkpoint_path" : "/PATH/TO/CHECKPOINTS",
    "model_name" : "faster_rcnn_resnet50",
    "model_type" : "detection",
    "config" : data,
    "editable_parameters" :para_data}
# print(collection_object)
    # if not mp.countDocuments ==0:
    #     pass
    # else:
    model_collection = mp.insert_one(collection_object)    
    return model_collection 

def get_model(experiment_type):
    mp = MongoHelper().getCollection("model_collections")
    para = mp.find({"model_type":experiment_type})
    # list_ed_para = []
    for doc in para:
        values = [{ "id" :doc["_id"],"ckpt_path" :doc["checkpoint_path"],"model_name" :doc["model_name"],"editable_para" : doc["editable_parameters"]}]    
        return values

def test_fastai():
    config =  {"opt": "radam", "status": "initialized", "img_size": 224, "augmentations": {"flip_horizontly": True, "do_flip": True, "zoom": 0.2},
     "metrics": ["accuracy"], "bs": 2, "dataset_id": "5ea2046403ca3b758a5727b4", "datapath": "D://Lincode//LIVIS//Datasets//new_dataset", 
     "experiment_name": "experiment_test", 
    "experiment_type": "classification", "lr": 0.0001, "experiment_id": "64cd166f-49ab-49d8-87c0-1f6ef27afd14", "model": "mobilenet"}
    return train_fastai(config)


#TODO : handle nones
#TODO : add logging
#TODO : include more stages as mixup, augmentations
def add_experiment(config):
    part_id = config.get('part_id')
    label_list = config.get('label_list')
    experiment_name = config.get('experiment_name', None)
    experiment_type = config.get('experiment_type', None)
    mp = MongoHelper().getCollection(part_id + '_experiment')
    collection_obj = {
            'status' : 'started',
            'label_list' : label_list,
            'experiment_name' : experiment_name,
            'experiment_type' : experiment_type
    }
    experiment_id = mp.insert(collection_obj)
    return experiment_id



def add_experiment_modified(config):
    part_id = config.get('part_id')
    experiment_name = config.get('experiment_name', None)

    part_collection = MongoHelper().getCollection(settings.PARTS_COLLECTION)

    part_obj = part_collection.find({'_id' : ObjectId(part_id)})

    for obj in part_obj:  
        part_number = obj["part_number"]
    part_name_list = part_number.split()
    part_temp_list = []
    for i in part_name_list:
        val = i[0]
        part_temp_list.append(val)  
    seq_lett = "".join(part_temp_list)
     
    if experiment_name == None:
        experiment_name = str(part_number)+"_version_"+str(1)
        version  = 100000 + 1     
        experiment_name = seq_lett + str(version)
    else:
        temp_name =  int(experiment_name.split(seq_lett)[-1]) + 1 
        experiment_name = seq_lett + str(temp_name)

    exp_coll = MongoHelper().getCollection('experiment_settings')
    obj = exp_coll.find({'part_id' : part_id})
    for doc in obj:
        # part_id = doc["part_id"],
        # experiment_name = doc["experiment_name"],
        experiment_type = doc["experiment_type"],
        hyperparameters = doc["hyperparameters"]
    mp = MongoHelper().getCollection('experiment')

    myquery = { "part_id": part_id }
    newvalues = { "$set": { "experiment_name": experiment_name } }

    exp_coll.update_one(myquery, newvalues)

    print(experiment_name)
    collection_obj = {
            'status' : 'Initialized',
            'created_at':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'experiment_name' : experiment_name,
            'experiment_type' : experiment_type,
            'hyperparameters' : hyperparameters,
            'mount_data_path':"null",
            'retrain': False,
            'part_id' : part_id,
            'model_id':"null",
            'threshold':"0"
    }
    experiment_id_ = mp.insert(collection_obj)
    return  experiment_id_

    
    
def add_retrain_experiment(config):
    experiment_id = config.get('experiment_id') 
    retrain_status = config.get('retrain_status')
    epochs = config.get('epochs')
    # print(retrain_status)
    mp =MongoHelper().getCollection('experiment') 
    # curser = mp.find({'_id' : ObjectId(experiment_id)})
    # for val in curser:
    #     updated_no_steps = int(val["hyperparameters"]["no_of_steps"]) + int(no_of_steps)
    status = "Success" 
    mp.find_and_modify(query={'_id' : ObjectId(experiment_id)}, update={"$set": {'retrain': retrain_status}}, upsert=False, full_response= True)
    mp.find_and_modify(query={'_id' : ObjectId(experiment_id)}, update={"$set": {'hyperparameters.epochs': epochs}}, upsert=False, full_response= True)
    mp.find_and_modify(query={'_id' : ObjectId(experiment_id)}, update={"$set": {'status': 'Initialized'}}, upsert=False, full_response= True)
    return status

def train_fastai(config, experiment_id):
    pass
"""
def train_fastai(config, experiment_id):
  #  try:
        print(config)
        #1 Get values from config
        part_id = config.get('part_id', None)
        experiment_name = config.get('experiment_name', None)
        #experiment_id = config.get()
        sz = config.get('img_size', 224)
        lr = config.get('lr', 0.001)
        opt = config.get('opt')
        bs = config.get('bs' , 2)
        model = config.get('model', "resnet34")
        metrics = config.get('metrics', error_rate)
        label_list = config.get('label_list',None)

        #3 Set status "started" in monodb for current experiment_id (started, running, failed, success, pending)
        #status = 'started'
        part_collection = MongoHelper().getCollection(settings.PARTS_COLLECTION)
        part_obj = part_collection.find_one({'_id' : ObjectId(part_id)})
        mp = MongoHelper().getCollection(part_id + '_experiment')
        
        #experiment_id = mp.insert(collection_obj)    

        #4 Create apropriate folders.
        images_path = settings.TRAIN_DATA_STATIC
        #weights_path = "./experiments/{}/weights/".format(str(experiment_id))
        #logs_path = "./experiments/{}/logs/".format(str(experiment_id))
        #csv_path = "./experiments/{}/csv/".format(str(experiment_id))
        settings.BASE_DIR = '/root/freedom/backend/LIVIS/livis'
        print(settings.BASE_DIR)
        weights_path = os.path.join(settings.BASE_DIR+"/experiments/{}/weights/".format(str(experiment_id)))
        print(weights_path)
        logs_path = os.path.join(settings.BASE_DIR+"/experiments/{}/logs/".format(str(experiment_id)))
        csv_path = os.path.join(settings.BASE_DIR+"/experiments/{}/csv/".format(str(experiment_id)))
        
        Path(images_path).mkdir(parents=True, exist_ok=True)
        Path(weights_path).mkdir(parents=True, exist_ok=True)
        Path(logs_path).mkdir(parents=True, exist_ok=True)
        Path(csv_path).mkdir(parents=True, exist_ok=True)
        #5 Prepare image dataset via csv of tagged images in the created folder.
        #
        train_df, test_df = ExperimentDataset(part_id, experiment_id).to_csv('classification')

        train_df.to_csv(os.path.join(csv_path, 'train.csv'),index=False)
        
        #6 get model
        pre_model = MODEL_MAP.get(model)
        np.random.seed(42)
        df = pd.read_csv(Path(csv_path)/'train.csv')
        #7 prepare dataset
        # data = ImageDataBunch.from_df(df=df,path=images_path, valid_pct=0.2,ds_tfms=get_transforms(), size=sz).normalize(imagenet_stats)

        data = DataBlock(blocks=(ImageBlock, MultiCategoryBlock),
                   splitter=RandomSplitter(),
                   get_x=ColReader(0, pref=Path(images_path)),
                   get_y=ColReader(1, label_delim=' '),
                   item_tfms=Resize(sz),
                   batch_tfms=aug_transforms())

        dls = ImageDataLoaders.from_df(df, Path('/root/freedom/backend/LIVIS/livis/training'),
         folder='image_data', valid_pct=0.2,num_workers=0, sz=244,item_tfms=[ToTensor,Resize(sz)], batch_tfms = [IntToFloatTensor, Normalize.from_stats(*imagenet_stats)])

        print(len(dls.train))

        #8 Set status running in monodb for current experiment_id (started, running, failed, success, pending)
        status = 'running'

        experiment = mp.find_one({'_id' : ObjectId(experiment_id)})
        experiment['status'] = status

        mp.update_one({'_id' : experiment['_id']}, {'$set' : experiment})
        

        #9 initialize network and pass data and metrics
        # learn = create_cnn(data, pre_model, metrics=error_rate)
        learn = cnn_learner(dls, pre_model, metrics=accuracy)
        learn.dls.fake_l.num_workers = 0
        defaults.device = torch.device('cuda') # makes sure the gpu is used
        #learn.recorder.plot_loss()
        # learn.fit_one_cycle(1)
        # learn.fit_one_cycle(4)
        # learn.unfreeze() # must be done before calling lr_find
        
        #10 Learning rate finder
#        learn.lr_find()
        learn.fine_tune(3, base_lr=3e-3, freeze_epochs=4)

        #learn.recorder.plot_loss()
        learn.fit_one_cycle(3, lr_max=slice(1e-5,1e-3))
        #learn.save(experiment_name + '-stage-1')

        #11 save weights to weights_path
        learn.export(os.path.join(weights_path, experiment_id + ".pkl"))

        #12 save logs to logs path
        #preds,y,losses = learn.get_preds(with_loss=True, n_workers=1)
        #probs = np.argmax(preds, axis=1)
        #interp = ClassificationInterpretation.from_learner(learn)

        logs = {
           # "confusion_matrix" : interp.confusion_matrix().tolist(),
            #"report" : classification_report(y, probs, target_names=list(dls.vocab), output_dict=True),
            "report" : {},
            "model_file" : os.path.join(weights_path, experiment_id + ".pkl")
        }
        # logs = {'test':'result'}
        
        #13 insert overall experiment details to mongo_db (path,logs,status) 
        
        experiment = mp.find_one({'_id' : ObjectId(experiment_id)})

        experiment['logs'] = logs
        experiment['status'] = 'success'
        experiment['images_path'] = os.path.join(os.getcwd(),images_path.replace('./',''))
        experiment['weights_path'] = os.path.join(os.getcwd(),weights_path.replace('./',''), experiment_id + ".pkl")
        experiment['logs_path'] = os.path.join(os.getcwd(),logs_path.replace('./','')) 

        mp.update_one({'_id' : experiment['_id']}, {'$set' : experiment})
        p = mp.find_one({'_id' : experiment['_id']})
        print(p)
    #except:
     #   return {"message" : "Create Experiment Failed"}
    
"""
def train_tf(config, experiment_id):
    try:
        experiment_name = config.get('experiment_name', None)
        part_id = config.get('part_id', None)
        selected_labels = config.get('selected_labels', None)
        images_path = settings.TRAIN_DATA_STATIC
        experiments_directory = settings.EXPERIMENT_DATA_STATIC 

        required_annotations_format = "csv"

        traindf, testdf = gen_annotations(exp_id, part_id, list_of_labels_selected, get_type)

        status = 'running'

        part_obj = part_collection.find_one({'_id' : ObjectId(part_id)})

        _id = experiment_id 
        mp = MongoHelper().getCollection(part_id + '_experiment')
        experiment = mp.find_one({'_id' : _id})
        experiment['status'] = status
        mp.update_one({'_id' : experiment['_id']}, {'$set' : experiment})

        # start training
        to_save_path = os.path.join(experiments_directory, experiment_id)

        # get_env_path = subprocess.check_output("which python", shell=True)
        # python_env_path = get_env_path.decode('utf-8').strip()
        python_env_path = "/root/anaconda3/envs/livis_tensorflow/bin/python"
        
        #print("{} /root/freedom/backend/LIVIS/livis/training/detection_pipelines/tf_training/train_shell.py --to_save_path '{}' --images_path '{}' --num_steps {}".format(python_env_path, to_save_path, images_path, num_steps))

        #os.system("{} /root/freedom/backend/LIVIS/livis/training/detection_pipelines/tf_training/train_shell.py --to_save_path '{}' --images_path '{}' --num_steps {}".format(python_env_path, to_save_path, images_path, num_steps))
        # start_training.train_tensorflow_object_detection_api(base_config_path, to_save_path, images_path, num_steps)
        # generate inference_graph

        mp = MongoHelper().getCollection(part_id + '_experiment')
        experiment = mp.find_one({'_id' : _id})
        experiment['logs'] = logs
        experiment['status'] = 'success'
        experiment['images_path'] = os.path.join(os.getcwd(),images_path.replace('./',''))
        experiment['weights_path'] = os.path.join(os.getcwd(),weights_path.replace('./',''), experiment_id + ".pkl")
        experiment['logs_path'] = os.path.join(os.getcwd(),logs_path.replace('./','')) 
        mp.update_one({'_id' : experiment['_id']}, {'$set' : experiment})
        return mp.find_one({'_id' : experiment['_id']})
    
    except:
        mp = MongoHelper().getCollection(part_id + '_experiment')
        experiment = mp.find_one({'_id' : ObjectId(_id)})
        experiment['status'] = 'failed'
        mp.update_one({'_id' : dataset['_id']}, {'$set' : dataset})
        return mp.find_one({'_id' : dataset['_id']})


def get_experiment_status(part_id,experiment_id):
    try:
        mp = MongoHelper().getCollection(part_id + 'experiment')
        return mp.find_one({'_id' : ObjectId(experiment_id)})
        #return {"status" : mp.find_one({'_id' : _id})['status']}
    except:        
        return {}

#@app.task(bind=True)
@shared_task
def process_job_request(config, experiment_id):
    print(config)
    if config['experiment_type'] == 'classification':
        return train_fastai(config,experiment_id)
    if config['experiment_type'] == 'detection':
        return train_tf(config, experiment_id)
        # return None


def getModel(iden, typ= 'fastai'):
    if typ == 'fastai':
        model_path = os.path.join(EXPERIMENT_SAVE_PATH, iden + '.pkl')
        if os.path.exists(model_path):
            learn = load_learner(EXPERIMENT_SAVE_PATH, iden + '.pkl')
        return learn
    if typ == 'tf':
        tf_model = get_tf_model(iden)
        return tf_model 

def train_tensorflow(config):
    ## do processing here 
    return None

def get_tf_model(iden):
    ## write tf model load 
    return None


def get_running_experiment_status(part_id):
    try:
        mp = MongoHelper().getCollection(str(part_id) + '_experiment')
        exp = [i for i in mp.find()]
        list_of_running = []
        for i in exp:
            if i["status"] == "running":
                list_of_running.append(i)
        data={}
        data["running_experiments"] = list_of_running
        return data
        #return {"status" : mp.find_one({'_id' : _id})['status']}
    except:        
        return {}

def get_all_running_experiments_status():
    mp = MongoHelper().getCollection(PARTS_COLLECTION)
    parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).sort( "$natural", -1 )]
    #parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).skip(skip).limit(limit)]
    list_of_running = []
    for i in parts:
        part_obj_id = i["_id"]
        mp = MongoHelper().getCollection('experiment')
        exp = [i for i in mp.find({'part_id' : str(part_obj_id)})]
        print(exp)
        for i in exp:
            if i["status"].lower() in ['initialized','started',"running"]:
                list_of_running.append(i)
    data={}
    data["running_experiments"] = list_of_running
    return data


def set_threshold_util(data):

    experiment_id = data["experiment_id"]
    threshold = data["threshold"]
    mp = MongoHelper().getCollection('experiment')
    
    collection_obj = {'threshold':threshold}
    
    mp.update({'_id' : ObjectId(experiment_id)}, {'$set' : collection_obj})
    
    #p = [ p for p in mp.find({"_id":experiment_id})]
    
    exp = [i for i in mp.find({'_id' : ObjectId(experiment_id)})]
    
    return exp[0]
    

def deploy_experiment_util(data):

    
    part_id = data["part_id"]
    experiment_id = data["experiment_id"]
    workstation_ids = data["workstation_ids"]
    
    #try:
    mp = MongoHelper().getCollection('experiment')
    #parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]})]
    exp = [i for i in mp.find({"$and" : [{"part_id":part_id}]})]
    print("LENGTH OF EXP",len(exp))
    for i in exp:
       #print("chayaaaa")
        #if 'deployed_on_workstations' in i.keys() and workstation_ids in i['deployed_on_workstations']:
            
        #if str(ObjectId(i['_id']))==str(experiment_id):
       collection_obj = {
                'deployed':False,
                'deployed_on_workstations': [],
                'container_deployed':False
            }
       mp.update({'_id' : ObjectId(i['_id'])}, {'$set' : collection_obj})
       #return i  
       # return mp.find_one({'_id' : ObjectId(i['_id'])})     
    #except Exception as e:   
    #   print(e)     
    #    #return {}
    #    pass

    part_id = data["part_id"]
    experiment_id = data["experiment_id"]
    workstation_ids = data["workstation_ids"]
    try:
        mp = MongoHelper().getCollection('experiment')
        exp = [i for i in mp.find()]
        for i in exp:
            if str(ObjectId(i['_id']))==str(experiment_id):
                collection_obj = {
                    'deployed':True,
                    'container_deployed':False,
                    # 'deployed_at':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                    'deployed_on_workstations': workstation_ids
                }
                mp.update({'_id' : ObjectId(i['_id'])}, {'$set' : collection_obj})
                #return i  
                return mp.find_one({'_id' : ObjectId(i['_id'])})     
    except Exception as e:   
        print(e)     
        return {}



def get_deployment_list_util():
    return_list = []
    from capture.utils import get_inference_feed_url_util
    part_collection = MongoHelper().getCollection(settings.PARTS_COLLECTION)
    workstation_collection = MongoHelper().getCollection(settings.WORKSTATION_COLLECTION)
    parts = [p for p in part_collection.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).sort( "$natural", -1 )]
    for part in parts:
        #print(part)
        part_id = part['_id']
        mp = MongoHelper().getCollection('experiment')
        exp = [i for i in mp.find()]
        print("Length:",len(exp))
        for experiment in exp:
            #print(experiment)
            try:
                if 'deployed' in experiment and experiment['deployed']:
                    print("in if deployed is true ")
                    print(experiment["_id"])
                    for dw in experiment['deployed_on_workstations']:
                        print("if deployed on wk")
                        #print(dw)
                        ws = workstation_collection.find_one({'_id' : ObjectId(dw)})
                        ws_name = ws['workstation_name']
                        print(ws_name)
                        #print(experiment)
                        resp = {
                            "experiment_name" : experiment['experiment_name'],
                            "part_number" : part['part_number'],
                            "experiment_type" : experiment['experiment_type'],
                            "workstation" : ws_name,
                            "inference_urls" :  get_inference_feed_url_util(ws["_id"] , part_id),
                            "experiment_id" : experiment['_id'],
                            "container_state" : experiment['container_state']
                        }
                        try:
                            threshold =  experiment['threshold']
                            resp['threshold'] = threshold
                        except:
                            print("Exception")
                        print(resp)
                        #print("PAAAAAAAA:",part_id)
                        print("SSSSSSSS:",experiment['part_id'])
                        #return_list.append(resp)
                        if str(part_id) == str(experiment['part_id']):
                            return_list.append(resp)
                            #print("in if")
            except Exception as e:
                print(e)
            #print("below exc")
    	    #return return_list   
    print(return_list)
    return return_list





def get_deployment_list_util_updated():
    return_list = []
    from capture.utils import get_inference_feed_url_util
    part_collection = MongoHelper().getCollection(settings.PARTS_COLLECTION)
    workstation_collection = MongoHelper().getCollection(settings.WORKSTATION_COLLECTION)
    parts = [p for p in part_collection.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).sort( "$natural", -1 )]
    for part in parts:
        # print(part)
        part_id = part['_id']
        mp = MongoHelper().getCollection('experiment')
        exp = [i for i in mp.find({"part_id": str(part_id)})]

        for experiment in exp:     
                #print(experiment)
                
                    if 'deployed' in experiment and experiment['deployed']:
                        print("in if")
                        
                        for dw in experiment['deployed_on_workstations']:    
                            ws = workstation_collection.find_one({'_id' : ObjectId(dw)})
                            ws_name = ws['workstation_name']
                            resp = {
                                "experiment_name" : experiment['experiment_name'],
                                "part_number" : part['part_number'],
                                "experiment_type" : experiment['experiment_type'],
                                "workstation" : ws_name,
                                "inference_urls" :  get_inference_feed_url_util(ws["_id"] , part_id),
                                "experiment_id" : experiment['_id'],
                               
                                }
                            try:
                                threshold =  experiment['threshold']
                                container_state : experiment['container_state']
                                resp['threshold'] = threshold
                                resp['container_state'] = container_state
                            except Exception as e:
                                print(" exception "+str(e))
                                pass
                            print("resp is"+str(resp))
                            return_list.append(resp)
                            resp = {}
                            #print(return_list)
                


    return return_list    



#crud
def create_model_static_util(data):
    part_id = data['part_id']
    
    try:
        batch_size = data['batch_size']
        no_of_steps = data['no_of_steps']
        epochs = data['epochs']
        learning_rate = data['learning_rate']
    except:
        pass
        
    mp = MongoHelper().getCollection("experiment_settings")
    para = [i for i in mp.find({"part_id":str(part_id)})]
    
    
    if len(para) == 0:
        pass
        """
        #create
        pth = os.path.join(os.getcwd(),'training/expe.json')
        with open(pth) as f:
            collection_obj = json.loads(f)
        
        collection_obj['part_id'] = str(part_id)
        
        mp1 = MongoHelper().getCollection(PARTS_COLLECTION)
        para1 = mp1.find({"part_id":str(part_id)})
        part_name = para1[0]['part_name']
        
        
        mp1 = MongoHelper().getCollection("experiment")
        para1 = mp1.find({"part_id":str(part_id)})
        
        if len(para1) == 0:
            #no exp found
            collection_obj['experiment_name'] = str(part_name)+'_version_1'
        else:
            #exp found incr++
            versions = []
            for i in para1:
                versions.append( int(str(i['experiment_name']).split('_')[-1]) )
            versions.sort()
            collection_obj['experiment_name'] = str(part_name)+"_version_"+str(version[-1])
        
        experiment_id = mp.insert(collection_obj)
        return collection_obj
        """
        
    else:
        #update
        pth = os.path.join(os.getcwd(),'training/expe.json')
        with open(pth) as f:
            collection_obj = json.load(f)
        
        del collection_obj['experiment_name']
        collection_obj['part_id'] = str(part_id)
        
        mp1 = MongoHelper().getCollection(PARTS_COLLECTION)
        #para1 = mp1.find({"part_id":str(part_id)})
        #para1 = [i for i in mp1.find({"part_id":ObjectId(part_id)})]
        para1 = mp1.find_one({'_id' : ObjectId(part_id)})
        
        #mp1 = MongoHelper().getCollection(PARTS_COLLECTION)
        #pc = mp.find_one({'_id' : ObjectId(_id)})
        print(para1)
        part_name = para1['part_number']
        
        
        mp1 = MongoHelper().getCollection("experiment")
        para1 = [i for i in mp1.find({"part_id":str(part_id)})]
        #para1 = mp1.find({"part_id":str(part_id)})
        
        #if len(para1) == 0:
        #    #no exp found
        #    collection_obj['experiment_name'] = str(part_name)+'_version_1'
        #else:
        #    #exp found incr++
        #    versions = []
        #    for i in para1:
        #        versions.append( int(str(i['experiment_name']).split('_')[-1]) )
        #    versions.sort()
        #    collection_obj['experiment_name'] = str(part_name)+"_version_"+str(version[-1])
        
        collection_obj['hyperparameters']['batch_size'] = batch_size
        collection_obj['hyperparameters']['no_of_steps'] = no_of_steps
        collection_obj['hyperparameters']['epochs'] = epochs
        collection_obj['hyperparameters']['learning_rate'] = learning_rate
        print(collection_obj)
        
        
        #experiment = mp.find_one({'_id' : ObjectId(experiment_id)})
        #experiment['status'] = status
        
        
        _id = para[0]['_id']
        _id = ObjectId(_id)
        mp.update_one({'_id' : _id}, {'$set' : collection_obj})
        
        return collection_obj
        
def get_model_static_util(part_id):
    print("in")
    mp = MongoHelper().getCollection("experiment_settings")
    para = [i for i in mp.find({"part_id":str(part_id)})]
    print(para)
    
    return para
    

# stop training 
def interrupt_training_utils(config):

    experiment_id = config.get('experiment_id')
    mp = MongoHelper().getCollection('experiment')
    cursor = mp.find({'_id':ObjectId(experiment_id)})
    for ele in cursor:
        status = ele["status"]
        # print(status)
   
    if status.lower() == "initialized":
        mp.find_and_modify(query={'_id' : ObjectId(experiment_id)}, update={"$set": {'status': 'Failed'}}, upsert=False, full_response= True)
        # changing status to failed so that celery won't pick up the experiment

    if status.lower() =="running":
        comm2 = "docker stop" + " " + str(experiment_id)   
        import subprocess
        process = subprocess.Popen(comm2.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()    
        mp.find_and_modify(query={'_id' : ObjectId(experiment_id)}, update={"$set": {'status': 'Failed'}}, upsert=False, full_response= True)
    return experiment_id 


#Train APIS FOR Deployment and get running experiments 

def all_experiments_filter_utils(config):
    status = config.get('status')
    experiment_name= config.get('experiment_name')
    created_at = config.get('created_at')
    try :
        page = config.get('page')
        page = int(page)
    except:    
        page = 0

    try:    
        number_of_items = config.get('no_of_items')
        number_of_items = int(number_of_items)
    except:
        number_of_items = 0    

    mp = MongoHelper().getCollection(PARTS_COLLECTION)
    parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).sort( "$natural", -1 )]
    #parts = [p for p in mp.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).skip(skip).limit(limit)]
    list_of_running = []
    for i in parts:
        part_obj_id = i["_id"]
        mp = MongoHelper().getCollection('experiment')
        # cursor = mp.find({'part_id' : str(part_obj_id)})
        query_ = []

        if status != "" :
            exp = '^'+status
            print(exp)
            # query_.append({'status':{'$regex':exp}})
            query_.append({"status":re.compile(status, re.IGNORECASE)})
        if experiment_name != "":
            exp =  '^'+experiment_name 
            print(exp)  
            # query_.append({'experiment_name':{'$regex':exp}})
            query_.append({"experiment_name":re.compile(experiment_name, re.IGNORECASE)})

        if status == "" and experiment_name =="":
            query_.append({})    

        
        pr_ids = [i for i in mp.find({"$and":query_})]    
        # except:
        #     if status == "" and experiment_name == "" :
        #         pr_ids = [i for i in mp.find({})]

        for i in pr_ids:   
            if status in i["status"] and i["status"].lower() in ['initialized',"running"]:
                print("1")
                list_of_running.append(i)


        # exp = [i for i in mp.find({'part_id' : str(part_obj_id)})]
        # # print(exp)
        # for i in exp:   
        #     if status in i["status"] and i["status"].lower() in ['initialized',"running"]:
        #         print("1")
        #         list_of_running.append(i)
        #     # if status == None and i["status"].lower() in ['initialized',"running"]:
        #     #         list_of_running.append(i)    
        #     if experiment_name in i["experiment_name"] and i["status"].lower() in ['initialized',"running"]:
        #         print("2")
        #         list_of_running.append(i)  
        #     if status == "" and experiment_name == " " and created_at == "":
        #         print("3")
        #         if i["status"].lower() in ['initialized',"running"]:
        #             list_of_running.append(i)

    # list_of_running =pr_ids
    list_ = []
    unique_list = []

    for item in list_of_running:
        id = item["_id"]
        if id not in unique_list:        
            unique_list.append(id)
        if item["_id"] in unique_list:
            if item not in list_:
                list_.append(item)
    
    # print(unique_list)        

    for i in list_:
    #     try:    
    #         i["created_at"] = datetime.datetime.strptime(str(i["created_at"]), "%Y - %m - %d, %H:%M:%S")  
    #     except ValueError:
        i["created_at"] = datetime.datetime.strptime(str(i["created_at"]), "%m/%d/%Y, %H:%M:%S") 
    


    if created_at != "descending":

        # for i in list_:
        #     i["created_at"] = datetime.datetime.strptime(str(i["created_at"]), "%m/%d/%Y, %H:%M:%S") 
        list_.sort(key = lambda x: x["created_at"].date())
    else:
        list_ = list_[::-1]        


    skip_from = ((page*number_of_items)-number_of_items)
    start_idx = skip_from

    if page == 0 and number_of_items == 0:
        list_ = list_
    
    else:
        list_ = list_[start_idx:start_idx+number_of_items]
        # list_ = [list_[i:i+number_of_items] for i in range(0, len(list_), number_of_items)]
        # print(list_)

    data={"count":len(list_)}
    data["running_experiments"] = list_
    return data




def deployment_list_filter_utils(config):
    """
    payload :
    {
    part_number: object id of part number,
    experiment_name: string,
    workstation: object id of ws,
    page: 0,
    number_of_items: 10
    }
    """


    part_number = config.get('part_number',None)
    experiment_name= config.get('experiment_name',None)
    workstation = config.get('workstation',None)
    location = config.get('location',None)
    # page = config.get('page',None)
    # number_of_items = config.get('number_of_items',None)
    try :
        page = config.get('page')
        page = int(page)
    except:    
        page = 0

    try:    
        number_of_items = config.get('no_of_items')
        number_of_items = int(number_of_items)
    except:
        number_of_items = 0   

    from capture.utils import get_inference_feed_url_util
    part_collection = MongoHelper().getCollection(settings.PARTS_COLLECTION)
    workstation_collection = MongoHelper().getCollection(settings.WORKSTATION_COLLECTION)

    ###### filter ######
    query_list = []
    mp = MongoHelper().getCollection('experiment')
    if part_number != "" :
        print("in parts loop")
        # exp = '^'+part_number
        # print(exp)
        query_list.append({'part_id':part_number})
    if experiment_name != "":
        exp =  '^'+experiment_name 
        print(exp)  
        # query_list.append({'experiment_name':{'$regex':exp}})
        query_list.append({"experiment_name":re.compile(experiment_name, re.IGNORECASE)})

    if workstation != "" :
        # print("in workstation")
        query_list.append({'deployed_on_workstations':workstation})     

    if part_number == "" and experiment_name =="":
        print("empty string")
        exp =  '^true'
        query_list.append({'deployed':True})    

    mp = MongoHelper().getCollection('experiment')
    pr_ids = [i for i in mp.find({"$and":query_list})] 
    return_list = []
    
        

    # parts = [p for p in part_collection.find({"$and" : [{"isdeleted": False}, { "isdeleted" : {"$exists" : True}}]}).sort( "$natural", -1 )]

    for experiment in pr_ids:     
            #print(experiment)
            
                if 'deployed' in experiment and experiment['deployed']:
                    print("in if")
                    
                    for dw in experiment['deployed_on_workstations']:    
                        ws = workstation_collection.find_one({'_id' : ObjectId(dw)})
                        ws_name = ws['workstation_name']
                        part_id = experiment["part_id"]
                        cursor = part_collection.find({"_id":ObjectId(part_id)})
                        for i in cursor:
                            part_name = i["part_number"]
                        resp = {
                            "experiment_name" : experiment['experiment_name'],
                            "part_number" : part_name,
                            "experiment_type" : experiment['experiment_type'],
                            "workstation" : ws_name,
                            "inference_urls" :  get_inference_feed_url_util(ws["_id"] , part_id),
                            "experiment_id" : experiment['_id'],
                            
                            }
                        try:
                            threshold =  experiment['threshold']
                            container_state : experiment['container_state']
                            resp['threshold'] = threshold
                            resp['container_state'] = container_state
                        except Exception as e:
                            print(" exception "+str(e))
                            pass
                        print("resp is"+str(resp))
                        return_list.append(resp)
                        resp = {}


    ####################
    list_ = []
    unique_list = []

    for item in return_list:
        # print(item)
        id = item["experiment_id"]
        if id not in unique_list:        
            unique_list.append(id)
        if item["experiment_id"] in unique_list:
            if item not in list_:
                list_.append(item)


    skip_from = ((page*number_of_items)-number_of_items)
    start_idx = skip_from

    if page == 0 and number_of_items == 0:
        list_ = list_
    
    else:
        list_ = list_[start_idx:start_idx+number_of_items]
        # list_ = [list_[i:i+number_of_items] for i in range(0, len(list_), number_of_items)]
        # print(list_)

    out_dict = {"count":len(list_),"data" :list_}
    return out_dict



