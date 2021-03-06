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
from HOS_Unassigned_Driving_Test_Case import HOS_Unassigned_Driving_Test_Case
from Certify_Test_Case import Certify_Test_Case
import connection_credentials as cfg
#import pyGPSFeed_IMR
from ImageProcessor import ImageProcessor
from General_Access_Functions import General_Access

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)

print('log "***Script name OHOS2839***"') 

ivg_common.loginDriver('JOSH0089', 'JOSH0089', '', '')
eld_core.general.goTo('.GoToDriverInAdminDriverId')
ivg_common.logOutAllDrivers()
ivg_common.loginDriver('DriverId', 'DriverId', 'True', ' ')
ivg_common.sendMessageToUpdateLogs()
eld_core.general.goTo(' ')
eld_core.dayForward('DayLog', 8)
ivg_common.loginDriver('Test', 'Test', '', '')
#ConnectUnit
eld_core.general.goTo(' ')
ivg_common.clearAlerts()
ivg_common.sendMessageToUpdateLogs()
ivg_common.loginDriver('Test', 'Test', '', '')
#ConnectUnit
eld_core.general.goTo(' ')
ivg_common.clearAlerts()
ivg_common.sendMessageToUpdateLogs()