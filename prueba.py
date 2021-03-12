from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from Certify_Test_Case import Certify_Test_Case
import connection_credentials as cfg
#import pyGPSFeed_IMR
from ImageProcessor import ImageProcessor

img_proc = ImageProcessor('192.168.1.118', 'None', .15)

eld_core = IVG_ELD_CORE()
ivg_common = IVG_Common()
certify = Certify_Test_Case()
daylog = Daylog_Test_Case()


print('log "***Script name OHOS2810***"') 

certify.getTable('Bottom', 'Asc', int(5))
