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

    def retrieve_duration(self):
        string = ""
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')

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

    def retrieve_start(self, screen):
        string = ""
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')

        if screen.lower() == 'certify':
            y, y1 = 285, 310
        else:
            y, y1 = 310, 325


        for i in range(3):

            '''This defines with region is being captured (hh:mm:ss) for CERTIFY screen'''
            if screen.lower() == 'certify':
                if i == 0:
                    x, x1 = 34, 56
                    time_char = ":"
                elif i == 1:
                    x, x1 = 57, 77
                    time_char = ":"
                else:
                    x, x1 = 80, 100
                    time_char = ""
            else:
                '''This defines with region is being captured (hh:mm:ss) for DAYLOG screen'''
                if i == 0:
                    x, x1 = 170, 189
                    time_char = ":"
                elif i == 1:
                    x, x1 = 192, 206
                    time_char = ":"
                else:
                    x, x1 = 210, 235
                    time_char = ""

            crop_img2 = img[int(y):int(y1), int(x):int(x1)]
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
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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

    def run_vehsim_script(self, ip_address, script_path, duration_min=0):
        print("*** General_Access_Functions.run_vehsim_script ***")
        cmd = self.img_proc.get_project_root_directory() + "\ClientCommands\ClientCommands.exe"
        input_data = os.linesep.join([ip_address, 'connect', f'open,{script_path}', 'run', os.linesep])
        p = Popen(cmd, stdin=PIPE, bufsize=0)
        p.communicate(input_data.encode('ascii'))
        if p.returncode != 0:
           raise CalledProcessError(p.returncode, cmd)

        if duration_min > 0:
            seconds = duration_min * 60
            time.sleep(seconds)
        print(f">>>> The Vehicle Simulator script {script_path} has been loaded and RUN")

    def stop_vehsim_script(self, ip_address):
        print("*** General_Access_Functions.stop_vehsim_script ***")
        cmd = self.img_proc.get_project_root_directory() + "\ClientCommands\ClientCommands.exe"
        input_data = os.linesep.join([ip_address, 'stop', os.linesep])
        p = Popen(cmd, stdin=PIPE, bufsize=0)
        p.communicate(input_data.encode('ascii'))
        if p.returncode != 0:
            raise CalledProcessError(p.returncode, cmd)
        print(f">>>> The Vehicle Simulator script has been STOPPED")
