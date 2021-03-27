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
import re
import pytest
import sys
from General_Access_Functions import General_Access


class IVG_ELD_CORE(object):

    def __init__(self, general):
        self.general = general
        self.img_proc = self.general.img_proc
        self.ivg_common = IVG_Common(general)
        

    #Code to discard/accept Certify Day prompt
    def closeCertifyDayPrompt(self):
        print('*** IVG_ELD_Core.closeCertifyDayPrompt ***')
        print("Discarding/Accepting Certify Day Prompt...")

        self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/AgreeButton/AgreeButton")
        '''total_x, total_y = self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/NotReadyButton/NotReadyButton")
        if total_x == -1:
            print("'Agree' button is clicked because 'Not Ready' is not longer available")
            self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/AgreeButton/AgreeButton")'''

        #Click on Agree button in case Certify Prompt "Duty Status Spans in more than 1 day"
        if self.img_proc.expect_image("vnc-certifyday-statusspans-pop-up", "ExpectedScreens", 1):
            print("Handling Certify Prompt 'Duty Status Spans in more than 1 day' ")
        #self.goToHOS()


    #Here add the code to close every alert as a function
    def closeLoadInfoAlert(self):
        print('*** IVG_ELD_Core.closeLoadInfoAlert ***')
        print(">>>> Closing LOAD INFO")
        self.img_proc.click_image_by_max_key_points("IVG_Common/Home/EnterLoadInfoButton/EnterLoadInfoButton")
        self.img_proc.expect_image("vnc-load-enter-info-popup", "ExpectedScreens", 5)
        self.img_proc.click_image_by_max_key_points_offset("please-enter-load-info-label", -40, 60 )
        self.img_proc.send_keys("Test")
        self.img_proc.click_image_by_max_key_points_offset("please-enter-load-info-label", 320, 66 )
        self.img_proc.send_keys("1213")
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        self.img_proc.expect_image("vnc-load-enter-info-popup", "ExpectedScreens", 5) 
        self.img_proc.click_image_by_max_key_points('ELD_Core/CertifyTab/SaveButton/SaveButton')


    def changeDriverStatus(self,newStatus, condition, remark1, remark2, complete=True):
        print("*** IVG_ELD_Core.changeDriverStatus ***")

        self.img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 3)
        self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/StatusTabActive/StatusTabActive')

        self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/ChangeButton/ChangeButton')
        self.img_proc.expect_image('vnc_change_main', 'ExpectedScreens', 3)

        print(f">>>> Selecting new status: {newStatus}")
        if newStatus == "OFF":
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/OFF_Status/OFF_Status')
        elif newStatus == "SB":
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SB_Status/SB_Status')
        elif newStatus == "D":
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/DR_Status/DR_Status')
        else:
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/ON_Status/ON_Status')

        if condition != ' ':
            print(f">>>> Selecting condition: {condition}")
            if condition == 'N':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/None/None', -90, 0)
            elif condition == 'OW':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/OilWell/OilWell', -90, 0)
            elif condition == 'PC' or condition == 'YM':
                self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", -235, 210)
            elif condition == 'RB':
                self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/RestBreak/RestBreak', -90, 0)
            #elif condition == 'YM':
                #self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/YardMove/YardMove', -90, 0)
            else:
                print("The special condition is not valid !!!")

        if remark1 != ' ':
            print(f">>>> Entering remark1: {remark1}")
            self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks1/Remarks1', 0, 50)
            self.img_proc.send_keys(str(remark1))
            self.img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        if remark2 != ' ':
            print(f">>>> Entering remark2: {remark2}")
            self.img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks2/Remarks2', 0, 148)
            self.img_proc.send_keys(str(remark2))

            self.img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
            self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        time.sleep(5)
        if complete != 'False' and complete != 'false':
            print(f">>>> Confirm of Status Change")
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')
            time.sleep(10)

    def goToHOS(self):
        print('*** IVG_ELD_Core.goToHOS ***')
        if not self.img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 2):
            self.ivg_common.goToMainScreen()
            self.img_proc.click_image_by_max_key_points("HOS_ELD")

    def goToELD(self):
        print('*** IVG_ELD_Core.goToELD ***')
        self.goToHOS()

        screen = 0
        sString = ""
        while True:
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
            else:
                self.goToHOS()

        print(sString)

    def goToHistory(self):
        print('*** IVG_ELD_Core.goToHistory ***')
        self.general.goTo("Load")
        self.img_proc.click_image_by_max_key_points("ELD_Core/LoadTab/HistoryButton/HistoryButton")
        found = self.img_proc.expect_image("vnc-load-history-screen", "ExpectedScreens", 4)
        if found:
            print("Load History Screen")
        else:
            print("Load History not found")

    def getLoadDate(self, TimePoint):
        print('*** IVG_ELD_Core.getLoadDate ***')
        self.general.goTo("Load")
        if TimePoint == "Start":
            x, y = self.img_proc.click_image_by_max_key_points_offset("ELD_Core/StatusTab/Start_A/Start_A", 60, -5)
        elif TimePoint == "End":
            x, y = self.img_proc.click_image_by_max_key_points_offset("ELD_Core/StatusTab/Start_A/Start_A", 450, -5)
            x += 355
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        crop_img2 = img[int(y-20):int(y+20), int(x+70-30):int(x+60+100)]

        #plt.imshow(crop_img2)
        #plt.show()
        print(pytesseract.image_to_string(crop_img2))
        loadDate = pytesseract.image_to_string(crop_img2)
        return loadDate

    def dayBack(self, page, reset, clicks):
        print('*** IVG_ELD_Core.dayBack ***')
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
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
            crop_img2 = img[int(y+firstAddY):int(y+secondAddY), int(x+firstAddX-17):int(x+secondAddX+105)]

            print(pytesseract.image_to_string(crop_img2))
            dateDevice = pytesseract.image_to_string(crop_img2)
            dateDevice = parse(str(dateDevice))
            #print("Todays date DEVICE is " + dateDevice.day)
            print(dateDevice.day, dateDevice.month)

            while dateDevice.day != currentDay.day:
                time.sleep(0.5)
                self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
                img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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
        print('*** IVG_ELD_Core.dayForward ***')
        found = self.img_proc.expect_image('vnc-hos-daylog-screen', 'ExpectedScreens', 3)

        if found:
            print('Already in DAYLOG screen')
        else:
            self.goTo(page)

        if page == 'Graph':
            x, y = 535, 150
        else:
            x, y  = 550, 150
        
        for i in range(clicks):
            self.img_proc.click_image_by_max_key_points_offset("IVG_Common/Home/HoursofServicePage/HoursofServicePage", x, y)

            #self.img_proc.click_image_by_max_key_points("ELD_Core/NavigationButtons/Enabled/DayForward/DayForward")
    
    
    
    def createLoad(self, loadId, Trailer1, Trailer2, Trailer3, BL, StartDate, EndDate, Finish):
        print('*** IVG_ELD_Core.createLoad ***')
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
        print("*** IVG_ELD_CORE.goToERODS ***")
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
    

    def update_logs(self):
        print('*** IVG_ELD_Core.update_logs ***')
        string = ""
        self.ivg_common.clearAlerts()
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
        time.sleep(1)
        self.goToHOS()
        self.goTo("Days")
        self.img_proc.expect_image('vnc-8days-screen', 'ExpectedScreens', 3)
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
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')

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
        self.goToELD()

    def select_driver_from_dropdown(self, driver_id):
        print('*** IVG_ELD_Core.select_driver_from_dropdown ***')
        driver_found = False
        unidentified_profile = False

        #Clicks on banner of HOS app to remove highlight of DriverID
        # This because tesseract shows erros when the word is highlighted
        self.img_proc.click_image_by_max_key_points_offset(
            "IVG_Common/Home/HoursofServicePage/HOSPageTitle_split",
            -0, 130)

        #Capture of current screen in the IVG
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')

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
            img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')

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

                string = self.general.retrieve_text_with_config(124, 200, 40, 327)

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
        print('*** IVG_ELD_Core.validate_status ***')
        #self.goToHOS()
        actual_status = self.general.retrieve_text(245, 270, 132, 370)
        expected_status = string.lower()
        assert expected_status in actual_status, \
            f"expected_status '{expected_status}' is no substring of '{actual_status}'"

    def get_clock(self, x, x1, y, y1):
        print('*** IVG_ELD_Core.get_clock ***')
        if self.img_proc.expect_image('vnc-summary-screen','ExpectedScreens',1):
            print("Already in Summary page")
        else:
            self.goToHOS()
            self.goTo('Summary')
        
        self.img_proc.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img = cv2.imread(self.img_proc.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
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
        print('*** IVG_ELD_Core.get_driving_clock ***')
        clock_val = self.get_clock(840,940,245,280)
        return clock_val

    def get_on_duty_clock(self):
        print('*** IVG_ELD_Core.get_on_duty_clock ***')
        clock_val = self.get_clock(840,940,275,315)
        return clock_val
     
    def get_duty_cycle_clock(self):
        print('*** IVG_ELD_Core.get_duty_cycle_clock ***')
        clock_val = self.get_clock(840,940,315,355)
        return clock_val

    def get_rest_break_clock(self):
        print('*** IVG_ELD_Core.get_rest_break_clock ***')
        clock_val = self.get_clock(835,925,365, 395)
        return clock_val

    def review_carrier_edits(self):
        print('*** IVG_ELD_Core.review_carrier_edits ***')
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

    def goTo(self, page):
        print('*** IVG_ELD_Core.goTo ***')
        print(page)
        self.goToELD()
        if page == 'Summary':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/SummaryTab/SummaryTabInactive/SummaryTabInactive")
            if total_x > 120 and total_x < 170:
                self.img_proc.click_image_by_max_key_points("ELD_Core/SummaryTab/SummaryTabInactive/SummaryTabInactive")
        elif page == 'Status':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/StatusTab/StatusTabInactive/StatusTabInactive")
            print(total_x, total_y)
            if total_x > 0 and total_x < 100:
                self.img_proc.click_image_by_max_key_points("ELD_Core/StatusTab/StatusTabInactive/StatusTabInactive")
        elif page == 'Clocks':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/ClocksTab/ClocksTabInactive/ClocksTabInactive")
            print(total_x, total_y)
            if total_x > 250 and total_x < 290:
                self.img_proc.click_image_by_max_key_points("ELD_Core/ClocksTab/ClocksTabInactive/ClocksTabInactive")
        elif page == 'Graph':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/GraphTab/GraphTabInactive/GraphTabInactive")
            print(total_x, total_y)
            if total_x > 300 and total_x < 330:
                self.img_proc.click_image_by_max_key_points("ELD_Core/GraphTab/GraphTabInactive/GraphTabInactive")
        elif page == 'DayLog':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/DayLogTab/DayLogTabInactive/DayLogTabInactive")
            print(total_x, total_y)
            if total_x > 400 and total_x < 430:
                self.img_proc.click_image_by_max_key_points("ELD_Core/DayLogTab/DayLogTabInactive/DayLogTabInactive")
        elif page == 'Days':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/8DaysTab/7DaysTabInactive/7DaysTabInactive")
            print(total_x, total_y)
            if total_x > 500 and total_x < 550:
                self.img_proc.click_image_by_max_key_points("ELD_Core/8DaysTab/7DaysTabInactive/7DaysTabInactive")
            elif total_x > 400 and total_x < 430:
                self.img_proc.click_image_by_max_key_points_offset(
                    "ELD_Core/DayLogTab/DayLogTabInactive/DayLogTabInactive", 130, 0)
        elif page == 'Certify':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/CertifyTab/CertifyTabInactive/CertifyTabInactive")
            print(total_x, total_y)
            if total_x > 590 and total_x < 620:
                self.img_proc.click_image_by_max_key_points("ELD_Core/CertifyTab/CertifyTabInactive/CertifyTabInactive")
        elif page == 'Load':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/LoadTab/LoadTabInactive/LoadTabInactive")
            print(total_x, total_y)
            if total_x > 690 and total_x < 730:
                self.img_proc.click_image_by_max_key_points("ELD_Core/LoadTab/LoadTabInactive/LoadTabInactive")
        elif page == 'Carriers':
            total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
                "ELD_Core/CarriersTab/CarriersTabInactive/CarriersTabInactive")
            print(total_x, total_y)
            if total_x > 740 and total_x < 780:
                self.img_proc.click_image_by_max_key_points(
                    "ELD_Core/CarriersTab/CarriersTabInactive/CarriersTabInactive")

    def changeCarrier(self,Carrier, Send):
        pass

    def reviewCarrierEdits(self):
        pass