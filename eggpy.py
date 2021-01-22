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
from EquiProc import EquiProc
#import pyGPSFeed_IMR


equi_proc = EquiProc()
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
            elif(str(doc[0]) == 'BeforeTest'):
                toadd = "\nequi_proc.logOutAllDrivers()"
                print(toadd)
                file2.writelines(toadd)
                #logOutAllDrivers()
            elif(doc[0].pos_ == 'VERB'):
                file2.writelines('\n#Funcion de eggplant ' + str(doc[0]) + '\n')
                if str(doc[0]) == 'log':
                    toadd = str("print('"+str(doc[0:len(doc)-1])+"') \n")
                    file2.writelines(toadd)
                elif str(doc[0]) == 'put' and doc[2].pos_ == 'PROPN':
                    toadd = "\nequi_proc.loginDriver('"+ str(doc[2]) +"', '"+ str(doc[2]) +"', '', '')"
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
                toadd = "\nequi_proc.changeDriverStatus('"+ params[0] +"', '"+ params[1] +"', '"+ params[2] +"', '"+ params[3] +"', '"+ params[4] +"')"
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
                toadd = "\nequi_proc.loginDriver('"+ params[0] +"', '"+ params[0] +"', '"+ params[2] +"', '"+ params[3] +"')"
                file2.writelines(toadd)
            elif str(doc[0]) == 'BackToHome':
                toadd = "\nequi_proc.backToHome()"
                file2.writelines(toadd)
            elif str(doc[0]) == 'GoToLoginPage':
                toadd = "\nequi_proc.goToLoginPage()"
                file2.writelines(toadd)
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