#!/usr/bin/python3
""" wemo_bylt1.py: 
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time
from .device_wemo import DeviceWemo


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
class Wemo_bylt1(DeviceWemo):
    def __init__(self, name, ip, msg_out_queue, logger=None):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)        
        # Init parent class
        super().__init__(name, ip, msg_out_queue, self.logger)


    def check_rules(self, **kwargs):
        """ This method contains the rule-set that controls external security lights """
        self.home = False
        # Process input variables if present  
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
                    self.utcOffset = value
                if key == "sunriseOffset":
                    self.sunriseOffset = value
                if key == "sunsetOffset":
                    self.sunsetOffset = value   
                if key == "timeout":
                    self.timeout = value                                                          
        # Calculate sunrise / sunset times
        self.sunrise = datetime.datetime.combine(datetime.datetime.today(), self.s.sunrise(self.dt, self.utcOffset))
        self.sunset = datetime.datetime.combine(datetime.datetime.today(), self.s.sunset(self.dt, self.utcOffset)) 
        # Decision tree to automatically time-out light after 15 minutes in the "on" state
        if self.status == 1:
            if datetime.datetime.now() >= self.statusChangeTS + self.timeout:
                self.state = False
                self.state_mem = None
                self.status = None
                self.statusChangeTS = None
        # Return result
        return self.state