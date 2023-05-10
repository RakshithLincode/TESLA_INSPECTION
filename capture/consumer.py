import os
# from kafka import KafkaProducer,  KafkaConsumer
import json
import cv2
import numpy as np
import base64
import time
import sys
import logging
import pandas as pd
from pymongo import MongoClient
from common.utils import MongoHelper
from bson import ObjectId

consumer_mount_path = "/apps/Livis"

class Consumer():
    """
    Receives the image feed form the subscribed topic
    """
    def __init__(self, KAFKA_BROKER_URL, topic, auto_offset_reset_value):
        """
        Instantiates the Consumer object

        Arguments:
            KAFKA_BROKER_URL: url to connect to Kafka Broker
            topic: topic to subscribe the video frame from
            auto_offset_reset_value: What to do when there is no initial offset in Kafka or if the current offset \
            does not exist any more on the server (e.g. because that data has been deleted):
        """
        self.obj = KafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda value: json.loads(value), auto_offset_reset=auto_offset_reset_value,)
        
        self.topic = topic

    def apply_crops(img, x,y,w,h):
        height,width,channels = img.shape
        x0 = x * width
        y0 = y * height
        x1 = ((x + w) * width)
        y1 = ((y + h) * height)
        img = img[y0:y1,x0:x1]
        return img

    def collect_stream_for_capture(self, part_id, workstation_id):
        """"
        Receives the encoded image frames from the prescribed topic

        Arguments:
            mongo_client: client to access the mongo server
            part_id: part name/id being captured in the image frames

        """
        logging.info("\nReceiving the stream images\n")
        frame_iter_ = 0
        for message in self.obj:
            # Decoding the image stream
            print("Consuming the value")
            im_b64_str = message.value["frame"]
            im_b64 = bytes(im_b64_str[2:], 'utf-8')
            im_binary = base64.b64decode(im_b64)

            im_arr = np.frombuffer(im_binary, dtype=np.uint8)
            img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

            preprocessing_list = MongoHelper().getCollection(part_id + "_preprocessingpolicy")
            p = [p for p in preprocessing_list.find()]
            iter_ = 0
            for policy in p:
                if policy['workstation_id'] == workstation_id:
                    regions = policy['regions']
                    if regions != []:
                        x, y, w, h = regions
                        img = self.apply_crops(img, x,y,w,h)
                    else:
                        pass
                iter_ = iter_ + 1
                ## save image by policy and add collection
                # Saving the frame
                save_path = consumer_mount_path + "/" + str(part_id) + "/frame" + str(frame_iter_)+str(iter_) + ".jpg"
                cv2.imwrite(save_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 90]) ##--- need to check this????
                img_path = str(part_id) + "/frame" + str(frame_iter_)+str(iter_) + ".jpg"

                capture_doc = {
                    "file_path": img_path,
                    "file_url": "http//0.0.0.0:3306/"+str(img_path),
                    "state": "untagged",
                    "annotation_detection": [],
                    "annotation_detection_history": [],
                    "annotation_classification": "",
                    "annotation_classification_history": [],
                    "annotator": ""}

                mp = MongoHelper().getCollection(part_id+"_dataset")
                mp.insert(capture_doc)

            print("\n\n")
            print(frame_iter_)
            frame_iter_ = frame_iter_ + 1
            logging.info('Received frame %s of part %s', frame_iter_, part_id)
        return 1




    def collect_stream_for_preview(self, part_id, workstation_id):
        print("called1")
        """"
        Receives the encoded image frames from the prescribed topic

        Arguments:
            mongo_client: client to access the mongo server
            part_id: part name/id being captured in the image frames

        """
        
            
        while True:
            
            for message in self.obj:
                print("called2")

                im_b64_str = message.value["frame"]
                im_b64 = bytes(im_b64_str[2:], 'utf-8')
                im_binary = base64.b64decode(im_b64)

                im_arr = np.frombuffer(im_binary, dtype=np.uint8)
                img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            

                ret, jpeg = cv2.imencode('.jpg', img)
                print(jpeg)
                cv2.imshow("frane",jpeg)
                cv2.waitKey(0)
            
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
