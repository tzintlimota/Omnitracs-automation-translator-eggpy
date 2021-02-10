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
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
#import pyGPSFeed_IMR


eld_core = IVG_ELD_CORE()
ivg_common = IVG_Common()
"""
    file2.writelines(imports) 
    print(imports)


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
            elif (str(doc[0]) == 'BeforeTest'):
                toadd = "\nivg_common.logOutAllDrivers()"
                file2.writelines(toadd)
                #logOutAllDrivers()
            elif(doc[0].pos_ == 'VERB'):
                file2.writelines('\n#Funcion de eggplant ' + str(doc[0]) + '\n')
                if str(doc[0]) == 'log':
                    toadd = str("print('"+str(doc[0:len(doc)-1])+"') \n")
                    file2.writelines(toadd)
                elif str(doc[0]) == 'SendMessageToUpdateLogs':
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
            #for token in doc:
            #    print(token.text, token.pos_, token.dep_)

            elif (str(doc[0]) == 'GoTo' and str(doc[2]) == 'DayForward'):
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
            elif (str(doc[0]) == 'GoTo' and str(doc[2]) == 'DayBack'):
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
            
            '''
            #Change to CREATE LOAD 8 params
            elif (str(doc[0]) == 'GoTo' and str(doc[2]) == 'DayBack'):
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
            '''

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
                toadd = "\neld_core.changeDriverStatus('" + params[0] + "', '" + params[1] + "', '" + params[2] + "', '" + params[3] + "', '" + params[4] + "')"
                file2.writelines(toadd)
            elif str(doc[0]) == 'LoginDriver':
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
                toadd = "\neld_core.loginDriver('" + params[0] + "', '" + params[0] + "', '" + params[2] + "', '" + \
                        params[3] + "')"
                file2.writelines(toadd)
            elif str(doc[0]) == 'BackToHome':
                toadd = "\nivg_common.backToHome()"
                file2.writelines(toadd)
            elif str(doc[0]) == 'ClearAlerts':
                toadd = "\nivg_common.clearAlerts()"
                file2.writelines(toadd)
            elif str(doc[0]) == 'SendMessage':
                #Enviar mensaje
                message = ''
                for token in doc:
                    print(token.text, token.pos_, token.dep_)
                    if str(token.text) != '"' and str(token.text) != str(doc[0]):
                        message += str(token.text) + " "
                toadd = "\nivg_common.sendMessage('" + message + "')"
                file2.writelines(toadd)
            elif str(doc[0]) == 'GoToMessagingPage':
                toadd = "\nivg_common.goToMessagingPage()"
                file2.writelines(toadd)
            elif str(doc[0]) == 'DeleteAllOutboxMessages':
                toadd = "\nivg_common.deleteAllOutboxMessages()"
                file2.writelines(toadd)
            elif str(doc[0]) == 'GoToLoginPage':
                toadd = "\nivg_common.goToLoginPage()"
                file2.writelines(toadd)
            elif str(doc[0]) == 'GoTo':
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
                toadd = "\neld_core.goTo('" + params[0] + "')"
                file2.writelines(toadd)
            else:
                #file2.writelines('\n AUN NO CONOZCO ESTA FUNCION ' + line[0: len(line)-1] + '\n')
                file2.writelines('\n')
                for token in doc:
                    print(token.text, token.pos_, token.dep_)
            
            #file2.writelines(line)  

tokenization()

file2.close()
