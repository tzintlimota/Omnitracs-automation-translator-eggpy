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

print('"***Script name OHOS2601***"')

driver_id = 'TMOTA03'
driver_id_2 = 'TMOTA04'

# Before Test
ivg_common.logOutAllDrivers()

ivg_common.loginDriver(driver_id, '123456', 'True', ' ')
ivg_common.loginDriver(driver_id_2, '123456', 'False', ' ')
eld_core.update_logs()

# Check active driver day logs, should be a Team Split for logging in and out a co-driver
eld_core.dayForward('DayLog', 8)

driver_records = daylog.day_log_records_driver('Bottom', 'Asc', 1)

assert 'team split' in str(driver_records[0][7]).lower(), 'Team split comment was not generated for active driver' \
                                         'for co-driver logging out'



