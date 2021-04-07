import time
from datetime import datetime
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from HOS_Unassigned_Driving_Test_Case import HOS_Unassigned_Driving_Test_Case
from Certify_Test_Case import Certify_Test_Case
from General_Access_Functions import General_Access
import re

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)

'''OHOS-2805: Verify in "Day Log" tab that an "Off Duty" status of 1 second 
is recorded just before the Personal Conveyance status
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
driver_logs = daylog.day_log_records_driver('', 'Asc', 2)
print(">>>> Driver Records Retrieved: \n" + str(driver_logs))

daylog.find_inspector_record('Personal Conveyance', 'Event', 'Bottom', 'Asc')#Translator
inspector_logs = daylog.daylog_get_records_inspector('', 'Asc', 2)
print(">>>> Inspector Records Retrieved: \n" + str(inspector_logs))

certify_logs = certify.getTable('Bottom', 'Asc', 2)
print(">>>> Certify Records Retrieved: \n" + str(certify_logs))

# Driver Profile Validations
assert 'PC' in str(driver_logs[0][1])
assert 'OFF' in str(driver_logs[1][1]), 'Daylog Driver: Off Duty status not found before PC'
assert '1s' in str(driver_logs[1][3]), 'Daylog Driver: Off Duty status is not 01 second of duration'

# Inspector Profile Validations
assert 'personal conveyance' in str(inspector_logs[0][1]).lower()
assert 'off duty' in str(inspector_logs[1][1]).lower(), 'Daylog Inspector: Off Duty status not found before PC'

# Certify Validations
assert 'personal conveyance' in str(certify_logs[0][2]).lower()
assert 'off duty' in str(certify_logs[1][2]).lower(), 'Certify: Off Duty status not found before PC'
assert '1s' in str(certify_logs[1][3]), 'Certify: Off Duty status is not 01 second of duration'

time_format = '%H:%M:%S'

origin_off = inspector_logs[0][0].split()
origin_pc = inspector_logs[1][0].split()

# This is to subtract the minutes (time) to (current_time2) to new_time that will be entered.
new_time = datetime.strptime(str(origin_off[0]), time_format) - datetime.strptime(str(origin_pc[0]), time_format)
print(f'>>>> Off Duty status duration before PC ({new_time})')

# This will return NONE if the time is not xx:xx:01
lat_match_regex = re.match(r'\d*:\d*:01$', str(new_time))

# Validation that an Off Duty status with a duration of 01 second has been generated before PC
assert lat_match_regex is not None, "Off Duty status duration is not equals to 1 second before Personal Conveyance record on Driver records"
