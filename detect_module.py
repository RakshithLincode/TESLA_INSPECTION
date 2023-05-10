import argparse
import os
import platform
import sys
from pathlib import Path
import torch
import numpy as np
import numpy

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, smart_inference_mode
from config_module import *
import numpy as np
from utils.segment.general import masks2segments, process_mask, process_mask_native
from PIL import Image, ImageEnhance

sys.path.insert(0,"D:/BACKEND_HEMLOCK/Hemlock_Backend/LINCODE_AI_WORKER/GAN/")
from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)


def image_preprocess(image ,img_size=640, stride=32):
        # Padded resize
    img = letterbox(image, img_size , stride=stride)[0]

    # Convert
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    # img = img.transpose()
    img = np.ascontiguousarray(img)
    return img

opt = opt_config()

def load_detector(weights,half,device,imgsz):
    dnn=False
    data=ROOT / 'data/coco128.yaml' 
    bs = 6    
    half = False
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    imz = (1280, 1280)
    for i in range(6):
        model.warmup(imgsz=(1 if pt else bs, 3, *imz))
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    print("Model loaded! and WarmUp is done!!")
    return model , stride , names

def load_detector_mask(weights,half,device,imgsz):
    dnn=False
    data=ROOT / 'data/coco128.yaml' 
    bs = 6    
    half = False
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    imz = (640, 640)
    for i in range(6):
        model.warmup(imgsz=(1 if pt else bs, 3, *imz))
        seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    print("Model loaded! and WarmUp is done!!")
    return model , stride , names

def detector_get_inference(opt ,im0, names,img_size  ,stride, model, device ,half ):
    # img0 = cv2.imread(path)
    print("inside inference!!")
    predictions = []
    cord = []
    imc = im0.copy()
    im = im0.astype('float32')
    im = torch.from_numpy(im).to(model.device)
    im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim


    pred = model(im)[0]
    pred = non_max_suppression(pred)

    # Process predictions
    for i, det in enumerate(pred):
        annotator = Annotator(im0, line_width=3, example=str(names))
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class

            # Write results
            for *xyxy, conf, cls in reversed(det):
                c = int(cls)  # integer class
                label = None if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')
                annotator.box_label(xyxy, label, color=colors(c, True))
    
    return im0

