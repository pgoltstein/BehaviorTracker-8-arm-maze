----------------------------------------------------------------------

BehavioralTracker
Version 0.1
May 15th, 2017 by Pieter Goltstein

Tracks a mouse using simple background subtraction
Outputs a video file, tracking coordinates and a .csv file with analyzed occupancy

----------------------------------------------------------------------

Runs on Python version 3.5
- Tested using python 3.5 Mac OSX 64bit, Opencv3 version 3.0.0 (from jlaura)
- Tested using python 3.5 Windows 64bit, Opencv3 version 3.0.0 (from memex)

----------------------------------------------------------------------

Some Installation tips

1. Install python 3.5 (e.g. from the anaconda distribution)

2. Install the ffmpeg binary from the website (not sure if needed, but better to have it)
and install the ffmpeg from menpo (Mac OSX 64) or conda-forge (windows 64)
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
----------------------------------------------------------------------
