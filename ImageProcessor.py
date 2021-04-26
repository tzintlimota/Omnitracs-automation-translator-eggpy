"""
==============================================================================
	Copyright (c) 2020 Omnitracs, LLC. All rights reserved.

	Confidential and Proprietary - Omnitracs, LLC
	This software may be subject to U.S. and international export, re-export,
	or transfer ("export") laws.

	Diversion contrary to U.S. and international laws is strictly prohibited.
==============================================================================
	ImageProcessor v1.0, originally created by Edgar López
	Last updated on 11/24/2020

	Purpose:
		This script is designed to automate an IVG devide through a VNC Connection
		based on Image Recognition

	Revision history:
		v1.0 (Edgar Lopez, 11/24/2020):
			- Released
"""

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from vncdotool import api
import math
from PIL import Image
import os
from datetime import datetime, timedelta
from datetime import timedelta
import pytesseract
import sys


class ImageProcessor:

    def __init__(self, vnc_ip, vnc_password, precision):
        self.vnc_ip = vnc_ip
        self.vnc_password = vnc_password
        self.client = api.connect(vnc_ip, password=vnc_password)
        self.precision = precision
        self.orb = cv2.ORB_create()
        self.sift = cv2.xfeatures2d.SIFT_create()
        self.img3 = None

    '''This will obtain a screenshot of the full screen. Default resolution 1024x600 for VNC'''

    def get_vnc_full_screen(self, name, images_folder):
        proj_root_path = self.get_project_root_directory()
        target_folder = proj_root_path + "/Images/" + images_folder + "/"
        image = target_folder + name + ".png"
        self.client.captureScreen(image)

    '''This will obtain a screenshot from the rectangle generated by X and Y. Consider that 
    the width and height must be within the limits of the full image'''

    def get_vnc_region_screen(self, name, images_folder, x, y, width, height):

        target_folder = self.get_project_root_directory() + "/Images/" + images_folder + "/"
        image = target_folder + name + ".png"
        #print(image)
        self.client.captureRegion(image, int(x), int(y), int(width), int(height))

    def compare_image(self, img_source, img_compare):
        diffcount = 0
        np_im = np.array(img_compare)
        np_im2 = np.array(img_source)

        '''Subtracs the numpy arrays'''
        np_im_sub = np.subtract(np_im, np_im2)

        '''Converts 3d to 2d'''
        result = np_im_sub[:, :, 0]

        '''Iteration over the 2d numpy array to find values diff from 0'''
        for i in range(len(result)):
            for j in range(len(result[0])):

                if result[i][j] != 0:
                    diffcount += 1

        '''Error Threshold to pass Compare with difference < 10% '''
        error_range = (len(result) * len(result[0])) * float(self.precision)
        #print(int(error_range))

        if int(diffcount) > int(error_range):
            return False
        else:
            print("Image is a Match")
            return True

    def send_keys(self, text):
        for i in range(len(text)):
            self.client.keyPress(text[i])

    def clear_keys(self, count):

        for i in range(count):
            self.client.keyPress("bsp")

    def expect_image(self, image_name, folder_name, wait_seconds):

        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        target_folder = self.get_project_root_directory() + "/Images/"
        image = folder_name + "/" + image_name + ".png"
        image_compare = Image.open(self.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        image_source = Image.open(target_folder + image)
        max_time = datetime.now() + timedelta(seconds=float(wait_seconds))
        img_found = True

        while not self.compare_image(image_compare, image_source):
            print("Comparing Image {" + image_name + "} ...")
            img_found = False
            if datetime.now() >= max_time:
                print("Time limit has been exceeded")
                return img_found

            self.client.captureScreen(target_folder + 'last_screen.png')
            image_compare = Image.open(target_folder + 'last_screen.png')
            time.sleep(.5)

        img_found = True
        return img_found

    def check_md_alert(self):

        self.get_vnc_full_screen('last_screen', 'ExpectedScreens')
        proj_root_path = self.get_project_root_directory()
        image_compare = Image.open(proj_root_path + '\\Images\\ExpectedScreens\\last_screen.png')
        image_source = Image.open(proj_root_path + '\\Images\\ExpectedScreens\\vnc_unknown_position_alert_1.png')

        while self.compare_image(image_compare, image_source):
            print("\n Alert pop-up on HOS app \n")
            self.click_image_by_max_key_points('ELD_Core/StatusTab/OkButton/OkButton')


    def get_image_coordinates(self, screen_capture, image_name):

        img2 = cv2.imread(self.get_project_root_directory() + '\\Images\\Buttons\\' + image_name + '.png')
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        img1 = cv2.imread(self.get_project_root_directory() + '\\Images\\ExpectedScreens\\' + screen_capture + '.png')
        
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        try:
            kp1, descs1 = self.sift.detectAndCompute(img1, None)
            kp2, descs2 = self.sift.detectAndCompute(img2, None)

            # feature matching
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

            matches = bf.match(descs1, descs2)
            matches = sorted(matches, key=lambda x: x.distance)

            list_kp1 = []
            list_kp2 = []

            for mat in matches[:6]:
                # Get the matching keypoints for each of the images
                img1_idx = mat.queryIdx
                img2_idx = mat.trainIdx
                # x - columns
                # y - rows
                # Get the coordinates
                (x1, y1) = kp1[img1_idx].pt
                (x2, y2) = kp2[img2_idx].pt

                # Append to each list
                list_kp1.append((x1, y1))
                list_kp2.append((x2, y2))

            # To identify matches that are probably not correct
            total_x = 0
            total_y = 0
            for i in range(len(list_kp1)):
                total_x += list_kp1[i][0]
                total_y += list_kp1[i][1]

            total_x = total_x / len(list_kp1)
            total_y = total_y / len(list_kp1)

            good_matches = []
            for i in range(len(list_kp1)):
                # print(list_kp1[i][0])
                # print(list_kp1[i][1])

                if not (list_kp1[i][0] < (total_x - 200) or list_kp1[i][0] > (total_x + 200) or list_kp1[i][1] <
                        (total_y - 200) or list_kp1[i][1] > (total_y + 200)):
                    good_matches.append(matches[i])

            list_kp1 = []

            # To get the average of matches
            for mat in good_matches:
                # Get the matching keypoints for each of the images
                img1_idx = mat.queryIdx
                img2_idx = mat.trainIdx
                # x - columns
                # y - rows
                # Get the coordinates
                (x1, y1) = kp1[img1_idx].pt

                # Append to each list
                list_kp1.append((x1, y1))

            total_x = 0
            total_y = 0
            for i in range(len(list_kp1)):
                total_x += list_kp1[i][0]
                total_y += list_kp1[i][1]

            total_x = total_x / len(list_kp1)
            total_y = total_y / len(list_kp1)

            img3 = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, img2, flags=2)
            #plt.imshow(img3)
            #plt.show()
        except:
            total_x = -1
            total_y = -1 
            print("No matches were found")
        return total_x, total_y

    def get_image_coordinates_by_max_key_points(self, image_name):

        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img2 = cv2.imread(self.get_project_root_directory() + '/Images/Buttons/' + image_name + '.png')

        try:
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        except cv2.error as cv_error:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n" + "Error: " + str(cv_error))
            print("Possible cause: The path to the button's image is not correct. By default it will search on "
                  f"Images\Buttons\ \n Path received:  '{os.getcwd()}/Images/Buttons/{image_name}.png' ")
            sys.exit(1)


        img1 = cv2.imread(self.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

        try:
            kp1, descs1 = self.sift.detectAndCompute(img1, None)
            kp2, descs2 = self.sift.detectAndCompute(img2, None)

            # feature matching
            bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

            matches = bf.match(descs1, descs2)
            matches = sorted(matches, key=lambda x: x.distance)

            list_kp1 = []
            list_kp2 = []

            for mat in matches[:6]:
                # Get the matching keypoints for each of the images
                img1_idx = mat.queryIdx
                img2_idx = mat.trainIdx
                # x - columns
                # y - rows
                # Get the coordinates
                (x1, y1) = kp1[img1_idx].pt
                (x2, y2) = kp2[img2_idx].pt

                # Append to each list
                list_kp1.append((x1, y1))
                list_kp2.append((x2, y2))

            # To identify matches that are probably not correct
            avg_distances = []

            for i in range(len(list_kp1)):

                point_x = list_kp1[i][0]
                point_y = list_kp1[i][1]
                acum_dist_avg = 0
                for j in range(len(list_kp1)):
                    acum_dist_avg += math.sqrt((list_kp1[j][0] - point_x) ** 2 + (list_kp1[j][1] - point_y) ** 2)

                acum_dist_avg = acum_dist_avg / len(list_kp1)
                avg_distances.append(acum_dist_avg)

            good_matches = []
            avg_distances_max = np.max(avg_distances)
            for i in range(len(avg_distances)):
                if not avg_distances[i] == avg_distances_max:
                    good_matches.append(matches[i])

            avg_distances = list(filter((avg_distances_max).__ne__, avg_distances))

            avg_avg_distances = np.average(avg_distances)
            cleaned_good_matches = []

            #print(avg_avg_distances)
            #Checar esto con mucho cuidado
            
            max_allowed = avg_avg_distances + avg_avg_distances * .10
            #max_allowed = avg_avg_distances * .90
                # max_allowed = avg_avg_distances
            for i in range(len(avg_distances)):
                if avg_distances[i] <= math.floor(max_allowed):
                    cleaned_good_matches.append(good_matches[i])

            list_kp1 = []
            # To get the average of matches
            for mat in cleaned_good_matches:
                # Get the matching keypoints for each of the images
                img1_idx = mat.queryIdx
                img2_idx = mat.trainIdx
                # x - columns
                # y - rows
                # Get the coordinates
                (x1, y1) = kp1[img1_idx].pt

                # Append to each list
                list_kp1.append((x1, y1))
            
            #print(list_kp1)

            total_x = 0
            total_y = 0

            for i in range(len(list_kp1)):
                total_x += list_kp1[i][0]
                total_y += list_kp1[i][1]

            self.img3 = cv2.drawMatches(img1, kp1, img2, kp2, cleaned_good_matches, img2, flags=2)
            #plt.imshow(self.img3)
            #plt.show()
            avg_distances = []

            for i in range(len(list_kp1)):
                point_x = list_kp1[i][0]
                point_y = list_kp1[i][1]
                acum_dist_avg = 0
                for j in range(len(list_kp1)):
                    acum_dist_avg += math.sqrt((list_kp1[j][0] - point_x) ** 2 + (list_kp1[j][1] - point_y) ** 2)
                acum_dist_avg = acum_dist_avg / len(list_kp1)
                avg_distances.append(acum_dist_avg)
            avg_avg_distances = np.average(avg_distances)

            if avg_avg_distances < 250:
            
                total_x = total_x / len(list_kp1)
                total_y = total_y / len(list_kp1)
            else:
                print(f"Image not identified correctly, try resizing or using another image: {image_name}")
                total_x = -1
                total_y = -1
        except:
            total_x = -1
            total_y = -1 
            print("No matches were found")

        return total_x, total_y

    def click_image(self, image_name):

        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        total_x, total_y = self.get_image_coordinates("last_screen", image_name)
        self.client.mouseMove(math.floor(total_x), math.floor(total_y))
        self.client.mousePress(1)
        time.sleep(0.5)
        print("Clicked on image: " + str(image_name))

    def click_image_by_coordinates(self, x, y):

        self.client.mouseMove(int(x), int(y))
        self.client.mousePress(1)
        time.sleep(0.5)
        print("Clicked on image: " + str(x) + "," + str(y))

    def click_image_pixel_offset(self, image_name, x_offset, y_offset):

        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        total_x, total_y = self.get_image_coordinates("last_screen", image_name)
        self.client.mouseMove(math.floor(total_x + float(x_offset)), math.floor(total_y + float(y_offset)))
        self.client.mousePress(1)
        time.sleep(0.5)
        print("Clicked on image: " + str(image_name) + " with offset in x, y:" + str(x_offset) + "," + str(y_offset))

    def click_image_by_max_key_points_offset(self, image_name, x_offset, y_offset):

        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        total_x, total_y = self.get_image_coordinates_by_max_key_points(image_name)
        cv2.line(self.img3, (math.floor(total_x), math.floor(total_y)),
                 (math.floor(total_x + x_offset), math.floor(total_y + y_offset)), (0, 255, 0), 3)
        #plt.imshow(self.img3)
        #plt.show()
        self.client.mouseMove(math.floor(total_x + float(x_offset)), math.floor(total_y + float(y_offset)))
        self.client.mousePress(1)
        time.sleep(0.5)
        print("Clicked on image: " + str(image_name))
        return total_x, total_y

    def click_image_by_max_key_points(self, image_name):

        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        total_x, total_y = self.get_image_coordinates_by_max_key_points(image_name)
        #plt.imshow(self.img3)
        #plt.show()
        if total_x > 0:
            print('Clicking')
            self.client.mouseMove(math.floor(total_x), math.floor(total_y))
            self.client.mousePress(1)
            time.sleep(0.5)
            print("Clicked on image: " + str(image_name))
        return total_x, total_y

    def get_text_from_image(self, image_name):

        text = pytesseract.image_to_string(os.getcwd() + "\\Images\\" + image_name + ".png")
        return text

    def wait_for_seconds(self, seconds):
        time.sleep(float(seconds))

    def get_timestamp(self):
        time_now = datetime.now()
        print(" Current Time: " + str(time_now))
    
    def roi(self, x, y, im):
        # Select ROI
        img = im
        crop_img = img[int(y-5):int(y+5), int(x-5):int(x+5)]
        plt.imshow(crop_img)
        plt.show()     
        return crop_img 
        # Display cropped image

    
    def color_check(self, x,y ,im):
        img = im
        crop_img = img[int(y-5):int(y+5), int(x-5):int(x+5)]
        crop_img2 = img[int(y-20):int(y+20), int(x-20):int(x+20)]
        #Space color conversion
        #crop_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)
        avg_color_per_row = np.average(crop_img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        print(avg_color)
        #Crop_img2 is just for user convenience, no processing is being made with that image
        plt.imshow(crop_img)
        plt.show()  
        if(avg_color[0] == 255 and avg_color[1] == 255 and avg_color[2] == 255):
            color = 'white'
        elif(avg_color[0] == 0 and avg_color[1] == 0 and avg_color[2] == 0):
            color = 'black'
        elif(avg_color[0] == avg_color[1] and avg_color[0] == avg_color[2] and avg_color[0] >= 110):
            color = 'gray active'
        elif(avg_color[0] == avg_color[1] and avg_color[0] == avg_color[2] and avg_color[0] < 110):
            color = 'gray inactive'
        elif(avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2] and avg_color[1] > 80 and avg_color[1] > avg_color[2]):
            color = 'orange'
        elif(avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]):
            color = 'red'
        elif(avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]):
            color = 'green'
        elif(avg_color[2] > avg_color[0] and avg_color[2] > avg_color[1]):
            color = 'blue'
        elif(avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2] and avg_color[1] > 150 and avg_color[1] > avg_color[2]):
            color = 'yellow'
        else:
            color ='help me learn this color'
        
        return color
    
    def button_is_active(self, image_name, tx, ty):
        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        img2 = cv2.imread(self.get_project_root_directory() + '/Images/Buttons/' + image_name + '.png')
        #img2 = cv2.imread(os.getcwd() +'/' + image_name + '.png')
        #print(img2)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

        img1 = cv2.imread(self.get_project_root_directory() + '/Images/ExpectedScreens/last_screen.png')
        #img1 = cv2.imread(os.getcwd() + '/last_screen.png')
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)

        kp1, descs1 = self.sift.detectAndCompute(img1, None)
        kp2, descs2 = self.sift.detectAndCompute(img2, None)

        # feature matching
        bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

        matches = bf.match(descs1, descs2)
        matches = sorted(matches, key=lambda x: x.distance)

        list_kp1 = []
        list_kp2 = []

        for mat in matches[:8]:
            # Get the matching keypoints for each of the images
            img1_idx = mat.queryIdx
            img2_idx = mat.trainIdx
            # x - columns
            # y - rows
            # Get the coordinates
            (x1, y1) = kp1[img1_idx].pt
            (x2, y2) = kp2[img2_idx].pt

            # Append to each list
            list_kp1.append((x1, y1))
            list_kp2.append((x2, y2))

        # To identify matches that are probably not correct
        avg_distances = []

        for i in range(len(list_kp1)):

            point_x = list_kp1[i][0]
            point_y = list_kp1[i][1]
            acum_dist_avg = 0
            for j in range(len(list_kp1)):
                acum_dist_avg += math.sqrt((list_kp1[j][0] - point_x) ** 2 + (list_kp1[j][1] - point_y) ** 2)

            acum_dist_avg = acum_dist_avg / len(list_kp1)
            avg_distances.append(acum_dist_avg)

        good_matches = []
        avg_distances_max = np.max(avg_distances)
        for i in range(len(avg_distances)):
            if not avg_distances[i] == avg_distances_max:
                good_matches.append(matches[i])

        avg_distances = list(filter((avg_distances_max).__ne__, avg_distances))

        avg_avg_distances = np.average(avg_distances)
        cleaned_good_matches = []

        max_allowed = avg_avg_distances + avg_avg_distances * .10
        # max_allowed = avg_avg_distances
        for i in range(len(avg_distances)):
            if avg_distances[i] <= math.floor(max_allowed):
                cleaned_good_matches.append(good_matches[i])

        list_kp1 = []
        # To get the average of matches
        for mat in cleaned_good_matches:
            # Get the matching keypoints for each of the images
            img1_idx = mat.queryIdx
            img2_idx = mat.trainIdx
            # x - columns
            # y - rows
            # Get the coordinates
            (x1, y1) = kp1[img1_idx].pt

            # Append to each list
            list_kp1.append((x1, y1))

        total_x = 0
        total_y = 0

        for i in range(len(list_kp1)):
            total_x += list_kp1[i][0]
            total_y += list_kp1[i][1]

        total_x = total_x / len(list_kp1)
        total_y = total_y / len(list_kp1)

        self.img3 = cv2.drawMatches(img1, kp1, img2, kp2, cleaned_good_matches, img2, flags=2)
        #plt.imshow(self.img3)
        #plt.show()

        total_x = total_x + tx
        total_y = total_y + ty
        color = self.color_check(total_x, total_y, img1)

        return total_x, total_y, color

    def imageResizer(self, image_name):
        #src = cv2.imread(os.getcwd() + '/Images/Buttons/ELD_Core/LoadTab/EndDay/EndDay.png', cv2.IMREAD_UNCHANGED)

        #percent by which the image is resized
        scale_percent = 100

        #calculate the 50 percent of original dimensions
        width = int(image_name.shape[1] * scale_percent / 100)
        height = int(image_name.shape[0] * scale_percent / 100)

        # dsize
        dsize = (width, height)

        # resize image
        output = cv2.resize(image_name, dsize)
        return output
        #cv2.imwrite(os.getcwd() + '/Images/Buttons/ELD_Core/LoadTab/EndDay/EndDay.png',output)

    def image_exists(self, image_name):

        self.get_vnc_full_screen("last_screen", "ExpectedScreens")
        total_x, total_y = self.get_image_coordinates_by_max_key_points(image_name)
        #plt.imshow(self.img3)
        #plt.show()
        if total_x > 0:
            print(f'Image {image_name} was found')
            return True
        else:
            print(f'Could NOT find Image {image_name}')
            return False

    def get_project_root_directory(self):
        proj_root_path = ''
        file_path = os.getcwd()
        proj_name = 'Omnitracs-automation-translator-eggpy'

        if '/' in file_path:
            dir_list = file_path.split('/')
        else:
            dir_list = file_path.split('\\')

        for i in range(len(dir_list)):
            if dir_list[i] != proj_name:
                proj_root_path += str(dir_list[i]) + '/'
            else:
                break

        proj_root_path += proj_name
        return str(proj_root_path)
