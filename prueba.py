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

#Funcion de eggplant put

#equi_proc.loginDriver('TMOTA001', 'TMOTA001', '', '')
#Global DeviceType
''' (*log driver in*)

'''

#ConnectUnit
equi_proc.logOutAllDrivers()
equi_proc.loginDriver('ELOPEZ01', 'ELOPEZ01', ' ', ' ')
equi_proc.changeDriverStatus('ON', 'DIME', ' ', ' ', ' ')
equi_proc.goToLoginPage()
equi_proc.logOutAllDrivers()