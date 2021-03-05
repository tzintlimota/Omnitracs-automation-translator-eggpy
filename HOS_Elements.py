#WebElements repository of HOS Portal
from selenium.webdriver.common.by import By

class webElem():
    #----- Administration page -----
    ADMIN_URL = "https://hos.int.omnitracs.com/QHOS/~admin/admin.aspx"
    ADMIN_DRIVER_URL = "https://hos.int.omnitracs.com/QHOS/~admin/mdriver.aspx"
    ADMIN_DRIVER_LINK = (By.ID,"AdminUC1_hlDrivers")
    ADMIN_CARRIER_LINK = (By.ID,"AdminUC1_h1Carriers")
    ADMIN_VEHICLE_LINK = (By.ID,"AdminUC1_hlVehicles")
    ADMIN_HOSSETUP_LINK = (By.ID,"AdminUC1_hlHOSSetup")

    #----- Driver administration page -----
    DA_SEARCH_DEPOT_TXT = (By.ID,"MDriverUC1_searchDepotTextBox")
    DA_SEARCH_DEPOT_ALLDRI_OPT = (By.LINK_TEXT,"--- All drivers ---")
    DA_SEARCH_DRIVER_TXT = (By.ID,"MDriverUC1_searchDriverTextBox")
    DA_EXEMPT_RADIO_YES = (By.ID,"MDriverUC1_rblELDExemption_0")
    DA_REASON_TXT = (By.ID,"MDriverUC1_txtELDComment")
    DA_EXEMPT_RADIO_NO = (By.ID,"MDriverUC1_rblELDExemption_1")
    DA_SAVE_BUTTON = (By.ID,"MDriverUC1_cmdSave")
    DA_YARDMOVE_RADIO_YES = (By.ID,"MDriverUC1_rblYardMove_0")
    DA_YARDMOVE_RADIO_NO = (By.ID,"MDriverUC1_rblYardMove_1")

    #----- Carrier administration page -----
    CA_CARRIER_SELECT = (By.ID,"MCarrierUC1_ddlCarriers")

    #----- Vehicle administration page -----
    VA_SEARCH_DEPOT_TXT = (By.ID,"MVehicleUC1_searchDepotTextBox")
    VA_SEARCH_DEPOT_ALLVEHI_OPT = (By.LINK_TEXT,"--- All vehicles ---")
    VA_SEARCH_VEHICLE_TXT = (By.ID,"MVehicleUC1_searchVehicleTextBox")

    #----- Driver details page -----
    DD_DUTYSTATUSCHANGES_SELECT = (By.ID,"ddlTimeFrame")
    DD_24HRS_SELECT_OPT = (By.XPATH,"//select[@id='ddlTimeFrame']/option[text()='Past 24 hours']")
    DD_DRIVINGSWAP_BUTTON = (By.XPATH,"//table[@id='dgDetails']//input[contains(@id,'dgDetails_cmdDrvTimeSwap_')]")

    #----- Driver's configuration popup -----
    DCP_SPLIT_ICON = (By.ID,"imgSplit")
    DCP_DUTY1_SELECT = (By.ID,"ddlDuty1")
    DCP_EXCEPTION1_SELECT = (By.ID,"ddlEventFlag1")
    DCP_DUTY2_SELECT = (By.ID, "ddlDuty2")
    DCP_EXCEPTION2_SELECT = (By.ID, "ddlEventFlag2")
    DCP_EDITREASON_TXT = (By.ID,"comboboxEditReason")
    DCP_SAVE_BUTTON = (By.ID,"cmdChange")

    #----- Driving swap popup -----
    DSP_DRIVERID_TEXT = (By.ID,"DrvIDTextBox")
    DSP_SAVE_BUTTON = (By.ID,"cmdSwap")
    DSP_SWAPSUCCESS_MSGBAR = (By.ID,"messageBar_imgMessage")

    #----- HOS setup page -----
    HS_YARDMOVE_CHECKBOX = (By.ID,"rblYardMoveEnable_1")
    HS_POWER_CHECKBOX = (By.ID,"rblYardMoveTermination_0")
    HS_SPEED_CHECKBOX = (By.ID, "rblYardMoveTermination_1")
    HS_BOTH_CHECKBOX = (By.ID, "rblYardMoveTermination_2")
    HS_SAVE_BUTTON = (By.ID,"cmdSave")

