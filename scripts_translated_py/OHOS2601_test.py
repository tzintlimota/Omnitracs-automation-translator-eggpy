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
import pytest
from General_Access_Functions import General_Access

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)

'''OHOS-2601: Verify when a co-driver is logged out in the mobile, a team split comment is generated in the day log of the active driver.
- Two driver IDs and its passwords from a company. 
- Mobile has been provisioned on the same company of both driver IDs. 
- Mobile has the lastest build installed. 
- Mobile is configured as ELD device. 
- The Active driver must be previously logged in the mobile device.'''

print('-------------------- OHOS2601 ----------------------')

driver_id = 'TMOTA002'
driver_id_2 = 'TMOTA003'

# Before Test
ivg_common.logOutAllDrivers()

ivg_common.loginDriver(driver_id, driver_id, 'OFF')
ivg_common.loginDriver(driver_id_2, driver_id_2, 'OFF', False)
eld_core.update_logs()

ivg_common.logoutDriver('', 'OF')

# Check active driver day logs, should be a Team Split for logging in and out a co-driver
eld_core.dayForward('DayLog', 8)

driver_records = daylog.day_log_records_driver('Bottom', 'Asc', 1)

# Validation that (team split) appears in the COMMENTS
new_str = str(driver_records[0][7]).lower()
new_str = str(driver_records[0][7]).replace('oplit', 'split')
assert 'team split' in new_str



