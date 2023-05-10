import cv2
import time
import redis
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

rch = CacheHelper()

def work_with_captured_video(cam):
    while True:
        ret, frame = cam.read()
        if not ret:
            cam.release()
            rch.set_json({'camera_health_check':False})
            return False
        else:
            rch.set_json({'camera_health_check':True})
            cv2.imshow('frame', frame)
            rch.set_json({'camera_live_frame':frame})
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return True

while True:
    cam = cv2.VideoCapture(1)
    if cam.isOpened():
        print('Camera is connected')
        response = work_with_captured_video(cam)
        if response == False:
            print("Camera is disconnected")
            continue
    else:
        continue


