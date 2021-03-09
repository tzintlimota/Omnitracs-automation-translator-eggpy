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












print('log "***Script name OHOS2810***"') 


eld_core.getTable('Bottom', 'Asc', int(5))

eld_core.findTableRecord('OnDuty', 'Status','Bottom','Asc')