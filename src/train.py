#!/bin/env python3

import sys, os;

from ultralytics import YOLO;

if __name__ == "__main__":
   
   target="../tmp";
   runs  ="../runs";
   
   yaml_file = os.path.join(target,'dataset.yaml');
   basemodel = 'yolov8n.pt';
   
   model = YOLO(task="detect", model=basemodel);
   
   # https://docs.ultralytics.com/es/usage/cfg/#augmentation
   params={ "augment"      : False,
            "hsv_h"        : 0,
            "hsv_s"        : 0,
            "hsv_v"        : 0, 
            "degrees"      : 0,
            "translate"    : 0,
            "scale"        : 0,
            "shear"        : 0,
            "perspective"  : 0,
            "flipud"       : 0,
            "fliplr"       : 0,
            "mosaic"       : 0,
            "mixup"        : 0,
            "copy_paste"   : 0,
            "auto_augment" : False,
          };
   

   model.train(imgsz=640, batch=-1, epochs=100, data=yaml_file, device="cuda", patience=False, project=runs, name=".", exist_ok=True, plots=True, seed=17, **params);
   
   #model.export(format="onnx"  );
   #model.export(format="engine");

