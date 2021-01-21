import spacy

from spacy.lang.en import English


nlp = spacy.load('en_core_web_sm')

#Read Content of file to translate
file1 = open('OHOS2810.script', 'r') 
Lines = file1.readlines() 
file1.close() 

#Open output file
file2= open('prueba.py', 'w')


def addImports():
    imports = """from ImageProcessor import ImageProcessor
import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
#import pyGPSFeed_IMR"""
    file2.writelines(imports) 
    print(imports)


def backToHome():
    toadd = '''
total_x, total_y = img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')

if total_x == -1:
    total_x, total_y = img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

while not img_proc.expect_image('main', 'Im', 3):     
    total_x, total_y = img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
    time.sleep(.5) '''
    file2.writelines(toadd)

def goToLoginPage():
    toadd = '''total_x, total_y = img_proc.click_image_by_max_key_points('login_active')'''
    file2.writelines(toadd)

def loginDriver(username, password, p3, p4):
    goToLoginPage()
    login_info = '''#Click Login Icon
#Click ADD button
total_x, total_y = img_proc.click_image_by_max_key_points('login_add_active')
img_proc.click_image_by_max_key_points('login_add_active')
img_proc.expect_image('vnc-driver-input', 'ExpectedScreens', 2)

#Type DriverID
img_proc.click_image_by_max_key_points_offset('login_driver_box', 250, 0)'''
    login_info2 = '\nimg_proc.send_keys(str("'+ username + '"))'
    login_info3= '''\nimg_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 2)
#Type Password
img_proc.click_image_by_max_key_points_offset('login_password_box', 250, 0)
'''
    login_info4 = '\nimg_proc.send_keys(str("'+ username + '"))'
    login_info5 = '''
img_proc.expect_image('vnc-driver-input-2', 'ExpectedScreens', 3)

#Hide Keyboard
img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)

# Click OK to Login
img_proc.click_image_by_max_key_points('ok_btn_active')
img_proc.expect_image('vnc-driver-credentials', 'ExpectedScreens', 3)'''
    file2.writelines(login_info)
    file2.writelines(login_info2)
    file2.writelines(login_info3)
    file2.writelines(login_info4)
    file2.writelines(login_info5)

    backToHome()

def changeDriverStatus(newStatus, condition, remark1, remark2, complete):
    toadd = str("\nprint('Status_ChangeTestCase.ChangeDriverStatus') \n")
    toadd += '\ntime.sleep(10)'
    goToTab = '''\n
img_proc.expect_image('vnc_hos_main', 'ExpectedScreens', 3)
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/StatusTabActive/StatusTabActive')

img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/ChangeButton/ChangeButton')
img_proc.expect_image('vnc_change_main', 'ExpectedScreens', 3)
    '''

    if newStatus == "OFF":
        goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/OFF_Status/OFF_Status')
            '''
    elif newStatus == "SB":
        goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SB_Status/SB_Status')
                    '''
    elif newStatus == "D":
        goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/DR_Status/DR_Status')
                        '''
    else:
        goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/ON_Status/ON_Status')
                            '''

    if condition != ' ':
        print("Looking for condition: " + condition)
        if condition == 'N':
            goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SpecialConditions/None/None', -90, 0)
'''
        elif condition == 'OW':
            goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SpecialConditions/OilWell/OilWell', -90, 0)
'''
        elif condition == 'PC':
            goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SpecialConditions/PersonalConveyance/PersonalConveyance', -90, 0)
            '''
        elif condition == 'RB':
            goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/Change_Status/SpecialConditions/RestBreak/RestBreak', -90, 0)
                    '''
        elif condition == 'YM':
            goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/SpecialConditions/YardMove/YardMove', -90, 0)
                        '''
        else:
            print("The special condition is not valid")

    if remark1 != ' ':
        goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks1/Remarks1', 0, 50)
'''
        goToTab += '\nimg_proc.send_keys(str("' + remark1 + '"))'

        goToTab += '''\n
img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
'''

    if remark2 != ' ':
        goToTab += '''\n
#Translator
img_proc.click_image_by_max_key_points_offset('ELD_Core/StatusTab/Change_Status/Remarks2/Remarks2', 0, 148)
    '''
        goToTab += '\nimg_proc.send_keys(str("' + remark2 + '"))'

        goToTab += '''\n
img_proc.expect_image('vnc_remarks1_entered', 'ExpectedScreens', 5)
img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
'''

    goToTab += '\ntime.sleep(5)'

    if complete != 'False' and complete != 'false':
        goToTab += '''\n
img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')
        '''
        goToTab += '\ntime.sleep(10)'

        goToTab += '''\n
img_proc.check_md_alert()
'''

    #If img_proc.expect_image() == False -> CheckMDAlert


    file2.writelines(toadd)
    file2.writelines(goToTab)


