#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10, 2017

Simple example of digital output.

@author: pgoltstein
"""

import nidaqmx
import time

from nidaqmx.constants import (
    LineGrouping)

with nidaqmx.Task() as task:
    task.do_channels.add_do_chan(
        'Dev1/port0/line0:3',
        line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)

    print('1 Channel N Lines 1 Sample Unsigned Integer Write: ')
    
    for x in range(4):
        print( task.write(x, auto_start=True) )
        time.sleep(0.5)
    
    print( task.write(0, auto_start=True) )
    time.sleep(0.5)
