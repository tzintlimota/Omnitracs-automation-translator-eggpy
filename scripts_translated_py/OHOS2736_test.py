from ImageProcessor import ImageProcessor
#import pytesseract
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from HOS_Unassigned_Driving_Test_Case import HOS_Unassigned_Driving_Test_Case
from Certify_Test_Case import Certify_Test_Case
from HOS_Status_Test_Case import HOS_Status_Test_Case
from General_Access_Functions import General_Access

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)
status = HOS_Status_Test_Case(gral_access)

'''OHOS-2736: Verify that you can perform a Clock In from the mobile
- A SSO company ID. 
- Mobile is provisioned on the selected SSO company. 
- Mobile has the latest build installed. 
- Mobile is configured as ELD Device. 
- Driver ID and Password correspondent to SSO company selected. 
- Driver must be logged in the mobile (OFF Duty or Slepper Berth status). 
- Vehicle and Driver should not have any pending Carrier Edits, Certification Events, Unidentified Driving Events and Pending Loads Information.'''


print('-------------------- OHOS2736 --------------------')
driver_id = 'JOSH0015'
remark1 = 'test'
remark2 = 'testing'
clockin_reason = 'automation'

# Before Test
ivg_common.logOutAllDrivers()

ivg_common.loginDriver(driver_id, driver_id, 'OFF')
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
