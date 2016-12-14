#!/usr/bin/python3
""" device.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
from rpihome.modules.sun import Sun
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




# Device state class ******************************************************************************
class Device(object):
    def __init__(self, name, msg_out_queue, logger=None):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)        
        self.name = name
        self.msg_out_queue = msg_out_queue
        self.state = False
        self.state_mem = None
        self.status = 0
        self.statusChangeTS = datetime.datetime.now()
        self.online = False
        self.dt = datetime.datetime.now()
        self.home = False
        self.homeArray = []
        self.homeTime = []
        self.homeNew = False
        self.s = Sun(lat=38.566, long=-90.410)
        self.utcOffset = datetime.timedelta(hours=0)
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.timeout = datetime.timedelta(minutes=-15)
        self.msg_to_send = Message()
        self.check_int = int()


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, str) is True:
            self.__name = value
        else:
            self.logger.error(
                "Improper type attmpted to load into self.name (should be type: str)")

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

    @property
    def dt(self):
        return self.__dt

    @dt.setter
    def dt(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__dt = value
        else:
            self.logger.error("Improper type attmpted to load into self.dt")

    @property
    def home(self):
        return self.__home

    @home.setter
    def home(self, value):
        if isinstance(value, bool) is True or value == None:
            self.__home = value
        else:
            self.logger.error("Improper type attmpted to load into self.home (should be type: bool or None)")

    @property
    def homeArray(self):
        return self.__homeArray

    @homeArray.setter
    def homeArray(self, value):
        if isinstance(value, list) is True:
            self.__homeArray = value
        else:
            self.logger.error("Improper type attmpted to load into self.homeArray \
                          (should be type: list)")

    @property
    def utcOffset(self):
        return self.__utcOffset

    @utcOffset.setter
    def utcOffset(self, value):
        if isinstance(value, datetime.timedelta) is True:
            self.__utcOffset = value
        else:
            self.logger.error("Improper type attmpted to load into self.utcOffset \
                          (should be type: datetime.timedelta)")                                  
