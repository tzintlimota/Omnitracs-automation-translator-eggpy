from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from EquiProc import EquiProc
#import pyGPSFeed_IMR


equi_proc = EquiProc()


''''''

img_proc = ImageProcessor('192.168.1.118', 'None', .15)











#Funcion de eggplant log
print('log "***Script name OHOS2810***"') 

#equi_proc.goTo('Status')
#equi_proc.goTo('Summary')
#equi_proc.dayForward('DayLog', 3)
equi_proc.dayBack('Graph', bool(True), 3)