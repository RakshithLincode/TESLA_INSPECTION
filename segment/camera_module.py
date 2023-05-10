#!/usr/bin/env python
from threading import Thread, Lock
import cv2
import redis 
from pymongo import MongoClient
import pickle

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
        return None

rch = CacheHelper()

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror: 
            img = cv2.flip(img, 1)
        # cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27: 
            break  # esc to quit
    cv2.destroyAllWindows()
    return img

def main():
    frame = show_webcam(mirror=False)
    rch.set_json({'frame':frame})

if __name__ == '__main__':
    main()