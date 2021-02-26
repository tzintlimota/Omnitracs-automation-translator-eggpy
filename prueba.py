from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
import connection_credentials as cfg
#import pyGPSFeed_IMR


eld_core = IVG_ELD_CORE()
ivg_common = IVG_Common()


''''''

img_proc = ImageProcessor(cfg.vnc["ivg_ip"], cfg.vnc["password"], cfg.vnc["precision"])











#Funcion de eggplant log
print('log "***Script name OHOS2810***"') 

prueba =eld_core.getTable('Bottom', 'Asc', int(2))
print(prueba)