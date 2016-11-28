#!/usr/bin/python3
""" device_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import logging
from device import Device
from rpihome.modules.message import Message



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
        super().__init__(name, msg_out_queue)
        self.name = name
        self.address = address
        self.msg_out_queue = msg_out_queue
        self.discover_device()

    def discover_device(self):
        self.logger.debug("Sending command to wemo gateway to find device at address: %s",
                          self.address)
        self.msg_to_send = Message(source="11", dest="16", type="160",
                                   name=self.name, payload=self.address)
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)


    def command(self):
        """ This method is used to send a single command to various devices when necessary instead
        of sending the same command over and over again """
        if self.state != self.state_mem:
            if self.state is True:
                self.msg_to_send = Message(
                    source="11", dest="16", type="161", name=self.name, payload="on")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug(
                    "Sending command to wemo gateway to turn ON device: %s", self.name)
            else:
                self.msg_to_send = Message(
                    source="11", dest="16", type="161", name=self.name, payload="off")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug(
                    "Sending command to wemo gateway to turn OFF device: %s", self.name)
            pass
            # Snapshot new device state in memory so the command is only sent once
            self.state_mem = copy.copy(self.state)
