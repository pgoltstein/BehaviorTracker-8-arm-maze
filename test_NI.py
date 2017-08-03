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

analog_input = PyDAQmx.Task()
read = PyDAQmx.int32()
data = numpy.zeros((1000,), dtype=numpy.float64)

# DAQmx Configure Code
analog_input.CreateAIVoltageChan("Dev1/ai0","",PyDAQmx.DAQmx_Val_Cfg_Default,-10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)
analog_input.CfgSampClkTiming("",10000.0,PyDAQmx.DAQmx_Val_Rising,PyDAQmx.ArrayDAQmx_Val_FiniteSamps,1000)

# DAQmx Start Code
analog_input.StartTask()

# DAQmx Read Code
analog_input.ReadAnalogF64(1000,10.0,PyDAQmx.DAQmx_Val_GroupByChannel,data,1000,byref(read),None)

print("Acquired {} points".format(read.value))
