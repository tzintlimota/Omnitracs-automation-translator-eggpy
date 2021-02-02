from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
#import pyGPSFeed_IMR
from EquiProc import EquiProc

img_proc = ImageProcessor('192.168.1.118', 'None', .15)
equi_proc = EquiProc()


while True:
    time.sleep(1)
    if img_proc.expect_image("demo_main_screen", "ExpectedScreens",1):
        print("Main Page Found")
    #Put all alerts here
    elif img_proc.expect_image("vnc-load-info-required-popup", "ExpectedScreens",1):
        print("Close load info required popup")
        equi_proc.closeLoadInfoAlert()
    else:
        total_x, total_y = img_proc.get_image_coordinates_by_max_key_points('alert-sign')
        print( total_x, total_y)

        if total_x == -1:
            print("No alert sign found")
        else:
            if total_x > 170 and total_x < 300 and total_y < 350 and total_y > 200:
                print("Alert sign found")
                print("Closing Alert")
                equi_proc.closeUnknownPositionAlert()
            else:
                print("No alerts have been found")
        
