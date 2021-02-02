from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from EquiProc import EquiProc
#import pyGPSFeed_IMR


equi_proc = EquiProc()


''''''

img_proc = ImageProcessor('192.168.1.118', 'None', .15)

#Funcion de eggplant log
print('log "***Script name OHOS2810***"') 
#equi_proc.sendMessage("Hello")

#Here include an or
#In all future expect image either remove maximum time or add a while in test case
#This should really be in equiproc


#equi_proc.clearAlerts()
equi_proc.goToELD()

#!/usr/bin/python
'''
import multiprocessing
import time


var = True

def test_case():

    #Aqui meter lo de expect screen quitarle el tiempo maximo
    for i in range(5):
        print(i)
        time.sleep(2)
    var = False

def checkForAlerts():
    while var:
        print("Checking for alerts")
        time.sleep(2)
    print("Test case finished")

p1 = multiprocessing.Process(target=test_case)
p2 = multiprocessing.Process(target=print_num)


p1.start()
p2.start()

p1.join()
p2.join()

finish = time.perf_counter()

print("Finished")
'''



'''
from multiprocessing import Process
from EquiProc import EquiProc


def p():
    print("HOIHSOIS")
    

def print_func(continent='Asia'):
    print('The name of continent is : ', continent)

def print2():
    equi_proc = EquiProc()
    equi_proc.sendMessage("hello")

if __name__ == '__main__' :

    #proc = Process(target=print_func)
    proc2 = Process(target=print2)

    #proc.start()
    proc2.start()




#!/usr/bin/python
from threading import Thread
import time

def run():
    while True:
        time.sleep(2)
        print('ok')



def run2():
    while True:
        time.sleep(1)
        print("HIijwijoinwiniwniuw")



t = Thread(target=run, args=())
t2 = Thread(target=run2)

t.start()
t2.start()
'''