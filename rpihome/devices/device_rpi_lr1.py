#!/usr/bin/python3
""" device_rpi.py:  
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time
from .device_rpi import DeviceRPI


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
class RPImain(DeviceRPI):
    def __init__(self, name, msg_out_queue, logger=None):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)        
        super().__init__(name, msg_out_queue, self.logger)


    def check_rules(self, **kwargs):
        """ This method contains the rule-set that controls the wake/sleep state of the RPi Homescreen """
        # Process input variables if present
        self.homeArray = []   
        self.home = False  
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value
                if key == "homeArray":
                    self.homeArray = value                                       
        # Determine if anyone is home
        for h in self.homeArray:
            if h is True:
                self.home = True
        # Decision tree to determine if screen should be awake or not    
        if 0 <= self.dt.weekday() <= 4:           
            if self.homeArray[0] is True:
                if self.homeArray[1] is True or self.homeArray[2] is True:
                    if datetime.time(5,30) <= self.dt.time() <= datetime.time(22,0):
                        if self.state is False:
                            self.logger.info("Turning on rpi screen")
                        self.state = True
                    else:
                        if self.state is True:
                            self.logger.info("Turning off rpi screen")
                        self.state = False
                else:
                    if datetime.time(6,30) <= self.dt.time() <= datetime.time(22,0):
                        if self.state is False:
                            self.logger.info("Turning on rpi screen")
                        self.state = True
                    else:
                        if self.state is True:
                            self.logger.info("Turning off rpi screen")
                        self.state = False 
            else:
                if self.state is True:
                    self.logger.info("Turning off rpi screen")
                self.state = False
        elif 5 <= self.dt.weekday() <= 6:
            if self.home is True:
                if datetime.time(6,30) <= self.dt.time() <= datetime.time(22,0):
                    if self.state is False:
                        self.logger.info("Turning on rpi screen")
                    self.state = True
                else:
                    if self.state is True:
                        self.logger.info("Turning off rpi screen")
                    self.state = False
            else:
                if self.state is True:
                    self.logger.info("Turning off rpi screen")
                self.state = False               
        # Invalid day selection
        else:
            if self.state is True:
                self.logger.info("Turning off rpi screen")
            self.state = False
        # Return result
        return self.state           