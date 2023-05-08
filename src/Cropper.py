import sys, os, distutils.core
dist = distutils.core.run_setup("./detectron2/setup.py")
sys.path.insert(0, os.path.abspath('./detectron2'))

import torch, detectron2

# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random
# from google.colab.patches import cv2_imshow

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import os
import numpy as np
import json
from detectron2.structures import BoxMode
from detectron2.data import DatasetCatalog, MetadataCatalog

thing_classes = ['cheek','forehead']
thing_folder  = 'faces'

cfg = get_cfg()

cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
# cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model

cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")

cfg.MODEL.DEVICE = "cpu"
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
if __name__ == "__main__":
  cfg.MODEL.WEIGHTS = os.path.join("/Users/tomburnip/Library/CloudStorage/OneDrive-Personal/Uni Stuff/Level 5/DSTP/CNN-Cropper/src/model_final.pth")
else:
  cfg.MODEL.WEIGHTS = os.path.join("./model_final.pth")
# cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5 
# cfg.DATASETS.TEST = (thing_folder+"_test", )
predictor = DefaultPredictor(cfg)

CropGoodThreshold = 0.8

def crop(box,im):
  box = [int(el) for el in box]
  # print(box)
  top = box[1]
  bottom = box[3]
  left = box[0]
  right = box[2]
  return im[top:bottom,left:right,:]


def predictAndCrop(filename,outputFolder="/Users/tomburnip/Library/CloudStorage/OneDrive-Personal/Uni Stuff/Level 5/DSTP/CNN-Cropper/out",outputName="cropped"):
  im = cv2.imread(filename)
  crops = predictAndCropIm(im)

  for i,cropped in enumerate(crops):
    cv2.imwrite(os.path.join(outputFolder,outputName+str(i)+".png"),cropped) 

def predictAndCropIm(im):
  # print(im)
  outputs = predictor(im)

  good = [i for i,s in enumerate(list(vars(outputs["instances"].to("cpu"))["_fields"]["scores"])) if s > CropGoodThreshold]

  boxes = [(el.numpy(),list(vars(outputs["instances"].to("cpu"))["_fields"]["pred_classes"])[i]) for i,el in enumerate(list(vars(outputs["instances"].to("cpu"))["_fields"]["pred_boxes"])) if i in good]

  crops = {}

  for box in boxes:
    cropped = crop(box[0],im)
    key = thing_classes[int(box[1])]
    crops[key] = crops.get(key,[]) + [cropped]
  # print(crops.shape)
  return crops

if __name__ == "__main__":
  predictAndCrop("input.png")