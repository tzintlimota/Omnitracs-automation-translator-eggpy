from ImageProcessor import ImageProcessor
#import pytesseract
from IVG_Common import IVG_Common
import os
import cv2
import time
from datetime import datetime, timedelta, date
import math
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
from dateutil.parser import parse
import connection_credentials as cfg
import re
import sys

from General_Access_Functions import General_Access


class HOS_PC_YM(object):
    def __init__(self, general):
        self.eld_core = IVG_ELD_CORE(general)
        self.general = general
        self.img_proc = self.general.img_proc
        self.ivg_common = IVG_Common(general)

    def handle_pc_confirm_prompt(self, confirm=True):
        print("*** HOS_PC_YM.handle_pc_confirm_prompt ***")
        found = self.img_proc.expect_image('vnc-pc-confirm', 'ExpectedScreens', 5)
        if found and confirm:
            self.img_proc.click_image_by_max_key_points('msg-confirm-yes')
        else:
            self.img_proc.click_image_by_max_key_points('NoButton')

    def get_imui_view_text(self):
        print("*** HOS_PC_YM.get_imui_view_text ***")
        y, y1, x, x1 = 200, 400, 10, 1000
        dot_text = self.general.retrieve_text_with_config(y, y1, x, x1)
        print(f'Text retrieved from IMUI screen: {str(dot_text).strip()}')
        return str(dot_text).strip()


