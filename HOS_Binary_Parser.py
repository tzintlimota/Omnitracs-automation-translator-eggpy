from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from HOS_Elements import webElem
import time

globalDriver = webdriver.Chrome()
globalDriver.implicitly_wait(10)

class HOS_Binary_Parser:

    def go_to_parser(self):
        globalDriver.get(webElem.HOS_WEB_TOOLS_URL)
        WebDriverWait(globalDriver, 10).until(EC.title_contains(webElem.HOS_WEB_TOOLS_TITLE))
        globalDriver.maximize_window()

    def parser_return_message(self, binary_payload):
        try:
            self.go_to_parser()

            #  Click on Return Message Parser Link
            globalDriver.find_element(*webElem.HOS_WEB_TOOLS_RTN_MSG_PARSER_LINK).click()

            # Waiting for page to load
            WebDriverWait(globalDriver, 20).until(
                EC.presence_of_element_located((By.ID, 'binaryPayload'))
            )

            # Click on RETURN MESSAGE PARSER link
            time.sleep(3)
            globalDriver.find_element(*webElem.HOS_WEB_TOOLS_RTN_MSG_PARSER_INPUT_BOX_ID).click()
            globalDriver.find_element(*webElem.HOS_WEB_TOOLS_RTN_MSG_PARSER_INPUT_BOX_ID).send_keys(binary_payload)
            globalDriver.find_element(*webElem.HOS_WEB_TOOLS_RTN_MSG_PARSER_PARSE_BTN).click()

            # Wait for value to be parsed and retrieve the text
            WebDriverWait(globalDriver, 20).until(
                EC.presence_of_element_located(webElem.HOS_WEB_TOOLS_RTN_MSG_PARSER_TEXT_AREA))
            text = globalDriver.find_element(*webElem.HOS_WEB_TOOLS_RTN_MSG_PARSER_TEXT_AREA).text

            print(f'>>>> PARSED Binary Return Message: \n {text}')
            return text
        finally:
            globalDriver.quit()

    def get_key_value(self, parsed_message, key_to_search):

        split_parsed_msg = parsed_message.split('\n')

        for index in range(len(split_parsed_msg)):
            if key_to_search in split_parsed_msg[index]:
                print(f'>>>> Key: "{key_to_search}", has been found')
                value = split_parsed_msg[index].split('=')
                print(f'>>>> Key: "{key_to_search}", Value: "{str(value[1]).strip()}"')
                return str(value[1]).strip()
                break



