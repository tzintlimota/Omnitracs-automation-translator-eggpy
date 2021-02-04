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
    if img_proc.expect_image("vnc-load-info-required-popup", "ExpectedScreens",1):
        print("Close load info required popup")
        total_x, total_y = img_proc.click_image_by_max_key_points("IVG_Common/Login/OkLoginStatus/OkLoginStatus")
        if total_y == -1:
            equi_proc.closeLoadInfoAlert()
    elif img_proc.expect_image("vnc-certify-day-popup", "ExpectedScreens", 1):
        print("Handling Certify Day prompt ...")
        equi_proc.closeCertifyDayPrompt()
    elif img_proc.expect_image("vnc-certify-outside-cycle-alert", "ExpectedScreens", 1):
        print("Handling Certify Days Outside of Cycle prompt ...")
        equi_proc.closeCertifyDayPrompt()
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
        
