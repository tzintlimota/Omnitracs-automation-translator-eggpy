#import pytesseract
from IVG_Common import IVG_Common
import os
import cv2
import time
from datetime import datetime, timedelta, date
import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from dateutil.parser import parse
import connection_credentials as cfg
import re
import pytest
import sys

from General_Access_Functions import General_Access


class Certify_Test_Case(object):
    def __init__(self, general):
        self.eld_core = IVG_ELD_CORE(general)
        self.general = general
        self.img_proc = self.general.img_proc
        self.ivg_common = IVG_Common(general)

    def certifyAllLogs(self):
        self.general.goTo("Certify")
        f = open("IVG_var.txt", "w")
        f.write("Certify")
        f.close()
        
        self.eld_core.dayBack("Certify", True, 0)
        x, y  = 95,175
        firstAddX, secondAddX, firstAddY, secondAddY = 500, 500, 20, 70
   
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y+firstAddY):int(y+secondAddY), int(x+firstAddX-17):int(x+secondAddX+100)]
        print(pytesseract.image_to_string(crop_img2))
        certifiedDays = str(pytesseract.image_to_string(crop_img2))


        while certifiedDays[0] !=  "8" and (certifiedDays[0] != "1" or certifiedDays[1] != "5"):
            self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/CertifyButton/CertifyButton")
            self.img_proc.click_image_by_max_key_points("AgreeButton")
            self.img_proc.expect_image("vnc_certify_tab_main", "ExpectedScreens", 10)
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(y+firstAddY):int(y+secondAddY), int(x+firstAddX-17):int(x+secondAddX+100)]
            print(pytesseract.image_to_string(crop_img2))
            certifiedDays = str(pytesseract.image_to_string(crop_img2))
            self.eld_core.dayBack("Certify", False, 1)

        print("Nothing to certify")
        time.sleep(5)
        f = open("IVG_var.txt", "w")
        f.write("None")
        f.close()
    
    def certifyLogsOfDay(self,page):
        f = open("IVG_var.txt", "w")
        f.write("Certify")
        f.close()
        
        self.eld_core.dayBack("Certify", True, page)
        x, y  = 95,175
        firstAddX, secondAddX, firstAddY, secondAddY = 500, 500, 20, 70
   
        self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/CertifyButton/CertifyButton")
        self.img_proc.click_image_by_max_key_points("AgreeButton")
        self.img_proc.expect_image("vnc_certify_tab_main", "ExpectedScreens", 10)

        print("Nothing to certify")
        time.sleep(5)
        f = open("IVG_var.txt", "w")
        f.write("None")
        f.close()

    def findTableRecord(self,RecordToFind,ColumnToSearch,StartPoint, FindOrder):
        #CertifyTestCase.findTableRecord
        self.general.goTo("Certify")
        findOrder = ""
        if StartPoint =="Bottom":
            for i in range(10):
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        elif StartPoint =="Top":
            for i in range(10):
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
        else:
            print("In the middle of the table")

        if FindOrder == "Asc":
            findOrder = "Asc"
        elif FindOrder == "Desc":
            findOrder = "Desc"
        else:
            findOrder = "Asc"
        
        if ColumnToSearch == 'Start':
            y, y1,x, x1 = 285, 310, 30, 110
        elif ColumnToSearch == 'Status':
            y, y1,x, x1 = 285, 310, 115, 245
        elif ColumnToSearch == 'Duration':
            y, y1,x, x1 = 285, 310, 320, 445
        elif ColumnToSearch == 'Location':
            y, y1,x, x1 = 285, 310, 445, 600
        elif ColumnToSearch == 'Origin':
            y, y1,x, x1 = 285, 310, 850, 970
        else:
            y, y1,x, x1 = 285, 310, 90, 115

        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y):int(y1), int(x):int(x1)]
        #calculate the 50 percent of original dimensions
        width = int(crop_img2.shape[1] * 600 / 100)
        height = int(crop_img2.shape[0] * 600 / 100)
        # dsize
        dsize = (width, height)
        # resize image
        crop_img2 = cv2.resize(crop_img2, dsize)
        #plt.imshow(crop_img2)
        #plt.show()
        string = pytesseract.image_to_string(crop_img2)
        recordToCompare = string.lower()   
        print(recordToCompare)
        print(RecordToFind.lower())

        if self.general.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
            print("Found " + str(RecordToFind))
        else:
            print("Searching")
            found = False
            for i in range(10):
                if found:
                    print("Record Found")
                    break
                else:
                    self.img_proc.click_image_by_coordinates(150, 300)
                    self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
                    #self.img_proc.click_image_by_coordinates(150,300)
                    img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
                    crop_img2 = img[int(y):int(y1), int(x):int(x1)]
                    #calculate the 50 percent of original dimensions
                    width = int(crop_img2.shape[1] * 600 / 100)
                    height = int(crop_img2.shape[0] * 600 / 100)
                    # dsize
                    dsize = (width, height)
                    # resize image
                    crop_img2 = cv2.resize(crop_img2, dsize)
                    #plt.imshow(crop_img2)
                    #plt.show()
                    string = pytesseract.image_to_string(crop_img2)
                    recordToCompare = string.lower()   
                    print(recordToCompare)
                    if self.general.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
                        found = True
                        print("Found " + str(RecordToFind))
                        '''if findOrder == 'Asc':
                            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
                        else:
                            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
                        self.img_proc.click_image_by_coordinates(150,300)'''
                    else:
                        if findOrder == "Asc":
                            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
                        else:
                            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)


    def getTable(self, StartPoint, FindOrder, NumRecords):
        
        self.general.goTo("Certify")
        findOrder = ""
        
        if StartPoint =="Bottom":
            for i in range(2):
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        elif StartPoint =="Top":
            for i in range(2):
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
        else:
            print("In the middle of the table")

        if FindOrder == "Asc":
            findOrder = "Asc"
        elif FindOrder == "Desc":
            findOrder = "Desc"
        else:
            findOrder = "Asc"
        
        records = []
        for i in range(NumRecords):
            time.sleep(1)
            self.img_proc.click_image_by_coordinates(150, 300)
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            new_rec = []
            #CERTIFIED
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(280):int(305), int(0):int(40)]
            
            string = pytesseract.image_to_string(crop_img2)
            recordToCompare = string.lower() 
            color = self.img_proc.color_check(20,20 ,crop_img2)
            print("COLOR")
            print(color)
            
            if color == 'green':
                new_rec.append("Certified")
            else:
                new_rec.append("Empty")
            
            #START
            self.img_proc.click_image_by_coordinates(150, 300)
            recordToCompare = self.general.retrieve_start()
            new_rec.append(recordToCompare.strip())   
       
            #STATUS
            y, y1,x, x1 = 285, 310, 115, 245
            self.img_proc.click_image_by_coordinates(150, 300)
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(y):int(y1), int(x):int(x1)]
            #calculate the 50 percent of original dimensions
            width = int(crop_img2.shape[1] * 1200 / 400)
            height = int(crop_img2.shape[0] * 1200 / 400)
            # dsize
            dsize = (width, height)
            # resize image
            #crop_img2 = cv2.resize(crop_img2, dsize)
            crop_img2 = cv2.resize(crop_img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

            string = pytesseract.image_to_string(crop_img2, lang='eng', config="--psm 6")
            #string2 = ''.join(i for i in string if i.isalnum())
            recordToCompare = string.lower()
            new_rec.append(recordToCompare.strip())    

            #Duration
            recordToCompare = self.general.retrieve_duration()
            new_rec.append(recordToCompare.strip())

            #LOCATION
            y, y1,x, x1 = 285, 310, 445, 600
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(y):int(y1), int(x):int(x1)]
            #calculate the 50 percent of original dimensions
            width = int(crop_img2.shape[1] * 800 / 100)
            height = int(crop_img2.shape[0] * 800 / 100)
            # dsize
            dsize = (width, height)
            # resize image
            #crop_img2 = cv2.resize(crop_img2, dsize)
            crop_img2 = cv2.resize(crop_img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            '''plt.imshow(crop_img2)
            plt.show()'''
            
            custom_oem_psm_config = r'--oem 1 --psm 13'
            string = pytesseract.image_to_string(crop_img2, lang='eng', config=custom_oem_psm_config)
            recordToCompare = string.lower()
            new_rec.append(recordToCompare.strip())    
            
            #ORIGIN
            y, y1,x, x1 = 285, 310, 850, 960
            self.img_proc.click_image_by_coordinates(150, 300)
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")

            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            
            crop_img2 = img[int(y):int(y1), int(x):int(x1)]
            #calculate the 50 percent of original dimensions
            width = int(crop_img2.shape[1] * 600 / 100)
            height = int(crop_img2.shape[0] * 600 / 100)
            # dsize
            dsize = (width, height)
            # resize image
            crop_img2 = cv2.resize(crop_img2, dsize)
            #plt.imshow(crop_img2)
            #plt.show()
            
            string = pytesseract.image_to_string(crop_img2, lang='eng', config="--psm 8")
            #string = pytesseract.image_to_string(crop_img2)
            recordToCompare = string.lower() 
            new_rec.append(recordToCompare.strip()) 

            records.append(new_rec)
            if findOrder == "Asc":
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
            else:
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        return records

    