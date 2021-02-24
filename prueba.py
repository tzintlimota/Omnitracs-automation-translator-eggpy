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

#img_proc = ImageProcessor(cfg.vnc["ivg_ip"], cfg.vnc["password"], cfg.vnc["precision"])

img_proc = ImageProcessor('192.168.1.118', 'None', .15)









#Funcion de eggplant log
print('log "***Script name OHOS2810***"') 

eld_core.findTableRecord("On Duty","Status","Bottom", "Asc")
eld_core.findTableRecord("On Duty","Start","Bottom", "Asc")
eld_core.findTableRecord("On Duty","Duration","Bottom", "Asc")
eld_core.findTableRecord("On Duty","Location","Bottom", "Asc")
eld_core.findTableRecord("On Duty","Origin","Bottom", "Asc")

#eld_core.findTableRecord("Sleeper Berth","","Top", "Desc")