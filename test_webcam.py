#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 9, 2017

@author: pgoltstein
"""

import numpy as np
import cv2
import time, datetime


n_test_frames = 20

cap = cv2.VideoCapture(0)

print("Attempting to switch to manual mode")
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.1)
cap.set(cv2.CAP_PROP_FOCUS, 1)
cap.set(cv2.CAP_PROP_GAIN, 3)

# Read the current setting from the camera
test = cap.get(cv2.CAP_PROP_POS_MSEC)
ratio = cap.get(cv2.CAP_PROP_POS_AVI_RATIO)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
contrast = cap.get(cv2.CAP_PROP_CONTRAST)
saturation = cap.get(cv2.CAP_PROP_SATURATION)
hue = cap.get(cv2.CAP_PROP_HUE)
gain = cap.get(cv2.CAP_PROP_GAIN)
exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
auto_exposure = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
focus = cap.get(cv2.CAP_PROP_FOCUS)
auto_focus = cap.get(cv2.CAP_PROP_AUTOFOCUS)
auto_wb = cap.get(cv2.CAP_PROP_XI_AUTO_WB)
manual_wb = cap.get(cv2.CAP_PROP_XI_MANUAL_WB)

print("Test: {}".format(test))
print("Ratio: {}".format(ratio))
print("Frame Rate: {}".format(frame_rate))
print("Height: {}".format(height))
print("Width: {}".format(width))
print("Brightness: {}".format(brightness))
print("Contrast: {}".format(contrast))
print("Saturation: {}".format(saturation))
print("Hue: {}".format(hue))
print("Gain: {}".format(gain))
print("Exposure: {}".format(exposure))
print("Auto_exposure: {}".format(auto_exposure))
print("Focus: {}".format(focus))
print("Auto_focus: {}".format(auto_focus))
print("Auto_wb: {}".format(auto_wb))
print("Manual_wb: {}".format(manual_wb))
t_start = time.time()
for i in range(10):
    ret, frame = cap.read()
t_curr = time.time()
print('Frame time = {} ms'.format( 1000*(t_curr-t_start)/n_test_frames ))


print("Changing frame size to 640x480")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
t_start = time.time()
for i in range(10):
    ret, frame = cap.read()
t_curr = time.time()
print('Frame time = {} ms'.format( 1000*(t_curr-t_start)/n_test_frames ))

print("Changing frame size to 320x240")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
t_start = time.time()
for i in range(10):
    ret, frame = cap.read()
t_curr = time.time()
print('Frame time = {} ms'.format( 1000*(t_curr-t_start)/n_test_frames ))

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)

    # Exit if ESC pressed
    try:
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
    except:
        pass

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
