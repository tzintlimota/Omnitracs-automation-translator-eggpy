#import pytesseract
from ImageProcessor import ImageProcessor
import os
import cv2
import time
from datetime import datetime, timedelta, date
import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from dateutil.parser import parse
import connection_credentials as cfg
import re
import pytest
import sys
from subprocess import Popen, CalledProcessError, PIPE


#import pyGPSFeed_IMR

class General_Access:
    def __init__(self):
        self.img_proc = ImageProcessor('192.168.1.118', 'None', .15)

    def search_func(self, search, space):
        search = re.search(r"" + search + "", str(space))
        if search != None:
            return True
        return False
    
    def goTo(self, page):
        print(page)
        #self.goToELD()
        if page == 'Summary':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/SummaryTab/SummaryTabInactive/SummaryTabInactive")
            if total_x > 120 and total_x < 170:
                self.img_proc.click_image_by_max_key_points("ELD_Core/SummaryTab/SummaryTabInactive/SummaryTabInactive")
        elif page == 'Status':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/StatusTab/StatusTabInactive/StatusTabInactive")
            print(total_x, total_y)
            if total_x > 0 and total_x < 100:
                self.img_proc.click_image_by_max_key_points("ELD_Core/StatusTab/StatusTabInactive/StatusTabInactive")
        elif page == 'Clocks':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/ClocksTab/ClocksTabInactive/ClocksTabInactive")
            print(total_x, total_y)
            if total_x > 250 and total_x < 290:
                self.img_proc.click_image_by_max_key_points("ELD_Core/ClocksTab/ClocksTabInactive/ClocksTabInactive")
        elif page == 'Graph':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/GraphTab/GraphTabInactive/GraphTabInactive")
            print(total_x, total_y)
            if total_x > 300 and total_x < 330:
                self.img_proc.click_image_by_max_key_points("ELD_Core/GraphTab/GraphTabInactive/GraphTabInactive")
        elif page == 'DayLog':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/DayLogTab/DayLogTabInactive/DayLogTabInactive")
            print(total_x, total_y)
            if total_x > 400 and total_x < 430:
                self.img_proc.click_image_by_max_key_points("ELD_Core/DayLogTab/DayLogTabInactive/DayLogTabInactive")
        elif page == 'Days':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/8DaysTab/7DaysTabInactive/7DaysTabInactive")
            print(total_x, total_y)
            if total_x > 500 and total_x < 550:
                self.img_proc.click_image_by_max_key_points("ELD_Core/8DaysTab/7DaysTabInactive/7DaysTabInactive")
            elif total_x > 400 and total_x < 430:
                self.img_proc.click_image_by_max_key_points_offset("ELD_Core/DayLogTab/DayLogTabInactive/DayLogTabInactive", 130, 0)
        elif page == 'Certify':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/CertifyTab/CertifyTabInactive/CertifyTabInactive")
            print(total_x, total_y)
            if total_x > 590 and total_x < 620:
                self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/CertifyTabInactive/CertifyTabInactive")
        elif page == 'Load':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/LoadTab/LoadTabInactive/LoadTabInactive")
            print(total_x, total_y)
            if total_x > 690 and total_x < 730:
                self.img_proc.click_image_by_max_key_points("ELD_Core/LoadTab/LoadTabInactive/LoadTabInactive")
        elif page == 'Carriers':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("ELD_Core/CarriersTab/CarriersTabInactive/CarriersTabInactive")
            print(total_x, total_y)
            if total_x > 740 and total_x < 780:
                self.img_proc.click_image_by_max_key_points("ELD_Core/CarriersTab/CarriersTabInactive/CarriersTabInactive")
        
    def retrieve_duration(self):
        string = ""
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

        for i in range(3):
            '''This defines with region is being captured (hh:mm:ss)'''
            if i == 0:
                x, x1 = 320, 340
                time_char = "h "
            elif i == 1:
                x, x1 = 352, 372
                time_char = "m "
            else:
                x, x1 = 387, 407
                time_char = "s "

            crop_img2 = img[int(285):int(310), int(x):int(x1)]

            '''calculate the 50 percent of original dimensions'''
            width = int(crop_img2.shape[1] * 300 / 100)
            height = int(crop_img2.shape[0] * 300 / 100)
            # dsize
            dsize = (width, height)
            '''resize image'''
            crop_img2 = cv2.resize(crop_img2, dsize)

            '''Change to gray scale'''
            crop_img2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

            '''Otsu Tresholding automatically find best threshold value'''
            _, binary_image = cv2.threshold(crop_img2, 0, 255, cv2.THRESH_OTSU)

            '''Invert the colors of the image'''
            count_white = np.sum(binary_image > 0)
            count_black = np.sum(binary_image == 0)
            if count_black > count_white:
                binary_image = 255 - binary_image

            '''Padding'''
            crop_img2 = cv2.copyMakeBorder(binary_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            crop_img2 = cv2.GaussianBlur(crop_img2, (3, 3), 0)
            #plt.imshow(crop_img2)
            #plt.show()

            string += pytesseract.image_to_string(crop_img2,
                                                  config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
            string = string.strip()
            string += time_char
            print(string)

        return string

    def retrieve_start(self):
        string = ""
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

        for i in range(3):

            '''This defines with region is being captured (hh:mm:ss)'''
            if i == 0:
                x, x1 = 34, 56
                time_char = ":"
            elif i == 1:
                x, x1 = 57, 77
                time_char = ":"
            else:
                x, x1 = 80, 100
                time_char = ""

            crop_img2 = img[int(285):int(310), int(x):int(x1)]
            '''calculate the 50 percent of original dimensions'''
            width = int(crop_img2.shape[1] * 600 / 100)
            height = int(crop_img2.shape[0] * 600 / 100)

            # dsize
            dsize = (width, height)
            '''resize image'''
            crop_img2 = cv2.resize(crop_img2, dsize)

            '''Change to gray scale'''
            crop_img2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

            '''Otsu Tresholding automatically find best threshold value'''
            _, binary_image = cv2.threshold(crop_img2, 0, 255, cv2.THRESH_OTSU)

            # invert the image colors
            count_white = np.sum(binary_image > 0)
            count_black = np.sum(binary_image == 0)
            if count_black > count_white:
                binary_image = 255 - binary_image

            '''Padding'''
            crop_img2 = cv2.copyMakeBorder(binary_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))

            '''Blur the image'''
            crop_img2 = cv2.GaussianBlur(crop_img2, (3, 3), 0)

            #plt.imshow(crop_img2)
            #plt.show()

            string += pytesseract.image_to_string(crop_img2, config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
            string = string.strip()
            string += time_char
            print(string)

        return string
    
    def retrieve_text(self, y, y1, x, x1):
        self.img_proc.click_image_by_coordinates(150, 300)
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y):int(y1), int(x):int(x1)]
        
        width = int(crop_img2.shape[1] * 800 / 100)
        height = int(crop_img2.shape[0] * 800 / 100)
        # dsize
        dsize = (width, height)
        # resize image
        crop_img2 = cv2.resize(crop_img2, dsize)
        #crop_img2 = cv2.resize(crop_img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #crop_img2 = cv2.blur(crop_img2,(3,3))
        #plt.imshow(crop_img2)
        #plt.show()
        string = pytesseract.image_to_string(crop_img2)
        print(string)
        recordToCompare = string.lower()
        return recordToCompare

    def retrieve_text_with_config(self, y, y1, x, x1, params=None, lang_param=None):
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y):int(y1), int(x):int(x1)]

        width = int(crop_img2.shape[1] * 800 / 100)
        height = int(crop_img2.shape[0] * 800 / 100)
        # dsize
        dsize = (width, height)
        # resize image
        crop_img2 = cv2.resize(crop_img2, dsize)

        crop_img2 = cv2.cvtColor(crop_img2, cv2.COLOR_BGR2GRAY)

        # Otsu Tresholding automatically find best threshold value
        _, binary_image = cv2.threshold(crop_img2, 0, 255, cv2.THRESH_OTSU)

        # invert the image colors
        count_white = np.sum(binary_image > 0)
        count_black = np.sum(binary_image == 0)
        if count_black > count_white:
            binary_image = 255 - binary_image

        # Padding
        crop_img2 = cv2.copyMakeBorder(binary_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255))

        # Blur the image
        crop_img2 = cv2.GaussianBlur(crop_img2, (3, 3), 0)

        #This duplicates capture and appends it to original
        #crop_img2 = cv2.hconcat([crop_img2,crop_img2])
        #plt.imshow(crop_img2)
        #plt.show()

        string = pytesseract.image_to_string(crop_img2, lang=lang_param, config=params)
        return string

    def run_vehsim_script(self, ip_address_, script_path, duration_min):
        cmd = "ClientCommands\ClientCommands.exe"
        input_data = os.linesep.join([ip_address_, 'connect', f'open,{script_path}', 'run', os.linesep])
        p = Popen(cmd, stdin=PIPE, bufsize=0)
        p.communicate(input_data.encode('ascii'))
        if p.returncode != 0:
           raise CalledProcessError(p.returncode, cmd)

        seconds = duration_min * 60
        time.sleep(seconds)

        input_data = os.linesep.join([ip_address_, 'stop', os.linesep])
        p = Popen(cmd, stdin=PIPE, bufsize=0)
        p.communicate(input_data.encode('ascii'))
        if p.returncode != 0:
            raise CalledProcessError(p.returncode, cmd)
    