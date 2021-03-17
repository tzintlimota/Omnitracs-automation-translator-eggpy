import pytest
from IVG_ELD_CORE import IVG_ELD_CORE
from IVG_Common import IVG_Common


class HOS_Unassigned_Driving_Test_Case(object):
    def __init__(self, general):
        self.eld_core = IVG_ELD_CORE(general)
        self.general = general
        self.img_proc = self.general.img_proc
        self.ivg_common = IVG_Common(general)

    def accept_unassigned_events(self, uva_type='', remark1=None, remark2=None):
        if self.img_proc.expect_image('vnc-review-unassigned-driving-event', 'ExpectedScreens', 2):
            print('Already in Please Review All Unassigned Driving Events screen')
        else:
            self.eld_core.goToHOS()
            self.img_proc.expect_image('vnc-review-unassigned-driving-event', 'ExpectedScreens', 3)

        self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/NextButton/NextButton')

        # Accepting UVA by clicking NEXT button
        text = self.general.retrieve_text(530, 570, 755, 840)
        if 'reject' in text.lower():
            print('Currently in Review Unassigned Driving Time screen')
            self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/NextButton/NextButton')

        # Click on Status dropdown
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 55, 35)

        if not uva_type:
            print("Selecting D for unassigned driving event")
            self.img_proc.click_image_by_max_key_points_offset(
                'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 45, 70)
        elif uva_type.lower() in 'pc':
            print("Selecting PC for unassigned driving event")
            self.img_proc.click_image_by_max_key_points_offset(
                'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 45, 100)
        elif uva_type.lower() in 'ym':
            print("Selecting YM for unassigned driving event")
            self.img_proc.click_image_by_max_key_points_offset(
                'ELD_Core/UnassignedDriving/UVAStatusDropdownMenu_A/UVAStatusDropdownMenu_A', 45, 130)

        # Click on first field of remarks to enter a comment
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1', 45, 55)
        if not remark1:
            print("Entering text for default remarks1 'AUTOMATED TESTING'")
            self.img_proc.send_keys('AUTOMATION TESTING')
        else:
            print(f"Entering text for remarks1 {remark1}...")
            self.img_proc.send_keys(remark1)

        # Click to close the remarks1 dropdown
        self.img_proc.click_image_by_max_key_points(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1')

        # Click on the second field of remarks to enter a comment
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1', 545, 50)
        if not remark2:
            print("Entering text for default remarks1 'AUTOMATED TESTING'")
            self.img_proc.send_keys('AUTOMATION x2')
        else:
            print(f"Entering text for remarks1 {remark2}...")
            self.img_proc.send_keys(remark2)

        # Double Click to close the remarks2 dropdown
        self.img_proc.click_image_by_max_key_points(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1')
        self.img_proc.click_image_by_max_key_points(
            'ELD_Core/UnassignedDriving/RemarksTextBox1/RemarksTextBox1')

        # Enter LOCATION value in case the field is empty
        self.img_proc.click_image_by_max_key_points_offset(
            'ELD_Core/UnassignedDriving/Location/Location', 45, 50)
        self.img_proc.send_keys('AUTOMATED LOCATION')

        # Click CONFIRM button
        self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/ConfirmButton/ConfirmButton')

        # A prompt to confirm the unassigned driving event appears
        confirm_popup = self.img_proc.expect_image('vnc-unassigned-event-confirm-popup', 'ExpectedScreens', 3)
        assert confirm_popup, "CONFIRMATION pop up should have appeared"

        # Click YES to confirm the UVA
        self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/YesButton/YesButton')

        # Return Main HOS page
        self.eld_core.goToHOS()

        print("Unassigned Driving Event has been ACCEPTED")

    def reject_unassigned_events(self, confirm_bool, reject_comment=None):
        if self.img_proc.expect_image('vnc-review-unassigned-driving-event', 'ExpectedScreens', 2):
            print('Already in Please Review All Unassigned Driving Events screen')
        else:
            self.eld_core.goToHOS()
            self.img_proc.expect_image('vnc-review-unassigned-driving-event', 'ExpectedScreens', 3)

        self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/NextButton/NextButton')

        self.img_proc.expect_image('vnc-unassigned-event-review-time', 'ExpectedScreens', 2)

        # Rejecting UVA by clicking REJECT button
        text = self.general.retrieve_text(530, 570, 755, 840)
        if 'reject' in text.lower():
            print('Currently in Review Unassigned Driving Time screen')
            self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/RejectButton/RejectButton')

        assert self.img_proc.expect_image('vnc-unassigned-event-comment-reject', 'ExpectedScreens', 3)

        # Entering comment for reject reason
        self.img_proc.click_image_by_max_key_points_offset('ELD_Core/UnassignedDriving/RejectUnassignedDrivingTimeReason/'
                                                           'RejectUnassignedDrivingTimeReason', 10, 40)
        if not reject_comment:
            print("Entering text for default REJECT REASON")
            self.img_proc.send_keys('AUTOMATION TESTING')
        else:
            self.img_proc.send_keys(reject_comment)

        if self.img_proc.expect_image('vnc-unassigned-event-comment-reject-keyboard', 'ExpectedScreens', 2):
            # Closing Keyword
            self.img_proc.click_image_by_max_key_points('keyword_icon')

        if confirm_bool or str(confirm_bool).lower() == 'true':
            self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/SaveButton/SaveButton')
            print('Unassigned Driving Event has been SAVED')
        else:
            self.img_proc.click_image_by_max_key_points('ELD_Core/UnassignedDriving/CancelButton/CancelButton')
            print('Unassigned Driving Event has been CANCELED')

        assert self.img_proc.expect_image('vnc-unassigned-event-review-time', 'ExpectedScreens', 2), "REVIEW screen " \
                                                                                                     "should be displayed"
        # Returning to HOS Main page
        self.eld_core.goToHOS()
