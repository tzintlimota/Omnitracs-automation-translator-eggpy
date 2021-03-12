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
from dateutil.parser import parse
import connection_credentials as cfg
import re
import pytest
import sys


#import pyGPSFeed_IMR

class IVG_ELD_CORE:

    def __init__(self):
        self.img_proc = ImageProcessor('192.168.100.13', 'None', .15)
        #self.img_proc = ImageProcessor(cfg.vnc["ivg_ip"], cfg.vnc["password"], cfg.vnc["precision"])
        self.ivg_common = IVG_Common()

    def search_func(self, search, space):
        search = re.search(r"" + search + "", str(space))
        if search != None:
            return True
        return False

    #Code to discard/accept Certify Day prompt
    def closeCertifyDayPrompt(self):
        print("Discarding/Accepting Certify Day Prompt...")
        total_x, total_y = self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/NotReadyButton/NotReadyButton")
        if total_x == -1:
            print("'Agree' button is clicked because 'Not Ready' is not longer available")
            self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/AgreeButton/AgreeButton")

        #Click on Agree button in case Certify Prompt "Duty Status Spans in more than 1 day"
        if self.img_proc.expect_image("vnc-certifyday-statusspans-pop-up", "ExpectedScreens", 1):
            print("Handling Certify Prompt 'Duty Status Spans in more than 1 day' ")
        #self.goToHOS()


    #Here add the code to close every alert as a function
    def closeLoadInfoAlert(self):
        print("Closing LOAD INFO")
        self.img_proc.click_image_by_max_key_points("IVG_Common/Home/EnterLoadInfoButton/EnterLoadInfoButton")
        self.img_proc.expect_image("vnc-load-enter-info-popup", "ExpectedScreens", 5)
        self.img_proc.click_image_by_max_key_points_offset("please-enter-load-info-label", -40, 60 )
        self.img_proc.send_keys("Test")
        self.img_proc.click_image_by_max_key_points_offset("please-enter-load-info-label", 320, 66 )
        self.img_proc.send_keys("1213")
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        self.img_proc.expect_image("vnc-load-enter-info-popup", "ExpectedScreens", 5) 
        self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SaveButton/SaveButton')


    def changeDriverStatus(self,newStatus, condition, remark1, remark2, complete):
        #CHECAR CHANGE DRIVER STATUS
        self.img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 3)
        self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/StatusTabActive/StatusTabActive')

        self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/ChangeButton/ChangeButton')
        self.img_proc.expect_image('vnc_change_main', 'ExpectedScreens', 3)

        #Aqui hay que poner botones que solo digan OFF On sin Duty
        if newStatus == "OFF":
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/OFF_Status/OFF_Status')
        elif newStatus == "SB":
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SB_Status/SB_Status')
        elif newStatus == "D":
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/DR_Status/DR_Status')
        else:
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/ON_Status/ON_Status')

        if condition != ' ':
            print("Looking for condition: " + condition)
            if condition == 'N':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/None/None', -90, 0)
            elif condition == 'OW':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/OilWell/OilWell', -90, 0)
            elif condition == 'PC':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/PersonalConveyance/PersonalConveyance', -90, 0)
            elif condition == 'RB':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/RestBreak/RestBreak', -90, 0)
            elif condition == 'YM':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/YardMove/YardMove', -90, 0)
            else:
                print("The special condition is not valid")

        if remark1 != ' ':
            self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks1/Remarks1', 0, 50)
            self.img_proc.send_keys(str(remark1))
            self.img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        if remark2 != ' ':
            self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks2/Remarks2', 0, 148)
            self.img_proc.send_keys(str(remark2))

            self.img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        time.sleep(5)
        if complete != 'False' and complete != 'false':
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')
            time.sleep(10)

            self.img_proc.check_md_alert()

    def goToHOS(self):
        self.ivg_common.goToMainScreen()
        self.img_proc.click_image_by_max_key_points("HOS_ELD")

    def goToELD(self):
        self.goToHOS()

        screen = 0
        sString = ""
        #Cambiar las imageneeees para cada uno
        while True :
            if self.img_proc.expect_image("vnc_hos_main", "ExpectedScreens", 0.5):
                sString = "HOS MAIN"
                break
            elif self.img_proc.expect_image("vnc-codriver-login", "ExpectedScreens", 0.5):
                sString = "CODRIVER"
                break
            elif self.img_proc.expect_image("vnc-codriver-login-keyboard", "ExpectedScreens", 0.5):
                sString = "CODRIVER"
                break
            elif self.img_proc.expect_image("vnc-unidentified-profile-screen", "ExpectedScreens", 0.5):
                sString = "UNIDENTIFIED"
                break

        print(sString)

        #self.goToMainScreen()
        #go to hours of service
    def goToHistory(self):
        self.goTo("Load")
        self.img_proc.click_image_by_max_key_points("ELD_Core/LoadTab/HistoryButton/HistoryButton")
        found = self.img_proc.expect_image("vnc-load-history-screen", "ExpectedScreens", 4)
        if found:
            print("Load History Screen")
        else:
            print("Load History not found")


    def getLoadDate(self, TimePoint):
        self.goTo("Load")
        if TimePoint == "Start":
            x, y = self.img_proc.click_image_by_max_key_points_offset("ELD_Core/StatusTab/Start_A/Start_A", 60, -5)
        elif TimePoint == "End":
            x, y = self.img_proc.click_image_by_max_key_points_offset("ELD_Core/StatusTab/Start_A/Start_A", 450, -5)
            x += 355
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y-20):int(y+20), int(x+70-30):int(x+60+100)]

        #plt.imshow(crop_img2)
        #plt.show()
        print(pytesseract.image_to_string(crop_img2))
        loadDate = pytesseract.image_to_string(crop_img2)
        return loadDate

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

    def dayBack(self, page, reset, clicks):
        self.goTo(page)
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        firstAddX, secondAddX, firstAddY, secondAddY = 0,0,0,0
        if page == 'Graph':
            x, y = 90, 175
            x1, y1 = 300, 150
            x2, y2 = 535, 150
            firstAddX, secondAddX, firstAddY, secondAddY = 745, 745, 20, 70
        else:
            x, y  = 95,175
            x1, y1 = 375, 150
            x2, y2 = 550, 150
            firstAddX, secondAddX, firstAddY, secondAddY = 770, 770, 20, 70
        if reset:
            #ACTUALIZAR ESTO A QUE LA FECHA COINCIDA CON LA FECHA DE HOY
            today = date.today()
            currentDay = parse(str(today))
            print("Today's date:", today)
            print(currentDay.day, currentDay.month)
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(y+firstAddY):int(y+secondAddY), int(x+firstAddX-17):int(x+secondAddX+105)]

            print(pytesseract.image_to_string(crop_img2))
            dateDevice = pytesseract.image_to_string(crop_img2)
            dateDevice = parse(str(dateDevice))
            #print("Todays date DEVICE is " + dateDevice.day)
            print(dateDevice.day, dateDevice.month)

            while dateDevice.day != currentDay.day:
                time.sleep(0.5)
                self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
                img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
                crop_img2 = img[int(y+firstAddY):int(y+secondAddY), int(x+firstAddX-17):int(x+secondAddX+105)]

                print(pytesseract.image_to_string(crop_img2))
                dateDevice = pytesseract.image_to_string(crop_img2)
                dateDevice = parse(str(dateDevice))
                #print("Todays date DEVICE is " + dateDevice.day)
                print(dateDevice.day, dateDevice.month)
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", x2, y2)

            print("Cannot go any forward")

        for i in range(clicks):
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", x1, y1)

    def dayForward(self, page, clicks):
        self.goTo(page)
        if page == 'Graph':
            x, y = 535, 150
        else:
            x, y  = 550, 150

        for i in range(clicks):
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", x, y)

            #self.img_proc.click_image_by_max_key_points("ELD_Core/NavigationButtons/Enabled/DayForward/DayForward")

    def certifyAllLogs(self):
        self.goTo("Certify")
        f = open("IVG_var.txt", "w")
        f.write("Certify")
        f.close()

        self.dayBack("Certify", True, 0)
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
            self.dayBack("Certify", False, 1)

        print("Nothing to certify")
        time.sleep(5)
        f = open("IVG_var.txt", "w")
        f.write("None")
        f.close()

    def certifyLogsOfDay(self,page):
        f = open("IVG_var.txt", "w")
        f.write("Certify")
        f.close()

        self.dayBack("Certify", True, page)
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


    def createLoad(self, loadId, Trailer1, Trailer2, Trailer3, BL, StartDate, EndDate, Finish):
        self.goTo("Load")
        self.img_proc.click_image_by_max_key_points("ELD_Core/LoadTab/NewLoadButton/NewLoadButton")
        self.img_proc.expect_image("vnc-load-create-new", "ExpectedScreens", 3)
        self.img_proc.expect_image("vnc-load-create-new-keyboardopen", "ExpectedScreens", 3)
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", 0, 25)
        self.img_proc.send_keys(loadId)
        #Trailer1
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", 600, 25)
        self.img_proc.send_keys(Trailer1)
        #Trailer2
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", 600, 100)
        self.img_proc.send_keys(Trailer2)
        #Trailer3
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", 600, 175)
        self.img_proc.send_keys(Trailer3)
        #BL
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", 0, 250)
        self.img_proc.send_keys(BL)
        #START
        startDate = parse(StartDate)
        endDate = parse(EndDate)

        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", -90, 100)
        self.img_proc.send_keys(str(startDate.month))
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", -60, 100)
        self.img_proc.send_keys(str(startDate.day))
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", -30, 100)
        self.img_proc.send_keys(str(startDate.year))
        #END
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", -90, 180)
        self.img_proc.send_keys(str(endDate.month))
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", -60, 180)
        self.img_proc.send_keys(str(endDate.day))
        self.img_proc.click_image_by_max_key_points_offset("ELD_Core/LoadTab/LoadId/LoadIdRequired", -30, 180)
        self.img_proc.send_keys(str(endDate.year))

        found = self.img_proc.expect_image("vnc-load-create-new-keyboardopen", "ExpectedScreens", 3)
        if found:
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        if Finish:
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')
        else:
            self.img_proc.click_image_by_max_key_points('cancel_btn_active')

    def goToERODS(self):
        print("***Script name: IVG_ELD_CORE.goToERODS***")
        '''This will navigate to the ERODS File Transfer screen'''

        found = self.img_proc.expect_image("vnc-erods-file-transfer-screen", "ExpectedScreens", 2)
        if found:
            print("'ERODS File Transfer' screen is being displayed")
        else:
            self.goTo("DayLog")

            self.img_proc.click_image_by_max_key_points('ELD_Core/DayLogTab/DriverButton/DriverButton')
            time.sleep(1)
            self.img_proc.click_image_by_max_key_points('ELD_Core/DayLogTab/Button/ERODS/ERODS')
            self.img_proc.expect_image("vnc-erods-file-transfer-prompt", "ExpectedScreens", 2)
            print(" Prompt 'ERODS File Transfer' is being displayed")
            self.img_proc.click_image_by_max_key_points('ok_status_login_btn')
            self.img_proc.expect_image('vnc-erods-file-transfer-screen', "ExpectedScreens", 2)
            print("'ERODS File Transfer' screen is being displayed")

    def findTableRecord(self,RecordToFind,ColumnToSearch,StartPoint, FindOrder):
        #CertifyTestCase.findTableRecord
        self.goTo("Certify")
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

        if self.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
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
                    if self.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
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

        self.goTo("Certify")
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
            recordToCompare = self.retrieve_start()
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
            recordToCompare = self.retrieve_duration()
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

    def update_logs(self):
        string = ""
        self.ivg_common.clearAlerts()
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
        time.sleep(1)
        self.goToHOS()
        self.goTo("Days")
        self.img_proc.click_image_by_max_key_points("LogRequestButton")
        while self.img_proc.expect_image("log-request-confirmation", "ExpectedScreens", 1):
            print("Waiting")
            time.sleep(1)
        self.img_proc.click_image_by_max_key_points("ivg_header_alert")

        max_time = datetime.now() + timedelta(seconds=float(300))
        search = None
        while search == None:
            print("Waiting for logs")
            if datetime.now() >= max_time:
                print("Time limit has been exceeded, no logs found")
                break

            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

            crop_img2 = img[int(150):int(480), int(315):int(560)]

            '''calculate the 50 percent of original dimensions'''
            width = int(crop_img2.shape[1] * 600 / 100)
            height = int(crop_img2.shape[0] * 600 / 100)
            # dsize
            dsize = (width, height)
            '''resize image'''
            crop_img2 = cv2.resize(crop_img2, dsize)

            plt.imshow(crop_img2)
            plt.show()

            string += pytesseract.image_to_string(crop_img2)
            string = string.strip()
            print(string)

            search = re.search(r"Log Update|ELD Exempt", string)
            print(search)
        print("LOG UPDATE RECEIVED")

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
        plt.imshow(crop_img2)
        plt.show()
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
        plt.imshow(crop_img2)
        plt.show()

        string = pytesseract.image_to_string(crop_img2, lang=lang_param, config=params)
        return string

    def daylog_get_records_inspector(self,StartPoint, FindOrder, NumRecords):
        self.goTo("DayLog")

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
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #EVENT
            y, y1,x, x1 = 305, 340, 103, 245
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #LOCATION
            y, y1,x, x1 = 305, 340, 255, 374
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #ACCUM MILES
            y, y1,x, x1 = 305, 340, 417, 530
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #Eng. Hrs
            y, y1,x, x1 = 305, 340, 570, 650
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #Record Status
            y, y1,x, x1 = 305, 340, 672, 725
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #Seq ID
            y, y1,x, x1 = 305, 340, 735, 783
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1,'--psm 1 --oem 3 -c tessedit_char_whitelist=0123456789')
            new_rec.append(recordToCompare.strip())
            #COMMENT
            y, y1,x, x1 = 305, 340, 800, 960
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())

            records.append(new_rec)

            if findOrder == "Asc":
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
            else:
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        return records

    def day_log_records_driver(self,StartPoint, FindOrder, NumRecords):
        self.goTo("DayLog")

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
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1, '--psm 6 --oem 3 -c tessedit_char_whitelist=PCONSBYMDF')
            print(recordToCompare)
            new_rec.append(recordToCompare.strip())

            #START
            y, y1, x, x1 = 310, 330, 160, 245
            recordToCompare = self.retrieve_text(y,y1,x,x1)
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
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1, None, 'eng')
            new_rec.append(recordToCompare.strip())

            #CODRIVER
            y, y1, x, x1 = 310, 330, 602, 620
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1, '--psm 6 --oem 3 -c tessedit_char_whitelist=NoYes')
            new_rec.append(recordToCompare.strip())

            #ORIGIN
            y, y1, x, x1 = 310, 330, 645, 730
            recordToCompare = self.retrieve_text_with_config(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())
            #COMMENT
            y, y1, x, x1 = 310, 330, 740, 960
            recordToCompare = self.retrieve_text(y,y1,x,x1)
            new_rec.append(recordToCompare.strip())


            records.append(new_rec)
            if findOrder == "Asc":
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 200)
            else:
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", 550, 420)
        return records



    def find_driver_record(self,RecordToFind,ColumnToSearch,StartPoint, FindOrder):
        #CertifyTestCase.findTableRecord
        self.goTo("DayLog")
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

        if self.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
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

                    if self.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
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

        self.goTo("DayLog")

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

        if self.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
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

                    if self.search_func(str(RecordToFind.lower().strip()), str(recordToCompare.strip())):
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


    def select_driver_from_dropdown(self, driver_id):
            driver_found = False
            unidentified_profile = False

            #Clicks on banner of HOS app to remove highlight of DriverID
            # This because tesseract shows erros when the word is highlighted
            self.img_proc.click_image_by_max_key_points_offset(
                "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                -0, 130)

            #Capture of current screen in the IVG
            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

            #Gets the current DriverID selected
            crop_img2 = img[int(95):int(126), int(42):int(327)]
            current_driver = pytesseract.image_to_string(crop_img2)

            #Removes blank spaces at end/beginning of text
            current_driver = current_driver.strip()

            #Need to replace all O to 0 to fox error of tesseract confusing char with digits.
            driver_id = driver_id.replace("O", "0")
            current_driver = current_driver.replace("O", "0")

            #This compares driverID with values on dropdown to select the expected one.
            if driver_id in current_driver:
                print("Driver ID is already selected")
            else:
                #Click to open DriverID dropdown
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                                                                   -200, 45)

                self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
                img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

                #Selects 2nd option of dropdown
                self.img_proc.click_image_by_max_key_points_offset(
                    "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                    -250, 88)

                time.sleep(1)
                #Flag is set to True if UNIDENTIFIED Profile appears - This is to know if there is a copilot logged in
                if self.img_proc.expect_image('vnc-unidentified-profile-screen', 'ExpectedScreens', 2):
                    unidentified_profile = True

                if driver_id == 'UNIDENTIFIED' and not unidentified_profile:
                    print("Unidentified needs to be selected")
                    #Click to open the dropdown.
                    self.img_proc.click_image_by_max_key_points_offset(
                        "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                         -200, 45)
                    #Selects 3rd option from dropdown
                    self.img_proc.click_image_by_max_key_points_offset(
                        "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                        -250, 115)
                    driver_found = True
                elif driver_id == 'UNIDENTIFIED' and unidentified_profile:
                    print("Already in UNIDENTIFIED profile")
                else:
                    #Case when there is a Driver and Copilot logged in
                    self.img_proc.click_image_by_max_key_points_offset(
                        "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                        -200, 45)

                    time.sleep(1)

                    self.img_proc.click_image_by_max_key_points_offset(
                        "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                        -250, 115)

                    #Selects option to highlight UNIDENTIFIED
                    #This prevents error when the driver text is retrieved
                    self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                        -200, 45)

                    string = self.retrieve_text_with_config(124, 200, 40, 327)

                    string = string.strip()
                    slist = string.splitlines()
                    slist = list(filter(str.strip, slist))

                    for i in range(len(slist)):
                        text = str(slist[i])
                        text = text.replace("O", "0")
                        driver_id = driver_id.replace("O", "0")

                        if driver_id in text and i == 0:
                            self.img_proc.click_image_by_max_key_points_offset(
                                "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                                -250, 65)
                            driver_found = True
                            break

                        if driver_id in text and i == 1:
                            self.img_proc.click_image_by_max_key_points_offset(
                                "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                                -250, 88)
                            driver_found = True
                            break

                if driver_found:
                    print("The DriverID {" + str(slist[i]) + "} has been selected.")
                else:
                    print("The DriverID {" + str(slist[i]) + "} has NOT been selected.")

    def validate_status(self, string):
        #self.goToHOS()
        actual_status = self.retrieve_text(245, 270, 132, 370)
        expected_status = string.lower()
        assert expected_status in actual_status, \
            f"expected_status '{expected_status}' is no substring of '{actual_status}'"

    def get_clock(self, x, x1, y, y1):

        if self.img_proc.expect_image('vnc-summary-screen','ExpectedScreens',1):
            print("Already in Summary page")
        else:
            self.goToHOS()
            self.goTo('Summary')

        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y):int(y1), int(x):int(x1)]
        width = int(crop_img2.shape[1] * 100 / 100)
        height = int(crop_img2.shape[0] * 100 / 100)
        # dsize
        dsize = (width, height)
        # resize image
        crop_img2 = cv2.resize(crop_img2, dsize)
        #crop_img2 = cv2.resize(crop_img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        #crop_img2 = cv2.blur(crop_img2,(3,3))
        plt.imshow(crop_img2)
        plt.show()
        string = pytesseract.image_to_string(crop_img2, config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789:-' )
        print(string)
        recordToCompare = string.lower()
        return recordToCompare

    def get_driving_clock(self):
        clock_val = self.get_clock(840,940,245,280)
        return clock_val

    def get_on_duty_clock(self):
        clock_val = self.get_clock(840,940,275,315)
        return clock_val

    def get_duty_cycle_clock(self):
        clock_val = self.get_clock(840,940,315,355)
        return clock_val

    def get_rest_break_clock(self):
        clock_val = self.get_clock(835,925,365, 395)
        return clock_val

    def review_carrier_edits(self):
        if self.img_proc.expect_image('vnc-edits-carrier-summary', 'ExpectedScreens', 2):
            print('Already in Carrier Edits Screen')
        elif self.img_proc.expect_image('vnc-edits-review-carrier-edits', 'ExpectedScreens', 2):
            self.img_proc.click_image_by_max_key_points('ELD_Core/CarrierEdit/ReviewCarrierEditsButton/ReviewCarrierEditsButton')
            lbl_carrier_edit = self.img_proc.image_exists('ELD_Core/CarrierEdit/YourCarrierHasProposedThisEdit/YourCarrierHasProposedThisEdit')
            if lbl_carrier_edit:
                print("Carrier Edits Screen displayed successfully")
        else:
            self.goToHOS()
            if self.img_proc.expect_image('vnc-edits-review-carrier-edits', 'ExpectedScreens', 2):
                self.img_proc.click_image_by_max_key_points('ELD_Core/CarrierEdit/ReviewCarrierEditsButton/ReviewCarrierEditsButton')
                lbl_carrier_edit = self.img_proc.image_exists('ELD_Core/CarrierEdit/YourCarrierHasProposedThisEdit/YourCarrierHasProposedThisEdit')
                if lbl_carrier_edit:
                    print("Carrier Edits Screen displayed successfully")
            else:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!\n Error: Carrier Edit alert not found. Be sure the Carrier has requested edits.")
                sys.exit(1)

    def accept_unassigned_events(self, uva_type, remark1=None, remark2=None):
        '''if self.img_proc.expect_image('vnc-review-unassigned-driving-event', 'ExpectedScreens', 2):
            print('Already in Please Review All Unassigned Driving Events screen')
        else:
            self.goToHOS()
            self.img_proc.expect_image('vnc-review-unassigned-driving-event', 'ExpectedScreens', 3)

        self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/NextButton/NextButton')

        #Accepting UVA by clicking NEXT button
        text = self.retrieve_text(530, 570, 755, 840)
        if 'reject' in text.lower():
            print('Currently in Review Unassigned Driving Time screen')
            self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/NextButton/NextButton')


        # Click on Status dropdown
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 55, 35)

        if not uva_type:
            print("Selecting D for unassigned driving event")
            self.img_proc.click_image_by_max_key_points_offset(
                'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 45, 70)
        elif uva_type.lower() in 'pc':
            print("Selecting PC for unassigned driving event")
            self.img_proc.click_image_by_max_key_points_offset(
                'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 45, 100)
        elif uva_type.lower() in 'ym':
            print("Selecting YM for unassigned driving event")
            self.img_proc.click_image_by_max_key_points_offset(
                'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 45, 130)

        # Click on first field of remarks to enter a comment
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1', 45, 55)
        if not remark1:
            print("Entering text for default remarks1 'AUTOMATED TESTING'")
            self.img_proc.send_keys('AUTOMATION TESTING')
        else:
            print(f"Entering text for remarks1 {remark1}...")
            self.img_proc.send_keys(remark1)

        # Click to close the remarks1 dropdown
        self.img_proc.click_image_by_max_key_points(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1')

        # Click on the second field of remarks to enter a comment
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1', 545, 50)
        if not remark2:
            print("Entering text for default remarks1 'AUTOMATED TESTING'")
            self.img_proc.send_keys('AUTOMATION x2')
        else:
            print(f"Entering text for remarks1 {remark2}...")
            self.img_proc.send_keys(remark2)

        # Double Click to close the remarks2 dropdown
        self.img_proc.click_image_by_max_key_points(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1')
        self.img_proc.click_image_by_max_key_points(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1')

        # Enter LOCATION value in case the field is empty
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/Location/Location', 45, 50)
        self.img_proc.send_keys('AUTOMATED LOCATION')

        # Click CONFIRM button
        self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/ConfirmButton/ConfirmButton')

        # A prompt to confirm the unassigned driving event appears
        confirm_popup = self.img_proc.expect_image('vnc-unassigned-event-confirm-popup', 'ExpectedScreens', 3)
        assert confirm_popup, f"Confirm Unassigned Driving Event has appeared"'''

        # Click YES to confirm the UVA
        self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/YesButton/YesButton')







    def changeCarrier(self,Carrier, Send):
        pass

    def reviewCarrierEdits(self):
        pass

    def checkRecordStatus(ExpectedValue, RecordToCheck, EditedIndex):
        pass

    def confirmRejectCarrierEdit( BooleanReject):
        pass

    def reviewCarrierEdits2(self):
        pass

    def enterReasonForReject(ReasonForRejecting):
        pass

    def verifyCharactersEntered(ExpectedValue):
        pass

    #ESTOS DICEN FUNCTION
    def getRecord(RecordID, EditedIndex):
        pass

    def getTableValue(ColumnName, RecordID, EditedIndex):
        pass

    def testRecordAge(theRecord, differAge, testAge):
        pass

    #ESTOS DICEN ON
    def compareDates(firstRecord, secondRecord, type):
        pass



    #CertifyTestCase
