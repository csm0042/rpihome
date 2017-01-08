#!/usr/bin/python3
""" wemo_lrlt2.py: 
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
class Wemo_lrlt2(DeviceWemo):
    def __init__(self, name, ip, msg_out_queue, logger=None):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)        
        # Init parent class
        super().__init__(name, ip, msg_out_queue, self.logger)


    def check_rules(self, **kwargs):
        """This method contains the rule-set that controls internal security lights """
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
        # Determine if anyone is home
        for h in self.homeArray:
            if h is True:
                self.home = True
        # Calculate sunrise / sunset times
        self.sunrise = datetime.datetime.combine(self.dt, self.s.sunrise(self.dt, self.utcOffset))
        self.sunset = datetime.datetime.combine(self.dt, self.s.sunset(self.dt, self.utcOffset))
        # Decision tree to determine if screen should be awake or not
        if self.home is True:
            # If after 5am but before sunrise + the offset minutes
            if self.dt.time() >= datetime.time(5, 0) and self.dt.time() <= datetime.time(22, 0):
                if self.state is False:
                    self.logger.info("Turning on lrlt2")
                self.state = True
            else:
                if self.state is True:
                    self.logger.info("Turning off lrlt2")
                self.state = False
        else:
            if self.state is True:
                self.logger.info("Turning off lrlt2")
            self.state = False
        # Return result
        return self.state