def detector_get_inference1(opt ,im0, names,img_size  ,stride, model, device ,half ):
    print("inside inference!!")
    predictions = []
    cord = []

    im = image_preprocess(im0 , img_size = img_size ,stride = stride)
    im = torch.from_numpy(im).to(model.device)
    im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim

    pred = model(im, augment=False, visualize=False)

    pred = non_max_suppression(pred, conf_thres = opt.crop_conf, iou_thres = opt.crop_iou, classes = None, agnostic = False, max_det=1000)
    
    for i, det in enumerate(pred):  # per image
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        imc = im0.copy() 
        annotator = Annotator(im0, line_width=opt.line_thickness, example=str(names))
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
            # Write results
            for *xyxy, conf, cls in reversed(det):
                xmin = int(xyxy[0].item())
                ymin = int(xyxy[1].item())
                xmax = int(xyxy[2].item())
                ymax = int(xyxy[3].item())

                c = int(cls)  # integer class

                skip = None
                if opt.avoid_labels_cords:
                    if bool(opt.avoid_required_labels):
                        for label in opt.avoid_required_labels:
                            if label == names[c]:
                                for crd in opt.avoid_labels_cords:
                                    if round(xmin) >= crd['xmin'] and round(ymin) >= crd['ymin'] and round(xmax) <= crd['xmax'] and round(ymax) <= crd['ymax']:
                                        skip = True
                    else:
                        for crd in opt.avoid_labels_cords:
                            if round(xmin) >= crd['xmin'] and round(ymin) >= crd['ymin'] and round(xmax) <= crd['xmax'] and round(ymax) <= crd['ymax']:
                                skip = True
                if skip :
                    continue

                line_width = opt.line_thickness or max(round(sum(im0.shape) / 2 * 0.003), 2)

            ## Checking individual threshold for wach label 
                if names[c] in list(opt.individual_thres.keys()):
                    try:
                        if opt.individual_thres[names[c]] <= conf:
                            label = None if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')

                            p1, p2 = (int(xmin), int(ymin)), (int(xmax), int(ymax))
                            
                
                            if names[c]:
                                namer = None
                                if namer is None:
                                    names[c] = names[c]
                                else:
                                    names[c] = namer			
                                
                                ## Bounding color   
                                if names[c] in opt.defects :#or names[c] in ["stepmark_P","dent"]:
                                    color = (0,0,255) # Red color bounding box 
                                else:
                                    color = (0,128,0) # Green color bounding box 


                                cv2.rectangle(im0, p1, p2, color, thickness=line_width, lineType=cv2.LINE_AA)
                                
                                tf = max(line_width - 1, 1)  # font thickness
                                

                                w, h = cv2.getTextSize(names[c], 0, fontScale=line_width / 3, thickness=tf)[0]  # text width, height
                                outside = p1[1] - h - 3 >= 0  # label fits outside box
                                p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
                                cv2.rectangle(im0, p1, p2, color, -1, cv2.LINE_AA)  # filled
                                cord.append({names[c]:[int(xmin),int(ymin),int(xmax),int(ymax)]})
                                
                                cv2.putText(im0, names[c], (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, line_width / 3, (255,255,255),
                                            thickness=tf, lineType=cv2.LINE_AA)
                                    
                                predictions.append(names[c])
                                # cord.append({label:[xmin,ymin,xmax,ymax]})

                    except:
                        pass
                
                ## If not individual threshold
                else:
                    # line_width or max(round(sum(im.shape) / 2 * 0.003), 2)
                    p1, p2 = (int(xmin), int(ymin)), (int(xmax), int(ymax))	

                    
                
                    if names[c]:
                        # namer = opt.rename_labels(names[c])
                        label = None if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')
                        namer = None
                        if namer is None:
                            names[c] = names[c]
                        else:
                            names[c] = namer
                        
                        ## Bounding color   
                        if names[c] in opt.defects:
                            color = (0,0,255) # Red color bounding box 
                        else:
                            color = (0,128,0) # Green color bounding box
                        
                        cv2.rectangle(im0, p1, p2, color, thickness=line_width, lineType=cv2.LINE_AA)

                        
                        tf = max(line_width - 1, 1)  # font thickness
                        # tf = self.line_thickness
                        w, h = cv2.getTextSize( names[c], 0, fontScale=line_width / 3, thickness=tf)[0]  # text width, height
                        outside = p1[1] - h - 3 >= 0  # label fits outside box
                        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
                        cv2.rectangle(im0, p1, p2, color, -1, cv2.LINE_AA)  # filled
                        cord.append({names[c]:[int(xmin),int(ymin),int(xmax),int(ymax)]})

                        
                        cv2.putText(im0, names[c], (p1[0], p1[1] - 2 if outside else p1[1] + h + 2), 0, line_width / 3, (255,255,255),
                                    thickness=tf, lineType=cv2.LINE_AA)
                        predictions.append(names[c])
                        # cord.append({label:[xmin,ymin,xmax,ymax]})          
                # if names[c] in list(opt.individual_thres.keys()):
                #     if conf > opt.individual_thres[names[c]] :
                #         label = None if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')
                #         if bool(opt.defects) :
                #             if names[c] in opt.defects :#or names[c] in ["stepmark_P","dent"]:
                #                 bndbox_color = [60,20,250]#RED
                #             # if names[c] in ["burr","scratch","white_rust"]:
                #             #     bndbox_color = [0,165,255] #Orange
                #             else:
                #                 bndbox_color = [0,128,0]#GREEN
                #         # if bool(opt.features_extra) :
                #         #     if names[c] in opt.features_extra :#or names[c] in ["stepmark_P","dent"]:
                #         #         # bndbox_color = [60,20,250]#RED
                #         #     # if names[c] in ["burr","scratch","white_rust"]:
                #         #         bndbox_color = [0,165,255] #Orange
                #         #     else:
                #         #         bndbox_color = [0,128,0]#GREEN
                        

                #         else:
                #             bndbox_color = colors(c, True)
                        
                #         annotator.box_label(xyxy, label, color=bndbox_color)
                #         predictions.append(names[c])
                #         cord.append({label:[xmin,ymin,xmax,ymax]})
                # else:
                #     label = None if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')
                #     if bool(opt.defects) :
                #         if names[c] in opt.defects:
                #             bndbox_color = [60,20,250]#RED
                #         else:
                #             bndbox_color = [0,128,0]#GREEN
                #     else:
                #         bndbox_color = colors(c, True)
                    
                #     annotator.box_label(xyxy, label, color=bndbox_color)
                #     predictions.append(names[c])
                #     cord.append({label:[xmin,ymin,xmax,ymax]})
                
    #torch.cuda.empty_cache()
    return im0 , predictions,cord

def detector_mask_inference(opt ,im0, names,img_size  ,stride, model, device ,half ):
    print("inside inference!!")
    import time
    worker_start = time.time()
    predictions = []
    cord = []
    im = image_preprocess(im0 , img_size = img_size ,stride = stride)
    im = torch.from_numpy(im).to(model.device)
    im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
    im /= 255  # 0 - 255 to 0.0 - 1.0
    if len(im.shape) == 3:
        im = im[None]  # expand for batch dim
    pred = model(im, augment=False, visualize=False)
    agnostic_nms = False
    # Dataloader
    bs = 1  # batch_size       
    pred, proto = model(im, augment=False, visualize=False)[:2]
    pred = non_max_suppression(pred, conf_thres = opt.crop_conf, iou_thres = opt.crop_iou, classes = None, agnostic = False, max_det=opt.max_det, nm=32)
    mask_results = []
    for i, det in enumerate(pred):  # per image
        # seen += 1
        retina_masks=True
        save_masks=True
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        imc = im0.copy() 
        annotator = Annotator(im0, line_width=opt.line_thickness, example=str(names))
        if len(det):
            if retina_masks:
                # scale bbox first the crop masks
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()  # rescale boxes to im0 size
                masks = process_mask_native(proto[i], det[:, 6:], det[:, :4], im0.shape[:2])  # HWC
                masks = masks.detach().cpu().numpy()
                masks = np.around(masks)
                unified_mask = np.sum(masks, axis=0)
                unified_mask = (unified_mask / np.max(unified_mask)) * 255
                mask_image = unified_mask.astype(np.uint8)
            else:
                masks = process_mask(proto[i], det[:, 6:], det[:, :4], im.shape[2:], upsample=True)  # HWC
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()  # rescale boxes to im0 size
                masks = masks.detach().cpu().numpy()
                masks = np.around(masks)
                unified_mask = np.sum(masks, axis=0)
                unified_mask = (unified_mask / np.max(unified_mask)) * 255
                mask_image = unified_mask.astype(np.uint8)
            print("TIME TAKEN BY MODEL TO PREDICT MASK :::::::::::::::::::::::::::::::::::::::::::::",time.time() - worker_start)    
            return mask_image
            
def load_gan_model(weights):
    model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu')
    netscale = 4
    upsampler = RealESRGANer(scale=netscale,model_path=weights,dni_weight=None,model=model,tile=0,tile_pad=10,pre_pad=0,half=True,gpu_id=None)   
    print('GAN "Model loaded! and is done!!"')             
    return upsampler

# def order_points(pts):
#     rect = np.zeros((4, 2), dtype="float32")
#     s = pts.sum(axis=1)
#     rect[0] = pts[np.argmin(s)]
#     rect[2] = pts[np.argmax(s)]
#     diff = np.diff(pts, axis=1)
#     rect[1] = pts[np.argmin(diff)]
#     rect[3] = pts[np.argmax(diff)]
#     return rect

# def four_point_transform(image, pts):
#     rect = order_points(pts)
#     (tl, tr, br, bl) = rect
#     widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
#     widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
#     maxWidth = max(int(widthA), int(widthB))
#     heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
#     heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
#     maxHeight = max(int(heightA), int(heightB))
#     dst = np.array([
#         [0, 0],
#         [maxWidth - 1, 0],
#         [maxWidth - 1, maxHeight - 1],
#         [0, maxHeight - 1]], dtype="float32")
#     M = cv2.getPerspectiveTransform(rect, dst)
#     warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
#     return warped

def get_gan_image(upsampler,img,pts):
    output, _ = upsampler.enhance(img, outscale=4)
    output = Image.fromarray(output)
    contrast = 1.5
    output = ImageEnhance.Contrast(output).enhance(contrast)
    brightness = 1.6
    output = ImageEnhance.Brightness(output).enhance(brightness)
    output = np.asarray(output)
    output = cv2.resize(output,(1280,960))
    return output

     