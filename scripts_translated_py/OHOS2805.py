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

'''OHOS-2805: Verify in "Day Log" tab that an "Off Duty" status of 1 second is recorded just before the Personal Conveyance status
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- Personal Conveyance is checked as "Unlimited" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver is in HOS App'''

print('-------------------- OHOS2805 ----------------------')
driver_id = 'JOSH0003'

ivg_common.logOutAllDrivers()
ivg_common.loginDriver(driver_id, driver_id, 'OF')
eld_core.update_logs()

eld_core.changeDriverStatus('OFF', 'PC', '1234', ' ', ' ')
eld_core.validate_status('Personal Conveyance') #Translator Removed

eld_core.dayForward('DayLog', 8)
daylog.find_driver_record('PC', 'Status', 'Bottom', 'Asc')#Translator
driver_log = daylog.day_log_records_driver('', 'Asc', 2)

daylog.find_inspector_record('Personal Conveyance', 'Event', 'Bottom', 'Asc')#Translator
inspector_log = daylog.daylog_get_records_inspector('', 'Asc', 2)

#ConnectUnit
certify_logs = certify.getTable('Bottom', 'Asc', 2)