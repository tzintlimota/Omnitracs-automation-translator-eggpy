
import time
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from HOS_Unassigned_Driving_Test_Case import HOS_Unassigned_Driving_Test_Case
from Certify_Test_Case import Certify_Test_Case
from HOS_PC_YM import HOS_PC_YM
from General_Access_Functions import General_Access

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
pc_ym = HOS_PC_YM(gral_access)

'''OHOS-2820: Verify in "Day Log" tab that no new record is created when the driver is on "Yard Move" and starts to move the vehicle up to 20MPH.
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- A vSIM script that moves the vehicle 10 minutes at 15MPH. 
- Yard Move is checked as "Allowed" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver is on special condition "Yard Move". 
- Driver is in "HOS App" screen.'''

print('log "***Script name OHOS2820***"')
driver_id = 'JOSH0003'

ivg_common.logOutAllDrivers()
ivg_common.loginDriver('JOSH0003', 'JOSH0005', 'OFF')
eld_core.update_logs()

eld_core.changeDriverStatus('ON', 'YM', '1234', ' ', ' ')
time.sleep(60)
ivg_common.backToHome()

# Start a DRIVING event
gral_access.run_vehsim_script('192.168.100.16', 'C:\ELD_VSIM\Moving10min15MPH.xml', 10)

imui_text = pc_ym.get_imui_view_text()

try:
    assert 'yard move' in imui_text.lower(), 'IMUI does not display Yard Move label'
    assert 'dot' in imui_text.lower(), 'IMUI does not display DOT label'
except AssertionError:
    print('No "Yard Move" or "DOT" label on IMUI screen')

# Stop DRIVING
gral_access.stop_vehsim_script('192.168.100.16')

# Check to see if driver is still in Yard Move
eld_core.validate_status('Yard Move') #Translator Removed

# Get the newest driver logs, inspector logs, and certify table
eld_core.dayForward('DayLog', 8)

# The last record on DayLog Driver screen is retrieved
driver_logs = daylog.day_log_records_driver('Bottom', 'Asc', 1)

# The last record on DayLog Inspector screen is retrieved
inspector_logs = daylog.daylog_get_records_inspector('Bottom', 'Asc', 1)

# The last record on Certify screen is retrieved
certify_logs = certify.getTable('Bottom', 'Asc', 1)

# Validation that the last record that appears is Yard Move and no new record was generated after VSIM script
assert 'yard move' in driver_logs[0][1]

# Check inspector logs
assert 'yard move' in inspector_logs[0][1]
assert '3-2' in inspector_logs[0][1]

# Check Certify Tab
assert 'yard move' in certify_logs[0][1]