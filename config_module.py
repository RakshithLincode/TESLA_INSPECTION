import os
import sys

from utils.torch_utils import select_device
from detect_module import *

class opt_config():
    def __init__(self):
        self.base_path = ""
        # self.detector_weights_path = "D:/BACKEND_HEMLOCK/Hemlock_Backend/LINCODE_AI_WORKER/segment/AI_WEIGHTS/hemlock_version_1.pt" # working
        self.detector_mask_weights_path = "D:/Tesla/DEMO/LIVIS_AI_WORKER/segment/tesla_tyre.pt" 
        # self.gan_weight = "D:/BACKEND_HEMLOCK/Hemlock_Backend/LINCODE_AI_WORKER/segment/AI_WEIGHTS/realesr-animevideov3.pth" # working
        self.separate_crop_model = False
        self.classifier_weights = ""
        self.segmentor_weights = ""
        self.ocr_weights = ""
        self.detector_input_image_size = 640
        self.detector_mask_input_image_size = 640
        self.common_conf_thres = 0.1
        self.iou_thres = 0.2
        self.max_det = 1000
        self.device = ""
        self.line_thickness = 2
        self.hide_labels = False
        self.hide_conf = True 
        self.half = False
        self.crop = False
        self.cord = []
        self.crop_class = ""
        self.min_crop_size = None
        self.max_crop_size = None
        self.crop_conf = 0.25
        self.crop_iou = 0.25
        self.padding  = 50
        self.crop_hide_labels = True
        self.crop_hide_conf = True
        self.classes = None
        self.defects = ["rivert-missing","rivet-damage","pad-damage","pad-rivet-missing","pin-damage","pin-missing","wrong-position-assembly"]
        self.feature = ["rivert","pin","pad-rivet","A3","S"]
        self.features_extra = ["bi_barcode","BagID","des_barcode","A3","S"]
        self.visualize = False
        self.individual_thres = {'bi_barcode':0.34,"BagID":0.5,"des_barcode":0.5,"A3":0.65,"S":0.3}#best_22.pt
        self.rename_labels = {} # {'person':'manju'}
        self.avoid_labels_cords = [{'xmin':0,'ymin':0,'xmax':1280,'ymax':720},{'xmin':0,'ymin':6,'xmax':569,'ymax':548}]
        self.avoid_required_labels = ['person'] # ['person','cell phone']
        self.detector_predictions = None # This will update from the predictions
       




