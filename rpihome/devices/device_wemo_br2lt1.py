#!/usr/bin/python3
""" wemo_b2lt1.py: 
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import datetime
import logging
import multiprocessing
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
class Wemo_br2lt1(DeviceWemo):
    def __init__(self, name, ip, msg_out_queue, logger=None):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)
        # Init parent class
        super().__init__(name, ip, msg_out_queue, self.logger)


    def check_rules(self, **kwargs):
        """ Overhead light in kids bedroom """
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
        # Determine if kid is home                    
        if self.homeArray[1] is True:
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
  