#!/usr/bin/python3
""" device_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import logging
from .device import Device
from rpihome.modules.message import Message
from rpihome.modules.schedule import Week



# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Device class ************************************************************************************
class DeviceWemo(Device):
    def __init__(self, name, address, msg_out_queue, logger=None):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)        
        super().__init__(name, msg_out_queue, self.logger)
        self.name = name
        self.address = address
        self.msg_out_queue = msg_out_queue
        self.discover_device()

    def discover_device(self):
        self.logger.debug("Sending command to wemo gateway to find device at address: %s", self.address)
        self.msg_to_send = Message(source="11", dest="16", type="160", name=self.name, payload=self.address)
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)


    def command(self):
        """ This method is used to send a single command to various devices when necessary instead
        of sending the same command over and over again """
        if self.state != self.state_mem:
            if self.state is True:
                self.msg_to_send = Message(source="11", dest="16", type="161", name=self.name, payload="on")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug("Sending command to wemo gateway to turn ON device: %s", self.name)
            else:
                self.msg_to_send = Message(source="11", dest="16", type="161", name=self.name, payload="off")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug("Sending command to wemo gateway to turn OFF device: %s", self.name)
            pass
            # Snapshot new device state in memory so the command is only sent once
            self.state_mem = copy.copy(self.state)


    def replace_keywords(self, on_range):
        """ This method takes a specific OnRange structure and checks its on and off trigger times to see if they match certain keywords (eg: sunset).  If a keyword is found, the value is replaced with the actual time that should be associated with that keyword based on the time of year """
        self.logger.debug("Checking on and off times for keyword substitutions")
        if isinstance(on_range.on_time, str):
            self.logger.debug("Keyword detected in place of time in on-time")
            if on_range.on_time.lower() == "sunrise":
                self.logger.debug("Replacing [sunrise] keyword in on-time with today's sunrise time: ", str(self.sunrise.time()))
                on_range.on_time = self.sunrise.time()
            elif on_range.on_time.lower() == "sunset":
                self.logger.debug("Replacing [sunset] keyword in on-time with today's sunrise time: ", str(self.sunset.time()))                
                on_range.on_time = self.sunset.time()  
        if isinstance(on_range.off_time, str):
            self.logger.debug("Keyword detected in place of time in off-time")
            if on_range.off_time.lower() == "sunrise":
                self.logger.debug("Replacing [sunrise] keyword in off-time with today's sunrise time: ", str(self.sunrise.time()))                
                on_range.off_time = self.sunrise.time()
            elif on_range.off_time.lower() == "sunset":
                self.logger.debug("Replacing [sunset] keyword in off-time with today's sunrise time: ", str(self.sunset.time()))                
                on_range.off_time = self.sunset.time()
        return on_range                                
