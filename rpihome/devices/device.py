#!/usr/bin/python3
""" device.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import datetime


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"




# Device state class **************************************************************************************************
class Device(object):
    def __init__(self, name, msg_out_queue):
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

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, str) is True:
            self.__name = value
        else:
            raise Exception("Improper type attmpted to load into self.name (should be type: str)")

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        if isinstance(value, bool) is True:
            self.__state = value
        else:
            raise Exception("Improper type attmpted to load into self.state (should be type: bool)")   

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if isinstance(value, int) is True:
            self.__status = value
        else:
            raise Exception("Improper type attmpted to load into self.status (should be type: int)")  

    @property
    def statusChangeTS(self):
        return self.__statusChangeTS

    @statusChangeTS.setter
    def statusChangeTS(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__statusChangeTS = value
        else:
            raise Exception("Improper type attmpted to load into self.statusChangeTS (should be type: datetime)")  

    @property
    def online(self):
        return self.__online

    @online.setter
    def online(self, value):
        if isinstance(value, bool) is True:
            self.__online = value
        else:
            raise Exception("Improper type attmpted to load into self.online (should be type: bool)") 

    @property
    def dt(self):
        return self.__dt

    @dt.setter
    def dt(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__dt = value
        else:
            raise Exception("Improper type attmpted to load into self.dt")             

    @property
    def home(self):
        return self.__home

    @home.setter
    def home(self, value):
        if isinstance(value, bool) is True:
            self.__home = value
        else:
            raise Exception("Improper type attmpted to load into self.home")                                                               