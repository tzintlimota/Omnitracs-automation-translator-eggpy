from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
#import pyGPSFeed_IMR


eld_core = IVG_ELD_CORE()
ivg_common = IVG_Common()




''''''

img_proc = ImageProcessor('192.168.1.118', 'None', .15)











eld_core.createLoad('Test', '1', '2', '3', 'Yes', '12/08/2022', '01/06/2023', '')

#img_proc.imageResizer()