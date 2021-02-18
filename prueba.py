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

eld_core.goTo('Status')
eld_core.goTo('Summary')
#Funcion de eggplant getLoadDate

eld_core.getLoadDate('02/21/2020')
eld_core.goToHistory()
eld_core.createLoad('loadId', 'Trailer1','Trailer2','Trailer3','BL','StartDate','EndDate', bool(True))
eld_core.certifyAllLogs()
eld_core.certifyLogsOfDAY(3)