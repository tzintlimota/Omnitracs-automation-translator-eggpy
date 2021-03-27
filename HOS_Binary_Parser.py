from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from HOS_Elements import webElem
import pytest

#Global variable to store web driver¿
globalDriver = webdriver.Chrome()
globalDriver.implicitly_wait(10)

class HOS_Binary_Parser:

    def go_to_parser(self):
        globalDriver.get(webElem.HOS_WEB_TOOLS_URL)
        globalDriver.maximize_window()
        title_elem = globalDriver.find_element(webElem.HOS_WEB_TOOLS_TITLE).text()
        print(title_elem)

    def parser_return_message(self, binary_payload):
        globalDriver.get(webElem.ADMIN_URL)
        globalDriver.find_element(webElem.ADMIN_CARRIER_LINK).click()

        globalDriver.find_element(webElem.CA_CARRIER_SELECT).click()