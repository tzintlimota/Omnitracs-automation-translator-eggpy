from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
#import pyGPSFeed_IMR

class EquiProc:

    def __init__(self):
        self.img_proc = ImageProcessor('192.168.1.118', 'None', .15)
    
    def goToMainScreen(self):
        while not self.img_proc.expect_image('vnc-main-screen', 'ExpectedScreens', 3):     
            total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
            time.sleep(.5) 

    def backToHome(self):
        total_x, total_y = self.img_proc.img_proc.get_image_coordinates_by_max_key_points('IVG_Common/Home/Return/Return')

        if total_x == -1:
            total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        while not self.img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 3):     
            total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
            time.sleep(.5) 

    def goToLoginPage(self):
        total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/DriverLogin/DriverLogin')
        

    def loginDriver(self,username, password, p3, p4):
        self.goToLoginPage()

        total_x, total_y = self.img_proc.click_image_by_max_key_points('login_add_active')
        
        self.img_proc.expect_image('vnc-driver-input', 'ExpectedScreens', 2)

        #Type DriverID
        self.img_proc.click_image_by_max_key_points_offset('login_driver_box', 250, 0)
        self.img_proc.send_keys(str(username))
        self.img_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 2)
        #Type Password
        self.img_proc.click_image_by_max_key_points_offset('login_password_box', 250, 0)
        self.img_proc.send_keys(str(username))
    
        self.img_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 3)

        #Hide Keyboard
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        self.img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)

        # Click OK to Login
        self.img_proc.click_image_by_max_key_points('ok_btn_active')
        self.img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)

        #Set status
        self.img_proc.click_image_by_max_key_points('IVG_Common/Login/OkLoginStatus/OkLoginStatus')

        self.backToHome()

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

    def logoutDriver(self, driver, status):
        if driver != '':
            print("Driver parameter not empty")
            self.img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver') 
        else:
            self.img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')
            found = self.img_proc.expect_image('logout_alert_diagnostic', 'ExpectedScreens', 5) #PONER IMAGEN LOGOUT Alert
            if found:
                print("Alert")
                self.img_proc.click_image_by_max_key_points('IVG_Common/Login/OkLoginStatus/OkLoginStatus') #CHECAR IMAGEN OK
                time.sleep(10)
                self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
                found = self.img_proc.expect_image('vnc-login-add-driver', 'ExpectedScreens', 5)
                self.img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')

            if status == 'ON':
                self.img_proc.click_image_by_max_key_points('IVG_Common/Login/OnDutyStatus/OnDutyStatus') 
            elif status == 'OF':
                self.img_proc.click_image_by_max_key_points('IVG_Common/Login/OffDutyStatus/OffDutyStatus') 
            elif status == 'SL':
                self.img_proc.click_image_by_max_key_points('IVG_Common/Login/SleeperStatus/SleeperStatus') 
            
            #Other devices "Home/MCP200Home", "HOme/MCP50Home"
            self.img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')


    def logOutAllDrivers(self):
        #Logout All Drivers Function
        found = self.img_proc.expect_image('vnc_login_no_drivers', 'ExpectedScreens', 5)
        if found:
            print("No logged drivers, continue")
        else:
            found = self.img_proc.expect_image('vnc-login-add-driver', 'ExpectedScreens', 5)
            if found:
                print("Already in login page")
            else:
                found = self.img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 3)
                if not found:
                    total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')

                    if total_x == -1:
                        total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
                    
                    self.goToMainScreen()
                total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/DriverLogin/DriverLogin')

        while True:
            time.sleep(5)
            found = self.img_proc.expect_image('vnc_login_no_drivers', 'ExpectedScreens', 5)
            if found:
                break
            self.logoutDriver('','OF')
            print("All drivers logged out")

    def clearAlerts(self):
        total_x, total_y, color = self.img_proc.button_is_active("ivg_header_alert")
        print(color)
        if color != 'gray inactive':
            self.img_proc.click_image_by_max_key_points("ivg_header_alert")
            self.img_proc.expect_image("vnc_alert_hos_update", 'ExpectedScreens', 4)
            self.img_proc.click_image_by_max_key_points("IVG_Common/Alerts/DeleteAllButton/DeleteAllButton")
            print("Alerts Cleared")
            self.goToMainScreen()
        else:
            print("No alerts to clear")

    def goToMessagingPage(self):
        self.goToMainScreen()
        self.img_proc.click_image_by_max_key_points("msg-icon")
        time.sleep(2)
    
    def deleteAllOutboxMessages(self):
        self.goToMessagingPage()
        self.img_proc.click_image_by_max_key_points("msg-outbox-tab")
        self.img_proc.expect_image("msg-outbox-screen", "ExpectedScreens", 3)
        total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("IVG_Common/Alerts/DeleteAllButton/DeleteAllButton")
        if total_x != -1:
            self.img_proc.click_image_by_max_key_points("IVG_Common/Alerts/DeleteAllButton/DeleteAllButton")
            self.img_proc.click_image_by_max_key_points("msg-confirm-yes")
            print("All Messages were deleted")
    
    def sendMessage(self, message):
        self.goToMessagingPage()
        #self.img_proc.expect_image("msg-outbox-screen", "ExpectedScreens", 3)
        self.img_proc.click_image_by_max_key_points("ComposeTabInactive")

        total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points('IVG_Common/Home/Return/Return')

        if total_x == -1:
            total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        found = self.img_proc.expect_image("vnc_compose_freeform_blank", "ExpectedScreens", 3)
        if not found:
            self.img_proc.click_image_by_max_key_points("ScrollDownButton")
            self.img_proc.click_image_by_max_key_points("FreeformButton")
        self.img_proc.send_keys(str(message))
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        self.img_proc.click_image_by_max_key_points('SendButton')
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points("msg-confirm-yes")
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points("msg-outbox-tab")
        total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points("IVG_Common/Messaging/MessageSended/MessageSended")
        print(total_x)
        if total_x > -1:
            print("Message sended")
        
    #Wait for log updates
    
    def sendMessageToUpdateLogs(self):
        self.clearAlerts()
        self.goToMessagingPage()
        self.deleteAllOutboxMessages()
        self.sendMessage("Test message")
        #repeat wait for log updates


    #(AlertsTestCase)


    def sendMessagesToOpenConnections(self):
        '''on SendMessagesToOpenConnections
        ClearAlerts
        Log "Sending message to open connections..."
        SendMessage "TEST MESSAGE"	
    end SendMessagesToOpenConnections
    '''
        pass

    #(AlertsTestCase)
    def waitForRuleChangeAlert(self):
        '''
    on WaitForRuleChangeAlert
        put False into found
        Log "Waiting for HOS Rule Change..."	
        WaitForAlert 60	
        If ImageFound(1, Translator("Notifications/Alerts/HOSRuleChange"))		
        ClearAlerts		
        Log "Rule Changed"	
        put True into found		
        Else	
            ClearAlerts		
            put False into found
        End If
        repeat until found is True
            SendMessagesToOpenConnections	
            Log "Waiting for HOS Rule Change..."	
            WaitForAlert 60
            If ImageFound(1, Translator("Notifications/Alerts/HOSRuleChange"))		
                ClearAlerts		
                Log "Rule Changed"		
                put True into found			
            Else		
                ClearAlerts			
                put False into found
            End If
        end repeat
    end WaitForRuleChangeAlert'''
        pass

    def changeCarrier(Carrier, Send):
        pass

    #CarrierEditTestCase
    def goTo():
        pass

    def reviewCarrierEdits():
        pass

    def checkRecordStatus(ExpectedValue, RecordToCheck, EditedIndex):
        pass

    def confirmRejectCarrierEdit( BooleanReject):
        pass

    def reviewCarrierEdits2():
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
