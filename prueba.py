from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
import connection_credentials as cfg
#import pyGPSFeed_IMR


eld_core = IVG_ELD_CORE()
ivg_common = IVG_Common()
print('log "***Script name OHOS2810***"') 
'''
eld_core.getTable('Bottom', 'Asc', int(5))
ivg_common.logOutAllDrivers()
ivg_common.sendMessageToUpdateLogs()
eld_core.findTableRecord('OnDuty', 'Status','Bottom','Asc')

eld_core.getLoadDate(' ')
eld_core.loginDriver(' ', ' ', ' ', ' ')
eld_core.dayForward('Certify', 3)
eld_core.dayBack('Certify', bool(False),  )
eld_core.goToHistory()
eld_core.changeDriverStatus('ON', ' ', ' ', ' ', ' ')
ivg_common.backToHome()
ivg_common.clearAlerts()
ivg_common.sendMessage('
 ')
ivg_common.goToMessagingPage()
ivg_common.goToLoginPage()
eld_core.goTo('Certify')
eld_core.findTableRecord(' ', ' ',' ',' ')
eld_core.select_driver_from_dropdown(' ')

eld_core.get_driving_clock()
eld_core.get_on_duty_clock()
eld_core.get_duty_cycle_clock()
eld_core.get_rest_break_clock()


eld_core.get_on_duty_clock()
eld_core.get_duty_cycle_clock()'''

eld_core.find_driver_record('Unknown position', 'Location', 'Bottom', 'Asc')
eld_core.find_inspector_record('Unknown position', 'Location', 'Bottom', 'Asc')
#eld_core.find_driver_record('No', 'CoDriver', 'Bottom', 'Asc')