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
from HOS_Status_Test_Case import HOS_Status_Test_Case
import connection_credentials as cfg
#import pyGPSFeed_IMR
import pytest
from ImageProcessor import ImageProcessor
from General_Access_Functions import General_Access

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)
status = HOS_Status_Test_Case(gral_access)


print('log "***Script name OHOS2736***"')
driver_id = 'JOSH0015'
remark1 = 'test'
remark2 = 'testing'
clockin_reason = 'automation'

# Before Test
ivg_common.logOutAllDrivers()

ivg_common.loginDriver(driver_id, driver_id, 'True', ' ')
eld_core.update_logs()

eld_core.goToELD()
status.clock_in('1', remark1, remark2, clockin_reason)

eld_core.dayForward('DayLog', 8)
driver_records = daylog.day_log_records_driver('Bottom', 'Asc', 1)
print(str(driver_records))

# Validation of ON value in STATUS column
assert 'on' in str(driver_records[0][1]).lower()

# Validation of the COMMENTS value
assert clockin_reason.lower() in str(driver_records[0][7]).lower()

assert remark1.lower() in str(driver_records[0][7]).lower()

assert remark2.lower() in str(driver_records[0][7]).lower()
