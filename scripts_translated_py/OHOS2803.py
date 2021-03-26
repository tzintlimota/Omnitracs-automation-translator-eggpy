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
import pyodbc

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)

'''OHOS-2803: Verify in "Day Log" tab "Driver" mode that a "Special Driving Event Cleared" with reduced location record is created when driver in on "Personal Conveyance" and logs out from the vehicle.
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- Access to the "Binary Payload". 
- Personal Conveyance is checked as "Unlimited" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver is on special condition "Personal Conveyance". 
- Driver is in "Home" screen.'''

print('-------------------- OHOS2803 ----------------------')
driver_id = 'TMOTA03'

#ivg_common.logOutAllDrivers()
#ivg_common.loginDriver(driver_id, '123456', 'ON', True)
#eld_core.update_logs()

eld_core.changeDriverStatus('OFF', 'PC', '1234', ' ')
time.sleep(60)

ivg_common.logoutDriver('OF', driver_id)

ivg_common.loginDriver(driver_id, driver_id, 'OF')
eld_core.update_logs()

eld_core.goToELD()

eld_core.dayForward('DayLog', 8)
daylog.find_driver_record('PC', 'Status', 'Bottom', 'Asc')#Translator
driver_log = daylog.day_log_records_driver('', 'Desc', 3)

daylog.find_driver_record('Special Driving', 'Event', 'Bottom', 'Asc')#Translator
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

#DB Validation penging
#credentials = mysql.connector.connect(type='odbc', dns_srv='HOS_DB', user='itko_lisa', password='S8Jxj3LY', host='DEVQESSQLST201e,31205')
'''server = 'DEVQESSQLST201e,31205'
dsn = 'HOS_DB'
user = 'itko_lisa'
password = 'S8Jxj3LY'
driver1 = 'SQL Server Native Client 11.0'
#conn = pyodbc.connect(driver=driver1, server=server, database=dsn, user=user, password=password)
cnxn = pyodbc.connect('DSN=HOS_DB;UID=itko_lisa;PWD=S8Jxj3LY')

#credentials = mysql.connector.connect(user='itko_lisa', password='S8Jxj3LY', host='DEVQESSQLST201e,31205')
db = cnxn.cursor()

query = "select top 1 BINARY_PAYLOAD from RETURN_MSG where UNIFIED_ADDRESS =? AND BINARY_PAYLOAD LIKE '8dfe6%' ORDER BY INSERT_TIME DESC"

db.execute(query, '108087841')

for (BINARY_PAYLOAD) in db:
    response = BINARY_PAYLOAD

db.close()
cnxn.close()

binary_payload = response[0]'''
