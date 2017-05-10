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
print("Test: ", test)
print("Ratio: ", ratio)
print("Frame Rate: ", frame_rate)
print("Height: ", height)
print("Width: ", width)
print("Brightness: ", brightness)
print("Contrast: ", contrast)
print("Saturation: ", saturation)
print("Hue: ", hue)
print("Gain: ", gain)
print("Exposure: ", exposure)
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
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
