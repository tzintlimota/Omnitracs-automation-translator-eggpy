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

equi_proc.goTo("Carriers")
equi_proc.goTo("Load")
equi_proc.goTo("Certify")
equi_proc.goTo("Days")
equi_proc.goTo('DayLog')
equi_proc.goTo('Graph')
equi_proc.goTo('Clocks')