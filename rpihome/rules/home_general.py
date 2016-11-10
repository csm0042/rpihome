#!/usr/bin/python3
"""
home_general.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import datetime
import logging
import os
import platform
import ipaddress
import subprocess


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Define Occupancy Class **********************************************************************************************
class HomeGeneral(object):
    def __init__(self):
        self.yes = False
        self.__yes = False
        self.mem = None
        self.mode = 2        
        self.mac = "00:00:00:00:00:00"
        self.ip = "192.168.1.1"
        self.pingResponse = None
        self.home_time = datetime.datetime.now() + datetime.timedelta(seconds=-30)
        self.last_seen = datetime.datetime.now() + datetime.timedelta(seconds=-30)
        self.last_arp = datetime.datetime.now() + datetime.timedelta(seconds=-30)
        self.last_ping = datetime.datetime.now() + datetime.timedelta(seconds=-30) 
        self.eveningCutoff = datetime.time(18,0)
        self.morningCutoff = datetime.time(8,0)               
        self.dt = datetime.datetime.now()
        self.output = str()
        self.index = int()

    @property
    def yes(self):
        return self.__yes

    @yes.setter
    def yes(self, value):
        if isinstance(value, bool) is True or value == None:
            self.__yes = value
        else:
            logging.log(logging.DEBUG, "Invalid type attmpted to load into self.yes (should be type bool or None)")

    @property
    def mem(self):
        return self.__mem

    @mem.setter
    def mem(self, value):
        self.__mem = value       

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, value):
        if 0 <= value <= 5:
            self.__mode = value
        else:
            self.__mode = 2
            logging.log(logging.DEBUG, "Invalid mode entered.  Defaulting to mode=2 (by schedule)")        

    @property
    def mac(self):
        return self.__mac

    @mac.setter
    def mac(self, value):
        if isinstance(value, str) is True:
            self.__mac = value
        else:
            logging.log(logging.DEBUG, "Invalid mac id entered")
            self.__mac = "00:00:00:00:00:00"

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        try:
            ipaddress.ip_address(value)
            self.__ip = value
        except:
            self.__ip = "192.168.1.1"
            logging.log(logging.DEBUG, "Invalid IP address entered")

    @property
    def home_time(self):
        return self.__home_time

    @home_time.setter
    def home_time(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__home_time = value 
        else:
            logging.log(logging.DEBUG, "Invalid value entered for self.home_time.  Leaving value unchanged") 

    @property
    def last_seen(self):
        return self.__last_seen

    @last_seen.setter
    def last_seen(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__last_seen = value 
        else:
            logging.log(logging.DEBUG, "Invalid value entered for self.last_seen.  Leaving value unchanged")  

    @property
    def last_arp(self):
        return self.__last_arp

    @last_arp.setter
    def last_arp(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__last_arp = value 
        else:
            logging.log(logging.DEBUG, "Invalid value entered for self.last_arp.  Leaving value unchanged")  

    @property
    def last_ping(self):
        return self.__last_ping

    @last_ping.setter
    def last_ping(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__last_ping = value 
        else:
            logging.log(logging.DEBUG, "Invalid value entered for self.last_ping.  Leaving value unchanged")                    

    @property
    def dt(self):
        return self.__dt

    @dt.setter
    def dt(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__dt = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.dt")

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        if isinstance(value, int) is True:
            self.__index = value
        else:
            logging.log(logging.DEBUG, "Tried to load a non-integer value into self.index")                


    def by_arp(self, **kwargs):      
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value                
                if key == "mac":
                    self.mac = value
                if key == "lastseen":
                    self.last_seen = value                    
        # Query local arp table
        self.output = subprocess.Popen("arp -a", shell=True, stdout=subprocess.PIPE).communicate()
        self.last_arp = self.dt
        # Search result for mac id
        self.index = str(self.output).find(self.mac)
        # If not found, try again replacing : in address with -
        if self.index <= 0:
            self.mac = self.mac.replace(":", "-")
            self.index = str(self.output).find(self.mac)
        # Determine if device was seen recently enough to be considered "home"
        if self.dt <= self.last_seen + datetime.timedelta(minutes=30):
            self.yes = True
        else:
            self.yes = False
            print("arp failed")
        # Return result
        return self.yes


    def by_ping(self, **kwargs):        
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value                
                if key == "ip":
                    self.ip = value
                if key == "lastseen":
                    self.last_seen = value 
        # Perform ping using OS-specific option flags
        self.ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
        self.result = os.system("ping " + self.ping_str + " " + self.ip)  
        self.last_ping = self.dt 
        # Determine if user is home based on ping
        if self.result == 0:
            self.yes = True
        else: 
            self.yes = False  
            print("ping failed")
        # Return result
        return self.yes


    def by_arp_and_ping(self, **kwargs):                 
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value  
                if key == "mac":
                    self.mac = value                                  
                if key == "ip":
                    self.ip = value
        # Evaluate home/away based on arp tables and ping's if necessary
        if self.yes is True and self.dt.time().hour >= 20:
            self.yes is True
        else:
            if self.dt > self.last_arp + datetime.timedelta(seconds=15):
                self.yes = self.by_arp(datetime=self.dt, mac=self.mac)
                if self.yes is False:
                    if self.dt > self.last_ping + datetime.timedelta(seconds=30):
                        self.yes = self.by_ping(datetime=self.dt, ip=self.ip)
        # Return result
        return self.yes


    def by_ping_with_delay(self, **kwargs):         
        self.eveningCutoff = datetime.time(18,0)
        self.morningCutoff = datetime.time(8,0)       
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value                                    
                if key == "ip":
                    self.ip = value
        # Ping device every 30 seconds - If device found, set home status true
        if self.dt >= self.last_ping + datetime.timedelta(seconds=30):
            self.pingResponse = self.by_ping()
            if self.pingResponse is True:
                self.yes = True
                self.last_seen = self.dt
        # Rule-set to follow during the daytime hours
        if self.morningCutoff <= self.dt.time() <= self.eveningCutoff:
            if self.pingResponse is True:
                # If a ping hasn't been received in an hour, assume the user just got home after being gone
                if self.dt > self.last_seen + datetime.timedelta(minutes=60):
                    self.home_time = self.dt
                # Regardless, a positive ping indicates the user is home
                self.yes = True
                self.last_seen = self.dt
            else:
                # Wait 30 minutes with no positive pings before declaring the user "away"
                if self.dt < self.last_seen + datetime.timedelta(minutes=30):
                    self.yes = True
                else:
                    self.yes = False
        # Rule-set to follow after dark and overnight
        if self.dt.time() > self.eveningCutoff or self.dt.time() < self.morningCutoff:
            if self.pingResponse is True:
                # If a ping hasn't been received in an hour, assume the user just got home after being gone
                if self.dt > self.last_seen + datetime.timedelta(minutes=60):
                    self.home_time = self.dt   
                # Regardless, a positive ping indicates the user is home                                 
                self.yes = True
                self.last_seen = self.dt
            else:
                # Will not declare a user as "away" if transition occurs after 6pm
                pass
        # Return result                
        return self.yes                
             