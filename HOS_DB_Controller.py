from selenium import webdriver
import pyodbc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from HOS_Elements import webElem
import time

globalDriver = webdriver.Chrome()
globalDriver.implicitly_wait(10)

class HOS_DB_Coontroller:

    def __init__(self):
        self.cnxn = pyodbc.connect('DSN=HOS_DB;UID=itko_lisa;PWD=S8Jxj3LY')
        self.db = self.cnxn.cursor()

    def close_connection(self, db):
        self.db.close()
        self.cnxn.close()

    def execute_parametrized_query(self, query, *params):
        self.db.execute(query, *params)
        for (BINARY_PAYLOAD) in self.db:
            response = BINARY_PAYLOAD

        self.close_connection(self.db)

        return response

