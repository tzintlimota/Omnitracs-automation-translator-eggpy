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
import pyodbc
import connection_credentials as cfg
#import pyGPSFeed_IMR
from ImageProcessor import ImageProcessor
from General_Access_Functions import General_Access

gral_access = General_Access()
eld_core = IVG_ELD_CORE(gral_access)
ivg_common = IVG_Common(gral_access)
certify = Certify_Test_Case(gral_access)
daylog = Daylog_Test_Case(gral_access)
uva_events = HOS_Unassigned_Driving_Test_Case(gral_access)

'''OHOS-2804: Verify in "Day Log" tab "Driver" mode that a "Special Driving Event Cleared" with reduced location record is created when driver changes from "Personal Conveyance" to another status.
- Mobile has the latest build. 
- DriverID and Pwd for at least one driver. 
- Access to the "Binary Payload". 
- Yard Move is checked as "Allowed" in HOS Portal. 
- Driver is logged in the mobile. 
- Logs are updated. 
- Driver is on special condition "Yard Move". 
- Driver is in HOS App.'''

print('-------------------- OHOS2804 ----------------------')
driver_id = 'JOSH0001'

ivg_common.logOutAllDrivers()
ivg_common.loginDriver(driver_id, driver_id, 'OF')
eld_core.update_logs()

# driver switches to Personal Conveyance and than to another status
eld_core.changeDriverStatus('OFF', 'PC', '1234', ' ', ' ')
time.sleep(5)
eld_core.changeDriverStatus('OFF', 'N', 'Test', ' ', ' ')

# Get the newest Inspector logs
eld_core.dayForward('DayLog', 8)
daylog.find_driver_record('PC', 'Status', 'Bottom', 'Asc')#Translator
driver_logs = daylog.day_log_records_driver('', 'Desc', 2)

daylog.find_driver_record('Special Driving', 'Event', 'Bottom', 'Asc')#Translator
inspector_logs = daylog.day_log_records_driver('Bottom', 'Asc', 3)

print(">>>> Driver Records Retrieved: \n" + str(driver_logs))
print(">>>> Inspector Records Retrieved: \n" + str(inspector_logs))

# Check driver logs
assert 'PC' in str(driver_logs[0][1])

# Validation of Special Driving Event Record - Inspector
assert 'special driving' in str(inspector_logs[0][1]).lower()
assert '3-0' in str(inspector_logs[0][1]).lower()
assert 'driver' in str(inspector_logs[0][0]).lower()

#DB Validation penging
#credentials = mysql.connector.connect(type='odbc', dns_srv='HOS_DB', user='itko_lisa', password='S8Jxj3LY', host='DEVQESSQLST201e,31205')
server = 'DEVQESSQLST201e,31205'
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

binary_payload = response[0]
