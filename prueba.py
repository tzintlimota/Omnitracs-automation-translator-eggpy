from ImageProcessor import ImageProcessor
import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
#import pyGPSFeed_IMR

'''﻿(*OHOS-2810: Verify in "Edit" screen that a "Yard Move" status is able to be edited to "On Duty", "Off Duty", "Sleeper Berth", "Driving", "Personal Conveyance"
Yard Move with different location or remarks (Automatic recorded location cannot be edited, only manually entered or unknown position can be edited)
Remarks should have a length > than 4 chars to be taken as valid. 
If Remarks are empty and only the Location is edited, NEXT button will not appear enabled
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- Yard Move is checked as "Allowed" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver has at least one "Yard Move" record on the current cycle that is not the current duty status, (Recommended that "Yard Move" is the previous status from current status). 
- Driver is in "HOS App" screen.*)

log "***Script name OHOS2810***"
'''

img_proc = ImageProcessor('192.168.100.13', 'None', .15)

#Global DeviceType
''' (*log driver in*)

'''

#ConnectUnit
total_x, total_y = img_proc.click_image_by_max_key_points('login_active')#Click Login Icon
#Click ADD button
total_x, total_y = img_proc.click_image_by_max_key_points('login_add_active')
img_proc.click_image_by_max_key_points('login_add_active')
img_proc.expect_image('vnc-driver-input', 'ExpectedScreens', 2)

#Type DriverID
img_proc.click_image_by_max_key_points_offset('login_driver_box', 250, 0)
img_proc.send_keys(str("JOSH0055"))
img_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 2)
#Type Password
img_proc.click_image_by_max_key_points_offset('login_password_box', 250, 0)

img_proc.send_keys(str("JOSH0055"))
img_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 3)

#Hide Keyboard
img_proc.click_image_by_max_key_points('keyword_icon')
img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)

# Click OK to Login
img_proc.click_image_by_max_key_points('ok_btn_active')
img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)
total_x, total_y = img_proc.click_image_by_max_key_points('Back')

if total_x == -1:
    total_x, total_y = img_proc.click_image_by_max_key_points('keyword_icon')

while not img_proc.expect_image('main', 'Im', 3):     
    total_x, total_y = img_proc.click_image_by_max_key_points('Back')
    time.sleep(.5) 

# // Change to YM status


print('Status_ChangeTestCase.ChangeDriverStatus') 

time.sleep(10)

img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 3)
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/StatusTabActive/StatusTabActive')

img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/ChangeButton/ChangeButton')
img_proc.expect_image('vnc_change_main', 'ExpectedScreens', 3)
    

#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/ON_Status/ON_Status')
                            

#Translator
img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/YardMove/YardMove', -90, 0)
                        

#Translator
img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks1/Remarks1', 0, 50)

img_proc.send_keys(str("AUTOMATION"))

img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

time.sleep(5)

img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')
        
time.sleep(10)

img_proc.check_md_alert()

#Funcion de eggplant wait

time.sleep(60)
#Funcion de eggplant wait

time.sleep(60)
#Funcion de eggplant wait

time.sleep(10)
#Funcion de eggplant wait

time.sleep(10)
print('Status_ChangeTestCase.ChangeDriverStatus') 

time.sleep(10)

img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 3)
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/StatusTabActive/StatusTabActive')

img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/ChangeButton/ChangeButton')
img_proc.expect_image('vnc_change_main', 'ExpectedScreens', 3)
    

#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/ON_Status/ON_Status')
                            

#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SpecialConditions/None/None', -90, 0)


#Translator
img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks1/Remarks1', 0, 50)

img_proc.send_keys(str("AUTOMATION"))

img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

time.sleep(5)

img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')
        
time.sleep(10)

img_proc.check_md_alert()

# // go to edit screen





#Funcion de eggplant Click


# // Check the status on the dropdown of the Top Half


#Funcion de eggplant put


#Funcion de eggplant replace






# //Check Off Duty - Exceptions



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put




# //Check On Duty



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put



# //Check SB



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put



# //Check Driving



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put



# //Click on SPLIT button


#Funcion de eggplant Click


# //Check the status on the dropdown of the Bottom Half


#Funcion de eggplant put






# //Check Off Duty - Exceptions



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put




# //Check On Duty - Exceptions



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put



# //Check SB - Exceptions



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put



# //Check Driving - Exceptions



# //This will retrieve the values of the Exceptions Dropdown


#Funcion de eggplant put



# //Click on SPLIT button


#Funcion de eggplant Click


''' (*The following validates that if ON with YM is selected, the NEXT button appears disabled. It is an invalid edit*)

'''

# //Select ON Duty with YM




''' (*The following validates that if ON with YM is selected and REMARKS*)

'''



# //Remarks (lenght > 4 chars) need to be entered in orther to change Location (If it is editable)


# //This already validates that the field can be edited if empty or contains Unknown Position


''' (*Certify_EditTestCase.enterNewLocation "MEXICO CITY" 

assert ImageFound(imageName:"CertifyTab/NextButton", waitFor:3) with error "Next button appears enabled with status ON-YM, REMARKS and EDITED LOCATION"*)
'''
