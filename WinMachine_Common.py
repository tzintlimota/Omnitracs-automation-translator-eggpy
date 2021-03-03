from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from HOS_Elements import webElem

#Global variable to store web driver
globalDriver = webdriver.Chrome()

class WinMachine_Common:
    def some_method(self):
        pass

    def goToCarrierInAdmin(carrier):
        globalDriver.get(webElem.ADMIN_URL)
        globalDriver.find_element(webElem.ADMIN_CARRIER_LINK).click()

        globalDriver.find_element(webElem.CA_CARRIER_SELECT).click()

        globalDriver.find_element(webElem.CA_CARRIER_SELECT).send_keys(carrier,Keys.ENTER)














