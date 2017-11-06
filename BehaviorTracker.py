#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple GUI to track 8-arm maze mouse behavior in real time

Created on Wed May 10, 2017
@author: pgoltstein
"""


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
import tkinter as tk
import cv2
import numpy as np
import sys, os, time, datetime
import UserSettings as settings
from sys import platform as _platform

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Detect operating system
if "linux" in _platform.lower():
   OS = "linux" # linux
elif "darwin" in _platform.lower():
   OS = "macosx" # MAC OS X
elif "win" in _platform.lower():
   OS = "windows" # Windows

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Initialize national instruments card
# Warning: WINDOWS ONLY!!!
if OS == "windows" and settings.use_NI == True:
    import nidaqmx
    from nidaqmx.constants import (
        LineGrouping)
    do_ni = True
    DIG_OUT_ALL_ZERO = 0
    DIG_OUT_ACQ_LOW = 1
    DIG_OUT_ACQ_HIGH = 3

    ni_task = nidaqmx.Task()
    ni_task.do_channels.add_do_chan(
        settings.NI_digital_output_port,
        line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
    ni_task.write(DIG_OUT_ALL_ZERO, auto_start=True)
else:
    do_ni = False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Maze coordinates
maze_coordinate_path = os.path.join(settings.data_path,'maze_coordinates.npy')
if not os.path.isfile(maze_coordinate_path):
    maze_coordinates = {}
    maze_coordinates['maze_type']     = "n_arm"
    maze_coordinates['maze_n_arms']   = 8
    maze_coordinates['maze_center']   = (310,287)
    maze_coordinates['maze_radius']   = 30
    maze_coordinates['maze_arm1']     = (366,214)
    maze_coordinates['maze_area_bbx'] = (0,0,
        settings.video_resolution[0],settings.video_resolution[1])
    maze_coordinates['maze_loc_bbxs'] = None
    np.save(maze_coordinate_path,maze_coordinates)
else:
    maze_coordinates = np.load(maze_coordinate_path).item()
maze_type     = maze_coordinates['maze_type']
maze_n_arms   = maze_coordinates['maze_n_arms']
maze_center   = maze_coordinates['maze_center']
maze_radius   = maze_coordinates['maze_radius']
maze_arm1     = maze_coordinates['maze_arm1']
maze_area_bbx = maze_coordinates['maze_area_bbx']
maze_loc_bbxs = maze_coordinates['maze_loc_bbxs']


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main class that handles the video tracking
class MainWindow():
    """Class that runs the main options window"""

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Initialization of the webcam and main window
    def __init__(self, main):

        # Start main window
        self.main = main
        self.main.title("Behavior Tracker")
        tk.Label(self.main, text="-",
            font=(None,16)).grid(sticky=tk.W, row=0, column=0)
        tk.Label(self.main, text="Behavior Tracker (8 arm maze)",
            font=(None,16)).grid(sticky=tk.W, row=0, column=1, columnspan=3)
        tk.Label(self.main, text="-",
            font=(None,16)).grid(sticky=tk.W, row=0, column=4)
        tk.Label(self.main, text="Version 0.1 (May 15th, 2017 by Pieter Goltstein)",
            fg="#555555",font=(None,9)).grid(sticky=tk.W, column=1, columnspan=3)
        tk.Frame(height=2, width=260, bd=1, bg="#aaaaaa",
            relief=tk.SUNKEN).grid(column=1, columnspan=3,pady=10)

        # Create mouse selector menu (row=10)
        tk.Label(self.main, text="Experiment settings").grid(
            column=1, sticky=tk.W, columnspan=3)
        self.mouse_name = tk.StringVar()
        self.mouse_name.set(settings.mouse_names[0])
        tk.Label(self.main, text="Mouse: ").grid(row=10,column=1,sticky=tk.E)
        self.mouse_menu = tk.OptionMenu( self.main,
                                self.mouse_name,*settings.mouse_names)
        self.mouse_menu.config(width=10)
        self.mouse_menu.grid(row=10,column=2,columnspan=2,sticky=tk.W)

        self.flavor_name = tk.StringVar()
        self.flavor_name.set(settings.flavor_names[0])
        tk.Label(self.main, text="Flavor: ").grid(row=11,column=1,sticky=tk.E)
        self.flavor_menu = tk.OptionMenu( self.main,
                                self.flavor_name,*settings.flavor_names)
        self.flavor_menu.config(width=10)
        self.flavor_menu.grid(row=11,column=2,columnspan=2,sticky=tk.W)

        self.startbox_name = tk.StringVar()
        self.startbox_name.set(settings.startbox_names[0])
        tk.Label(self.main, text="Start box: ").grid(row=12,column=1,sticky=tk.E)
        self.startbox_menu = tk.OptionMenu( self.main,
                                self.startbox_name,*settings.startbox_names)
        self.startbox_menu.config(width=10)
        self.startbox_menu.grid(row=12,column=2,columnspan=2,sticky=tk.W)

        tk.Label(self.main, text="Trial duration: ").grid(
            row=18,column=1,sticky=tk.E)
        self.trial_dur_entry = tk.Entry( self.main )
        self.trial_dur_entry.insert(0,str(settings.trial_duration))
        self.trial_dur_entry.config(width=5)
        self.trial_dur_entry.grid(row=18,column=2)
        self.minute_label = tk.Label(self.main, text="min.")
        self.minute_label.grid(row=18,column=3,sticky=tk.W)

        # Preview (row=20)
        tk.Frame(height=2, width=260, bd=1, bg="#aaaaaa",
            relief=tk.SUNKEN).grid(column=1,columnspan=3,pady=10)
        self.preview_button = tk.Button(self.main, text="Preview",
            fg="black", command=self.preview)
        self.preview_button.grid(column=2, pady=5)

        # Template (row=30)
        tk.Frame(height=2, width=260, bd=1, bg="#aaaaaa",
            relief=tk.SUNKEN).grid(column=1,columnspan=3,pady=10)
        tk.Label(self.main, text="Template").grid(
            column=1,columnspan=3,sticky=tk.W)
        self.set_template_button = tk.Button(self.main, text="Set",
            fg="black", command=self.set_template)
        self.set_template_button.grid(row=30,column=1)
        self.show_template_button = tk.Button(self.main, text="Show",
            fg="black", command=self.show_template)
        self.show_template_button.grid(row=30,column=2)

        # Maze coordinates (row=40)
        tk.Frame(height=2, width=260, bd=1, bg="#aaaaaa",
            relief=tk.SUNKEN).grid(column=1,columnspan=3,pady=10)
        tk.Label(self.main, text="Maze coordinates").grid(
            column=1,columnspan=3,sticky=tk.W)
        self.set_maze_center_button = tk.Button(self.main, text="Center",
            fg="black", command=self.set_maze_center)
        self.set_maze_center_button.grid(row=40,column=1)
        self.set_maze_radius_button = tk.Button(self.main, text="Radius",
            fg="black", command=self.set_maze_radius)
        self.set_maze_radius_button.grid(row=40,column=2)
        self.set_maze_arm1_button = tk.Button(self.main, text="Arm 1",
            fg="black", command=self.set_maze_arm1)
        self.set_maze_arm1_button.grid(row=40,column=3)
        self.set_maze_save_button = tk.Button(self.main, text="Save",
            fg="black", command=self.set_maze_save)
        self.set_maze_save_button.grid(row=41,column=3)

        # Tracking (row=50)
        tk.Frame(height=2, width=260, bd=1, bg="#aaaaaa",
            relief=tk.SUNKEN).grid(column=1,columnspan=3,pady=10)
        tk.Label(self.main, text="Tracking").grid(
            column=1,columnspan=3,sticky=tk.W)
        self.start_tracking_button = tk.Button(self.main, text="Start",
            fg="black", command=self.track_mouse)
        self.start_tracking_button.grid(row=50,column=1)
        self.test_tracking_button = tk.Button(self.main, text="Test",
            fg="black", command=self.test_tracking)
        self.test_tracking_button.grid(row=50,column=2)
        self.remaining_label = tk.Label(self.main, text="Recording time:")
        self.remaining_label.grid(row=60,column=1,sticky=tk.E)
        self.rem_time_label = tk.Label(self.main, text="")
        self.rem_time_label.grid(row=60,column=2,sticky=tk.W)

        # Quit (row=100)
        tk.Frame(height=2, width=260, bd=1, bg="#aaaaaa",
            relief=tk.SUNKEN).grid(column=1,columnspan=3,pady=10)
        self.quit_button = tk.Button(self.main,
            text="Quit", fg="red", command=self.quit)
        self.quit_button.grid(row=100,column=3,pady=5,sticky=tk.E)

        # Set main window position
        self.main.update()
        w_main = self.main.winfo_width()
        h_main = 550
        self.main.geometry('{}x{}+{}+{}'.format(w_main, h_main,
            settings.screen_pos[0], settings.screen_pos[1]))

        # Calculate video window position
        self.vid_win_x = settings.screen_pos[0]+w_main
        self.vid_win_y = settings.screen_pos[1]

        # Open webcam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, settings.video_resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.video_resolution[1])


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Preview functions
    def preview(self):
        # Start window and move to correct position
        cv2.imshow('Preview',np.zeros( (settings.video_resolution[0],
                                    settings.video_resolution[1]), dtype=int ))
        cv2.moveWindow('Preview',self.vid_win_x,self.vid_win_y)

        # Capture and show frame-by-frame
        while True:
            ret, frame = self.cap.read()
            cv2.imshow('Preview',frame)
            try:
                k = cv2.waitKey(1) & 0xff
                if k == 27 : break
            except:
                pass

        # Release webcam and close window
        cv2.destroyAllWindows()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Template functions
    def set_template(self):
        # Grab frame, set as template and run show_template
        ret, frame = self.cap.read()
        self.template = frame
        self.show_template()

    def show_template(self):
        # Show template
        template = np.array(self.template)
        self.draw_maze( template )
        cv2.imshow('Template',template)
        cv2.moveWindow('Template',self.vid_win_x,self.vid_win_y)

        # Set callback to make a left click close the window
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.destroyAllWindows()
        cv2.setMouseCallback('Template', mouse_callback)

    def draw_maze(self, image):
        # Draws outline of maze in image
        arm1_ang = np.arctan2( maze_arm1[0]-maze_center[0],
                                maze_arm1[1]-maze_center[1] )
        arm1_radius = int( np.sqrt( ((maze_center[0]-maze_arm1[0])**2) + \
                                    ((maze_center[1]-maze_arm1[1])**2) ) )
        cv2.circle(image, maze_center, maze_radius, (0,0,255), 1)
        cv2.circle(image, maze_center, arm1_radius, (0,0,255), 1)
        for arm in range(8):
            arm_ang = np.mod( ((arm*np.pi)/4) + arm1_ang, 2*np.pi )
            x = int(maze_center[0] + (arm1_radius * np.sin(arm_ang)))
            y = int(maze_center[1] + (arm1_radius * np.cos(arm_ang)))
            plot_col = (127-(127*np.sin(arm_ang)),127,127-(127*np.cos(arm_ang)))
            cv2.arrowedLine(image, maze_center, (x,y), plot_col, 2)
            x = int(maze_center[0] + (arm1_radius*0.7 * np.sin(arm_ang)))
            y = int(maze_center[1] + (arm1_radius*0.7 * np.cos(arm_ang)))
            cv2.putText( image, str(arm+1), (x,y), cv2.FONT_HERSHEY_SIMPLEX,
                2, (0,0,0), thickness=3 )


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Maze coordinate functions
    def set_maze_save(self):
        maze_coordinates = {}
        maze_coordinates['maze_type']     = maze_type
        maze_coordinates['maze_n_arms']   = maze_n_arms
        maze_coordinates['maze_center']   = maze_center
        maze_coordinates['maze_radius']   = maze_radius
        maze_coordinates['maze_arm1']     = maze_arm1
        maze_coordinates['maze_area_bbx'] = maze_area_bbx
        maze_coordinates['maze_loc_bbxs'] = maze_area_bbx
        np.save(maze_coordinate_path,maze_coordinates)

    def set_maze_center(self):
        # Show template
        cv2.imshow('Template',self.template)
        cv2.moveWindow('Template',self.vid_win_x,self.vid_win_y)

        # Set callback to read the maze positions
        def maze_pos_callback(event, x, y, flags, param):
            global maze_center
            if event == cv2.EVENT_LBUTTONDOWN:
                maze_center = (x,y)
                cv2.destroyAllWindows()
                print("Maze center @ coordinates: {} (x,y)".format(maze_center))
        cv2.setMouseCallback('Template', maze_pos_callback)

    def set_maze_radius(self):
        # Show template
        cv2.imshow('Template',self.template)
        cv2.moveWindow('Template',self.vid_win_x,self.vid_win_y)

        # Set callback to read the maze positions
        def maze_pos_callback(event, x, y, flags, param):
            global maze_radius
            if event == cv2.EVENT_LBUTTONDOWN:
                maze_radius = int( np.sqrt( \
                    ((maze_center[0]-x)**2) + ((maze_center[1]-y)**2) ) )
                cv2.destroyAllWindows()
                print("Maze radius @ coordinate {} (x,y)".format(maze_radius))
        cv2.setMouseCallback('Template', maze_pos_callback)

    def set_maze_arm1(self):
        # Show template
        cv2.imshow('Template',self.template)
        cv2.moveWindow('Template',self.vid_win_x,self.vid_win_y)

        # Set callback to read the maze positions
        def maze_pos_callback(event, x, y, flags, param):
            global maze_arm1
            if event == cv2.EVENT_LBUTTONDOWN:
                maze_arm1 = (x,y)
                cv2.destroyAllWindows()
                print("Arm1 @ coordinates: {} (x,y)".format(maze_arm1))
        cv2.setMouseCallback('Template', maze_pos_callback)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Tracking functions
    def track_mouse(self):

        # Get identifiers
        mouse_str = self.mouse_name.get()
        flavor_str = self.flavor_name.get()
        startbox_str = self.startbox_name.get()

        # Create data directory for this mouse
        mouse_path = os.path.join(settings.data_path,mouse_str)
        if not os.path.isdir(mouse_path):
            os.mkdir(mouse_path)

        # Create path for this experiment
        date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        exp_path = \
            os.path.join(mouse_path,date_time)+'-'+flavor_str+'-'+startbox_str
        os.mkdir(exp_path)

        # Define the codec and create VideoWriter object
        if OS == "macosx":
            video_file_name = os.path.join(exp_path,'VideoTracking.mov')
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0,
                (settings.video_resolution[0],settings.video_resolution[1]) )
        elif OS == "windows":
            video_file_name = os.path.join(exp_path,'VideoTracking.avi')
            fourcc = cv2.VideoWriter_fourcc(*'divx')
            video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0,
                (settings.video_resolution[0],settings.video_resolution[1]) )
        elif OS == "linux":
            video_file_name = os.path.join(exp_path,'VideoTracking.avi')
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0,
                (settings.video_resolution[0],settings.video_resolution[1]) )

        # Do the tracking
        timestamps,positions,arm = self.perform_tracking(video_object=video_object)

        # Release video file
        video_object.release()

        # Analyze arm accupancy
        last_time = timestamps[0]
        arm_occupancy = np.zeros(9)
        for t,a in enumerate(arm):
            arm_occupancy[a] = arm_occupancy[a] + (timestamps[t]-last_time)
            last_time = timestamps[t]

        # Save the timestamps and positions
        info_file_name = os.path.join(exp_path,
            'TrackingInfo-'+mouse_str+'-'+flavor_str+'-'+startbox_str)
        occ_file_name = os.path.join(exp_path,'RelativeOccupancy.csv')
        tracker_info = {}
        tracker_info['timestamps'] = timestamps
        tracker_info['positions'] = positions
        tracker_info['arm'] = arm
        tracker_info['arm_occupancy'] = arm_occupancy
        tracker_info['relative_occupancy'] = arm_occupancy/arm_occupancy.sum()
        tracker_info['template'] = np.array(self.template)
        tracker_info['datetime'] = date_time
        tracker_info['mouse'] = mouse_str
        tracker_info['flavor'] = flavor_str
        tracker_info['startbox'] = startbox_str
        np.save(info_file_name, tracker_info)

        # Calculate and save relative occupancy
        rel_occ = list(arm_occupancy/arm_occupancy.sum())
        with open(occ_file_name, "w") as csv_file:
            save_str = "".join(["{:0.5f}, ".format(itm) for itm in rel_occ])
            print("sep=,", file=csv_file)
            print(save_str, file=csv_file)

    def test_tracking(self):
        timestamps,positions,arm = self.perform_tracking(video_object=None)

    def perform_tracking(self, video_object=None):

        # Calculate list with arm angles
        arm_angles = np.zeros(8)
        arm1_ang = np.arctan2( maze_arm1[0]-maze_center[0],
                               maze_arm1[1]-maze_center[1] )
        arm1_offset = (np.pi/8) - arm1_ang
        for arm in range(8):
            arm_angles[arm] = np.mod( ((arm*np.pi)/4) +arm1_offset +arm1_ang, 2*np.pi )

        # Start window and move to correct position
        cv2.imshow('Preview',np.zeros( (settings.video_resolution[0],
                                    settings.video_resolution[1]), dtype=int ))
        cv2.moveWindow('Preview',self.vid_win_x,self.vid_win_y)

        # Adjust template blur
        template = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
        template = cv2.GaussianBlur( template, (61, 61), 11 ).astype(np.float)

        # Capture, track and show frame-by-frame
        mouse_pos = []
        mouse_arm = []
        timestamps = []

        exp_dur_seconds = int(float(self.trial_dur_entry.get()) * 60)
        max_time = exp_dur_seconds + time.time()
        time_remaining = int(max_time-time.time())
        self.rem_time_label.config(text=str(exp_dur_seconds-time_remaining-1)+" s")
        self.main.update()
        last_time = max_time

        # Start NI trigger
        if do_ni:
            ni_task.write(DIG_OUT_ACQ_LOW, auto_start=True)
        while time.time() < max_time:
            time_remaining = int(max_time-time.time())
            if time_remaining != last_time:
                self.rem_time_label.config(text=str(exp_dur_seconds-time_remaining-1)+" s")
                self.main.update()
                last_time = time_remaining

            # Get frame
            if do_ni:
                ni_task.write(DIG_OUT_ACQ_HIGH, auto_start=True)
            ret, frame = self.cap.read()
            if do_ni:
                ni_task.write(DIG_OUT_ACQ_LOW, auto_start=True)

            # Process frame
            timestamps.append(time.time())
            if video_object is not None:
                video_object.write(frame)
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_bw = cv2.GaussianBlur( frame_bw.astype(np.float), (61, 61), 11 )

            # Subtract background
            frame_bw = template-frame_bw
            frame_bw = frame_bw/frame_bw.max()

            # Find mouse
            (_,__,___,max_loc) = cv2.minMaxLoc(frame_bw)
            mouse_pos.append(max_loc)
            mouse_angle = np.mod( np.arctan2( max_loc[0]-maze_center[0],
                                    max_loc[1]-maze_center[1] ) +arm1_offset , 2*np.pi )
            mouse_radius = np.sqrt( ((maze_center[0]-max_loc[0])**2) + \
                                    ((maze_center[1]-max_loc[1])**2) )

            # Classify mouse positions
            if mouse_radius < maze_radius:
                # Mouse = center
                mouse_arm.append(0)
                plot_col = (255,255,255)
            else:
                mouse_arm.append( np.argmin( np.abs(arm_angles-mouse_angle) )+1 )
                plot_col = (127-(127*np.sin(mouse_angle)),127,127-(127*np.cos(mouse_angle)))

            # Draw mouse
            cv2.circle(frame, maze_center, 10, plot_col, 2)
            cv2.circle(frame, max_loc, 10, plot_col, 2)
            cv2.line(frame, maze_center, max_loc, plot_col, 2)

            # Show image and mouse
            cv2.imshow('Preview',frame)
            try:
                k = cv2.waitKey(1) & 0xff
                if k == 27 : break
            except:
                pass

        # Close window and return timestamps and positions
        cv2.destroyAllWindows()
        if do_ni:
            ni_task.write(DIG_OUT_ALL_ZERO, auto_start=True)
        return timestamps,mouse_pos,mouse_arm

    def quit(self):
        self.cap.release()
        quit()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up main window and start main loop
root = tk.Tk()
MainWindow(root)
root.mainloop()
