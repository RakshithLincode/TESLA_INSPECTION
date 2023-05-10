import sys

import numpy as np
sys.path.append("D:\deployment")

import os
import glob
import cv2
from detect_module import *
# from classifier_module import *
from config_module import *
# from common_utils import *
import torch
from datetime import  datetime
import uuid


#@singleton
class Inference:
    def __init__(self):
        self.opt = opt_config()
        self.device = device = select_device(self.opt.device)
        self.half = self.opt.half
        self.crop = self.opt.crop
        self.cropped_frame = None
        self.input_frame = None
        self.mask_input_frame = None
        self.gan_frame = None
        self.predicted_frame = None
        self.detector_predictions = None
        self.points = None
        # self.detector , self.detector_stride , self.detector_names  = load_detector(weights = self.opt.detector_weights_path,
        #                                                 half = self.half,device = self.device ,
        #                                                 imgsz = self.opt.detector_input_image_size )
        self.detector_mask , self.detector_stride_mask , self.detector_names_mask  = load_detector_mask(weights = self.opt.detector_mask_weights_path,
                                                        half = self.half,device = self.device ,
                                                        imgsz = self.opt.detector_mask_input_image_size )
        # self.upsampler  = load_gan_model(weights = self.opt.gan_weight)

    def dummy(self):
        self.predicted_frame, self.detector_predictions,self.cord = detector_get_inference1(opt = self.opt,
                                                                                    im0 = self.input_frame , names = self.detector_names,
                                                                                    img_size = self.opt.detector_input_image_size ,
                                                                                    stride = self.detector_stride ,
                                                                                    model= self.detector , device = self.device,
                                                                                    half = self.half)
        # self.predicted_frame = cv2.resize(self.predicted_frame,(400,400))
        return self.predicted_frame, self.detector_predictions,self.cord #, self.classifier_predictions
        # return self.predicted_frame

    def mask_dummy(self):
        self.predicted_frame = detector_mask_inference(opt = self.opt,
                                                        im0 = self.mask_input_frame , names = self.detector_names_mask,
                                                        img_size = self.opt.detector_input_image_size ,
                                                        stride = self.detector_stride_mask ,
                                                        model= self.detector_mask , device = self.device,
                                                        half = self.half)
        return self.predicted_frame #, self.classifier_predictions
    
    # def gan_output(self):
    #     self.predicted_frame = get_gan_image(self.upsampler,img = self.gan_frame, pts = self.points)
    #     return self.predicted_frame 


