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
from HOS_PC_YM import HOS_PC_YM
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
pc_ym =HOS_PC_YM(gral_access)

print('log "***Script name OHOS2791***"')
driver_id = 'JOSH0015'

eld_core.changeDriverStatus('ON', 'YM', '1234', ' ', ' ')

'''ivg_common.logOutAllDrivers()
ivg_common.loginDriver(driver_id, driver_id, 'True', '')
eld_core.update_logs()

eld_core.goToELD()
eld_core.changeDriverStatus('OFF', 'PC', '1234', ' ', ' ')

# Run PowerCycle xml vsim file
gral_access.run_vehsim_script('192.168.100.16', 'C:\ELD_VSIM\powercycle1.xml', 1)
pc_ym.handle_pc_confirm_prompt()
gral_access.stop_vehsim_script('192.168.100.16')

eld_core.validate_status('Personal Conveyance') #Translator Removed
eld_core.dayForward('DayLog', 8)

driver_records = daylog.day_log_records_driver('Bottom', 'Asc', 2)
print(">>>> Driver Records Retrieved: \n" + str(driver_records))

assert 'PC' in str(driver_records[0][1])

assert 'OFF' in str(driver_records[1][1])'''


