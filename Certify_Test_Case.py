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
from Daylog_Test_Case import Daylog_Test_Case
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
        self.daylog = Daylog_Test_Case(general)

    def certifyAllLogs(self):
        self.eld_core.goTo("Certify")
        f = open("IVG_var.txt", "w")
        f.write("Certify")
        f.close()
        
        self.eld_core.dayBack("Certify", True, 0)
        x, y  = 95,175
        firstAddX, secondAddX, firstAddY, secondAddY = 500, 500, 20, 70
   
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y+firstAddY):int(y+secondAddY), int(x+firstAddX-17):int(x+secondAddX+100)]
        print(pytesseract.image_to_string(crop_img2))
        certifiedDays = str(pytesseract.image_to_string(crop_img2))


        while certifiedDays[0] !=  "8" and (certifiedDays[0] != "1" or certifiedDays[1] != "5"):
            self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/CertifyButton/CertifyButton")
            self.img_proc.click_image_by_max_key_points("AgreeButton")
            self.img_proc.expect_image("vnc_certify_tab_main", "ExpectedScreens", 10)
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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
        self.eld_core.goTo("Certify")
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

        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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
                    img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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

    def clickOnTableStatus(self, RecordToFind):
        self.findTableRecord(RecordToFind, 'Status', 'Bottom', 'Asc')

    def getTable(self, StartPoint, FindOrder, NumRecords):
        print('*** Certify_Test_Case.getTable ***')
        found = self.img_proc.expect_image('vnc-hos-certify-screen', 'ExpectedScreens', 3)

        if found:
            print('Already in CERTIFY screen')
        else:
            self.eld_core.goTo("Certify")

        findOrder = ""
        
        if StartPoint =="Bottom":
            self.daylog.go_to_bottom()
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
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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
            recordToCompare = self.general.retrieve_start('certify')
            new_rec.append(recordToCompare.strip())   
       
            #STATUS
            y, y1,x, x1 = 285, 310, 115, 300
            self.img_proc.click_image_by_coordinates(150, 300)
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())

            #Duration
            recordToCompare = self.general.retrieve_duration()
            new_rec.append(recordToCompare.strip())

            #LOCATION
            y, y1,x, x1 = 285, 310, 445, 600
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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

            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            
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
        print(">>>> Certify Records Retrieved: \n" + str(records))
        return records

    
    def edit_log(self, certifyAfter, newStatus, firstRemark, secondRemark, Continue, Finish):
        #self.eld_core.goToHOS()
        self.eld_core.goTo('Certify')
        for i in range(10):
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
        self.img_proc.click_image_by_coordinates(150, 300)

        self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/EditButton/Enabled/Enabled")

        newStatus = newStatus.lower()

        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 195)

        if newStatus == 'off':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 205)
        elif newStatus == 'on':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 270)
        elif newStatus == 'sb':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 235)
            
        elif newStatus == 'd':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 295)
    
        #OBTENER LA POSICION VACIA EN POSITION
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 250)
        self.img_proc.send_keys('Test')
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 0, 250)
        self.img_proc.send_keys(firstRemark)
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 300, 270)
        self.img_proc.send_keys(secondRemark)
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        
        if Continue:
            self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/NextButton/NextButton")
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 0, 150)
            self.img_proc.send_keys('Test')
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
            if Finish:
                self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SaveButton/SaveButton')
                self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/CertifyButton/CertifyButton')
                if certifyAfter:
                    self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/AgreeButton/AgreeButton')
                else:
                    self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/NotReadyButton/NotReadyButton')

    
    def select_new_status(self, newStatus, DropdownLocation, exception):
        newStatus = newStatus.lower()
       
        exception = exception.lower()
        DropdownLocation = DropdownLocation.lower()


        if DropdownLocation == 'top':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 195)
            if newStatus == 'off':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 205)
            elif newStatus == 'on':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 270)
            elif newStatus == 'sb':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 235)
            elif newStatus == 'd':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 295)
            
            if exception == 'ow':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 195)
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 235)
            elif exception == 'pc':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 195)
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 265)
            elif exception == 'ym':  
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 195)
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 235)
        else:
            
            self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SplitButton/SplitButton')

            time.sleep(2)

            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 315)
            if newStatus == 'off':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 350)
            elif newStatus == 'on':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 400)
            elif newStatus == 'sb':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 375)
            elif newStatus == 'd':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 440)
            
            if exception == 'ow':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 315)
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 375)
            elif exception == 'pc':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 315)
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 410)
            elif exception == 'ym':  
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 350, 315)
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 375)
        
    def split_log(self,certifyAfter, splitStatus, originalFirstRemark, splitFirstRemark,originalSecondRemark,splitSecondRemark, Location, Continue, Finish):
        f = open("IVG_var.txt", "w")
        f.write("Certify")
        f.close()
        
        #Click edit
        self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/EditButton/Enabled/Enabled")

        newStatus = splitStatus.lower()

        self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SplitButton/SplitButton')

        time.sleep(2)
        
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 315)
        if newStatus == 'off':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 350)
        elif newStatus == 'on':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 400)
        elif newStatus == 'sb':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -345, 375)
        elif newStatus == 'd':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 440)
        
        
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(450):int(480), int(20):int(250)]

        crop_img2 = cv2.resize(crop_img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #plt.imshow(crop_img2)
        #plt.show()
        string = pytesseract.image_to_string(crop_img2)
        print(len(string))
        
        if len(string) == 1:
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -300, 400)
            self.img_proc.send_keys('Test')
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 0, 250)
        self.img_proc.send_keys(originalFirstRemark)
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 300, 270)
        self.img_proc.send_keys(originalSecondRemark)
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        
        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 0, 390)
        self.img_proc.send_keys(splitFirstRemark)
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 300, 400)
        self.img_proc.send_keys(splitSecondRemark)
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        if Continue:
            self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/NextButton/NextButton")
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 0, 150)
            self.img_proc.send_keys('Test')
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
            if Finish:
                self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SaveButton/SaveButton')
                self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/CertifyButton/CertifyButton')
                if certifyAfter:
                    self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/AgreeButton/AgreeButton')
                else:
                    self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/NotReadyButton/NotReadyButton')

        
        f = open("IVG_var.txt", "w")
        f.write("None")
        f.close()
    
    #GetStatusDropdownValues
    #GetExceptionDropdownValues

    def getStatusDropdownValues(self, DropdownLocation):

        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(420):int(445), int(15):int(250)]

        crop_img2 = cv2.resize(crop_img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #plt.imshow(crop_img2)
        #plt.show()
        string = pytesseract.image_to_string(crop_img2)
        print(string)

        
        if DropdownLocation == 'Bottom' and len(string) < 3:
            self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SplitButton/SplitButton')
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 315)

            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 440)
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 315)
        
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(410):int(520), int(15):int(100)]

        elif DropdownLocation == 'Bottom' and len(string) > 3:
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 315)

            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 440)
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 315)
        
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(410):int(520), int(15):int(100)]

            
        elif DropdownLocation != 'Bottom' and len(string) > 3:
            self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SplitButton/SplitButton')
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 195)

            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 295)
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 195)
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(270):int(380), int(19):int(100)]

            
        else:
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 195)

            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -350, 295)
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -325, 195)
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(270):int(380), int(19):int(100)]

        string = pytesseract.image_to_string(crop_img2)
        string += 'D'
        return string


    def getExceptionDropdownValues(self, DropdownLocation):
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(420):int(445), int(15):int(250)]

        crop_img2 = cv2.resize(crop_img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #plt.imshow(crop_img2)
        #plt.show()
        string = self.general.retrieve_text(int(420), int(445), int(15), int(250))
        self.img_proc.click_image_by_max_key_points("IVG_Common/Home/HoursofServicePage/HoursofServicePage")
        print('click should have happened')
        if DropdownLocation == 'Bottom' and len(string) < 3:
            print('bOTTOM')
            self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SplitButton/SplitButton')

            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 315)
        
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(410):int(470), int(625):int(668)]
            #string = pytesseract.image_to_string(crop_img2)
            string = self.general.retrieve_text_with_config(int(410), int(470), int(625), int(668), '--psm 6 --oem 3 -c tessedit_char_whitelist=PCYM', 'eng')

            
            crop_img2 = img[int(410):int(495), int(625):int(668)]
            #string += pytesseract.image_to_string(crop_img2)
            string += self.general.retrieve_text_with_config(int(410), int(495), int(625), int(668), '--psm 6 --oem 3 -c tessedit_char_whitelist=PCYM' , 'eng')


        elif DropdownLocation == 'Bottom' and len(string) > 3:
            print('More than 1 special condition')
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 315)
        
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
       
            crop_img2 = img[int(410):int(470), int(625):int(668)]
            #string = pytesseract.image_to_string(crop_img2)
            string = self.general.retrieve_text(int(410), int(470), int(625), int(668))

            crop_img2 = img[int(410):int(495), int(625):int(668)]
            #string += pytesseract.image_to_string(crop_img2)
            string += self.general.retrieve_text(int(410), int(495), int(625), int(668))


            
        elif DropdownLocation != 'Bottom' and len(string) > 3:
            print('TOP')
            self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SplitButton/SplitButton')
            
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 195)

            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(270):int(330), int(625):int(668)]
            #string = pytesseract.image_to_string(crop_img2)
            string = self.general.retrieve_text(int(270),int(330), int(625),int(668))
            #crop_img2 = img[int(270):int(355), int(625):int(668)]
            #string += pytesseract.image_to_string(crop_img2)
            string += self.general.retrieve_text(int(270),int(355), int(625),int(668))


            
        else:
            print('ELSE')
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 250, 195)
            
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(270):int(330), int(625):int(668)]
            string = pytesseract.image_to_string(crop_img2) 
            crop_img2 = img[int(270):int(355), int(625):int(668)]
            string += pytesseract.image_to_string(crop_img2)


        #plt.imshow(crop_img2)
        #plt.show()

        #string = pytesseract.image_to_string(crop_img2)
        print(string)
        return string

    def getCertifyDateScreenDate(self):
        print ('***Certify_Test_Case.getCertifyDateScreenDate***')
        #self.eld_core.goTo("Certify")
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(200):int(240), int(850):int(975)]
        plt.imshow(crop_img2)
        plt.show()
        string = pytesseract.image_to_string(crop_img2)
        print(string)
        return string

    def verifyCertifyButtonStatus(self):

        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(510):int(590), int(870):int(1000)]
        plt.imshow(crop_img2)
        plt.show()
        color = self.img_proc.color_check(50,45, crop_img2)
        print(color)
        if color == 'gray active':
            print('Certify Button is enabled')
        else:
            print('Certify Button is disabled')
    
    def editTimeField(self, section, value):
        print ('***Certify_Test_Case.editTimeField***')
        #self.eld_core.goTo("Certify")
        section = section.lower()

        if section == 'hrs':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -210, 180)
        elif section == 'min':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -180, 180)
        elif section == 'sec':
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -140, 180)
        
        self.img_proc.send_keys(value)
        
        time.sleep(3)
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        
     
    def verifyEditButtonExist(self, enabled):
        print ('***Certify_Test_Case.verifyEditButtonExist***')
        #self.eld_core.goTo("Certify")
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(500):int(650), int(720):int(850)]
        plt.imshow(crop_img2)
        plt.show()
        string = pytesseract.image_to_string(crop_img2)
        print(string)
        color = self.img_proc.color_check(795,550 ,img)
        print(color)
        
        if enabled:
            if color == 'gray active':
                print("The button is displayed and enabled")
                return True
            else:
                print("The button is displayed and disabled")
                return False
        elif not enabled:
            if color == 'gray active':
                print("The button is displayed and enabled")
                return False
            else:
                print("The button is displayed and disabled")
                return True
        
        if len(string) < 3:
            print("The button is not displayed")
        else:
            print("The button is displayed")
 

    def getTableRecord(self, recordIndex):
        print ('***Certify_Test_Case.getTableRecord***')
        
        found = self.img_proc.expect_image('vnc-hos-certify-screen', 'ExpectedScreens', 3)

        if found:
            print('Already in CERTIFY screen')
        else:
            self.eld_core.goTo("Certify")


        for i in range(10):
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
        
        records = []
        for i in range(recordIndex):
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)

        time.sleep(1)
        self.img_proc.click_image_by_coordinates(150, 300)
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        new_rec = []
        
        #START
        self.img_proc.click_image_by_coordinates(150, 300)
        recordToCompare = self.general.retrieve_start('certify')
        new_rec.append(recordToCompare.strip())   
    
        #STATUS
        y, y1,x, x1 = 285, 310, 115, 300
        self.img_proc.click_image_by_coordinates(150, 300)
        recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
        new_rec.append(recordToCompare.strip())

        #Duration
        recordToCompare = self.general.retrieve_duration()
        new_rec.append(recordToCompare.strip())

        #LOCATION
        y, y1,x, x1 = 285, 310, 445, 600
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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

        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        
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

        return records[0]

    def verifyRecordStatusOrigin(self, recordIndex, columnStatus, columnOrigin):
        record = self.getTableRecord(recordIndex)
        print(record)
        if self.general.search_func(columnStatus.lower(), record[1].lower()):
            print("Column Status is a match " + str(record[1]))
        else:
            print("Column Status is NOT a match ")
        if self.general.search_func(columnOrigin.lower(), record[4].lower()):
            print("Column Origin is a match " + str(record[4]))
        else:
            print("Column Origin is NOT a match ")
    
    def TimeFormat(self, RecordTime):
        print ('***Certify_Test_Case.TimeFormat***')
        time_start_pattern = r'\d\d:\d\d:\d\d'      

        try:
            time_start_found = re.search(time_start_pattern, str(RecordTime))
            if time_start_found != None:
                hour = int(RecordTime[0:2])
                minute = int(RecordTime[3:5])
                second = int(RecordTime[6:7])
                
                if (hour >= 0 and hour <= 23) and (minute >= 0 and minute <= 59) and (second >= 0 and second <= 59): 
                    print("Correct Format " + RecordTime)
                else:
                    print("Format not correct " + RecordTime)
            else:
                print("Format not correct "  + RecordTime)
        except Exception:
            print("Format not correct "  + RecordTime)

    def DateFormat(self, RecordDate):
        print ('***Certify_Test_Case.TimeFormat***')
        date_start_pattern = r"[\d]{1,2}/[\d]{1,2}/[\d]{4}"          

        try:
            date_start_found = re.search(date_start_pattern, str(RecordDate))

            if date_start_found != None:
                month = int(RecordDate[0:2])
                day = int(RecordDate[3:5])
                year = int(RecordDate[6:])
                
                if (month >= 0 and month <= 12) and (day >= 0 and day <= 31) and (year >= 0 and year <= 9999): 
                    print("Correct Format " + RecordDate)
                else:
                    print("Format not correct " + RecordDate)
            else:
                print("Format not correct "  + RecordDate)
        except Exception:
            print("Format not correct EXCEPTION "  + RecordDate)

    def ValidateVirtualStatus(self, certificationStatus):
        
        print ('***Certify_Test_Case.ValidateVirtualStatus***')
        self.img_proc.expect_image('vnc-certifyday-statusspans-pop-up', 'ExpectedScreens', 5)

        f = open("IVG_var.txt", "w")
        f.write("Certify")
        f.close()
        
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
    
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        #img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/vnc-certifyday-statusspans-pop-up.png')
        crop_img2 = img[int(305):int(330), int(200):int(500)]


        string = pytesseract.image_to_string(crop_img2)
        print(string)
        
        more_thanOne_found = re.search('spans more than one', string)

        if more_thanOne_found != None and True:
            print("More than ONE")
            self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/AgreeButton/AgreeButton')
        elif more_thanOne_found == None and False:
            print("Not more than one")
            self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/NotReadyButton/NotReadyButton')
        
        f = open("IVG_var.txt", "w")
        f.write("None")
        f.close()
      


        
  

