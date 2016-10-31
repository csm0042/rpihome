#!/usr/bin/python3
""" wemo_bylt1.py: 
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time
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
class Wemo_bylt1(device_wemo.DeviceWemo):
    def __init__(self, name, msg_out_queue):
        super().__init__(name, msg_out_queue)


    def check_rules(self, **kwargs):
        """ This method contains the rule-set that controls external security lights """
        # Update value stored in dt_now to current datetime
        self.dt = datetime.datetime.now()
        # Process input variables if present 
        self.homeArray = []   
        self.home = False  
        self.utcOffset = -6
        self.sunriseOffset = datetime.timedelta(minutes=30)
        self.sunsetOffset = datetime.timedelta(minutes=-30)
        self.timeout = 15
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value
                if key == "homeArray":
                    self.homeArray = value 
                if key == "home":
                    self.home = value 
                if key == "utcOffset":
                    self.UTCoffset = value
                if key == "sunriseOffset":
                    self.UTCoffset = value
                if key == "sunsetOffset":
                    self.UTCoffset = value   
                if key == "timeout":
                    self.timeout = value                                                          
        # Calculate sunrise / sunset times
        self.sunrise = datetime.datetime.combine(datetime.datetime.today(), self.s.sunrise(self.dt, self.utcOffset))
        self.sunset = datetime.datetime.combine(datetime.datetime.today(), self.s.sunset(self.dt, self.utcOffset)) 
        # Decision tree to automatically time-out light after 15 minutes in the "on" state
        if self.status == 1:
            if datetime.datetime.now() >= self.statusChangeTS + self.timeout:
                self.state = 0
                self.state_mem = None
                self.status = None
                self.statusChangeTS = None
        # Return result
        return self.state