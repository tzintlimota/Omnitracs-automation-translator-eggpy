import pytest
from datetime import datetime
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common
import re
import time


class HOS_Status_Test_Case(object):
    def __init__(self, general):
        self.eld_core = IVG_ELD_CORE(general)
        self.general = general
        self.img_proc = self.general.img_proc
        self.ivg_common = IVG_Common(general)

    def clock_in(self, num_min=None, remark1=None, remark2=None, click_continue=None, finish=None):
        format = '%H:%M'
        format2 = '%M'
        clock_page = self.img_proc.expect_image('vnc-clock-in-screen', 'ExpectedScreens', 2)
        if not clock_page:
            self.eld_core.goTo('Status')
            self.img_proc.click_image_by_max_key_points('ELD_Core/StatusTab/ClockInEnabled/ClockInEnabled')
            self.img_proc.expect_image('vnc-clock-in-screen', 'ExpectedScreens', 5)

        print('Currently in CLOCK IN page')

        current_time2 = self.general.retrieve_text_with_config(285, 315, 170, 233, '--psm 1 --oem 3 -c tessedit_char_whitelist=0123456789:')

        # Used regex to remove blanks and jump lines (.strip did not work)
        current_time2 = re.findall(r'\d\d:\d\d', current_time2)
        print(f'Clock In - Current Time  ({current_time2})')

        # This is to subtract the minutes (time) to (current_time2) to new_time that will be entered.
        new_time = datetime.strptime(str(current_time2[0]), format) - datetime.strptime(str(num_min), format2)
        print(f'Clock In - Time to be entered  ({new_time})')

        # Split time to have a list with hh and mm separately
        split_time = str(new_time).split(':')
        print(split_time)

        # Click on hours section to enter new_time hh
        self.img_proc.click_image_by_max_key_points_offset(
            "ELD_Core/StatusTab/ClockRemark1/ClockOutRemarks1",
            140, -120)
        #time.sleep(2)
        print(f'Entering ({split_time[0]}) for HH')
        self.img_proc.send_keys(split_time[0])

        # Click on minutes section to enter new_time mm
        self.img_proc.click_image_by_max_key_points_offset(
            "ELD_Core/StatusTab/ClockRemark1/ClockOutRemarks1",
            170, -120)


        #time.sleep(2)
        print(f'Entering ({split_time[1]}) for MM')
        self.img_proc.send_keys(split_time[1])

        # Hide keyboard
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')

        # Wait for keyboard to close
        self.img_proc.expect_image('vnc-clock-in-screen', 'ExpectedScreens', 2)

        # Enter Remarks
        if remark1:
            total_x, total_y = self.img_proc.click_image_by_max_key_points_offset(
                "ELD_Core/StatusTab/ClockRemark1/ClockOutRemarks1",
                0, 40)
            #self.img_proc.click_image_by_coordinates(total_x, total_y)
            self.img_proc.wait_for_seconds(1)
            self.img_proc.send_keys(remark1)
            # Click again to close remarks dropdown
            self.img_proc.click_image_by_coordinates(total_x, total_y)

        if remark2:
            # Need to do a double click
            total_x, total_y = self.img_proc.click_image_by_max_key_points_offset(
                "ELD_Core/StatusTab/ClockRemark1/ClockOutRemarks1",
                600, 40)
            self.img_proc.wait_for_seconds(1)
            self.img_proc.send_keys(remark2)

        # Click on the OK  button

        #self.img_proc.click_image_by_max_key_points('')

        # Hide keyboard
        self.img_proc.click_image_by_max_key_points('IVG_Common/Home/KeyboardOpen/KeyboardOpen')


