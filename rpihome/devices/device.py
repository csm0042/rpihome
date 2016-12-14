#!/usr/bin/python3
""" device.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
from rpihome.modules.sun import Sun
from rpihome.modules.message import Message
from rpihome.modules.schedule import Day, Week, OnRange, Condition


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
        self.schedule = Week()


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
            self.__homeArray = value[:]
        else:
            self.logger.error("Improper type attmpted to load into self.homeArray \
                          (should be type: list)")
    
    @property
    def homeNew(self):
        return self.__homeNew

    @homeNew.setter
    def homeNew(self, value):
        if isinstance(value, bool) is True or value == None:
            self.__homeNew = value
        else:
            self.logger.error("Improper type attmpted to load into self.homeNew (should be type: bool or None)")                          

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
    def statusChangeTS(self):
        return self.__statusChangeTS

    @statusChangeTS.setter
    def statusChangeTS(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__statusChangeTS = value
        else:
            self.logger.error("Improper type attmpted to load into self.statusChangeTS (should be: datetime)")

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

    @property
    def schedule(self):
        return self.__schedule

    @schedule.setter
    def schedule(self, value):
        if isinstance(value, Week) is True:
            self.__schedule = value
        else:
            self.logger.error("Improper type attempted to load into self.schedule (should be type Week())")
     

    def check_rules(self, **kwargs):
        """ This method evaluates a custom rule-set provided by a schedule data class
        """
        self.home = False
        # Process on_range variables if present   
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value
                if key == "homeArray":
                    self.homeArray = value 
                if key == "homeTime":
                    self.homeTime = value                    
                if key == "home":
                    self.home = value 
                if key == "utcOffset":
                    self.utcOffset = value
                if key == "sunriseOffset":
                    self.sunriseOffset = value
                if key == "sunsetOffset":
                    self.sunsetOffset = value   
                if key == "timeout":
                    self.timeout = value
                if key == "schedule":
                    self.schedule = value
        # Calculate sunrise / sunset times
        self.sunrise = datetime.datetime.combine(self.dt.date(), self.s.sunrise(self.dt, self.utcOffset))
        self.sunset = datetime.datetime.combine(self.dt.date(), self.s.sunset(self.dt, self.utcOffset)) 
        # Decision tree to determine if screen should be awake or not
        self.temp_state = False
        self.today = self.schedule.day[self.dt.weekday()]
        self.logger.debug("Schedule: %s", self.today)
        
        # Iterate through possible multipe on/off time pairs for today
        for index, onRange in enumerate(self.today.on_range):
            self.logger.debug("Iterating through on-ranges: %s", onRange)
            # Replace any keywords in the on and off times with their equivalent actual time values
            onRange = self.replace_keywords(onRange)
            # Verify all required substitutions have been made so comparison can be made
            if isinstance(onRange.on_time, datetime.time) and isinstance(onRange.off_time, datetime.time):
                # Evaluate rule
                if onRange.on_time < onRange.off_time:
                    self.logger.debug("on-time for device is earlier in the day than the off time (not an overnight event)")
                    # Check if current time falls between the on and off times (daytime events)
                    if onRange.on_time <= self.dt.time() <= onRange.off_time:
                        self.logger.debug("Current time is within acceptable range for device to turn on.  Checking auxilary conditons")
                        # If the current time falls within the range, check extra condtion array
                        if self.check_conditions(onRange.condition) is True:
                            self.logger.debug("Auxilary conditions evaluate TRUE")
                            # If all extra conditions are true, enable device output
                            self.logger.debug("Device should be turned ON")
                            self.temp_state = True
                        else:
                            self.logger.debug("Auxilary conditions evaluate FALSE")
                else:
                    self.logger.debug("on-time for device is later in the day than the off time (overnight event)")
                    # Check if current time falls between the on and off times (overnight events)
                    if self.dt.time() < onRange.off_time or self.dt.time() >= onRange.on_time:
                        self.logger.debug("Current time is within acceptable range for device to turn on.  Checking auxilary conditons")
                        # If the current time falls within the range, check extra condtion array
                        if self.check_conditions(onRange.condition) is True:
                            self.logger.debug("Auxilary conditions evaluate TRUE")
                            # If all extra conditions are true, enable device output
                            self.logger.debug("Device should be turned ON")
                            self.temp_state = True
                        else:
                            self.logger.debug("Auxilary conditions evaluate FALSE")
            else:
                self.logger.error("Invalid keyword used in schedule input data")
        
        # Based on the evaluation of the rules, set the final output state
        if self.temp_state != self.state and self.temp_state is True:
            self.logger.info("Turning on device [%s]", self.name)
            self.state = True
        elif self.temp_state != self.state and self.temp_state is False:
            self.logger.info("Turning off device [%s]", self.name)
            self.state = False
        # Return result
        return self.state


    def replace_keywords(self, on_range):
        """ This method takes a specific OnRange structure and checks its on and off trigger times to see if they match certain keywords (eg: sunset).  If a keyword is found, the value is replaced with the actual time that should be associated with that keyword based on the time of year
        """
        self.logger.debug("Checking on and off times for keyword substitutions")
        if isinstance(on_range.on_time, str):
            self.logger.debug("Keyword detected in place of time in on-time")
            if on_range.on_time.lower() == "sunrise":
                self.logger.debug("Replacing [sunrise] keyword in on-time with today's sunrise time: ", str(self.sunrise.time()))
                on_range.on_time = self.sunrise.time()
            elif on_range.on_time.lower() == "sunset":
                self.logger.debug("Replacing [sunset] keyword in on-time with today's sunrise time: ", str(self.sunset.time()))
                on_range.on_time = self.sunset.time()
        if isinstance(on_range.off_time, str):
            self.logger.debug("Keyword detected in place of time in off-time")
            if on_range.off_time.lower() == "sunrise":
                self.logger.debug("Replacing [sunrise] keyword in off-time with today's sunrise time: ", str(self.sunrise.time()))
                on_range.off_time = self.sunrise.time()
            elif on_range.off_time.lower() == "sunset":
                self.logger.debug("Replacing [sunset] keyword in off-time with today's sunrise time: ", str(self.sunset.time()))
                on_range.off_time = self.sunset.time()
        return on_range          


    def check_conditions(self, condition_array):
        """ This method checks all ancilary conditions in an array associated with each on/off time pair
        """
        self.code_to_execute = str()
        self.logger.debug("Building if statement")
        # iterate through all conditions in array and create custom if statement
        for index, cond in enumerate(condition_array):
            if len(self.code_to_execute) == 0:
                self.code_to_execute.append("if ")
            else:
                self.code_to_execute.append(self.condition_sub(cond.andor))
                self.code_to_execute.append(" ")
            self.code_to_execute.append(self.condition_sub(cond.condition))
            self.code_to_execute.append(" ")
            self.code_to_execute.append(self.condition_sub(cond.state))
        self.code_to_execute.append(":")
        self.logger.debug("Built custom if statement: [%s]", self.code_to_execute)
        if exec(self.code_to_execute) is True:
            self.logger.debug("Statement evaluates TRUE")
            return True
        else:
            self.logger.debug("Statement evaluates FALSE")
            return False


    def condition_sub(self, keyword):
        """ This method is used to substitute tag variable names for keywords in the condition evaluation method
        """
        if keyword == "user1":
            return "self.homeArray[0]"
        elif keyword == "user2":
            return "self.homeArray[2]"
        elif keyword == "user3":
            return "self.homeArray[3]"
        elif keyword == "true":
            return "True"
        elif keyword == "false":
            return "False"
        elif keyword == "and":
            return "and"
        elif keyword == "or":
            return "or"                                                
