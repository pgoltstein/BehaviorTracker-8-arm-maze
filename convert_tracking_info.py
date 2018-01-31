#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Saves tracking info to mat file

Created on Wed May 10, 2017
@author: pgoltstein
"""

import numpy as np
import scipy.io as io
import os

dirname = r"I:\Annet Glas\Awake miniscope\170813\A170609\20170813-141407"
source = (dirname + '\TrackingInfo.npy').replace( '\\', '/' )
target = (dirname + '\TrackingInfo.mat').replace( '\\', '/' )

data = np.load( source ).item()
print("Loaded file: {}".format(source))

io.savemat( target , data )
print("Saved as file: {}".format(target))

