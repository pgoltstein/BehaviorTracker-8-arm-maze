####
###
## Settings for BehaviorTracker.py
#

# Pulldown list contents
mouse_names = ["Tst1","Tst2"]
flavor_names = ["Chocolate","Banana","Grape","Citrus","Bacon",\
                "Raspberry", "Peanutbutter","Raspberry-Peanutbutter"]
startbox_names = ["North","East","South","West"]

# Duration of a single trial
trial_duration = 1 # minute

# Location where to store data
# data_path = "D:/data/track"
data_path = "/data/track"

# Position of the program on the computer monitor
screen_pos = (200,100) # (x,y)

# Resolution of the acquired video
video_resolution = (640,480) # (x,y)

# Digital output port (WINDOWS ONLY)
NI_digital_output_port = 'Dev1/port0/line0:1'
