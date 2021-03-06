from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
#import pyGPSFeed_IMR
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from General_Access_Functions import General_Access
import connection_credentials as cfg

#img_proc = ImageProcessor(cfg.vnc["ivg_ip"], cfg.vnc["password"], cfg.vnc["precision"])
gral_access = General_Access()
img_proc = ImageProcessor('192.168.1.118', 'None', .15)
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)

f = open("IVG_var.txt", "w")
f.write("None")
f.close()


while True:
    f = open("IVG_var.txt", "r")

    if img_proc.expect_image("vnc-load-info-required-popup", "ExpectedScreens",1) or img_proc.expect_image("vnc-load-info-required-popup2", "ExpectedScreens",1):
        print("Close load info required popup")
        #total_x, total_y = img_proc.click_image_by_max_key_points("IVG_Common/Login/OkLoginStatus/OkLoginStatus")
        #if total_y == -1:
        eld_core.closeLoadInfoAlert()
    elif img_proc.expect_image("vnc-certify-day-popup", "ExpectedScreens", 1):
        f = open("IVG_var.txt", "r")
        if f.read() == "Certify":
            print("Case Certify Alert Check Suspended")
        else:
            print("Handling Certify Day prompt ...")
            eld_core.closeCertifyDayPrompt()
    elif img_proc.expect_image("vnc-certify-outside-cycle-alert", "ExpectedScreens", 1):
        f = open("IVG_var.txt", "r")
        if f.read() == "Certify":
            print("Case Certify Alert Check Suspended")
        else:
            print("Handling Certify Days Outside of Cycle prompt ...")
            eld_core.closeCertifyDayPrompt()   
    elif img_proc.expect_image("vnc-certifyday-statusspans-pop-up", "ExpectedScreens", 1):
        f = open("IVG_var.txt", "r")
        if f.read() == "Certify":
            print("Case Certify Alert Check Suspended")
        else:
            print("Handling Certify Day Status Span alert")
            img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/AgreeButton/AgreeButton")
            img_proc.click_image_by_max_key_points("ok_status_login_btn")
    else:
        f = open("IVG_var.txt", "r")
        if f.read() == "Certify":
            print("Alert Sign Check Suspended")
        else:
            total_x, total_y = img_proc.get_image_coordinates_by_max_key_points('alert-sign')
            print( total_x, total_y)

            if total_x == -1:
                print("No alert sign found")
            elif img_proc.expect_image("vnc_change_main", "ExpectedScreens", 1):
                print("Case Certify Alert Check Suspended - On Status Change screen")
            else:
                if total_x > 170 and total_x < 300 and total_y < 350 and total_y > 200:
                    print("Alert sign found")
                    print("Closing Alert")
                    ivg_common.closeUnknownPositionAlert()
                else:
                    print("No alerts have been found")
