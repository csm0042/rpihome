#!/usr/bin/python3
""" device_rpi.py:
"""

# Import Required Libraries (Standard, Third Party, Local) *****************************************
import copy
import logging
from rpihome.devices.device import Device
from rpihome.modules.message import Message


# Authorship Info **********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Device class *************************************************************************************
class DeviceRPI(Device):
    """ Test class and methods for the DeviceRPI class """
    def __init__(self, name, msg_out_queue):
        super().__init__(name, msg_out_queue)

    def command(self):
        """ This method is used to send a single command to various devices when necessary instead
        of sending the same command over and over again """
        if self.state != self.state_mem:
            if self.state is True:
                self.msg_out_queue.put_nowait(
                    Message(source="11", dest="15", type="150", name="rpi", payload="export DISPLAY=:0; xset s reset").raw)
                logging.log(logging.DEBUG, "Sending wake command to RPi Monitor")
            else:
                self.msg_out_queue.put_nowait(
                    Message(source="11", dest="15", type="150", name="rpi", payload="export DISPLAY=:0; xset s activate").raw)
                logging.log(logging.DEBUG, "Sending sleep command to RPi Monitor")
            self.state_mem = copy.copy(self.state)
                              