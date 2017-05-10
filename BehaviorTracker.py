#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple GUI to track mouse behavior in a 8-arm radial maze

Created on Wed May 10, 2017
@author: pgoltstein
"""

# Imports
import tkinter as tk
from tkinter import filedialog
# from PIL import Image, ImageTk
import cv2
import numpy as np
import sys

import UserSettings.py

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Class that handles the main window

class MainWindow():
    """Class that runs the main options window"""

    def __init__(self, main):
        self.main = main

        # variables
        self.zoom = 2.2
        self.int_adj = 2
        self.video_filename = ""

        # Create load and save buttons
        self.main.title("Behavior video tracker")
        self.button_load = tk.Button(self.main, text="Select video file",
            fg="black", command=self.select_video_file)
        self.button_load.pack()
        self.button_set_template = tk.Button(self.main, text="Set template",
            fg="black", command=self.set_template)
        self.button_set_template.pack()
        self.button_check_tracking = tk.Button(self.main, text="Check tracking",
            fg="black", command=self.check_tracking)
        self.button_check_tracking.pack()
        self.button_about = tk.Button(self.main,
            text="About", fg="blue", command=self.about)
        self.button_about.pack()
        self.button_quit = tk.Button(self.main,
            text="Quit", fg="red", command=quit)
        self.button_quit.pack()

        # Set main window position
        main.update()
        w_main = self.main.winfo_width()
        h_main = 400
        w_scr = self.main.winfo_screenwidth()
        h_scr = self.main.winfo_screenheight()
        x_main = int(w_scr*0.01)
        y_main = int(h_scr*0.1)
        main.geometry('{}x{}+{}+{}'.format(w_main, h_main, x_main, y_main))

        # start info window
        self.main_position = {'x': x_main+w_main, 'y': y_main}
        self.info_win = InfoWindow(self.main, self.main_position)

        self.select_video_file()
