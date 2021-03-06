#!/usr/bin/python3
""" wemo_drlt1.py: 
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
class Wemo_drlt1(DeviceWemo):
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
        # Determine if anyone is home
        for h in self.homeArray:
            if h is True:
                self.home = True
        # Decision tree to determine if screen should be awake or not
        # If before sunrise + 30 minutes
        if 0 <= self.dt.weekday() <= 4:
            if self.homeArray[0] is True:
                if self.homeArray[1] is True or self.homeArray[2] is True:
                    if datetime.time(5,50) <= self.dt.time() <= datetime.time(6,30):
                        if self.state is False:
                            self.logger.info("Turning on drlt1")
                        self.state = True
                    else:
                        if self.state is True:
                            self.logger.info("Turning off drlt1")
                        self.state = False
                else:
                    if datetime.time(6,30) <= self.dt.time() <= datetime.time(7,0):
                        if self.state is False:
                            self.logger.info("Turning on drlt1")
                        self.state = True
                    else:
                        if self.state is True:
                            self.logger.info("Turning off drlt1")
                        self.state = False
            else:
                if self.state is True:
                    self.logger.info("Turning off drlt1")
                self.state = False
        # Return result
        return self.state