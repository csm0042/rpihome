#!/usr/bin/python3
""" wemo_fylt1.py: Decision making engine for the RPi Home application  
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import datetime
import logging
import multiprocessing
import devices.device_wemo as device_wemo


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Device class ********************************************************************************************************
class Wemo_b3lt1(device_wemo.DeviceWemo):
    def __init__(self, name, msg_out_queue):
        super().__init__(name, msg_out_queue)


    def check_rules(self, **kwargs):
        """ Overhead light in kids bedroom """
        # Update value stored in dt_now to current datetime
        self.dt = datetime.datetime.now()
        # Process input variables if present  
        self.homeArray = []   
        self.home = False  
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value
                if key == "homeArray":
                    self.homeArray = value 
        # Determine if kid is home                    
        if self.homeArray[2] is True:
            self.home = True                     
        # Decision tree to determine if screen should be awake or not                
        # Monday - Friday
        if 0 <= self.dt.weekday() <= 4:
            if self.home is True:
                if datetime.time(6,0) <= self.dt.time() <= datetime.time(6,30):
                    self.state = True
                else:
                    self.state = False
            else:
                self.state = False
        # Saturday - Sunday
        elif 5 <= self.dt.weekday() <= 6:
            self.state = False
        else:
            self.state = False
        # Return result
        return self.state     