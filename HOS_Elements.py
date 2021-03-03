#WebElements repository of HOS Portal
from selenium.webdriver.common.by import By

class webElem():
    #----- Administration page -----
    ADMIN_URL = "https://hos.int.omnitracs.com/QHOS/~admin/admin.aspx"
    ADMIN_DRIVERS_LINK = (By.ID,"AdminUC1_hlDrivers")
    ADMIN_CARRIER_LINK = (By.ID,"AdminUC1_h1Carriers")

    #----- Driver administration page -----
    DA_SEARCH_DEPOT_TXT = (By.ID,"MDriverUC1_searchDepotTextBox")
    DA_SEARCH_DEPOT_ALLDRI_OPT = (By.LINK_TEXT,"--- All drivers ---")
    DA_SEARCH_DRIVER_TXT = (By.ID,"MDriverUC1_searchDriverTextBox")

    #----- Carrier administration page -----
    CA_CARRIER_SELECT = (By.ID,"MCarrierUC1_ddlCarriers")


