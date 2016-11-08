#!/usr/bin/python3
""" home_user2.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time
from rpihome.rules import home_general


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
class HomeUser2(home_general.HomeGeneral):
    def __init__(self, msg_out_queue):
        super().__init__()
        self.msg_out_queue = msg_out_queue


    def by_schedule(self, **kwargs):
    # Update value stored in dt_now to current datetime
        self.dt = datetime.datetime.now()
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value
                if key == "lastseen":
                    self.ishome.last_seen = value
        # Monday
        if self.dt.weekday() == 0:
            if 2016 <= self.dt.date().isocalendar()[0] <= 2017:
                # If even number week (non-custody week)
                if self.dt.date().isocalendar()[1] % 2 == 0:
                    if self.dt.time() < datetime.time(7,0):
                        self.yes = True
                    else:
                        self.yes = False
                else:
                    self.yes = False
            else:
                self.yes = False
        # Tuesday
        elif self.dt.weekday() == 1:
            self.yes = False            
        # Wednesday
        elif self.dt.weekday() == 2:
            if self.dt.time() >= datetime.time(17,0):
                self.yes = True
            else:
                self.yes = False            
        # Thursday
        elif self.dt.weekday() == 3:
            if self.dt.time() < datetime.time(7,0) or self.dt.time() >= datetime.time(17,0):
                self.yes = True
            else:
                self.yes = False            
        # Friday
        elif self.dt.weekday() == 4:
            if 2016 <= self.dt.date().isocalendar()[0] <= 2017:
                # If odd number week (custody week)
                if self.dt.date().isocalendar()[1] % 2 == 1:
                    # Home before 7am or after 5pm
                    if self.dt.time() < datetime.time(7,0) or self.dt.time() >= datetime.time(17,0):
                        self.yes = True
                    else:
                        self.yes = False                    
                else:
                    # Home only before 7am
                    if self.dt.time() < datetime.time(7,0):
                        self.yes = True
                    else:
                        self.yes = False
            else:
                self.yes = False          
        # Saturday
        elif self.dt.weekday() == 5:
            if 2016 <= self.dt.date().isocalendar()[0] <= 2017:
                # If odd number week (custody week)
                if self.dt.date().isocalendar()[1] % 2 == 1:
                    self.yes = True 
                else:
                    self.yes = False          
        # Sunday
        elif self.dt.weekday() == 6:
            if 2016 <= self.dt.date().isocalendar()[0] <= 2017:
                # If odd number week (custody week)
                if self.dt.date().isocalendar()[1] % 2 == 1:
                    self.yes = True 
                else:
                    self.yes = False           
        # Invalid day
        else:
            self.yes = False
        # Return result
        return self.yes        


    def command(self):
        if self.yes != self.mem:
            if self.yes is True:
                self.msg_out_queue.put_nowait("13,11,101,user2")
                logging.log(logging.DEBUG, "Sending 'user2 home' message to logic solver")                
            else:
                self.msg_out_queue.put_nowait("13,11,100,user2")
                logging.log(logging.DEBUG, "Sending 'user2 NOT home' message to logic solver")                 
            self.mem = copy.copy(self.yes)                           