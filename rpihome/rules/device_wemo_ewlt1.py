#!/usr/bin/python3
""" wemo_ewlt1.py: 
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
class Wemo_ewlt1(device_wemo.DeviceWemo):
    def __init__(self, name, msg_out_queue):
        super().__init__(name, msg_out_queue)
        


    def check_rules(self, **kwargs):
        """ This method contains the rule-set that controls external security lights """
        # Update value stored in dt_now to current datetime
        self.dt = datetime.datetime.now()
        # Process input variables if present 
        self.homeArray = []  
        self.homeTime = []          
        self.home = False 
        self.homeNew = False 
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
                if key == "homeTime":
                    self.homeTime = value                    
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
        # Determine if anyone is home
        for h in self.homeArray:
            if h is True:
                self.home = True
        # Determine if someone has recently come home
        for i, j in enumerate(self.homeArray):
            if j is True:
                if self.dt < self.homeTime[i] + datetime.timedelta(minutes=10):
                    self.homeNew = True
        # Decision tree to determine if screen should be awake or not
        if self.homeNew is True and (self.dt.time() >= self.sunset.time() or self.dt.time() <= self.sunrise.time()):
            self.state = True
        else:
            # If before sunrise + 30 minutes
            if 0 <= self.dt.weekday() <= 4:
                if self.homeArray[0] is True:
                    if self.homeArray[1] is True or self.homeArray[2] is True:
                        if datetime.time(5,50) <= self.dt.time() <= datetime.time(6,40):
                            self.state = True
                        else:
                            self.state = False
                    else:
                        if datetime.time(6,30) <= self.dt.time() <= datetime.time(7,10):
                            self.state = True
                        else:
                            self.state = False
                else:
                    self.state = False
            elif 5 <= self.dt.weekday() <= 6:
                self.state = False
        # Return result
        return self.state