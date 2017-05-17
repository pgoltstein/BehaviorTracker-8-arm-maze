----------------------------------------------------------------------

BehavioralTracker
Version 0.1
May 16th, 2017 by Pieter Goltstein

Tracks a mouse in an 8 armed maze using simple background subtraction
Outputs
1. Video file
    Windows: DIVX codec, .avi container
    Mac OSX: h264 codec, .mov container
    Linux: MJPG codec, .avi container
2. Tracking coordinates in a numpy file
3. Analyzed, normalize occupancy per maze arm (Location 0=center) in a .csv file

----------------------------------------------------------------------

Runs on Python version 3.5
- Tested using python 3.5 Mac OSX 64bit, Opencv3 version 3.0.0 (from jlaura)
- Tested using python 3.5 Windows 64bit, Opencv3 version 3.0.0 (from memex)
- NOT TESTED ON LINUX (yet)...

----------------------------------------------------------------------

Some Installation tips

1. Install python 3.5 (e.g. from the anaconda distribution)
If you are already running an anaconda distribution with a different python version,
you can downgrade or create an enviroment with a python 3.5 install

2. Install the ffmpeg binary from the website (not sure if needed, but better to have it)
and install the ffmpeg from menpo (Mac OSX 64, Linux) or conda-forge (windows 64)
>> conda install -c menpo ffmpeg=3.2.4
>> conda install -c conda-forge ffmpeg=3.2.4

3. Make sure you have the numpy, scipy and tkinter packages installed in python

4. Install opencv3 (best to use version 3.0.0)
I had some versioning trouble. The error was cryptic: Opencv seemed to find only python 2.7
It turned out that the problem was that I was running python 3.6, so make sure to run 3.5
You can find the versions of the distrbution in the files list on the anaconda cloud page

On Mac OSX 64 bit: The jlaura distribution from the Anaconda Cloud works well.
>> conda install -c jlaura opencv=3.0.0

On Windows 64 bit: Find a distribution that has Opencv3.0.0 and runs python 3.5.x
    on e.g. the Anaconda Cloud.
>> conda install -c memex opencv=3.0.0

On Linux 64 bit: I did not try, but supposedly the jlaura distribution should work

----------------------------------------------------------------------
