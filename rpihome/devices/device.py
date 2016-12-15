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
        self.result = 0
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

        # Pull today's data from schedule to evaluate
        self.today = self.schedule.day[self.dt.weekday()]
        self.logger.debug("Schedule: %s", self.today)

        # Check each on_range associated with this device and day in the schedule.  If any evaluate true, then the device should be turned on.  If none evaluate true, the device will remain off (or turn off if previously on)
        self.result = 0
        for index, on_range in enumerate(self.today.on_range):
            self.result = self.eval_on_range(self.dt, on_range, self.result)

        # Based on the evaluation of the rules, set the final output state
        if self.result == 0 and self.state is not False:
            self.logger.info("Turning off device [%s]", self.name)
            self.state = False
        elif self.result > 0 and self.state is not True:
            self.logger.info("Turning on device [%s]", self.name)
            self.state = True

        # Return result
        return self.state


    def eval_on_range(self, dt_current, on_range, result):
        """ This method evaluates a single on-range and its associated conditons and determines if it's true or not """
        if on_range.on_time <= on_range.off_time:
            # Device turns on and then back off in the same Day
            if dt_current.time() >= on_range.on_time and dt_current.time() < onrange.off_time:
                # If true, current time falls between defined on and off times
                if self.eval_conditions(on_range.condition) is true:
                    result += 1
        elif on_range.on_time > on_range.off_time:
            # This assignment represents an overnight assignment and must be evaluated differently
            if dt_current.time() >= on_range.on_time or dt_current.time() < on_range.off_time:
                # If true, current time falls between defined on and off times
                if self.eval_conditions(on_range.condition) is true:
                    result += 1
        # Return result (a non-zero result means the range and associated conditions passed)
        return result


    def eval_conditions(self, conditions):
        self.result = ()
        self.result_list = []
        # Create a list of individual condition results
        for i, cond in enumerate(conditions):
            if cond.condition.lower() == "user1":
                self.result_list.append(self.eval_user(cond, self.homeArray[0]))
            elif cond.condition.lower() == "user2":
                self.result_list.append(self.eval_user(cond, self.homeArray[2]))
            elif cond.condition.lower() == "user3":
                self.result_list.append(self.eval_user(cond, self.homeArray[3]))
        # Build combined if statement
        self.statement = str()
        for i, result in enumerate(self.result_list):
            if i == 0:
                self.statement = self.statement + str(result[1])
            else:
                self.statement = self.statement + " " + str(result[0] + " " + str(result[1]))
        print(self.statement)
        print(eval(self.statement))
        return eval(self.statement)
        


    def eval_user(self, cond, home_flag):
        self.result = None
        if cond.state.lower() == "true":
            if home_flag is True:
                self.result = (cond.andor, True)
            elif home_flag is False:
                self.result = (cond.andor, False)
        elif cond.state.lower() == "false":
            if home_flag is True:
                self.result = (cond.andor, False)
            elif home_flag is False:
                self.result = (cond.andor, True)
        # Return result
        return self.result
              
        


        
        
        
