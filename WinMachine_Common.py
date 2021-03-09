from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import pytest

from HOS_Elements import webElem

#Global variable to store web driver
globalDriver: WebDriver = webdriver.Chrome()

class WinMachine_Common:

    def goToCarrierInAdmin(self, carrier):
        globalDriver.get(webElem.ADMIN_URL)
        globalDriver.find_element(webElem.ADMIN_CARRIER_LINK).click()

        globalDriver.find_element(webElem.CA_CARRIER_SELECT).click()

        globalDriver.find_element(webElem.CA_CARRIER_SELECT).send_keys(carrier,Keys.ENTER)

    def goToVehicleInAdmin(self, UA):
        globalDriver.get(webElem.ADMIN_URL)
        globalDriver.find_element(webElem.ADMIN_VEHICLE_LINK).click()

        globalDriver.find_element(webElem.VA_SEARCH_DEPOT_TXT).clear()
        globalDriver.find_element(webElem.VA_SEARCH_DEPOT_TXT).send_keys("All vehicles")
        globalDriver.find_element(webElem.VA_SEARCH_DEPOT_ALLVEHI_OPT).click()

        globalDriver.find_element(webElem.VA_SEARCH_VEHICLE_TXT).clear()
        globalDriver.find_element(webElem.VA_SEARCH_VEHICLE_TXT).send_keys(UA)

        globalDriver.find_element_by_partial_link_text(UA).click()

    def hos_portal_login(self, customer, username, password, portaltype):

        # For Non-SSO portal
        if portaltype is not 'SSO':
            # globalDriver.get(webElem.HOS_NON_SSO_PORTAL) //Non-SSO page
            globalDriver.get(webElem.HOS_DST_PORTAL)  # DST Page
            globalDriver.maximize_window()

            # Filling information to log in a driver
            globalDriver.find_element(webElem.NON_SSO_COMPANY_NAME).send_keys(customer)
            globalDriver.find_element(webElem.NON_SSO_USER_NAME).send_keys(username)
            globalDriver.find_element(webElem.NON_SSO_PASSWORD).send_keys(password)

            # Clicking on Log in button
            globalDriver.find_element(webElem.NON_SSO_LOGIN_BTN).click()

        # For SSO portal
        else:
            globalDriver.get(webElem.HOS_SSO_PORTAL)
            globalDriver.maximize_window()

            # Filling information to log in a driver
            globalDriver.find_element(webElem.SSO_COMPANY_NAME).send_keys(customer)
            globalDriver.find_element(webElem.SSO_USER_NAME).send_keys(username)
            globalDriver.find_element(webElem.SSO_PASSWORD).send_keys(password)

            # Clicking on Log in button
            globalDriver.find_element(webElem.SSO_LOGIN_BTN).click()

        assert 'Hours of Service - Home' in globalDriver.title

    def go_to_driver_in_admin(self, driverid):

        # Navigate to the Administration link
        globalDriver.get(webElem.ADMIN_URL)
        globalDriver.maximize_window()

        # Click on the Driver Admin tab link
        globalDriver.find_element(webElem.ADMIN_DRIVER_LINK).click()

        # Selecting All drivers in the Depot combo to find the provided driver
        depot = globalDriver.find_element(webElem.DA_SEARCH_DEPOT_TXT)
        depot.clear()
        depot.send_keys('All drivers')
        globalDriver.find_element(webElem.DA_SEARCH_DEPOT_ALLDRI_OPT).click()

        # Selecting the driver provided
        driver = globalDriver.find_element(webElem.DA_SEARCH_DRIVER_TXT)
        driver.clear()
        driver.send_keys(driverid)
        globalDriver.find_element_by_link_text(driverid).click()

    def find_driver(self, driver):

        # Navigate to the Drivers link
        globalDriver.get(webElem.DRIVERS_URL)
        globalDriver.maximize_window()

        # Select 'Search' radio button
        search_rbtn = globalDriver.find_element(webElem.DRIVERS_SEARCH_RADIO_BTN)

        if search_rbtn.is_selected():
            print('Search radio button is already checked')
        else:
            search_rbtn.click()

        # Search for driver
        search_txt = globalDriver.find_element(webElem.DRIVERS_SEARCH_TXT)
        search_txt.clear()
        search_txt.send_keys(driver)
        globalDriver.find_element(webElem.DRIVERS_GO_BUTTON).click()

        week_chart = globalDriver.find_element(webElem.DRIVERS_WEEK_CHART_BUTTON)
        details = globalDriver.find_element(webElem.DRIVERS_DETAILS_BUTTON)
        error_img = globalDriver.find_element(webElem.DRIVERS_ERROR_MESSAGE_IMG)

        # Verify the driver id was found
        try:
            if week_chart.is_displayed() and details.is_displayed():
                print('Driver search was successful')
                details.click()
        except:
            if error_img.is_displayed():
                print('The driver was not found')

    def make_edit_on_day(self, time, date, split, message, recordnum, remark1, remark2, splitremark1, splitremark2):

        # Display options in Duty status changes combo
        duty_changes = Select(globalDriver.find_element(webElem.DRIVERS_DETAILS_TIME_COMBO))

        # Select time if Time parameter is not empty or select past 24hrs option as default
        if time != '':
            duty_changes.select_by_visible_text(time)
        else:
            duty_changes.select_by_visible_text(webElem.DRIVERS_DETAILS_TIME_COMBO_24HRS)

        records_on_day_list = []

        date_lbl = globalDriver.find_elements_by_xpath("//table[@id='dgDetails']//td[contains(text(),'{}')]".format(date))
        next_btn = globalDriver.find_element(webElem.DRIVERS_EDIT_NEXT_PAGE_BTN)

        while len(records_on_day_list) == 0:
            for i in date_lbl:
                correct = i.find_element_by_xpath(webElem.DRIVERS_EDIT_CORRECTION_BTN_XPATH)
                records_on_day_list.append(correct)

            if len(records_on_day_list) == 0:
                correct2 = globalDriver.find_elements_by_xpath("//table[@id='dgDetails']//*[contains(text(),'{}')]/../..//input[contains(@id,'dgDetails_cmdCorrect_')]".format(date))
                records_on_day_list.append(correct2)

            if len(records_on_day_list) == 0:
                if next_btn.is_enabled():
                    next_btn.click()
                else:
                    pytest.fail("No status registries found for the specified date.")

        # Get the number of the web element identifier for afterwards validations
        if len(records_on_day_list) == 1:
            first_btn = records_on_day_list[0]
        else:
            first_btn = records_on_day_list[recordnum]

        locatorid = first_btn.get_attribute("id")
        locator_split = locatorid.split("_")
        idnumber = locator_split[-1]

        main_window = globalDriver.window_handles[0]

        first_btn.click()

        edit_popup = globalDriver.window_handles[1]
        globalDriver.switch_to.window(edit_popup)

        # Read information of original status to modify
        header_info = globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_ENTRY)
        status_info = header_info.text

        if not split:
            status_dd = globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_STATUS_DROPDOWN1)
            status = Select(status_dd)

            if 'On Duty' in status_info:
                status.select_by_visible_text('Off Duty')
                new_status = 'Off Duty'
            elif 'Sleeper Berth' in status_info:
                status.select_by_visible_text('On Duty')
                new_status = 'On Duty'
            elif 'Off Duty' in status_info:
                status.select_by_visible_text('Sleeper Berth')
                new_status = 'Sleeper Berth'
            else:
                status.select_by_visible_text('On Duty')
                new_status = 'On Duty'

        else:
            globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_SPLIT_IMG).click()

            status_dd = globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_STATUS_DROPDOWN2)
            status2 = Select(status_dd)

            if 'On Duty' in status_info:
                status2.select_by_visible_text('Off Duty')
                new_status = 'Off Duty'
            elif 'Sleeper Berth' in status_info:
                status2.select_by_visible_text('On Duty')
                new_status = 'On Duty'
            elif 'Off Duty' in status_info:
                status2.select_by_visible_text('Sleeper Berth')
                new_status = 'Sleeper Berth'
            else:
                status2.select_by_visible_text('On Duty')
                new_status = 'On Duty'

        if remark1 is not '':
            rmk1 = globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_REMARK1_TXT)
            rmk1.clear()
            rmk1.send_keys(remark1)

        if remark2 is not '':
            rmk2 = globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_REMARK2_TXT)
            rmk2.clear()
            rmk2.send_keys(remark2)

        if splitremark1 is not '':
            srmk1 = globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_SPLIT_REMARK1_TXT)
            srmk1.clear()
            srmk1.send_keys(splitremark1)

        if splitremark2 is not '':
            srmk2 = globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_SPLIT_REMARK2_TXT)
            srmk2.clear()
            srmk2.send_keys(splitremark2)

        globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_EDIT_REASON_TXT).send_keys(message)
        globalDriver.find_element(webElem.DRIVERS_CORRECT_POPUP_SAVE_BTN).click()

        globalDriver.switch_to.window(main_window)

        record_updated_id = 'dgDetails_lblActivity_' + idnumber

        record = globalDriver.find_element_by_xpath("//span[@id='{0}' and text()='{1}' - Pending']".format(record_updated_id, new_status))

        assert record in globalDriver.page_source

    def enable_yard_move(self, enable):

        # Navigate to the Administration link
        globalDriver.get(webElem.ADMIN_URL)

        # Click on the HOS Setup tab link
        globalDriver.find_element(webElem.ADMIN_HOS_SETUP_LINK)

        ym_not_allowed = globalDriver.find_element(webElem.HOS_SETUP_YARD_MOVE_NOT_ALLOWED_RBTN)
        ym_allowed = globalDriver.find_element(webElem.HOS_SETUP_YARD_MOVE_ALLOWED_RBTN)

        # Checking current setup for Yard Move and enabled/disabled according to the parameter Enable
        if enable is True:
            if ym_allowed.is_displayed() and ym_allowed.is_selected() is False:
                ym_allowed.click()
                print('Yard Move company setup set to Allowed')
            else:
                print('Yard Move company setup is already set to Allowed')
        elif enable is False:
            if ym_not_allowed.is_displayed() and ym_not_allowed.is_selected() is False:
                ym_not_allowed.click()
                print('Yard Move company setup set to Not Allowed')
            else:
                print('Yard Move company setup is already set to Not Allowed')
        else:
            raise TypeError('Enable parameter only accepts boolean values')

        # Click 'Save' button
        globalDriver.find_element(webElem.HOS_SETUP_SAVE_BTN).click()

        alert = globalDriver.switch_to.alert

        # If the Javascript Alert appears the following code will handle it
        if alert.is_displayed():
            alert.accept()

        update_msg = globalDriver.find_element(webElem.HOS_SETUP_UPDATE_MSG)

        # The 'updated' message is searched to validate the change
        assert update_msg in globalDriver.page_source

    def enable_remarks_on_status_changes(self, enable):

        # Navigate to the Administration link
        globalDriver.get(webElem.ADMIN_URL)

        # Navigate to the Administration link
        globalDriver.find_element(webElem.ADMIN_HOS_SETUP_LINK).click()

        req_remarks = globalDriver.find_element(webElem.HOS_SETUP_REQUIRE_REMARKS_STATUS_CHANGES_CHECK)
        flag_req_remarks = False

        # The checkbox's status is retrieved and enabled/disabled according to the parameter Enable
        if enable is True:
            if req_remarks.is_displayed() and req_remarks.is_selected() is False:
                req_remarks.click()
                flag_req_remarks = False
                print('Require remarks for all status changes has been ENABLED')
            else:
                flag_req_remarks = True
                print('Require remarks for all status changes was already ENABLED')
        elif enable is False:
            if req_remarks.is_displayed() and req_remarks.is_selected() is True:
                req_remarks.click()
                flag_req_remarks = False
                print('Require remarks for all status changes has been DISABLED')
            else:
                flag_req_remarks = True
                print('Require remarks for all status changes was already DISABLED')
        else:
            raise TypeError('Enable parameter only accepts boolean values')

        # Click on Save button
        globalDriver.find_element(webElem.HOS_SETUP_SAVE_BTN).click()

        alert = globalDriver.switch_to.alert

        # This condition handles the Javascript Pop-Up that appears when FreeformRemarkMobile value is modified
        if flag_req_remarks is False:
            alert.accept()

        update_msg = globalDriver.find_element(webElem.HOS_SETUP_UPDATE_MSG)

        # This assertion is done only if there was a modification in the value to validate the Updated message
        assert update_msg in globalDriver.page_source

    def set_personal_conveyance_limit(self, type, limit):

        # Navigate to the Administration link
        globalDriver.get(webElem.ADMIN_URL)

        # Click on the HOS Setup tab link
        globalDriver.find_element(webElem.ADMIN_HOS_SETUP_LINK).click()

        pers_conv_none = globalDriver.find_element(webElem.HOS_SETUP_PERS_CONV_NONE)
        pers_conv_limited = globalDriver.find_element(webElem.HOS_SETUP_PERS_CONV_LIMITED)
        pers_conv_unlimited = globalDriver.find_element(webElem.HOS_SETUP_PERS_CONV_UNLIMITED)
        pers_conv_limit = globalDriver.find_element(webElem.HOS_SETUP_PERS_CONV_LIMIT)
        flag_pc_config = False
        existing_pc_limit = ''

        # Checking current setup for Yard Move and enabled/disabled according to the parameter Enable
        if type == 'None':
            if pers_conv_none.is_displayed() and pers_conv_none.is_selected() is False:
                pers_conv_none.click()
                flag_pc_config = False
                print('Personal Conveyance company setup set to None')
            else:
                flag_pc_config = True
                print('Personal Conveyance company setup is already set to None')
        elif type == 'Limited':
            if pers_conv_limited.is_displayed() and pers_conv_limited.is_selected() is False:
                pers_conv_limited.click()
                pers_conv_limit.click()

                if limit != '':
                    pers_conv_limit.clear()
                    pers_conv_limit.send_keys(limit)
                else:
                    limit = '5'
                    pers_conv_limit.send_keys(limit)

                flag_pc_config = False
                print('Personal Conveyance company setup set to Limited to {} minutes'.format(limit))
            else:
                existing_pc_limit = pers_conv_limit.get_attribute("value")

                if limit != existing_pc_limit and limit != '':
                    pers_conv_limit.clear()
                    pers_conv_limit.send_keys(limit)
                    flag_pc_config = False
                    print('Personal Conveyance company Limited setup updated to {} minutes'.format(limit))
                else:
                    flag_pc_config = True
                    print('Personal Conveyance company setup is already set to Limited and the Limit is set up to {} minutes'.format(existing_pc_limit))

        elif type == 'Unlimited':
            if pers_conv_unlimited.is_displayed() and pers_conv_unlimited.is_selected() is False:
                pers_conv_unlimited.click()
                flag_pc_config = False
                print('Personal Conveyance company setup set to Unlimited')
            else:
                flag_pc_config = True
                print('Personal Conveyance company setup is already set to Unlimited')

        else:
            raise ValueError('The PersonalConveyanceLimitValue is not a valid option (Unlimited,Limited,None)')

        # Saving New Configuration
        globalDriver.find_element(webElem.HOS_SETUP_SAVE_BTN).click()

        alert = globalDriver.switch_to.alert

        # This condition handles the Javascript Pop-Up that appears when FreeformRemarkMobile value is modified
        if flag_pc_config is False:
            alert.accept()

        update_msg = globalDriver.find_element(webElem.HOS_SETUP_UPDATE_MSG)

        # This assertion is done only if there was a modification in the value to validate the Updated message
        assert update_msg in globalDriver.page_source

    def enable_driver_personal_conveyance(self, driverid, enable):

        # Navigate to the Administration -> Driver Administration link
        globalDriver.get(webElem.DA_URL)

        # From Depot Dropdown select --All Drivers-- option
        depot = globalDriver.find_element(webElem.DA_SEARCH_DEPOT_TXT)
        depot.clear()
        depot.send_keys('All drivers')
        globalDriver.find_element(webElem.DA_SEARCH_DEPOT_ALLDRI_OPT).click()

        # Select Drivers dropdown, type the DriverId and select it
        drivers = globalDriver.find_element(webElem.DA_SEARCH_DRIVER_TXT)
        drivers.clear()
        drivers.send_keys(driverid)
        globalDriver.find_element_by_link_text(driverid).click()

        # Verify the DriverId was found
        driverid_txt = globalDriver.find_element(webElem.DA_DRIVER_ID_TXT).get_attribute("value")
        assert driverid in driverid_txt

        # Choose value for Enabled for Personal Conveyance
        pc_allowed_y = globalDriver.find_element(webElem.DA_PERS_CONV_Y)
        pc_allowed_n = globalDriver.find_element(webElem.DA_PERS_CONV_N)

        if enable is True:
            if pc_allowed_y.is_displayed() and pc_allowed_y.is_selected() is False:
                pc_allowed_y.click()
                print('Personal Conveyance driver setup set to Yes')
            else:
                print('Personal Conveyance driver setup is already set to Yes')
        elif enable is False:
            if pc_allowed_n.is_displayed() and pc_allowed_n.is_selected() is False:
                pc_allowed_n.click()
                print('Personal Conveyance driver setup set to No')
            else:
                print('Personal Conveyance driver setup is already set to No')
        else:
            raise TypeError('Enable parameter only accepts boolean values')

        # Save the changes
        globalDriver.find_element(webElem.DA_SAVE_BUTTON).click()

        # This condition handles the Javascript Pop-Up that appears when Canadian Rules is switched from Yes to No
        alert = globalDriver.switch_to.alert

        # If the Javascript Alert appears the following code will handle it
        if alert.is_displayed():
            alert.accept()

        update_msg = globalDriver.find_element(webElem.DA_UPDATE_MESSAGE)

        # The 'updated' message is searched to validate the change
        assert update_msg in globalDriver.page_source

    def update_carrier_name(self, carrier_to_update, new_carrier_name):

        # Go to Carrier page
        self.goToCarrierInAdmin(carrier_to_update)

        # Update carrier
        name = globalDriver.find_element(webElem.CA_CARRIER_NAME)
        name.clear()
        name.send_keys(new_carrier_name)

        # This condition handles the Javascript Pop-Up that appears when Canadian Rules is switched from Yes to No
        alert = globalDriver.switch_to.alert

        # If the Javascript Alert appears the following code will handle it
        if alert.is_displayed():
            alert.accept()

        # The 'updated' message is searched to validate the change
        update_msg = globalDriver.find_element(webElem.CA_UPDATE_MESSAGE)
        assert update_msg in globalDriver.page_source