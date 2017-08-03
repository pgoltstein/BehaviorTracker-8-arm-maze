#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 3, 2017

Simple example of digital output.
This example outputs the values of data on line 0 to 7

@author: pgoltstein
"""

import PyDAQmx
import numpy

# analog_input = PyDAQmx.Task()
digital_output = PyDAQmx.Task()
data = numpy.zeros((1,), dtype=numpy.uint8) + 4
# read = PyDAQmx.int32()
# data = numpy.zeros((1000,), dtype=numpy.float64)

# DAQmx Configure Code
digital_output.CreateDOChan( "Dev1/port0/line0:7", None, PyDAQmx.DAQmx_Val_ChanForAllLines )
# analog_input.CreateAIVoltageChan(
#     "Dev1/ai0","",PyDAQmx.DAQmx_Val_Cfg_Default,-10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)
# analog_input.CfgSampClkTiming("",10000.0,PyDAQmx.DAQmx_Val_Rising,PyDAQmx.DAQmx_Val_FiniteSamps,1000)

# DAQmx Start Code
digital_output.StartTask()
# analog_input.StartTask()

# DAQmx Read Code
samples_written = digital_output.WriteDigitalU8( \
    8, True, 0.1, PyDAQmx.DAQmx_Val_GroupByScanNumber, data, None, None )
# analog_input.ReadAnalogF64(1000,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,1000,PyDAQmx.byref(read),None)

print("Wrote {} samples".format(samples_written))
# print("Acquired {} points".format(read.value))
