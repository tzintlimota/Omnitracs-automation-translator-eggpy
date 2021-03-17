from ImageProcessor import ImageProcessor
#import pytesseract
import os
import time
from datetime import datetime, timedelta
import math
from PIL import Image
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from Certify_Test_Case import Certify_Test_Case
import connection_credentials as cfg
#import pyGPSFeed_IMR
from ImageProcessor import ImageProcessor
from General_Access_Functions import General_Access

img_proc = ImageProcessor('192.168.1.118', 'None', .15)

general = General_Access()
eld_core = IVG_ELD_CORE(general)
ivg_common = IVG_Common(general)
certify = Certify_Test_Case(general)
daylog = Daylog_Test_Case(general)


print('log "***Script name OHOS2810***"') 

'''
certify.getTable('Bottom', 'Asc', int(5))
ivg_common.logOutAllDrivers()
ivg_common.sendMessageToUpdateLogs()
certify.findTableRecord('OnDuty', 'Status','Bottom','Asc')
eld_core.get_rest_break_clock()
eld_core.get_driving_clock()
eld_core.get_on_duty_clock()
eld_core.get_duty_cycle_clock()
eld_core.getLoadDate(' ')
ivg_common.loginDriver(' ', ' ', ' ', ' ')
eld_core.dayForward('Certify', 3)
eld_core.dayBack('Certify', bool(False), 3 )
eld_core.goToHistory()
eld_core.changeDriverStatus('ON', ' ', ' ', ' ', ' ')
ivg_common.backToHome()
ivg_common.clearAlerts()
ivg_common.sendMessage('')
ivg_common.goToMessagingPage()
ivg_common.goToLoginPage()
eld_core.general.goTo('Certify')
certify.findTableRecord(' ', ' ',' ',' ')
eld_core.select_driver_from_dropdown(' ')'''

daylog.verify_driver_daylog("On Duty", 1, "Daylog")