def logOutAllDrivers():
    toadd = ''' 
#Logout All Drivers Function
def logoutDriver(driver, status):
    if driver != '':
        print("Driver parameter not empty")
        img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver') 
    else:
        img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')  #PONER IMAGEN LOGOUT-OK
        found = img_proc.expect_image('logout_alert_diagnostic', 'ExpectedScreens', 5) #PONER IMAGEN LOGOUT Alert
        if found:
            print("Alert")
            img_proc.click_image_by_max_key_points('IVG_Common/Login/OkLoginStatus/OkLoginStatus') #CHECAR IMAGEN OK
            time.sleep(10)
            img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
            found = img_proc.expect_image('vnc-login-add-driver', 'ExpectedScreens', 5)
            img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')
        
        if status == 'ON':
            img_proc.click_image_by_max_key_points('IVG_Common/Login/OnDutyStatus/OnDutyStatus') 
        elif status == 'OF':
            img_proc.click_image_by_max_key_points('IVG_Common/Login/OffDutyStatus/OffDutyStatus') 
        elif status == 'SL':
            img_proc.click_image_by_max_key_points('IVG_Common/Login/SleeperStatus/SleeperStatus') 
        
        #Other devices "Home/MCP200Home", "HOme/MCP50Home"
        img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')
        
found = img_proc.expect_image('vnc_login_no_drivers', 'ExpectedScreens', 5)
if found:
    print("No logged drivers, continue")
else:
    found = img_proc.expect_image('vnc-login-add-driver', 'ExpectedScreens', 5)
    if found:
        print("Already in login page")
    else:

        found = img_proc.expect_image('vnc-main-screen', 'ExpectedScreens', 3)

        if not found:
            total_x, total_y = img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')

            if total_x == -1:
                total_x, total_y = img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')
            
            while not img_proc.expect_image('vnc-main-screen', 'ExpectedScreens', 3):     
                total_x, total_y = img_proc.click_image_by_max_key_points('IVG_Common/Home/Return/Return')
                time.sleep(.5) 
        total_x, total_y = img_proc.click_image_by_max_key_points('IVG_Common/Home/DriverLogin/DriverLogin')

while True:
    time.sleep(5)
    found = img_proc.expect_image('vnc_login_no_drivers', 'ExpectedScreens', 5)
    if found:
        break
    logoutDriver('','OF')
    print("All drivers logged out")
    '''
    file2.writelines(toadd)

def logoutDriver(driver, status):
    toadd = '''
if driver != '':
    print("Driver parameter not empty")
    img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver') 
else:
    img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')
    found = img_proc.expect_image('logout_alert', 'ExpectedScreens', 5) #PONER IMAGEN LOGOUT Alert
    if found:
        print("Alert")
        img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')
        img_proc.expect_image('vnc-login-add-driver', 'ExpectedScreens', 5)

    img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')
    if status == 'ON':
        img_proc.click_image_by_max_key_points('IVG_Common/Login/OnDutyStatus/OnDutyStatus') 
    elif status == 'OF':
        img_proc.click_image_by_max_key_points('IVG_Common/Login/OffDutyStatus/OffDutyStatus') 
    elif status == 'SL':
        img_proc.click_image_by_max_key_points('IVG_Common/Login/SleeperStatus/SleeperStatus') 
    
    #Other devices "Home/MCP200Home", "HOme/MCP50Home"
    img_proc.click_image_by_max_key_points('IVG_Common/Login/LogoutDriver/LogoutDriver')'''
    file2.writelines(toadd)

#(AlertsTestCase)
def sendMessagesToOpenConnections():
    '''on SendMessagesToOpenConnections
	ClearAlerts
	Log "Sending message to open connections..."
	SendMessage "TEST MESSAGE"	
end SendMessagesToOpenConnections
'''
    pass

#(AlertsTestCase)
def waitForRuleChangeAlert():
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


