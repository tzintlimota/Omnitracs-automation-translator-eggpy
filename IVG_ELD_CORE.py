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


#import pyGPSFeed_IMR

class IVG_ELD_CORE:

    def __init__(self):
        self.img_proc = ImageProcessor('192.168.100.13', 'None', .15)
        #self.img_proc = ImageProcessor(cfg.vnc["ivg_ip"], cfg.vnc["password"], cfg.vnc["precision"])
        self.ivg_common = IVG_Common()

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

        plt.imshow(crop_img2)
        plt.show()       
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
        plt.imshow(crop_img2)
        plt.show()
        string = pytesseract.image_to_string(crop_img2)
        recordToCompare = string.lower()   
        print(recordToCompare)
        print(RecordToFind.lower())

        if str(recordToCompare.strip()) == str(RecordToFind.lower().strip()):
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
                    plt.imshow(crop_img2)
                    plt.show()
                    string = pytesseract.image_to_string(crop_img2)
                    recordToCompare = string.lower()   
                    print(recordToCompare)
                    if str(recordToCompare.strip()) == str(RecordToFind.lower().strip()):
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

    def select_driver_from_dropdown(self, driver_id):
        driver_found = False
        unidentified_profile = False

        self.img_proc.click_image_by_max_key_points_offset(
            "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
            -0, 130)

        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

        #Gets the current DriverID
        crop_img2 = img[int(95):int(126), int(42):int(327)]
        current_driver = pytesseract.image_to_string(crop_img2)
        current_driver = current_driver.strip()
        driver_id = driver_id.replace("O","0")
        current_driver = current_driver.replace("O", "0")
        print(driver_id)
        print(current_driver)

        if driver_id in current_driver:
            print("Driver ID is already selected")
        else:
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                                                               -200, 45)

            self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
            img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

            self.img_proc.click_image_by_max_key_points_offset(
                "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                -200, 45)

            self.img_proc.click_image_by_max_key_points_offset(
                "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                -250, 88)

            time.sleep(2)
            if self.img_proc.expect_image('vnc-unidentified-profile-screen', 'ExpectedScreens', 2):
                unidentified_profile = True
                print("On UNIDENTIFIED profile")

            if driver_id == 'UNIDENTIFIED' and not unidentified_profile:
                print("Unidentified needs to be selected")
                self.img_proc.click_image_by_max_key_points_offset(
                    "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                     -200, 45)

                self.img_proc.click_image_by_max_key_points_offset(
                    "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                    -250, 115)
                driver_found = True
            else:
                print('There are two drivers LOGGED IN')
                self.img_proc.click_image_by_max_key_points_offset(
                    "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                    -200, 45)

                time.sleep(1)

                self.img_proc.click_image_by_max_key_points_offset(
                    "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                    -250, 115)

                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
                -200, 45)

                time.sleep(1)

                self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
                img = cv2.imread(os.getcwd() + '/Images/ExpectedScreens/last_screen.png')

                # Gets the current DriverID
                crop_img2 = img[int(124):int(200), int(40):int(327)]
                plt.imshow(crop_img2)
                plt.show()

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

                string = pytesseract.image_to_string(crop_img2)

                string = string.strip()
                slist = string.splitlines()
                slist = list(filter(str.strip, slist))

                for i in range(len(slist)):
                    print("-----------------------")
                    print(i)
                    text = str(slist[i])
                    text = text.replace("O", "0")
                    driver_id = driver_id.replace("O", "0")
                    print(str(text) + " " + str(driver_id))
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
