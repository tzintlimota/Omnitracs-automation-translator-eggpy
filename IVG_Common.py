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
import connection_credentials as cfg

from General_Access_Functions import General_Access

#import pyGPSFeed_IMR

class IVG_Common(object):

    def __init__(self, general):
        self.general = general
        self.img_proc = self.general.img_proc
        

    def closeUnknownPositionAlert(self):
        self.img_proc.click_image_by_max_key_points("IVG_Common/Login/OkLoginStatus/OkLoginStatus")

    def goToMainScreen(self):
        print('***IVG_Common.goToMainScreen***')
        while not self.img_proc.expect_image('vnc-main-screen', 'ExpectedScreens', 3):
            print('Clicking RETURN button to go to IVG MAIN SCREEN')
            total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
            time.sleep(.5)

    def backToHome(self):
        total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points('IVG_Common/Home/Return/Return')

        if total_x == -1:
            total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        while not self.img_proc.expect_image('vnc-main-screen', 'ExpectedScreens', 3):
            total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
            time.sleep(.5)

    def goToLoginPage(self):
        self.goToMainScreen()
        total_x, total_y = self.img_proc.click_image_by_max_key_points('IVG_Common/Home/DriverLogin/DriverLogin')

    def loginDriver(self, username, password, p3, p4):
        self.goToLoginPage()

        total_x, total_y = self.img_proc.click_image_by_max_key_points('login_add_active')

        self.img_proc.expect_image('vnc-driver-input', 'ExpectedScreens', 2)

        # Type DriverID
        self.img_proc.click_image_by_max_key_points_offset('login_driver_box', 250, 0)
        self.img_proc.send_keys(str(username))
        self.img_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 2)
        # Type Password
        self.img_proc.click_image_by_max_key_points_offset('login_password_box', 250, 0)
        self.img_proc.send_keys(str(password))

        self.img_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 3)

        # Hide Keyboard
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
        self.img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)

        # Click OK to Login
        self.img_proc.click_image_by_max_key_points('ok_btn_active')
        self.img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)

        # Set status
        self.img_proc.click_image_by_max_key_points('IVG_Common/Login/OkLoginStatus/OkLoginStatus')

        self.backToHome()

    def logoutDriver(self, driver, status):
        if driver != '':
            print("Driver parameter not empty")
            self.img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')
        else:
            self.img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')
            found = self.img_proc.expect_image('logout_alert_diagnostic', 'ExpectedScreens',
                                               5)  # PONER IMAGEN LOGOUT Alert
            if found:
                print("Alert")
                self.img_proc.click_image_by_max_key_points(
                    'IVG_Common/Login/OkLoginStatus/OkLoginStatus')  # CHECAR IMAGEN OK
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

                # Other devices "Home/MCP200Home", "HOme/MCP50Home"
            self.img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')

    def logOutAllDrivers(self):
        # Logout All Drivers Function
        self.goToLoginPage()
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
                        total_x, total_y = self.img_proc.click_image_by_max_key_points(
                            'IVG_Common/Home/KeyboardOpen/KeyboardOpen')

                    self.goToMainScreen()
                total_x, total_y = self.img_proc.click_image_by_max_key_points(
                    'IVG_Common/Home/DriverLogin/DriverLogin')

        while True:
            time.sleep(5)

            found = self.img_proc.expect_image('vnc_login_no_drivers', 'ExpectedScreens', 5)
            if found:
                break
            self.logoutDriver('', 'OF')
            print("All drivers logged out")

    def clearAlerts(self):
        total_x, total_y, color = self.img_proc.button_is_active("ivg_header_alert", 0, 0)
        print(color)
        if color != 'gray inactive':
            self.img_proc.click_image_by_max_key_points("ivg_header_alert")
            self.img_proc.expect_image("vnc_alert_hos_update", 'ExpectedScreens', 8)
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
        total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
            "IVG_Common/Alerts/DeleteAllButton/DeleteAllButton")
        if total_x != -1:
            self.img_proc.click_image_by_max_key_points("IVG_Common/Alerts/DeleteAllButton/DeleteAllButton")
            self.img_proc.click_image_by_max_key_points("msg-confirm-yes")
            print("All Messages were deleted")

    def sendMessage(self, message):
        self.goToMessagingPage()
        # self.img_proc.expect_image("msg-outbox-screen", "ExpectedScreens", 3)
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
        self.img_proc.expect_image("vnc_confirm_send_msg", "ExpectedScreens", 4)
        self.img_proc.click_image_by_max_key_points("msg-confirm-yes")
        time.sleep(2)
        self.img_proc.click_image_by_max_key_points("msg-outbox-tab")
        total_x, total_y = self.img_proc.get_image_coordinates_by_max_key_points(
            "IVG_Common/Messaging/MessageSended/MessageSended")
        print(total_x)
        if total_x > -1:
            print("Message sent")

    # Wait for log updates
    def waitForLogUpdates(self):
        pass

    def sendMessageToUpdateLogs(self):
        self.clearAlerts()
        self.goToMessagingPage()
        self.deleteAllOutboxMessages()
        self.sendMessage("Test message")
        #repeat wait for log updates

    def sendMessagesToOpenConnections(self):
        pass

    #(AlertsTestCase)
    def waitForRuleChangeAlert(self):
        pass
