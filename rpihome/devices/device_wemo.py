#!/usr/bin/python3
""" device_wemo.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import logging
from .device import Device
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
        super().__init__(name, msg_out_queue, self.logger)
        self.name = name
        self.address = address
        self.msg_out_queue = msg_out_queue
        self.discover_device()

    def discover_device(self):
        self.logger.debug("Sending command to wemo gateway to find device at address: %s", self.address)
        self.msg_to_send = Message(source="11", dest="16", type="160", name=self.name, payload=self.address)
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)


    def command(self):
        """ This method is used to send a single command to various devices when necessary instead
        of sending the same command over and over again """
        if self.state != self.state_mem:
            if self.state is True:
                self.msg_to_send = Message(source="11", dest="16", type="161", name=self.name, payload="on")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug("Sending command to wemo gateway to turn ON device: %s", self.name)
            else:
                self.msg_to_send = Message(source="11", dest="16", type="161", name=self.name, payload="off")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug("Sending command to wemo gateway to turn OFF device: %s", self.name)
            pass
            # Snapshot new device state in memory so the command is only sent once
            self.state_mem = copy.copy(self.state)


    def replace_keywords(self, on_range):
        """ This method takes a specific OnRange structure and checks its on and off trigger times to see if they match certain keywords (eg: sunset).  If a keyword is found, the value is replaced with the actual time that should be associated with that keyword based on the time of year """
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
        """ This method checks all ancilary conditions in an array associated with each on/off time pair.  It keeps a count of each condition that passes.  Once all have been checked, it determines if they have all passed if the number of successful checks equals the size of the condtion array """
        self.check_int = 0
        self.logger.debug("Checking condition tree")
        # iterate through all conditions in array and check them against their desired states
        for k, m in enumerate(condition_array):
            if m.conditon.lower() == "user1":
                self.logger.debug("Condition #[%s] is [%s]", str(k), m.condition)
                if m.state.lower() == "true":
                    self.logger.debug("Desired state is [%s]", m.state)
                    if self.homeArray[0] is True:
                        self.logger.debug("Actual state is [%s] - check passes", str(self.homeArray[0]))                        
                        self.check_int += 1
                    else:
                        self.logger.debug("Actual state is [%s] - check failed", str(self.homeArray[0]))                        
                elif m.state.lower() == "false":
                    self.logger.debug("Desired state is [%s]", m.state)
                    if self.homeArray[0] is False:
                        self.logger.debug("Actual state is [%s] - check passes", str(self.homeArray[0]))                         
                        self.check_int += 1
                    else:
                        self.logger.debug("Actual state is [%s] - check failed", str(self.homeArray[0]))                        
            elif m.condition.lower() == "user2":
                if m.state.lower() == "true":
                    self.logger.debug("Desired state is [%s]", m.state)
                    if self.homeArray[2] is True:
                        self.logger.debug("Actual state is [%s] - check passes", str(self.homeArray[2]))                        
                        self.check_int += 1
                    else:
                        self.logger.debug("Actual state is [%s] - check failed", str(self.homeArray[2]))                        
                elif m.state.lower() == "false":
                    self.logger.debug("Desired state is [%s]", m.state)
                    if self.homeArray[2] is False:
                        self.logger.debug("Actual state is [%s] - check passes", str(self.homeArray[2]))
                        self.check_int += 1
                    else:
                        self.logger.debug("Actual state is [%s] - check failed", str(self.homeArray[2]))
            elif m.condition.lower() == "user3":                
                if m.state.lower() == "true":
                    self.logger.debug("Desired state is [%s]", m.state)
                    if self.homeArray[3] is True:
                        self.logger.debug("Actual state is [%s] - check passes", str(self.homeArray[3]))
                        self.check_int += 1
                    else:
                        self.logger.debug("Actual state is [%s] - check failed", str(self.homeArray[3]))
                elif m.state.lower() == "false":
                    self.logger.debug("Desired state is [%s]", m.state)
                    if self.homeArray[3] is False:
                        self.logger.debug("Actual state is [%s] - check passes", str(self.homeArray[3]))
                        self.check_int += 1
                    else:
                        self.logger.debug("Actual state is [%s] - check failed", str(self.homeArray[3]))                        
        # Once all conditions are checked, if the number of condition-state pairs that passed equal the number of conditions, then all passed.
        if self.check_int == len(condition_array):
            self.logger.debug("All checks passed")
            return True
        else:
            self.logger.debug("Not all checks passed")
            return False


    def check_custom_rules(self, **kwargs):
        """ This method contains the rule-set that controls external security lights """
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
        
        # Iterate through possible multipe on/off time pairs for today
        for i, j in enumerate(self.today.on_range):
            # Replace any keywords in the on and off times with their equivalent actual time values
            j = self.replace_keywords(j)
            # Verify all required substitutions have been made so comparison can be made
            if isinstance(j.on_time, datetime.time()) and isinstance(j.off_time, datetime.time()):
                # Check if current time falls between the on and off times
                if j.on_time <= self.dt.time() <= j.off_time:
                    # If the current time falls within the range, check extra condtion array
                    if self.check_conditions(j.condition) is True:
                        # If all extra conditions are true, enable device output
                        self.temp_state = True
            else:
                self.logger.error("Invalid keyword used in schedule input data")
        
        # Based on the evaluation of the rules, set the final output state
        if self.temp_state != self.state and self.temp_state is True:
            self.logger.info("Turning on device [fylt1]")
            self.state = True
        elif self.temp_state != self.state and self.temp_state is False:
            self.logger.info("Turning off device [fylt1]")
            self.state = False
        # Return result
        return self.state              