def tokenization():
    start_of_script = False
    sf = 0
    count = 0
    addImports()
    file2.writelines("\n\n'''")
    commentb = False
    for line in Lines: 
        doc = nlp(line)
        doc_string = str(doc)
        #Normalmente debería representar la información del test case
        print(doc_string[0])
        print(doc_string[0])
        print(doc_string[0])
        print(doc_string)
        print(doc_string[len(doc_string)-2])
        if(doc[0].pos_ != 'VERB' and start_of_script == False or doc_string[0] == ' '):
            print("Line{}: {}".format(count, line.strip())) 
            
            file2.writelines(line)   
            #for token in doc:
            #    print(token.text, token.pos_, token.dep_)
        elif(commentb):
            file2.writelines(line)
            if(doc_string[len(doc_string)-2] == ')' and doc_string[len(doc_string)-3] == '*'):
                commentb = False
                file2.writelines("'''\n")
        else:
            #Functions from Eld Scripts
            start_of_script = True
            sf += 1
            if sf == 1:
                file2.writelines("'''\n\n")
                #file2.writelines("img_proc = ImageProcessor('192.168.100.13', 'None', .15)\n")
                file2.writelines("img_proc = ImageProcessor('192.168.1.118', 'None', .15)\n")
                #img_proc = ImageProcessor('192.168.1.18', 'None', .15)
            elif(str(doc[0]) == 'ConnectUnit' or str(doc[0])=='Global'):
                toadd = str("\n#"+str(doc[0:len(doc)-1])+"")
                file2.writelines(toadd)
            elif(str(doc[0]) == 'BeforeTest'):
                logOutAllDrivers()
            elif(doc[0].pos_ == 'VERB'):
                file2.writelines('\n#Funcion de eggplant ' + str(doc[0]) + '\n')
                if str(doc[0]) == 'log':
                    toadd = str("print('"+str(doc[0:len(doc)-1])+"') \n")
                    file2.writelines(toadd)
                elif str(doc[0]) == 'put' and doc[2].pos_ == 'PROPN':
                    loginDriver(str(doc[2]), str(doc[2]), '', '' )
                elif str(doc[0]) == 'wait':
                    if str(doc[2]) == 'minute' or str(doc[2]) == 'minutes':
                        toadd = '\ntime.sleep(' + str(int(str(doc[1])) * 60) + ')'
                    else:
                        toadd = '\ntime.sleep(' + str(doc[1]) + ')'
                    file2.writelines(toadd)
                else:
                    #file2.writelines('\n AUN NO CONOZCO ESTA FUNCION VERBO' + line[0: len(line)-1] + '\n')
                    file2.writelines('\n')
                    for token in doc:
                        print(token.text, token.pos_, token.dep_)
            elif(doc[0].pos_ == 'SPACE'):
                pass
            #Comments
            elif (doc_string[0] == '(' or doc_string[1] == '('):
                commentb = True
                file2.writelines("\n''' " + line + '\n')
                if(doc_string[len(doc_string)-2] == ')' and doc_string[len(doc_string)-3] == '*'):
                    commentb = False
                    file2.writelines("'''\n")
            elif(doc_string[0] == '/' ):
                file2.writelines('\n# ' + line + '\n')
            #This is the way to call functions with no verb in front
            #Parameters se iran metiendo con lo de abajo y probablemente usar eval
            #for token in doc:
            #    print(token.text, token.pos_, token.dep_)
            elif (str(doc[0]) == 'Status_ChangeTestCase' and str(doc[2]) == 'ChangeDriverStatus'):
                # (newStatus, condition, remark1, remark2, complete)
                params = []
                stringToPass = ''
                for i in range(3, len(doc)):
                    stringToPass += str(doc[i].text)
                print(stringToPass)

                new = stringToPass.replace('"', '')
                new = new.replace(',', ' ')
                params = new.split()

                print(params)
                while len(params) < 5:
                    params.append(' ')
                # "ON","N" ,"AUTOMATION"
                changeDriverStatus(params[0], params[1], params[2], params[3], params[4])
            elif str(doc[0]) == 'LoginDriver':
                params = []
                stringToPass = ''
                for i in range(3, len(doc)):
                    stringToPass += str(doc[i].text)
                print(stringToPass)

                new = stringToPass.replace('"', '')
                new = new.replace(',', ' ')
                params = new.split()

                print(params)
                while len(params) < 4:
                    params.append(' ')
                # "ON","N" ,"AUTOMATION"
                loginDriver(params[0], params[1], params[2], params[3])
            elif str(doc[0]) == 'BackToHome':
                backToHome()
            elif str(doc[0]) == 'GoToLoginPage':
                goToLoginPage()
            else:
                '''try:
                    str(doc[0])
                except:
                print("An exception occurred") '''
                #file2.writelines('\n AUN NO CONOZCO ESTA FUNCION ' + line[0: len(line)-1] + '\n')
                file2.writelines('\n')
                for token in doc:
                    print(token.text, token.pos_, token.dep_)
            
            #file2.writelines(line)  

tokenization()

file2.close() 