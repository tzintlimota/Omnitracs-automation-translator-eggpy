from ImageProcessor import ImageProcessor
#import pytesseract
import os
import cv2
import time
from datetime import datetime, timedelta
import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
#import pyGPSFeed_IMR

class IVG_ELD_CORE:

    def __init__(self):
        self.img_proc = ImageProcessor('192.168.100.13', 'None', .15)

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
            self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/AgreeButton/AgreeButton")
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
        self.goToMainScreen()
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

        if page == 'Graph':
            x, y = 90, 175
            x1, y1 = -150, 175
        else:
            x, y  = 95,175
            x1, y1 = -80, 175
       
        if reset:
            for i in range(1):
                time.sleep(0.5)
                self.img_proc.click_image_by_max_key_points_offset("ivg_header_alert", x, y)

            print("Cannot go any forward")
        
        for i in range(clicks):
            self.img_proc.click_image_by_max_key_points_offset("ivg_header_alert", x1, y1)

    def dayForward(self, page, clicks):
        self.goTo(page)
        if page == 'Graph':
            x, y = 90, 175
        else:
            x, y  = 95,175
        
        for i in range(clicks):
            self.img_proc.click_image_by_max_key_points_offset("ivg_header_alert", x, y)

            #self.img_proc.click_image_by_max_key_points("ELD_Core/NavigationButtons/Enabled/DayForward/DayForward")

    def changeCarrier(Carrier, Send):
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
