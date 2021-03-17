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

print('log "***Script name OHOS2820***"') 

ivg_common.loginDriver('JOSH0005', 'JOSH0005', '', '')
#Global UnitAddress
ivg_common.logOutAllDrivers()
ivg_common.loginDriver('DriverId', 'DriverId', 'True', ' ')
ivg_common.sendMessageToUpdateLogs()
eld_core.changeDriverStatus('ON', 'YM', '1234', ' ', ' ')
ivg_common.backToHome()
gral_access.run_vehsim_script('192.168.100.16', 'C:\ELD_VSIM\ .xml', '1')
#ConnectUnit
eld_core.validate_status('Other:YardMove') #Translator Removed
#ConnectUnit
eld_core.dayForward('DayLog', 8)