#!/usr/bin/python3
""" device_rpi.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time
import modules.sunrise as sunrise
from devices import device



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
class DeviceRPI(device.Device):
    def __init__(self, name, msg_out_queue):
        super().__init__(name, msg_out_queue) 
        self.new_status = int()
        self.s = sunrise.sun(lat=38.566, long=-90.410)
        self.utcOffset = datetime.timedelta(hours=-6)
        self.sunriseOffset = datetime.timedelta(minutes=30)
        self.sunsetOffset = datetime.timedelta(minutes=-30)
        self.timeout = datetime.timedelta(minutes=-15)
            

    def command(self):
        """ This method is used to send a single command to various devices when necessary instead of sending the same command over and over again """        
        if self.state != self.state_mem:
            if self.state is True:
                self.msg_out_queue.put_nowait("11,15,150,export DISPLAY=:0; xset s reset")
                logging.log(logging.DEBUG, "Sending wake command to RPi Monitor")
            else:
                self.msg_out_queue.put_nowait("11,15,150,export DISPLAY=:0; xset s activate")
                logging.log(logging.DEBUG, "Sending sleep command to RPi Monitor")
            self.state_mem = copy.copy(self.state) 
                              