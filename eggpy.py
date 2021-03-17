import spacy

from spacy.lang.en import English
import re


nlp = spacy.load('en_core_web_sm')

#Read Content of file to translate
file1 = open('OHOS2810.script', 'r') 
Lines = file1.readlines() 
file1.close() 

#Open output file
file2= open('prueba.py', 'w')


def addImports():
    imports = """from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from HOS_Unassigned_Driving_Test_Case import HOS_Unassigned_Driving_Test_Case
from Certify_Test_Case import Certify_Test_Case
import connection_credentials as cfg
#import pyGPSFeed_IMR
import pytest
from ImageProcessor import ImageProcessor
from General_Access_Functions import General_Access

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)

"""
    file2.writelines(imports) 
    print(imports)


def search_func(search, space):
    search = re.search(r""+search+"",str(space))
    if search != None:
        return True
    return False

def remove_translator_func(text):
    string = str(text).split('(')
    status = string[1].split(')')
    return status[0]


def tokenization():
    start_of_script = False
    sf = 0
    count = 0
    addImports()
    #file2.writelines("\n\n'''")
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
        if(str(doc[0]) == 'ConnectUnit' or str(doc[0])=='Global'):
                toadd = str("\n#"+str(doc[0:len(doc)-1])+"")
                file2.writelines(toadd)
        elif (search_func('BeforeTest', doc)):
            toadd = "\nivg_common.logOutAllDrivers()"
            file2.writelines(toadd)
        elif str(doc[0]) == 'log':
            toadd = str("print('"+str(doc[0:len(doc)-1])+"') \n")
            file2.writelines(toadd)
        elif (search_func('SendMessageToUpdateLogs', doc)):
            toadd = "\nivg_common.sendMessageToUpdateLogs()"
            file2.writelines(toadd)
        elif str(doc[0]) == 'put' and doc[2].pos_ == 'PROPN':
            toadd = "\nivg_common.loginDriver('" + str(doc[2]) + "', '" + str(doc[2]) + "', '', '')"
            file2.writelines(toadd)
        elif str(doc[0]) == 'wait':
            if str(doc[2]) == 'minute' or str(doc[2]) == 'minutes':
                toadd = '\ntime.sleep(' + str(int(str(doc[1])) * 60) + ')'
            else:
                toadd = '\ntime.sleep(' + str(doc[1]) + ')'
            file2.writelines(toadd)
        elif (search_func('getLoadDate', doc)):
            params = []
            stringToPass = ''
            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 1:
                params.append(' ')
            toadd = "\neld_core.getLoadDate('" + params[0] + "')"
            file2.writelines(toadd)

        elif (search_func('DayForward', doc)):
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
            while len(params) < 2:
                params.append(' ')
            # "ON","N" ,"AUTOMATION"
            toadd = "\neld_core.dayForward('" + params[0] + "', " + params[1] + ")"
            file2.writelines(toadd)
        elif (search_func('DayBack', doc)):
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
            while len(params) < 3:
                params.append(' ')
            # "ON","N" ,"AUTOMATION"
            if params[1] == 'true' or params[1] == 'True' or params[1] == "'true'":
                params[1] = 'True'
            else:
                params[1] = 'False'
            toadd = "\neld_core.dayBack('" + params[0] + "', bool(" + params[1] + "), " + params[2] + ")"
            file2.writelines(toadd)
        elif(search_func('GoToHistory', doc)):
            toadd = "\neld_core.goToHistory()"
            file2.writelines(toadd)
        elif (search_func('CreateLoad', doc)):
            # self, loadId, Trailer1, Trailer2, Trailer3, BL, StartDate, EndDate, Finish
            params = []
            stringToPass = ''
            for i in range(3, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 9:
                params.append(' ')
            # "ON","N" ,"AUTOMATION"
            if params[7] == 'true' or params[7] == 'True' or params[7] == "'true'":
                params[7] = 'True'
            else:
                params[7] = 'False'
            toadd = "\neld_core.createLoad('" + params[0] + "', '" + params[1] + "','" + params[2] + "','" + params[3] + "','" + params[4] + "','" + params[5] + "','" + params[6] + "', bool(" + params[7] + "))"
            file2.writelines(toadd)
        elif (search_func('ChangeDriverStatus', doc)):
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
            toadd = "\neld_core.changeDriverStatus('" + params[0] + "', '" + params[1] + "', '" + params[2] + "', '" + params[3] + "', '" + params[4] + "')"
            file2.writelines(toadd)
        elif (search_func('LoginDriver', doc)):
            params = []
            stringToPass = ''
            for i in range(2, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 4:
                params.append(' ')
            # "ON","N" ,"AUTOMATION"
            toadd = "\nivg_common.loginDriver('" + params[0] + "', '" + params[0] + "', '" + params[2] + "', '" + \
                    params[3] + "')"
            file2.writelines(toadd)
        elif (search_func('BackToHome', doc)):
            toadd = "\nivg_common.backToHome()"
            file2.writelines(toadd)
        elif (search_func('ClearAlerts', doc)):
            toadd = "\nivg_common.clearAlerts()"
            file2.writelines(toadd)
        elif (search_func('SendMessage', doc) and not (search_func('SendMessageToUpdateLogs', doc))):
            #Enviar mensaje
            message = ''
            for token in doc:
                print(token.text, token.pos_, token.dep_)
                if str(token.text) != '"' and str(token.text) != str(doc[0]):
                    message += str(token.text) + " "
            toadd = "\nivg_common.sendMessage('" + message + "')"
            file2.writelines(toadd)
        elif (search_func('GoToMessagingPage', doc)):
            toadd = "\nivg_common.goToMessagingPage()"
            file2.writelines(toadd)
        elif (search_func('DeleteAllOutboxMessages', doc)):
            toadd = "\nivg_common.deleteAllOutboxMessages()"
            file2.writelines(toadd)
        elif (search_func('GoToLoginPage', doc)):
            toadd = "\nivg_common.goToLoginPage()"
            file2.writelines(toadd)
        elif (search_func('CertifyAllLogs', doc)):
            toadd = "\ncertify.certifyAllLogs()"
            file2.writelines(toadd)
        elif (search_func('getRestBreakClockValue', doc)):
            toadd = "\neld_core.get_rest_break_clock()"
            file2.writelines(toadd)
        elif (search_func('getDrivingClockValue', doc)):
            toadd = "\neld_core.get_driving_clock()"
            file2.writelines(toadd)
        elif (search_func('getOnDutyClockValue', doc)):
            toadd = "\neld_core.get_on_duty_clock()"
            file2.writelines(toadd)
        elif (search_func('getDutyCycleClockValue', doc)):
            toadd = "\neld_core.get_duty_cycle_clock()"
            file2.writelines(toadd)
        elif (search_func('GoTo', doc) and not (search_func('GoToLoginPage', doc))):
            params = []
            stringToPass = ''
            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 1:
                params.append(' ')
            toadd = "\neld_core.general.goTo('" + params[0] + "')"
            file2.writelines(toadd)
            #eld_core.certifyLogOfDay(1)
        elif (search_func('CertifyLogsOfDay', doc)):
            params = []
            stringToPass = ''
            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 1:
                params.append(' ')
            toadd = "\ncertify.certifyLogsOfDay(" + params[0] + ")"
            file2.writelines(toadd)
        elif (search_func('findTableRecord', doc)):
            params = []
            stringToPass = ''
            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 5:
                params.append(' ')
            # "ON","N" ,"AUTOMATION"
            toadd = "\ncertify.findTableRecord('" + params[0] + "', '" + params[1] + "','" + params[2] + "','" + params[3] + "')"
            file2.writelines(toadd)
        
        elif (search_func('getTable', doc)):
            params = []
            stringToPass = ''
            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 4:
                params.append(' ')
            # "ON","N" ,"AUTOMATION"
            toadd = "\ncertify.getTable('" + params[0] + "', '" + params[1] + "', int(" + params[2] + "))"
            file2.writelines(toadd)
        
        elif (search_func('SelectDriverFromDropDown', doc)):
            # (driverID)
            params = []
            stringToPass = ''
            for i in range(3, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 1:
                params.append(' ')
            # "DriverID"
            toadd = "\neld_core.select_driver_from_dropdown('" + params[0] + "')"
            file2.writelines(toadd)

        elif (search_func('ValidateStatus', doc)):
            params = []
            stringToPass = ''
            for i in range(3, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            while len(params) < 1:
                params.append(' ')

            if "Translator" in params[0]:
                clean_param = remove_translator_func(params[0])

            toadd = "\neld_core.validate_status('" + clean_param + "') #Translator Removed"
            file2.writelines(toadd)

        elif (search_func('AcceptUnassignedEvents', doc)):
            params = []
            stringToPass = ''

            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            new = new.replace('.AcceptUnassignedEvents', '')
            params = new.split()

            print(params)
            while len(params) < 3:
                params.append(' ')

            toadd = f"\nuva_events.accept_unassigned_events('{params[0]}', '{params[1]}', '{params[2]}')"
            file2.writelines(toadd)

        elif (search_func('RejectUnassignedEvents', doc)):
            params = []
            stringToPass = ''

            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            new = new.replace('.RejectUnassignedEvents', '')
            params = new.split()

            print(params)
            while len(params) < 2:
                params.append(' ')

            if params[0] == 'true' or params[0] == 'True' or params[0] == "'true'":
                params[0] = 'True'
            else:
                params[0] = 'False'

            toadd = f"\nuva_events.reject_unassigned_events('{params[0]}', '{params[1]}')"
            file2.writelines(toadd)

        elif (search_func('RunVsimScript', doc)):
            params = []
            stringToPass = ''

            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 2:
                params.append(' ')

            toadd = f"\ngral_access.run_vehsim_script('192.168.100.16', 'C:\\ELD_VSIM\\{params[1]}.xml', '1')"
            file2.writelines(toadd)

        elif (search_func('CloseVsimAndWaitForUnlock', doc)):
            params = []
            stringToPass = ''

            for i in range(1, len(doc)):
                stringToPass += str(doc[i].text)
            print(stringToPass)

            new = stringToPass.replace('"', '')
            new = new.replace(',', ' ')
            params = new.split()

            print(params)
            while len(params) < 2:
                params.append(' ')

            toadd = f"\ngral_access.stop_vehsim_script()"
            file2.writelines(toadd)

        else:
            print('\n AUN NO CONOZCO ESTA FUNCION ' + line[0: len(line)-1] + '\n')
            #file2.writelines('\n')
            for token in doc:
                print(token.text, token.pos_, token.dep_)
        
        #file2.writelines(line)
        #Peguntar TZINTLI
        #daylog_get_records_driver (num_records, start_point, direction)
        #daylog_get_records_inspector (num_records, start_point, direction)
        #find_driver_record
tokenization()

file2.close()
