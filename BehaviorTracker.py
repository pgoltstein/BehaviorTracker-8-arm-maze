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


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Maze coordinates
maze_coordinate_path = os.path.join(settings.data_path,'maze_coordinates.npy')
if not os.path.isfile(maze_coordinate_path):
    maze_coordinates = {}
    maze_coordinates['maze_center'] = (310,287)
    maze_coordinates['maze_radius'] = 30
    maze_coordinates['maze_arm1'] = (366,214)
    np.save(maze_coordinate_path,maze_coordinates)
else:
    maze_coordinates = np.load(maze_coordinate_path).item()
maze_center = maze_coordinates['maze_center']
maze_radius = maze_coordinates['maze_radius']
maze_arm1 = maze_coordinates['maze_arm1']


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

        # Create mouse selector menu
        self.mouse_name = tk.StringVar()
        self.mouse_name.set(settings.mouse_names[0])
        self.mouse_label = tk.Label(self.main, text="Mouse: ")
        self.mouse_label.grid(row=0,column=0)
        self.mouse_menu = tk.OptionMenu( self.main,
                                self.mouse_name,*settings.mouse_names)
        self.mouse_menu.config(width=10)
        self.mouse_menu.grid(row=0,column=1,columnspan=2)

        self.trial_dur_label = tk.Label(self.main, text="Trial duration: ")
        self.trial_dur_label.grid(row=1,column=0)
        self.trial_dur_entry = tk.Entry( self.main )
        self.trial_dur_entry.insert(0,str(settings.trial_duration))
        self.trial_dur_entry.config(width=5)
        self.trial_dur_entry.grid(row=1,column=1)
        self.minute_label = tk.Label(self.main, text="min.")
        self.minute_label.grid(row=1,column=2)

        # Preview
        self.preview_button = tk.Button(self.main, text="Preview",
            fg="black", command=self.preview)
        self.preview_button.grid(row=3,column=0)

        # Template
        self.template_label = tk.Label(self.main, text="Template")
        self.template_label.grid(row=4,column=0)
        self.set_template_button = tk.Button(self.main, text="Set",
            fg="black", command=self.set_template)
        self.set_template_button.grid(row=5,column=0)
        self.show_template_button = tk.Button(self.main, text="Show",
            fg="black", command=self.show_template)
        self.show_template_button.grid(row=5,column=1)

        # Maze location
        self.maze_label = tk.Label(self.main, text="Maze")
        self.maze_label.grid(row=6,column=0)
        self.set_maze_center_button = tk.Button(self.main, text="Center",
            fg="black", command=self.set_maze_center)
        self.set_maze_center_button.grid(row=7,column=0)
        self.set_maze_radius_button = tk.Button(self.main, text="Radius",
            fg="black", command=self.set_maze_radius)
        self.set_maze_radius_button.grid(row=7,column=1)
        self.set_maze_arm1_button = tk.Button(self.main, text="Arm 1",
            fg="black", command=self.set_maze_arm1)
        self.set_maze_arm1_button.grid(row=7,column=2)
        self.set_maze_save_button = tk.Button(self.main, text="Save",
            fg="black", command=self.set_maze_save)
        self.set_maze_save_button.grid(row=8,column=2)

        # Tracking
        self.tracking_label = tk.Label(self.main, text="Tracking")
        self.tracking_label.grid(row=9,column=0)
        self.start_tracking_button = tk.Button(self.main, text="Start",
            fg="black", command=self.track_mouse)
        self.start_tracking_button.grid(row=10,column=0)
        self.test_tracking_button = tk.Button(self.main, text="Test",
            fg="black", command=self.test_tracking)
        self.test_tracking_button.grid(row=10,column=1)
        self.remaining_label = tk.Label(self.main, text="Remaining")
        self.remaining_label.grid(row=11,column=0)
        self.rem_time_label = tk.Label(self.main, text="")
        self.rem_time_label.grid(row=11,column=1)

        # Quit
        self.spacing_label = tk.Label(self.main, text=" ")
        self.spacing_label.grid(row=12,column=2)
        self.quit_button = tk.Button(self.main,
            text="Quit", fg="red", command=self.quit)
        self.quit_button.grid(row=13,column=2)

        # Set main window position
        self.main.update()
        w_main = self.main.winfo_width()
        h_main = 400
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
            arm_ang = ((arm*np.pi)/4) + arm1_ang
            x = int(maze_center[0] + (arm1_radius * np.sin(arm_ang)))
            y = int(maze_center[1] + (arm1_radius * np.cos(arm_ang)))
            cv2.arrowedLine(image, maze_center, (x,y), (255,0,0), 0)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Maze coordinate functions
    def set_maze_save(self):
        maze_coordinates = {}
        maze_coordinates['maze_center'] = maze_center
        maze_coordinates['maze_radius'] = maze_radius
        maze_coordinates['maze_arm1'] = maze_arm1
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

        # Create data directory for this mouse
        mouse_path = os.path.join(settings.data_path,self.mouse_name.get())
        if not os.path.isdir(mouse_path):
            os.mkdir(mouse_path)

        # Create path for this experiment
        date_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        exp_path = os.path.join(mouse_path,date_time)
        os.mkdir(exp_path)

        # Define the codec and create VideoWriter object
        video_file_name = os.path.join(exp_path,'VideoTracking.mov')
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        video_object = cv2.VideoWriter( video_file_name,fourcc, 30.0,
            (settings.video_resolution[0],settings.video_resolution[1]) )

        # Do the tracking
        timestamps,positions = self.perform_tracking(video_object=video_object)

        # Release video file
        video_object.release()

        # Save the timestamps and positions
        info_file_name = os.path.join(exp_path,'TrackingInfo')
        tracker_info = {}
        tracker_info['timestamps'] = timestamps
        tracker_info['positions'] = positions
        np.save(info_file_name, tracker_info)

    def test_tracking(self):
        timestamps,positions = self.perform_tracking(video_object=None)
        t0 = timestamps[0]
        for t,p in zip(timestamps,positions):
            print("{}: {}".format(int(1000*(t-t0)),p))

    def perform_tracking(self, video_object=None):
        # Start window and move to correct position
        cv2.imshow('Preview',np.zeros( (settings.video_resolution[0],
                                    settings.video_resolution[1]), dtype=int ))
        cv2.moveWindow('Preview',self.vid_win_x,self.vid_win_y)

        # Adjust template blur
        template = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
        template = cv2.GaussianBlur( template, (61, 61), 11 ).astype(np.float)

        # Capture, track and show frame-by-frame
        mouse_pos = []
        timestamps = []
        max_time = (float(self.trial_dur_entry.get()) * 60) + time.time()
        while time.time() < max_time:

            # Get and process frame
            ret, frame = self.cap.read()
            timestamps.append(time.time())
            if video_object is not None:
                video_object.write(frame)
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_bw = cv2.GaussianBlur( frame_bw.astype(np.float), (61, 61), 11 )

            # Subtract background
            frame_bw = template-frame_bw
            frame_bw = frame_bw/frame_bw.max()

            # Find and draw mouse
            (_,__,___,max_loc) = cv2.minMaxLoc(frame_bw)
            mouse_pos.append(max_loc)
            cv2.circle(frame, max_loc, 10, (0,0,255), 1)

            # Show image and mouse
            cv2.imshow('Preview',frame)
            try:
                k = cv2.waitKey(1) & 0xff
                if k == 27 : break
            except:
                pass

        # Close window and return timestamps and positions
        cv2.destroyAllWindows()
        return timestamps,mouse_pos

    def quit(self):
        self.cap.release()
        quit()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set up main window and start main loop
root = tk.Tk()
MainWindow(root)
root.mainloop()