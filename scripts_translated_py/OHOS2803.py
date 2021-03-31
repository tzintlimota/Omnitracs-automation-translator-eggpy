
import time
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from Daylog_Test_Case import Daylog_Test_Case
from General_Access_Functions import General_Access
from HOS_Binary_Parser import HOS_Binary_Parser
from HOS_DB_Controller import HOS_DB_Coontroller
import re

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
daylog = Daylog_Test_Case(gral_access)
bin_parser = HOS_Binary_Parser()
db = HOS_DB_Coontroller()

'''OHOS-2803: Verify in "Day Log" tab "Driver" mode that a
Special Driving Event Cleared" with reduced location record
is created when driver in on "Personal Conveyance" and logs out from the vehicle.
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- Access to the "Binary Payload". 
- Personal Conveyance is checked as "Unlimited" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver is on special condition "Personal Conveyance". 
- Driver is in "Home" screen.'''

print('-------------------- OHOS2803 ----------------------')
driver_id = 'JOSH0001'

ivg_common.logOutAllDrivers()
ivg_common.loginDriver(driver_id, driver_id, 'ON', True)
eld_core.update_logs()

eld_core.changeDriverStatus('OFF', 'PC', '1234', ' ')
time.sleep(60)

ivg_common.logoutDriver('OF', driver_id)

ivg_common.loginDriver(driver_id, driver_id, 'OF')
eld_core.update_logs()

eld_core.goToELD()

eld_core.dayForward('DayLog', 8)
daylog.find_driver_record('PC', 'Status', 'Bottom', 'Asc')#Translator
driver_log = daylog.day_log_records_driver('', 'Desc', 3)

daylog.find_inspector_record('Special Driving', 'Event', 'Bottom', 'Asc')#Translator
inspector_log = daylog.daylog_get_records_inspector('', 'Desc', 2)

print(">>>> Driver Records Retrieved: \n" + str(driver_log))
print(">>>> Inspector Records Retrieved: \n" + str(inspector_log))

# Validation of Driver Logs
assert 'PC' in str(driver_log[0][1])
assert 'OFF' in str(driver_log[1][1])
assert 'OFF' in str(driver_log[2][1])

# Validation of Special Driving Event Record - Inspector
assert 'special driving' in str(inspector_log[0][1]).lower()
assert '3-0' in str(inspector_log[0][1]).lower()
assert 'driver' in str(inspector_log[0][0]).lower()

assert 'eld logout' in str(inspector_log[1][1]).lower()
assert '5-2' in str(inspector_log[1][1]).lower()
assert 'driver' in str(inspector_log[0][0]).lower()

# DB Query to retrieve BINARY PAYLOAD
query = "select top 1 BINARY_PAYLOAD from RETURN_MSG where UNIFIED_ADDRESS =? AND BINARY_PAYLOAD LIKE '8dfe6%' ORDER BY INSERT_TIME DESC"
unified_address = '108087841'

query_response = db.execute_parametrized_query(query, unified_address)
bin_payload = query_response[0]

# Parsing of the BINARY_PAYLOAD
rtn_msg = bin_parser.parser_return_message(bin_payload)

# Validation of Return Message Title
assert 'ELD_Clear_Special_Driving_Event' in rtn_msg

# Get value of the keys in the Return Message
latitude = bin_parser.get_key_value(rtn_msg, 'latitude')
longitude = bin_parser.get_key_value(rtn_msg, 'longitude')

# This will return NONE if the number has more than 1 decimal number
lat_match_regex = re.match(r'^-?[0-9]\d*(\.\d{1})$', str(latitude).strip())
lon_match_regex = re.match(r'^-?[0-9]\d*(\.\d{1})$', str(longitude).strip())

# Assert for validation of the REDUCED LOCATION values for latitude and longitude
# Only one decimal number should be displayed
assert lat_match_regex is not None
assert lon_match_regex is not None
