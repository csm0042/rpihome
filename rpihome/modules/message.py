#!/usr/bin/python3
""" message.py: Helper Class and methods for inter-process message class
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Message Helper Class *****************************************************************************
class Message(object):
    def __init__(self, **kwargs):
        self.source = str()
        self.dest = str()
        self.type = str()
        self.name = str()
        self.payload = str()
        self.part = []
        # Process input variables if present    
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "source":
                    self.source = value
                if key == "dest":
                    self.dest = value 
                if key == "type":
                    self.type = value                    
                if key == "name":
                    self.name = value 
                if key == "payload":
                    self.payload = value
                if key == "raw":
                    self.raw = value


    @property
    def raw(self):
        return (self.source + "," + self.dest + "," + self.type + "," +
                self.name + "," + self.payload)

    @raw.setter
    def raw(self, value):
        if isinstance(value, str) is True:
            self.part = value.split(sep=",", maxsplit=4)
            if len(self.part) >= 1:
                self.source = self.part[0]
            if len(self.part) >= 2:                
                self.dest = self.part[1]
            if len(self.part) >= 3:                
                self.type = self.part[2]
            if len(self.part) >= 4:                
                self.name = self.part[3]
            if len(self.part) >= 5:                
                self.payload = self.part[4]

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        if isinstance(value, str) is True:
            self.__source = value

    @property
    def dest(self):
        return self.__dest

    @dest.setter
    def dest(self, value):
        if isinstance(value, str) is True:
            self.__dest = value

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if isinstance(value, str) is True:
            self.__type = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, str) is True:
            self.__name = value

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, value):
        if isinstance(value, str) is True:
            self.__payload = value
                         