from common.utils import *
from django.utils import timezone
from bson import ObjectId
from livis.settings import *
from common.utils import MongoHelper
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime
from datetime import datetime, timedelta


def total_production_util(data):
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection('inspection')
    if operator_id=="":
        objs = [i for i in mp.find()]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    total_count = 0
    for ins in objs:
        inspection_id = str(ins['_id'])
        log_coll = MongoHelper().getCollection(inspection_id)
        pr = [i for i in log_coll.find()]
        total_count = total_count + len(pr)
    return total_count, 200


def production_yield_util(data):
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection('inspection')
    if operator_id=="":
        objs = [i for i in mp.find()]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    total_prod_count, status = total_production_util(data)
    if total_prod_count == 0:
        return 0, 200
    total_accepted = 0
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        parts_coll = mp.find({"status":"Accepted"}).count()
        total_accepted = total_accepted + parts_coll
    percent_yield = (total_accepted/total_prod_count)*100
    return percent_yield, 200


def production_rate_util(data):
    time_period = "secs"
    seconds_count = 0
    doc_count = 0
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection('inspection')
    if operator_id=="":
        objs = [i for i in mp.find()]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        insp_colls = [p for p in mp.find()]
        start_time = ins["start_time"]
        if ins["end_time"] != "":
            end_time = ins["end_time"]
        else:
            end_time = start_time
        start_time_dt = datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
        end_time_dt = datetime.strptime(end_time,"%Y-%m-%d %H:%M:%S")
        time_delta = end_time_dt - start_time_dt
        seconds = time_delta.total_seconds()
        seconds_count = seconds_count + seconds
        doc_count = doc_count + len(insp_colls)
    if doc_count == 0:
        return 0, 200
    avg_rate_secs = int(seconds_count/doc_count)
    return avg_rate_secs, 200


def production_weekly_util(data):
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection('inspection')
    if operator_id=="":
        objs = [i for i in mp.find()]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    date_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().replace(microsecond=0)
    #toi ---> time of interest
    toi_end = datetime.strptime(str(now), date_format)
    prev = now - timedelta(days = 7)
    toi_start = datetime.strptime(str(prev), date_format)
    parts = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"0":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        insp_colls = [p for p in mp.find({"status":"Accepted"})]

        for i in insp_colls:
            end_time = i["time_stamp"]
            end_time="2021-08-16 16:21:26"
            end_time = datetime.strptime(end_time, date_format)
            print("toi_start "+str(toi_start))
            print("toi_end "+str(toi_end))
            print("end time"+str(end_time))
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                days = time_delta.days
                parts[str(days)] = parts[str(days)] + 1
    print(parts)
    defects = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"0":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        insp_colls = [p for p in mp.find({"status":"Rejected"})]
        for i in insp_colls:
            end_time = i["time_stamp"]
            end_time = "2021-08-16 16:21:26"
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                days = time_delta.days
                defects[str(days)] = defects[str(days)] + 1
    print(defects)
    parts_list = []
    for key, value in parts.items():
        if value ==0:
            value = None
        parts_list.append(value)
    defect_list = []
    for key, value in defects.items():
        if value ==0:
            value = None
        defect_list.append(value)
    data = [{"name":"Accepted", "data":parts_list},{"name":"Rejected", "data":defect_list}]
    return data, 200


def production_hourly_util(data):
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection('inspection')
    if operator_id == "":
        objs = [i for i in mp.find()]
    else:
        objs = [i for i in mp.find({"operator_id":operator_id})]
    date_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().replace(microsecond=0)
    toi_end = datetime.strptime(str(now), date_format)
    prev = now - timedelta(days = 1)
    toi_start = datetime.strptime(str(prev), date_format)
    parts = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        insp_colls = [p for p in mp.find({"status":"Accepted"})]
        for i in insp_colls:
            end_time = i["time_stamp"]
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                hours_ = int(time_delta.total_seconds() / 3600)
                key_ = int(hours_ / 3)
                parts[str(key_)] = parts[str(key_)] + 1
    print(parts)
    defects = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0}

    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        insp_colls = [p for p in mp.find({"status":"Rejected"})]
        for i in insp_colls:
            end_time = i["time_stamp"]
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                hours_ = int(time_delta.total_seconds() / 3600)
                key_ = int(hours_ / 3)
                defects[str(key_)] = defects[str(key_)] + 1
    print(defects)
    parts_list = []
    for key, value in parts.items():
        if value ==0:
            value = None
        parts_list.append(value)
    defect_list = []
    for key, value in defects.items():
        if value ==0:
            value = None
        defect_list.append(value)
    data = [{"name":"Accepted", "data":parts_list},{"name":"Rejected", "data":defect_list}]
    return data, 200


def defect_count_util(data):
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection('inspection')
    if operator_id=="":
        objs = [i for i in mp.find()]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    total_rejected = 0
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        parts_coll = [p for p in mp.find({"status":"Rejected"})]
        total_rejected = total_rejected + len(parts_coll)
    return total_rejected, 200


def production_monthly_util(data):
    try:
        operator_id = data['operator_id']
    except:
        return "operator id not provided", 400
    mp = MongoHelper().getCollection('inspection')
    if operator_id == "":
        objs = [i for i in mp.find()]
    elif operator_id != "":
        objs = [i for i in mp.find({"operator_id":operator_id})]
    date_format = "%Y-%m-%d %H:%M:%S"
    now = datetime.now().replace(microsecond=0)
    toi_end = datetime.strptime(str(now), date_format)
    prev = now - timedelta(days = 365)
    toi_start = datetime.strptime(str(prev), date_format)
    parts = {"0":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0, "10":0, "11":0}
    for ins in objs:
        inspection_id = str(ins['_id'])
        mp = MongoHelper().getCollection(inspection_id)
        insp_colls = [p for p in mp.find({"status":"Accepted"})]
        for i in insp_colls:
            end_time = i["time_stamp"]
            end_time = datetime.strptime(end_time, date_format)
            if end_time >= toi_start and end_time < toi_end:
                time_delta = abs(toi_end - end_time)
                days_ = int(time_delta.days / 30)
                print("days diff "+str(days_))
                parts[str(days_)] = parts[str(days_)] + 1
    print(parts)
    defects = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0, "8":0, "9":0, "10":0, "11":0}
    for ins in objs:
         inspection_id = str(ins['_id'])
         mp = MongoHelper().getCollection(inspection_id)
         insp_colls = [p for p in mp.find({"status":"Rejected"})]
         for i in insp_colls:
             end_time = i["time_stamp"]
             end_time = datetime.strptime(end_time, date_format)
             if end_time >= toi_start and end_time < toi_end:
                 time_delta = abs(toi_end - end_time)
                 hours_ = int(time_delta.days / 30)
                 print("days diff "+str(days_))
                 defects[str(days_)] = defects[str(days_)] + 1
    print(defects)
    parts_list = []
    for key, value in parts.items():
        if value ==0:
            value = None
        parts_list.append(value)
    defect_list = []
    for key, value in defects.items():
        if value ==0:
            value = None
        defect_list.append(value)
    data = [{"name":"Accepted", "data":parts_list},{"name":"Rejected", "data":defect_list}]
    return data, 200


