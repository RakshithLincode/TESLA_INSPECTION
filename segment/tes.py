# import argparse
# import os
# import numpy as np
# import cv2
# import paddle

# from paddleseg.cvlibs import manager, Config, SegBuilder
# from paddleseg.utils import get_sys_env 

# from paddleseg import utils
# from paddleseg.core import infer
# import time
# from paddleseg import utils
# from paddleseg.core import infer
# from paddleseg.utils import logger, progbar, visualize
# from PIL import Image

# def mkdir(path):
#     sub_dir = os.path.dirname(path)
#     if not os.path.exists(sub_dir):
#         os.makedirs(sub_dir)

# def predict(img, 
#             model, 
#             model_path,
#             transforms, 
#             scales=1.0, 
#             is_slide=False,
#             stride=None,
#             crop_size=None):
    
#     utils.utils.load_entire_model(model, model_path)
#     model.eval()
    
#     with paddle.no_grad():
#         timer1 = time.time()
#         ori_shape = img.shape[:2]
#         data = {}
#         data['img'] = img
#         data = transforms(data)
#         data['img'] = data['img'][np.newaxis, ...]
#         data['img'] = paddle.to_tensor(data['img'])
#         pred, _ = infer.inference(
#                     model,
#                     data['img'],
#                     trans_info=data['trans_info'],
#                     is_slide=is_slide,
#                     stride=stride,
#                     crop_size=crop_size)
#         pred = paddle.squeeze(pred)
#         pred = pred.numpy().astype('uint8')
#         custom_color = [0, 0, 0, 255, 255, 255]
#         color_map = visualize.get_color_map_list(256, custom_color=custom_color)
#         color_map = [color_map[i:i + 3] for i in range(0, len(color_map), 3)]
#         color_map = np.array(color_map).astype("uint8")
#         c1 = cv2.LUT(pred, color_map[:, 0])
#         c2 = cv2.LUT(pred, color_map[:, 1])
#         c3 = cv2.LUT(pred, color_map[:, 2])
#         pred = np.dstack((c3, c2, c1))
#         timer2 = time.time()
#         print("elapsed inf time: ", timer2 - timer1)
#         return pred

# def main():
#     env_info = get_sys_env()
#     place = 'gpu' if env_info['Paddle compiled with cuda'] and env_info[
#         'GPUs used'] else 'cpu'
#     paddle.set_device(place)
#     cfg = Config('C:/DEMO/Tesla_Tyre/TESLA_INSPECTION/segment/pp_liteseg_optic_disc_512x512_1k.yml')
#     builder = SegBuilder(cfg)
#     model_path = 'C:/DEMO/Tesla_Tyre/TESLA_INSPECTION/segment/iter_1500/model.pdparams'
#     builder = SegBuilder(cfg)
#     img = cv2.imread(r"C:\Users\info\OneDrive\Pictures\Camera Roll\WIN_20230511_15_21_09_Pro.jpg")
#     pred = predict(img, builder.model, model_path=model_path, transforms=builder.val_dataset.transforms)
#     cv2.imwrite('output.png', pred)

# if __name__ == '__main__':
#     main()

import argparse
import os

import paddle

from paddleseg.cvlibs import manager, Config, SegBuilder
from paddleseg.utils import get_sys_env, logger, get_image_list, utils
from paddleseg.core import predict
from paddleseg.transforms import Compose
from paddleseg import utils
from paddleseg.core import infer
from paddleseg.utils import logger, progbar, visualize

def mkdir(path):
    sub_dir = os.path.dirname(path)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)

def partition_list(arr, m):
    """split the list 'arr' into m pieces"""
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]

def preprocess(im_path, transforms):
    data = {}
    data['img'] = im_path
    data = transforms(data)
    data['img'] = data['img'][np.newaxis, ...]
    data['img'] = paddle.to_tensor(data['img'])
    return data

def merge_test_config(cfg):
    aug_pred = False
    scales = 1.0
    flip_horizontal = False
    flip_horizontal = False
    flip_vertical = False
    is_slide = None
    crop_size = None
    stride = None
    custom_color = [0, 0, 0, 255, 255, 255]
    test_config = cfg.test_config
    if 'aug_eval' in test_config:
        test_config.pop('aug_eval')
    if aug_pred:
        test_config['aug_pred'] = aug_pred
        test_config['scales'] = scales
        test_config['flip_horizontal'] = flip_horizontal
        test_config['flip_vertical'] = flip_vertical
    if is_slide:
        test_config['is_slide'] = is_slide
        test_config['crop_size'] = crop_size
        test_config['stride'] = stride
    if custom_color:
        test_config['custom_color'] = custom_color
    return test_config


def main():
    cfg = Config('./pp_liteseg_optic_disc_512x512_1k.yml')
    builder = SegBuilder(cfg)
    test_config = merge_test_config(cfg)
    utils.show_env_info()
    utils.show_cfg_info(cfg)
    utils.set_device('gpu')
    model = builder.model
    transforms = Compose(builder.val_transforms)
    image_list, image_dir = get_image_list('C:/Users/info/OneDrive/Pictures/Camera Roll/WIN_20230511_15_21_09_Pro.jpg')
    print(image_dir)
    logger.info('The number of images: {}'.format(len(image_list)))
    model_path = './iter_1500/model.pdparams'
    save_dir = 'C:/DEMO/Tesla_Tyre/TESLA_INSPECTION/segment/dump/'
    predict(
        model,
        model_path=model_path,
        transforms=transforms,
        image_list=image_list,
        image_dir=image_dir,
        save_dir=save_dir,
        **test_config)


if __name__ == '__main__':
    main()