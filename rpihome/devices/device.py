#!/usr/bin/python3
""" device.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"




# Device state class ******************************************************************************
class Device(object):
    def __init__(self, name, msg_out_queue, logger=None):
        self.name = name
        self.msg_out_queue = msg_out_queue
        self.logger = logger or logging.getLogger(__name__)
        self.state = False
        self.state_mem = None
        self.status = 0
        self.statusChangeTS = datetime.datetime.now()
        self.online = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, str) is True:
            self.__name = value
        else:
            self.logger.error("Improper type attmpted to load into self.name (should be type: str)")

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if isinstance(value, bool) is True:
            self.__state = value
        else:
            self.logger.error(
                "Improper type attmpted to load into self.state (should be type: bool)")

    @property
    def state_mem(self):
        return self.__state_mem

    @state_mem.setter
    def state_mem(self, value):
        if isinstance(value, bool) is True or value == None:
            self.__state_mem = value
        else:
            self.logger.error(
                "Improper type attmpted to load into self.state_mem (should be type: bool/None)")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if isinstance(value, int) is True:
            self.__status = value
        else:
            self.logger.error(
                "Improper type attmpted to load into self.status (should be type: int)")                      

    @property
    def statusChangeTS(self):
        return self.__statusChangeTS

    @statusChangeTS.setter
    def statusChangeTS(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__statusChangeTS = value
        else:
            self.logger.error("Improper type attmpted to load into self.statusChangeTS (should be: datetime)")


    @property
    def online(self):
        return self.__online

    @online.setter
    def online(self, value):
        if isinstance(value, bool) is True or value == None:
            self.__online = value
        else:
            self.logger.error("Improper type attmpted to load into self.online (should be type: bool or None)")
