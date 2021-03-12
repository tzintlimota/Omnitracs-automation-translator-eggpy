from ImageProcessor import ImageProcessor
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
import sys

from General_Access_Functions import General_Access


class Daylog_Test_Case:
    def __init__(self):
        self.eld_core = IVG_ELD_CORE()
        self.general = General_Access()
        self.img_proc = self.general.img_proc
        #self.img_proc = ImageProcessor(cfg.vnc["ivg_ip"], cfg.vnc["password"], cfg.vnc["precision"])
        self.ivg_common = IVG_Common()

    def daylog_get_records_inspector(self,StartPoint, FindOrder, NumRecords):
        self.general.goTo("DayLog")

        match = self.img_proc.image_exists('ELD_Core/DayLogTab/InspectorButton/InspectorButton')

        if match:
            print("Switching to INSPECTOR profile")
            self.img_proc.click_image_by_max_key_points('ELD_Core/DayLogTab/InspectorButton/InspectorButton')
        else:
            print("Currently in INSPECTOR profile")
        
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
        
        records = []
        for i in range(NumRecords):
            time.sleep(1)

            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            new_rec = []
            #TIME
            y, y1,x, x1 = 305, 340, 0, 95
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip()) 
            #EVENT 
            y, y1,x, x1 = 305, 340, 103, 245
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip()) 
            #LOCATION 
            y, y1,x, x1 = 305, 340, 255, 374
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip()) 
            #ACCUM MILES
            y, y1,x, x1 = 305, 340, 417, 530
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip()) 
            #Eng. Hrs
            y, y1,x, x1 = 305, 340, 570, 650
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip()) 
            #Record Status
            y, y1,x, x1 = 305, 340, 672, 725
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip()) 
            #Seq ID
            y, y1,x, x1 = 305, 340, 735, 783
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1,'--psm 1 --oem 3 -c tessedit_char_whitelist=0123456789')
            new_rec.append(recordToCompare.strip()) 
            #COMMENT
            y, y1,x, x1 = 305, 340, 800, 960
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip()) 

            records.append(new_rec)

            if findOrder == "Asc":
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
            else:
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        return records

    def day_log_records_driver(self,StartPoint, FindOrder, NumRecords):
        self.general.goTo("DayLog")

        match = self.img_proc.image_exists('ELD_Core/DayLogTab/InspectorButton/InspectorButton')

        if match:
            print("Currently in DRIVER profile")
        else:
            print("Switching to DRIVER profile")
            self.img_proc.click_image_by_max_key_points('ELD_Core/DayLogTab/DriverButton/DriverButton')

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
            
            #STATUS

            y, y1, x, x1 = 310, 325, 85, 115
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1, '--psm 6 --oem 3 -c tessedit_char_whitelist=PCONSBYMDF')
            print(recordToCompare)
            new_rec.append(recordToCompare.strip())   
       
            #START
            
            recordToCompare = self.general.retrieve_start()   
            new_rec.append(recordToCompare.strip()) 
       
            self.img_proc.click_image_by_coordinates(150, 300)
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            
            #Duration

            string = ""
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            #y, y1, x, x1 = 310, 330, 242, 320
            for i in range(3):
                '''This defines with region is being captured (hh:mm:ss)'''
                if i == 0:
                    x, x1 = 250, 265
                    time_char = "h "
                elif i == 1:
                    x, x1 = 275, 290
                    time_char = "m "
                else:
                    x, x1 = 300, 320
                    time_char = "s "

                crop_img2 = img[int(310):int(330), int(x):int(x1)]

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
            new_rec.append(string)
                
            #LOCATION
            y, y1, x, x1 = 310, 330, 340, 465
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1, None, 'eng')
            new_rec.append(recordToCompare.strip())

            #CODRIVER
            y, y1, x, x1 = 310, 330, 602, 620
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1, '--psm 6 --oem 3 -c tessedit_char_whitelist=NoYes')
            new_rec.append(recordToCompare.strip())
            
            #ORIGIN
            y, y1, x, x1 = 310, 330, 645, 730
            recordToCompare = self.general.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #COMMENT
            y, y1, x, x1 = 310, 330, 740, 960
            recordToCompare = self.general.retrieve_text(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())

            
            records.append(new_rec)
            if findOrder == "Asc":
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
            else:
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        return records



    def find_driver_record(self,RecordToFind,ColumnToSearch,StartPoint, FindOrder):
        #CertifyTestCase.findTableRecord
        self.general.goTo("DayLog")
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
        
        #Certified Status Start Duration Location CoDriver Origin Comment
        

        if ColumnToSearch == 'Certified':
            x = 0
        elif ColumnToSearch == 'Start':
            x = 2
        elif ColumnToSearch == 'Status':
            x = 1
        elif ColumnToSearch == 'Duration':
            x = 3
        elif ColumnToSearch == 'Origin':
            #ORIGIN
            x = 6
        elif ColumnToSearch == 'Location':
            #LOCATION
            x = 4
            
        elif ColumnToSearch == 'CoDriver':
            x = 5
        else:
            x = 7

        records = self.day_log_records_driver('', '', 1)
        print(records)
        print(records[0][x].lower())
        recordToCompare = records[0][x].lower()
        records = None

        if self.general.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
            print("Found " + str(RecordToFind))
            return records
        else:
            print("Searching")
            found = False
            for i in range(10):
                if found:
                    print("Record Found")
                    print(records)
                    return records
                else:
                    self.img_proc.click_image_by_coordinates(150, 300)
                    self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
                    #self.img_proc.click_image_by_coordinates(150,300)
                    img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
                    
                    records = self.day_log_records_driver('', '', 1)
                    print(records)
                
                    print(records[0][x].lower())
                    recordToCompare = records[0][x].lower()
                 
                    records = None
                    
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


    def find_inspector_record(self,RecordToFind,ColumnToSearch,StartPoint, FindOrder):
        #CertifyTestCase.findTableRecord

        self.general.goTo("DayLog")

        findOrder = ""
        if StartPoint == "Bottom":
            for i in range(10):
                self.img_proc.click_image_by_max_key_points_offset(
                    "IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        elif StartPoint == "Top":
            for i in range(10):
                self.img_proc.click_image_by_max_key_points_offset(
                    "IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
        else:
            print("In the middle of the table")

        if FindOrder == "Asc":
            findOrder = "Asc"
        elif FindOrder == "Desc":
            findOrder = "Desc"
        else:
            findOrder = "Asc"

        if ColumnToSearch == 'Time':
            x = 0
        elif ColumnToSearch == 'Location':
            x = 2
        elif ColumnToSearch == 'Event':
            x = 1
        elif ColumnToSearch == 'Odometer':
            x = 3
        elif ColumnToSearch == 'Eng.Hrs':
            #ORIGIN
            x = 4
        elif ColumnToSearch == 'Record Status':
            #LOCATION
            x = 5
            
        elif ColumnToSearch == 'Seq.ID':
            x = 6
        else:
            x = 7

        records = self.daylog_get_records_inspector('', '', 1)
        print(records)
        print(records[0][x].lower())
        recordToCompare = records[0][x].lower()
        records = None
        
        #Certified Status Start Duration Location CoDriver Origin Comment

        if self.general.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
            print("Found " + str(RecordToFind))
            return records
        else:
            print("Searching")
            found = False
            for i in range(10):
                if found:
                    print("Record Found")
                    print(records)
                    return records
                else:
                    self.img_proc.click_image_by_coordinates(150, 300)
                    self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
                    #self.img_proc.click_image_by_coordinates(150,300)
                    img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
                    
                    records = self.daylog_get_records_inspector('', '', 1)
                    print(records)
                
                    print(records[0][x].lower())
                    recordToCompare = records[0][x].lower()
            
                    records = None
                    
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
