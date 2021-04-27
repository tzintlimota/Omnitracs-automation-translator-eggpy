import time
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from HOS_Binary_Parser import HOS_Binary_Parser
from HOS_DB_Controller import HOS_DB_Coontroller
from General_Access_Functions import General_Access
import re

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
bin_parser = HOS_Binary_Parser()
daylog = Daylog_Test_Case(gral_access)
db = HOS_DB_Coontroller()

'''OHOS-2822: Verify in "Day Log" tab "Inspector" mode that a "Special Driving Event Cleared" record is created when driver is on "Yard Move" and logs out from the vehicle.
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- Access to the "Binary Payload". 
- Yard Move is checked as "Allowed" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver is on special condition "Yard Move". 
- Driver is in HOS App.'''
print('-------------------- OHOS2822 ----------------------')

driver_id = 'JOSH0010'

ivg_common.logOutAllDrivers()
ivg_common.loginDriver(driver_id, driver_id, 'OFF')
eld_core.update_logs()

# driver switches to Yard Move and than to another status
eld_core.changeDriverStatus('ON', 'YM', '1234', '')
time.sleep(60)

# Logout Driver
ivg_common.logoutDriver('', 'OFF')

# Log driver back in
ivg_common.loginDriver(driver_id, driver_id, 'OFF')
eld_core.update_logs()

# Get the newest driver and inspector mode logs
eld_core.dayForward('DayLog', 8)
daylog.find_driver_record('YM', 'Status', 'Bottom', 'Asc')
driver_logs = daylog.day_log_records_driver('', 'Desc', 3)

#daylog.find_inspector_record('Personal Conveyance', 'Event', 'Bottom', 'Asc')
inspector_logs = daylog.daylog_get_records_inspector('', 'Desc', 1)

# ------------- Check DRIVER logs ----------------
assert 'ym' in str(driver_logs[0][1]).lower()
assert 'off' in str(driver_logs[1][1]).lower(), 'Off Duty status was not generated after YM'

# ------------- Check INSPECTOR logs ----------------
# To find the record with Special Driving Event Cleared text in INSPECTOR records
for index1, inner_l in enumerate(inspector_logs):
    # Index2 is set to 1 so that the search is done only in Event column
    index2 = 1
    for index2, item in enumerate(inner_l):
        if 'special driving event' in str(item).lower():
            print(f'>>>> Event: {item} has been found with index ({index1},{index2})')
            break

# Remove all spaces using RegEx:\n and Valiadte Event = Special Driving Event
clean_event_str = re.sub(r"\s+", "", str(inspector_logs[index1][index2]))
assert 'specialdrivingeventcleared3-0' in clean_event_str.lower(), 'Special driving event not found in inspector logs'

# Remove all spaces using RegEx:\n and Valiadte Event = Logout
clean_event_str = re.sub(r"\s+", "", str(inspector_logs[index1][index2]))
assert 'eldlogout5-2' in clean_event_str.lower(), 'ELD Logout Event not found in inspector logs'

# ------------- Check DB ----------------

# DB Query to retrieve BINARY PAYLOAD
query = "select top 1 BINARY_PAYLOAD from RETURN_MSG where UNIFIED_ADDRESS = ? AND BINARY_PAYLOAD LIKE '8dfe6%' ORDER BY INSERT_TIME DESC"
unified_address = '108087841'

# Executing query and saving response in a varible
query_response = db.execute_parametrized_query(query, unified_address)
bin_payload = query_response[0]

# Parsing of the BINARY_PAYLOAD
rtn_msg = bin_parser.parser_return_message(bin_payload)

# Validation of Return Message Title
assert 'ELD_Clear_Special_Driving_Event' in rtn_msg
