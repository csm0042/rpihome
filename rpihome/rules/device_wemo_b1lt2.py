#!/usr/bin/python3
""" wemo_b1lt2.py: 
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
class Wemo_b1lt2(device_wemo.DeviceWemo):
    def __init__(self, name, msg_out_queue):
        super().__init__(name, msg_out_queue)


    def check_rules(self, **kwargs):
        """ Nightstand light in parent bedroom """
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
                if key == "home":
                    self.home = value 
        # Determine if anyone is home
        for h in self.homeArray:
            if h is True:
                self.home = True
        # Decision tree to determine if screen should be awake or not                
        # Monday - Friday
        if 0 <= self.dt.weekday() <= 4:
            if self.homeArray[0] is True:
                if self.homeArray[1] is True or self.homeArray[2] is True:
                    if datetime.time(5,40) <= self.dt.time() <= datetime.time(6,40):
                        self.state = True
                    else:
                        self.state = False
                else:
                    if datetime.time(6,20) <= self.dt.time() <= datetime.time(7,10):
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