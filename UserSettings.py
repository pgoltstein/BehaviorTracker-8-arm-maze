####
###
## Settings for BehaviorTracker.py
#

# Pulldown list contents
mouse_names = ["C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11", "C12", "D1", "D2", "D3", "D4"]
flavor_names = ["ST","CT","PT","yellow","blue","white"]
startbox_names = ["North","East","South","West","left", "right"]

# Duration of a single trial
trial_duration = 10 # minute

# Location where to store data
# data_path = "D:/data/track"
data_path = "C:\data\Script_TryOut"

# Position of the program on the computer monitor
screen_pos = (200,100) # (x,y)

# Resolution of the acquired video
video_resolution = (640,480) # (x,y)

# Digital output port (will only activate on Windows OS)
use_NI = False # Set to True/False to (not) use the NI card when running Windows
NI_digital_output_port = 'Dev1/port0/line0:1'
