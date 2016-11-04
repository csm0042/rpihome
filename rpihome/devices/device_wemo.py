#!/usr/bin/python3
""" device_wemo.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time
from rpihome.devices.device import Device



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
class DeviceWemo(Device):
    def __init__(self, name, msg_out_queue):
        super().__init__(name, msg_out_queue)
        self.new_status = int()             
          

    def command(self):  
        """ This method is used to send a single command to various devices when necessary instead of sending the same command over and over again """ 
        if self.state != self.state_mem:
            if self.state is True:
                self.msg_out_queue.put_nowait("11,16,161,%s" % self.name)
                logging.log(logging.DEBUG, "Sending command to wemo gateway to turn ON device: %s" % self.name)
            else:
                self.msg_out_queue.put_nowait("11,16,160,%s" % self.name)
                logging.log(logging.DEBUG, "Sending command to wemo gateway to turn OFF device: %s" % self.name)
            pass
            # Snapshot new device state in memory so the command is only sent once
            self.state_mem = copy.copy(self.state)                         