from ImageProcessor import ImageProcessor
import pytesseract
import os
import time
from datetime import datetime, timedelta
import math



img_proc = ImageProcessor('192.168.100.13', 'None', .15)

''' Colors:
active gray = buttons that are active
inactive gray = buttons that are inactive
'''


x, y , color = img_proc.button_is_active('sound_icon')
print(color)

x, y , color = img_proc.button_is_active('messaging_icon_top')
print(color)

x, y , color = img_proc.button_is_active('warn_2')
print(color)

x, y , color = img_proc.button_is_active('hos_label')
print(color)

x, y , color = img_proc.button_is_active('clockout_disable_french')
print(color)

x, y , color = img_proc.button_is_active('exceptions_btn')
print(color)

x, y , color = img_proc.button_is_active('ok_btn_active_complete')
print(color)


x, y , color = img_proc.button_is_active('active_driver')
print(color)


x, y , color = img_proc.button_is_active('VIR')
print(color)
