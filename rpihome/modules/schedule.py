#!/usr/bin/python3
""" schedule.py:
"""


# Import Required Libraries (Standard, Third Party, Local) ****************************************
from __future__ import print_function
import copy
import datetime
import logging
import httplib2
import re
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Class Definitions *******************************************************************************
class Condition(object):
    """ A class consisting of a conditoin to be checked and the desired state to pass """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.__andor = str()
        self.__condition = str()
        self.__state = str()
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "andor":
                    self.andor = value                
                if key == "condition":
                    self.condition = value
                if key == "state":
                    self.state = value

    @property
    def andor(self):
        """ Returns the condition type to be checked """
        return self.__andor

    @andor.setter
    def andor(self, value):
        """ Sets the condition type to be checked """
        if isinstance(value, str):
            if value.lower() == "and" or value.lower() == "or":
                self.__andor = value.lower()

    @property
    def condition(self):
        """ Returns the condition to be checked """
        return self.__condition

    @condition.setter
    def condition(self, value):
        """ Sets the condition to be checked """
        if isinstance(value, str):
            self.__condition = value.lower()

    @property
    def state(self):
        """ Returns the desired state to be checked against """
        return self.__state

    @state.setter
    def state(self, value):
        """ Sets the desired state to be checked against """
        if isinstance(value, str):
            if value.lower() == "true" or value.lower() == "false":
                self.__state = value.lower()



class OnRange(object):
    """ Single on/off range with aux conditions """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.__on_time = datetime.time()
        self.__off_time = datetime.time()
        self.__condition = [Condition()]
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "on_time":
                    self.on_time = value
                if key == "off_time":
                    self.off_time = value
                if key == "condition":
                    self.condition = value

    @property
    def on_time(self):
        """ Returns on time for a single on/off value pair """
        return self.__on_time

    @on_time.setter
    def on_time(self, value):
        """ Sets on time for a single on/off value pair """
        if isinstance(value, datetime.time):
            self.__on_time = value
        elif isinstance(value, datetime.datetime):
            self.__on_time = value.time()

    @property
    def off_time(self):
        """ Returns off time for a single on/off value pair' """
        return self.__off_time

    @off_time.setter
    def off_time(self, value):
        """ Sets off time for a single on/off value pair """
        if isinstance(value, datetime.time):
            self.__off_time = value
        elif isinstance(value, datetime.datetime):
            self.__off_time = value.time()      

    @property
    def condition(self):
        """ Returns the condition array for a single on/off value pair """
        return self.__condition

    @condition.setter
    def condition(self, value):
        """ Sets the condition array for a single on/off value pair """
        if isinstance(value, list):
            self.__condition = value[:]
        elif isinstance(value, Condition):
            self.__condition = [value]

    def add_condition(self, andor=None, condition=None, state=None):
        """ Adds a condition to the list of conditions associated with a given on/off time pair """
        self.__condition.append(Condition(andor=andor, condition=condition, state=state))

    def clear_all_conditions(self):
        """ Clears condition list for a given on/off time pair """
        self.__condition.clear()

    def remove_condition(self, index):
        """ Removes a specific condition from the condition list based on its position in the list (index) """
        try:
            self.__condition.pop(index)
        except:
            pass


class Day(object):
    """ Single day schedule """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.date = datetime.datetime.now().date()
        self.__on_range = [OnRange()]
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "date":
                    self.date = value
                if key == "on_range":
                    self.on_range = value

    @property
    def date(self):
        """ Returns entire week's schedule' """
        return self.__date

    @date.setter
    def date(self, value):
        """ Sets entire week's schedule' """
        if isinstance(value, datetime.date):
            self.__date = value
        elif isinstance(value, datetime.datetime):
            self.__date = value.date()

    @property
    def on_range(self):
        """ Returns entire week's schedule' """
        return self.__on_range

    @on_range.setter
    def on_range(self, value):
        """ Sets entire week's schedule' """
        if isinstance(value, list):
            self.__on_range = value[:]
        elif isinstance(value, OnRange):
            self.__on_range = [value]

    def add_range(self, on_time, off_time, condition):
        """ Adds a condition to the list of conditions associated with a given on/off time pair """
        self.__on_range.append(OnRange(on_time=on_time, off_time=off_time, condition=condition))

    def clear_all_ranges(self):
        """ Clears condition list for a given on/off time pair """
        self.__on_range.clear()

    def remove_range(self, index):
        """ Removes a specific condition from the condition list based on its position in the list (index) """
        try:
            self.__on_range.pop(index)
        except:
            pass       


class Week(object):
    """ Weekly schedule with on/off times and extra conditions for a single device """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.__day = [Day() for i in range(7)]
         # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "day":
                    self.day = value
                if key == "monday":
                    self.monday = value
                if key == "tuesday":
                    self.tuesday = value
                if key == "wednesday":
                    self.wednesday = value
                if key == "thursday":
                    self.thursday = value
                if key == "friday":
                    self.friday = value
                if key == "saturday":
                    self.saturday = value
                if key == "sunday":
                    self.sunday = value

    @property
    def day(self):
        """ Returns entire week's schedule' """
        return self.__day

    @day.setter
    def day(self, value):
        """ Sets entire week's schedule' """
        if isinstance(value, list):
            self.__day = value[:]

    @property
    def monday(self):
        """ Returns the day's schedule for Monday """
        return self.__day[0]

    @monday.setter
    def monday(self, value):
        """ Set's the schedule for Monday """
        if isinstance(value, Day):
            self.__day[0] = value

    @property
    def tuesday(self):
        """ Returns the day's schedule for Tuesday """
        return self.__day[1]

    @tuesday.setter
    def tuesday(self, value):
        """ Set's the schedule for Tuesday """
        if isinstance(value, Day):
            self.__day[1] = value

    @property
    def wednesday(self):
        """ Returns the day's schedule for Wednesday """
        return self.__day[2]

    @wednesday.setter
    def wednesday(self, value):
        """ Set's the schedule for Wednesday """
        if isinstance(value, Day):
            self.__day[2] = value

    @property
    def thursday(self):
        """ Returns the day's schedule for Thursday """
        return self.__day[3]

    @thursday.setter
    def thursday(self, value):
        """ Set's the schedule for thursday """
        if isinstance(value, Day):
            self.__day[3] = value

    @property
    def friday(self):
        """ Returns the day's schedule for Friday """
        return self.__day[4]

    @friday.setter
    def friday(self, value):
        """ Set's the schedule for Friday """
        if isinstance(value, Day):
            self.__day[4] = value

    @property
    def saturday(self):
        """ Returns the day's schedule for Satruday """
        return self.__day[5]

    @saturday.setter
    def saturday(self, value):
        """ Set's the schedule for Saturday """
        if isinstance(value, Day):
            self.__day[5] = value

    @property
    def sunday(self):
        """ Returns the day's schedule for Sunday """
        return self.__day[6]

    @sunday.setter
    def sunday(self, value):
        """ Set's the schedule for Sunday """
        if isinstance(value, Day):
            self.__day[6] = value      
