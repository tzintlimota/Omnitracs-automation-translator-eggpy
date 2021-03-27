# WebElements repository of HOS Portal
from selenium.webdriver.common.by import By


class webElem():
    # ----- Portal Sites -----
    HOS_SSO_PORTAL = "https://hos.int.omnitracs.com/QHOS/Home.aspx"
    HOS_NON_SSO_PORTAL = "https://hosx.int.omnitracs.com/QHOS/"
    HOS_DST_PORTAL = "https://qhos-dst.qualcommapps.com/QHOS/Login.aspx"

    # ----- Login Page -----
    SSO_COMPANY_NAME = (By.ID, 'companyName')
    NON_SSO_COMPANY_NAME = (By.ID, 'txtCustomer')
    SSO_USER_NAME = (By.ID, 'userName')
    NON_SSO_USER_NAME = (By.ID, 'txtUserName')
    SSO_PASSWORD = (By.ID, 'j_password')
    NON_SSO_PASSWORD = (By.ID, 'txtPassword')
    SSO_LOGIN_BTN = (By.ID, 'loginButton')
    NON_SSO_LOGIN_BTN = (By.ID, 'cmdLogin')

    # ----- Drivers page -----
    DRIVERS_URL = "https://hos.int.omnitracs.com/QHOS/~hours/driversummary.aspx"
    DRIVERS_SEARCH_RADIO_BTN = (By.ID, 'rblModes_4')
    DRIVERS_SEARCH_TXT = (By.ID, 'txtSearch')
    DRIVERS_GO_BUTTON = (By.ID, 'btnSearch')
    DRIVERS_WEEK_CHART_BUTTON = (By.ID, 'dgHours_hlDriverWeek_0')
    DRIVERS_DETAILS_BUTTON = (By.ID, 'dgHours_hlDriverDetails_0')
    DRIVERS_ERROR_MESSAGE_IMG = (By.ID, 'messageBar_imgMessage')
    DRIVERS_DETAILS_TIME_COMBO = (By.ID, 'ddlTimeFrame')
    DRIVERS_DETAILS_TIME_COMBO_24HRS = 'Past 24 hours'
    DRIVERS_EDIT_CORRECTION_BTN_XPATH = (By.XPATH, "//input[contains(@id,'dgDetails_cmdCorrect_')]")
    DRIVERS_EDIT_NEXT_PAGE_BTN = (By.ID, 'pager1_cmdNext')
    DRIVERS_CORRECT_POPUP_ENTRY = (By.ID, 'lblEntryDesc')
    DRIVERS_CORRECT_POPUP_STATUS_DROPDOWN1 = (By.ID, 'ddlDuty1')
    DRIVERS_CORRECT_POPUP_SPLIT_IMG = (By.ID, 'imgSplit')
    DRIVERS_CORRECT_POPUP_STATUS_DROPDOWN2 = (By.ID, 'ddlDuty2')
    DRIVERS_CORRECT_POPUP_REMARK1_TXT = (By.ID, 'comboboxRemark_1_1')
    DRIVERS_CORRECT_POPUP_REMARK2_TXT = (By.ID, 'comboboxRemark_1_2')
    DRIVERS_CORRECT_POPUP_SPLIT_REMARK1_TXT = (By.ID, 'comboboxRemark_2_1')
    DRIVERS_CORRECT_POPUP_SPLIT_REMARK2_TXT = (By.ID, 'comboboxRemark_2_2')
    DRIVERS_CORRECT_POPUP_EDIT_REASON_TXT = (By.ID, 'comboboxEditReason')
    DRIVERS_CORRECT_POPUP_SAVE_BTN = (By.ID, 'cmdChange')

    # ----- Administration page -----
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
    DA_MESSAGEBAR_LABEL = (By.ID,"MDriverUC1_messageBar_lblMessage")

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
    DCP_DURATIONHOURS_TEXT = (By.ID,"txtDuration2Hour")
    DCP_DURATIONMIN_TEXT = (By.ID,"txtDuration2Minute")
    DCP_DURATIONSEC_TEXT = (By.ID,"txtDuration2Second")

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

    ADMIN_CARRIER_LINK = (By.ID, "AdminUC1_h1Carriers")
    ADMIN_DRIVER_LINK = (By.ID, "AdminUC1_hlDrivers")
    ADMIN_VEHICLE_LINK = (By.ID, "AdminUC1_hlVehicles")
    ADMIN_HOS_SETUP_LINK = (By.ID, "AdminUC1_hlHOSSetup")

    # ----- Driver administration page -----
    DA_URL = "https://hos.int.omnitracs.com/QHOS/~admin/mdriver.aspx"
    DA_SEARCH_DEPOT_TXT = (By.ID, "MDriverUC1_searchDepotTextBox")
    DA_SEARCH_DEPOT_ALLDRI_OPT = (By.LINK_TEXT, "--- All drivers ---")
    DA_SEARCH_DRIVER_TXT = (By.ID, "MDriverUC1_searchDriverTextBox")
    DA_DRIVER_ID_TXT = (By.ID, 'MDriverUC1_txtDriverID')
    DA_PERS_CONV_Y = (By.ID, 'MDriverUC1_rblOffDutyDrv_0')
    DA_PERS_CONV_N = (By.ID, 'MDriverUC1_rblOffDutyDrv_1')
    DA_SAVE_BUTTON = (By.ID, 'MDriverUC1_cmdSave')
    DA_UPDATE_MESSAGE = (By.ID, 'MDriverUC1_messageBar_lblMessage')

    # ----- Carrier administration page -----
    CA_CARRIER_SELECT = (By.ID, "MCarrierUC1_ddlCarriers")
    CA_CARRIER_NAME = (By.ID, 'MCarrierUC1_txtCarrierName')
    CA_SAVE_BTN = (By.ID, 'MCarrierUC1_cmdSave')
    CA_UPDATE_MESSAGE = (By.ID, 'MCarrierUC1_messageBar_lblMessage')

    # ----- Vehicle administration page -----
    VA_SEARCH_DEPOT_TXT = (By.ID, "MVehicleUC1_searchDepotTextBox")
    VA_SEARCH_DEPOT_ALLVEHI_OPT = (By.LINK_TEXT, "--- All vehicles ---")
    VA_SEARCH_VEHICLE_TXT = (By.ID, "MVehicleUC1_searchVehicleTextBox")

    # ----- HOS Setup administration page -----
    HOS_SETUP_PERS_CONV_NONE = (By.ID, 'rblOVOffDutyDrv_0')
    HOS_SETUP_PERS_CONV_LIMITED = (By.ID, 'rblOVOffDutyDrv_1')
    HOS_SETUP_PERS_CONV_UNLIMITED = (By.ID, 'rblOVOffDutyDrv_2')
    HOS_SETUP_PERS_CONV_LIMIT = (By.ID, 'txtOffDutyDrvLimit')
    HOS_SETUP_YARD_MOVE_NOT_ALLOWED_RBTN = (By.ID, 'rblYardMoveEnable_0')
    HOS_SETUP_YARD_MOVE_ALLOWED_RBTN = (By.ID, 'rblYardMoveEnable_1')
    HOS_SETUP_REQUIRE_REMARKS_STATUS_CHANGES_CHECK = (By.ID, 'cbRequireRemarks')
    HOS_SETUP_SAVE_BTN = (By.ID, 'cmdSave')
    HOS_SETUP_UPDATE_MSG = (By.ID, 'messageBar_lblMessage')

    # ----- HOS Binary Parser -----
    HOS_WEB_TOOLS_URL = "http://sdhosintevt10.devqes.omnitracs.com:8080/hos-web-tools/home"
    HOS_WEB_TOOLS_TITLE = (By.TAG_NAME, "title")
    HOS_WEB_TOOLS_RTN_MSG_PARSER_LINK = (By.CSS_SELECTOR, "a[href='rtnmsgparser']")
    HOS_WEB_TOOLS_RTN_MSG_PARSER_FORM_ID = (By.ID, 'parserData')
    HOS_WEB_TOOLS_RTN_MSG_PARSER_INPUT_BOX_ID = (By.ID, 'binaryPayload')
    HOS_WEB_TOOLS_RTN_MSG_PARSER_PARSE_BTN = (By.CSS_SELECTOR, "input[value='PARSE']")
    HOS_WEB_TOOLS_RTN_MSG_PARSER_TEXT_AREA = (By.CSS_SELECTOR, "textarea[name='parseMessage']")