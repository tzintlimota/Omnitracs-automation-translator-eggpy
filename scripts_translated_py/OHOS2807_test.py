from datetime import datetime, timedelta
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

'''OHOS-2807: Verify in "Status" tab that a driver is able to select Personal Conveyance
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- Personal Conveyance is checked as "Unlimited" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver is in HOS App.'''

print('log "***Script name OHOS2807***"')
driver_id = 'JOSH0004'

ivg_common.logOutAllDrivers()
ivg_common.loginDriver(driver_id, driver_id, 'OFF', True)
eld_core.update_logs()

eld_core.validate_status('Personal Conveyance') #Translator Removed

eld_core.dayForward('DayLog', 8)
daylog.find_driver_record('PC', 'Status', 'Bottom', 'Asc')
driver_logs = daylog.day_log_records_driver('', 'Asc', 2)

time_format = '%H:%M:%S'

pc_time = driver_logs[0][2].split()
off_time = driver_logs[1][2].split()

# Driver Profile Validations
assert 'PC' in str(driver_logs[0][1])
assert 'OFF' in str(driver_logs[1][1]), 'Daylog Driver: Off Duty status not found before PC'

# This is to subtract the minutes (off_time) to (pc_time) to new_time that will be entered.
new_time = datetime.strptime(str(pc_time[0]), time_format) - datetime.strptime(str(off_time[0]), time_format)
print(f'>>>> Off Duty status duration before PC ({new_time})')

# This will return NONE if the time is not xx:xx:01
lat_match_regex = re.match(r'\d*:\d*:01$', str(new_time))

# Validation that an Off Duty status with a duration of 01 second has been generated before PC
assert lat_match_regex is not None, "Off Duty status duration is not equals to 1 second before Personal Conveyance record on Driver records"
