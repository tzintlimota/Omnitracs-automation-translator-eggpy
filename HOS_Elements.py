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

    # ----- Administration page -----
    ADMIN_URL = "https://hos.int.omnitracs.com/QHOS/~admin/admin.aspx"
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
    DA_UPDATE_IMG = (By.ID, 'MDriverUC1_messageBar_imgMessage')

    # ----- Carrier administration page -----
    CA_CARRIER_SELECT = (By.ID, "MCarrierUC1_ddlCarriers")

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
    HOS_SETUP_UPDATE_IMG = (By.ID, 'messageBar_imgMessage')
