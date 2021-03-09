from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from HOS_Elements import webElem

#Global variable to store web driver
globalDriver = webdriver.Chrome()
globalDriver.implicitly_wait(10)

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

    def editCertStatus(preStatus,type,change,recordNum,time,exceptionStatus):
        globalDriver.find_element(webElem.DD_DUTYSTATUSCHANGES_SELECT).click()
        if time != None:
            timeOption = globalDriver.find_element_by_xpath("//select[@id='ddlTimeFrame']/option[text()='"+time+"']")
            timeOption.click()
        else:
            globalDriver.find_element(webElem.DD_24HRS_SELECT_OPT).click()

        preStatusesList = globalDriver.find_elements_by_xpath("//table[@id='dgDetails']//img[contains(@id,'dgDetails_imgConfirmed_')]/following-sibling::span[text()='"+preStatus+"']/..//input[contains(@id,'dgDetails_cmdCorrect_')]")
        if preStatusesList.count() == 0:
            preStatusesList = globalDriver.find_elements_by_xpath("//table[@id='dgDetails']//img[contains(@id,'dgDetails_imgConfirmed_')]/following-sibling::span[text()='"+preStatus+"']/../..//input[contains(@id,'dgDetails_cmdCorrect_')]")

        assert preStatusesList.count() != 0

        firstButton = preStatusesList[0]

        locatorID = firstButton.get_property('id')
        splitLocator = locatorID.split("_")
        finalID = splitLocator[-1]

        firstButton.click()

        currentWindow = globalDriver.current_window_handle
        openWindows = globalDriver.window_handles
        globalDriver.switch_to.window(openWindows[-1])

        if type == "Split":
            globalDriver.find_element(webElem.DCP_SPLIT_ICON).click()
            if recordNum == 1:
                globalDriver.find_element(webElem.DCP_DUTY1_SELECT).click()
                globalDriver.find_element_by_xpath("//select[@id='ddlDuty1']/option[contains(text(),'"+change+"')]").click()
                if not exceptionStatus == None:
                    globalDriver.find_element(webElem.DCP_EXCEPTION1_SELECT).click()
                    globalDriver.find_element_by_xpath("//select[@id='ddlEventFlag1']/option[contains(text(),'"+exceptionStatus+"')]").click()

            elif recordNum == 2:
                globalDriver.find_element(webElem.DCP_DUTY1_SELECT).click()
                globalDriver.find_element_by_xpath("//select[@id='ddlDuty2']/option[contains(text(),'" + change + "')]").click()
                if not exceptionStatus == None:
                    globalDriver.find_element(webElem.DCP_EXCEPTION2_SELECT).click()
                    globalDriver.find_element_by_xpath("//select[@id='ddlEventFlag2']/option[contains(text(),'"+exceptionStatus+"')]").click()

        elif type == "Edit":
            globalDriver.find_element(webElem.DCP_DUTY1_SELECT).click()
            globalDriver.find_element_by_xpath("//select[@id='ddlDuty1']/option[contains(text(),'" + change + "')]").click()
            if not exceptionStatus == None:
                globalDriver.find_element(webElem.DCP_EXCEPTION1_SELECT).click()
                globalDriver.find_element_by_xpath("//select[@id='ddlEventFlag1']/option[contains(text(),'" + exceptionStatus + "')]").click()

        globalDriver.find_element(webElem.DCP_EDITREASON_TXT).click()
        globalDriver.find_element(webElem.DCP_EDITREASON_TXT).send_keys("Testing")

        globalDriver.find_element(webElem.DCP_SAVE_BUTTON).click()

        globalDriver.switch_to.window(currentWindow)

        editedID = "dgDetails_lblActivity_"+finalID

        try:
            editedRecord = globalDriver.find_element_by_xpath("//span[@id='"+editedID+"' and text()='"+change+" - Pending']")
        except NoSuchElementException:
            raise RuntimeError("Unable to find the edited record on the table.")

    def swapDrivingStatus (time, driverId, newStatus, reason, index):
        globalDriver.find_element(webElem.DD_DUTYSTATUSCHANGES_SELECT).click()
        if time != None:
            timeOption = globalDriver.find_element_by_xpath("//select[@id='ddlTimeFrame']/option[text()='" + time + "']")
            timeOption.click()
        else:
            globalDriver.find_element(webElem.DD_24HRS_SELECT_OPT).click()

        driveSwapButtonList = globalDriver.find_elements(webElem.DD_DRIVINGSWAP_BUTTON)
        swapButton = driveSwapButtonList[index]
        locatorID = swapButton.get_property("id")
        locatorID.split("_")
        idNumber = locatorID[-1]
        swapButton.click()

        currentWindow = globalDriver.current_window_handle
        openWindows = globalDriver.window_handles
        globalDriver.switch_to.window(openWindows[-1])

        globalDriver.find_element(webElem.DSP_DRIVERID_TEXT).clear()
        globalDriver.find_element(webElem.DSP_DRIVERID_TEXT).send_keys(driverId)

        if newStatus != None:
            globalDriver.find_element(webElem.DCP_DUTY2_SELECT).click()
            globalDriver.find_element_by_xpath("//select[@id='ddlDuty2']/option[text()='"+newStatus+"']")

        globalDriver.find_element(webElem.DCP_EDITREASON_TXT).click()

        if reason != None:
            globalDriver.find_element(webElem.DCP_EDITREASON_TXT).send_keys(reason)
        else:
            globalDriver.find_element(webElem.DCP_EDITREASON_TXT).send_keys("TESTING")

        globalDriver.find_element(webElem.DSP_SAVE_BUTTON).click()

        try:
            failElement =  globalDriver.find_element(webElem.DSP_SWAPSUCCESS_MSGBAR)
            raise RuntimeError("Unable to complete the swap process.")
        except NoSuchElementException:
            print("Swapping successful")

        globalDriver.switch_to.window(currentWindow)

        globalDriver.refresh()

        editedID = "dgDetails_lblActivity_" + idNumber
        try:
            editedRecord = globalDriver.find_element_by_xpath("//span[@id='"+editedID+"' and text()='"+newStatus+" - Pending']")
        except NoSuchElementException:
            raise RuntimeError("Unable to find the edited record on the table.")

    def exemptDriver (driverId, exempt, reason):
        #go_to_driver_in_admin driverId

        if exempt == True:
            yesRadio = globalDriver.find_element(webElem.DA_EXEMPT_RADIO_YES)

            if yesRadio.is_selected():
                print("US ELD Exempt is already enabled")
            else:
                yesRadio.click()
                eldComment = globalDriver.find_element(webElem.DA_REASON_TXT)
                eldComment.click()
                eldComment.send_keys(reason)

        else:
            noRadio = globalDriver.find_element(webElem.DA_EXEMPT_RADIO_NO)

            if noRadio.is_selected():
                print("US ELD Exempt is already disabled")
            else:
                noRadio.click()

        action0 = ActionChains(globalDriver)
        action0.double_click(globalDriver.find_element(webElem.DA_SAVE_BUTTON))
        action0.perform()

        try:
            resultElem = globalDriver.find_element_by_xpath("//span[@id='MDriverUC1_messageBar_lblMessage' and text()='"+driverId+" updated.']")
            print("Successful update")
        except NoSuchElementException:
            action0.double_click(globalDriver.find_element(webElem.DA_SAVE_BUTTON))
            action0.perform()
            resultElem = globalDriver.find_element_by_xpath("//span[@id='MDriverUC1_messageBar_lblMessage' and text()='" + driverId + " updated.']")

    def setYardMoveTermination(type):
        globalDriver.get(webElem.ADMIN_URL)
        globalDriver.find_element(webElem.ADMIN_HOSSETUP_LINK).click()

        yardMoveChck = globalDriver.find_element(webElem.HS_YARDMOVE_CHECKBOX)

        if yardMoveChck.get_property("checked") == "checked":
            if type == "Power":
                globalDriver.find_element(webElem.HS_POWER_CHECKBOX)
            elif type == "Speed":
                globalDriver.find_element(webElem.HS_SPEED_CHECKBOX)
            elif type == "Both":
                globalDriver.find_element(webElem.HS_BOTH_CHECKBOX)
            else:
               raise RuntimeError("The type option provided is not a valid value")

        globalDriver.find_element(webElem.HS_SAVE_BUTTON).click()

        try:
            popup = globalDriver.switch_to.alert()
            popup.accept()
        except:
            print("JS popup did not appear")

        else:
            raise RuntimeError("Yard move checkbox is not checked")

    def enableDriverYardMove(driverId,enable):
        globalDriver.get(webElem.ADMIN_DRIVER_URL)

        searchDepot = globalDriver.find_element(webElem.DA_SEARCH_DEPOT_TXT)
        searchDepot.click()
        searchDepot.clear()
        searchDepot.send_keys("All drivers")
        globalDriver.find_element(webElem.DA_SEARCH_DEPOT_ALLDRI_OPT)

        searchDriver = globalDriver.find_element(webElem.DA_SEARCH_DRIVER_TXT)
        searchDriver.clear()
        searchDriver.send_keys(driverId)

        try:
            driverOpt = globalDriver.find_element_by_xpath("//*[contains(text(),'"+driverId+"')]")
        except NoSuchElementException:
            raise RuntimeError("Unable to find the drivers id using the search combo")

        driverOpt.click()

        if enable == True:
            radioYes = globalDriver.find_element(webElem.DA_YARDMOVE_RADIO_YES)
            if radioYes.get_property("checked") != "checked":
                radioYes.click()
                print("Yard move set to yes")
            else:
                print("Yard move is already set to yes")

        elif enable == False:
            radioNo = globalDriver.find_element(webElem.DA_YARDMOVE_RADIO_NO)
            if radioNo.get_property("checked") != "checked":
                radioNo.click()
                print("Yard move is set to no")
            else:
                print("Yard move is already set to no")

        else:
            raise RuntimeError("The value provided is not a boolean value")

        globalDriver.find_element(webElem.DA_SAVE_BUTTON).click()

        try:
            popup = globalDriver.switch_to.alert()
            popup.accept()
        except:
            print("JS popup did not appear")

        try:
            globalDriver.find_element(webElem.DA_MESSAGEBAR_LABEL)
            print("The message bar was properly displayed")
        except NoSuchElementException:
            raise RuntimeError("Unable to find the success message bar")

    def editStatusWithMinDuration (preStatus, time, change, recordNum, duration, message):
        durationArray = duration.split(" ")
        durationHours =  durationArray[0].replace("h","")
        durationMin = durationArray[1].replace("m","")
        durationSeconds = durationArray[2].replace("s","")

        globalDriver.find_element(webElem.DD_DUTYSTATUSCHANGES_SELECT).click()
        if time != None:
            timeOption = globalDriver.find_element_by_xpath("//select[@id='ddlTimeFrame']/option[text()='" + time + "']")
            timeOption.click()
        else:
            globalDriver.find_element(webElem.DD_24HRS_SELECT_OPT).click()

        preStatusList = globalDriver.find_elements_by_xpath(
            "//table[@id='dgDetails']//img[contains(@id,'dgDetails_imgConfirmed_')]/following-sibling::span[text()='"+preStatus+"']/..//input[contains(@id,'dgDetails_cmdCorrect_')]")

        if len(preStatusList) == 0:
            preStatusList = globalDriver.find_elements_by_xpath(
                "//table[@id='dgDetails']//img[contains(@id,'dgDetails_imgConfirmed_')]/following-sibling::span[text()='" + preStatus + "']/../..//input[contains(@id,'dgDetails_cmdCorrect_')]")

        if len(preStatusList) == 0:
            raise RuntimeError("Could not identify any record corresponding to the pre-status indicated")

        firstButton = preStatusList[0]
        locatorID = firstButton.get_property('id')
        splitLocator = locatorID.split("_")
        finalID = splitLocator[-1]
        firstButton.click()

        currentWindow = globalDriver.current_window_handle
        openWindows = globalDriver.window_handles
        globalDriver.switch_to.window(openWindows[-1])

        globalDriver.find_element(webElem.DCP_SPLIT_ICON).click()

        if recordNum == 1:
            globalDriver.find_element(webElem.DCP_DUTY1_SELECT).click()
            globalDriver.find_element_by_xpath("//select[@id='ddlDuty1']/option[contains(text(),'" + change + "')]").click()

            #type down hours minutes and seconds
            globalDriver.find_element(webElem.DCP_DURATIONHOURS_TEXT).clear()
            globalDriver.find_element(webElem.DCP_DURATIONHOURS_TEXT).send_keys(durationHours)

            globalDriver.find_element(webElem.DCP_DURATIONMIN_TEXT).clear()
            globalDriver.find_element(webElem.DCP_DURATIONMIN_TEXT).send_keys(durationMin)

            globalDriver.find_element(webElem.DCP_DURATIONSEC_TEXT).clear()
            globalDriver.find_element(webElem.DCP_DURATIONSEC_TEXT).send_keys(durationSeconds)

        elif recordNum == 2:
            globalDriver.find_element(webElem.DCP_DUTY1_SELECT).click()
            globalDriver.find_element_by_xpath("//select[@id='ddlDuty2']/option[contains(text(),'" + change + "')]").click()

            # type down hours minutes and seconds
            globalDriver.find_element(webElem.DCP_DURATIONHOURS_TEXT).clear()
            globalDriver.find_element(webElem.DCP_DURATIONHOURS_TEXT).send_keys(durationHours)

            globalDriver.find_element(webElem.DCP_DURATIONMIN_TEXT).clear()
            globalDriver.find_element(webElem.DCP_DURATIONMIN_TEXT).send_keys(durationMin)

            globalDriver.find_element(webElem.DCP_DURATIONSEC_TEXT).clear()
            globalDriver.find_element(webElem.DCP_DURATIONSEC_TEXT).send_keys(durationSeconds)

        globalDriver.find_element(webElem.DCP_EDITREASON_TXT).click()
        globalDriver.find_element(webElem.DCP_EDITREASON_TXT).send_keys(message)

        globalDriver.find_element(webElem.DCP_SAVE_BUTTON).click()

        globalDriver.switch_to.window(currentWindow)

        editedID = "dgDetails_lblActivity_" + finalID

        try:
            editedRecord = globalDriver.find_element_by_xpath("//span[@id='"+editedID+"' and contains(text(),'"+change+"')]")
            print ("Record properly updated")
        except NoSuchElementException:
            raise RuntimeError("Unable to find the edited record on the table.")



