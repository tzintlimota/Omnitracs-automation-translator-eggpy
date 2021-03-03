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

    def goToVehicleInAdmin(UA):
        globalDriver.get(webElem.ADMIN_URL)
        globalDriver.find_element(webElem.ADMIN_VEHICLE_LINK).click()

        globalDriver.find_element(webElem.VA_SEARCH_DEPOT_TXT).clear()
        globalDriver.find_element(webElem.VA_SEARCH_DEPOT_TXT).send_keys("All vehicles")
        globalDriver.find_element(webElem.VA_SEARCH_DEPOT_ALLVEHI_OPT).click()

        globalDriver.find_element(webElem.VA_SEARCH_VEHICLE_TXT).clear()
        globalDriver.find_element(webElem.VA_SEARCH_VEHICLE_TXT).send_keys(UA)

        globalDriver.find_element_by_partial_link_text(UA).click()














