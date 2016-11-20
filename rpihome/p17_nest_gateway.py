#!/usr/bin/python3
""" p17_nest_gateway.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import linecache
import logging
import multiprocessing
import os
import sys
import time

import nest


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Process Class ***********************************************************************************
class NestProcess(multiprocessing.Process):
    """ Nest gateway process class and methods """
    def __init__(self, **kwargs):
        # Set default input parameter values
        self.name = "undefined"
        self.msg_in_queue = multiprocessing.Queue(-1)
        self.msg_out_queue = multiprocessing.Queue(-1)
        self.logfile = "logfile"
        self.log_remote = False    
        # Update default elements based on any parameters passed in
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "msgin":
                    self.msg_in_queue = value
                if key == "msgout":
                    self.msg_out_queue = value
                if key == "logqueue":
                    self.log_queue = value
                if key == "logfile":
                    self.logfile = value
                if key == "logremote":
                    self.log_remote = value
        # Initialize parent class 
        multiprocessing.Process.__init__(self, name=self.name)
        # Create remaining class elements        
        self.username = str()
        self.password = str()
        self.work_queue = multiprocessing.Queue(-1)
        self.msg_in = str()
        self.msg_to_process = str()
        self.last_hb = datetime.datetime.now()
        self.in_msg_loop = bool()
        self.main_loop = bool()
        self.close_pending = False
        self.structure = []
        self.current_condition = str()
        self.current_temp = str()
        self.current_wind_dir = str()
        self.current_humid = str()
        self.result = str()        
        self.forecast = []
        self.forecast_condition = str()
        self.forecast_temp_low = str()
        self.forecast_temp_high = str()
        self.forecast_humid = str()


    def configure_local_logger(self):
        """ Method to configure local logging """
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False        
        self.handler = logging.handlers.TimedRotatingFileHandler(self.logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
        self.formatter = logging.Formatter('%(processName)-16s |  %(asctime)-24s |  %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.debug("Logging handler for %s process started", self.name)


    def kill_logger(self):
        """ Shut down logger when process exists """
        self.handlers = list(self.logger.handlers)
        for i in iter(self.handlers):
            self.logger.removeHandler(i)
            i.flush()
            i.close()


    def process_in_msg_queue(self):
        """ Method to cycle through incoming message queue, filtering out heartbeats and
        mis-directed messages.  Messages corrected destined for this process are loaded
        into the work queue """
        self.in_msg_loop = True
        while self.in_msg_loop is True:
            try:
                self.msg_in = self.msg_in_queue.get_nowait()
            except:
                self.in_msg_loop = False
            if len(self.msg_in) != 0:
                if self.msg_in[3:5] == "17":
                    if self.msg_in[6:9] == "001":
                        self.last_hb = datetime.datetime.now()
                    elif self.msg_in[6:9] == "999":
                        self.logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in)
                        self.logger.debug("Moving message [%s] over to internal work queue", self.msg_in)
                    self.msg_in = str()
                else:
                    self.msg_out_queue.put_nowait(self.msg_in)
                    self.logger.debug("Redirecting message [%s] back to main" % self.msg_in)
                self.msg_in = str()
            else:
                self.in_msg_loop = False

    def process_work_queue(self):
        """ Method to perform work from the work queue """
        # Get next message from internal queue or timeout trying to do so
        try:
            self.msg_to_process = self.work_queue.get_nowait()
        except:
            pass
        # If there is a message to process, do so
        if len(self.msg_to_process) != 0:
            self.logger.debug("Processing message [%s] from internal work queue" % self.msg_to_process)
            if self.msg_to_process[6:9] == "020":
                self.connect()
                self.response = "17,02,020," + self.current_conditions()
                self.msg_out_queue.put_nowait(self.response)
                self.logger.debug("Message [%s] received.  Sending response [%s]" % (self.msg_to_process, self.response))
            elif self.msg_to_process[6:9] == "021":
                self.connect()
                self.response = "17,02,021," + self.current_forecast()
                self.msg_out_queue.put_nowait(self.response)
                self.logger.debug("Message [%s] received.  Sending response [%s]" % (self.msg_to_process, self.response))                
            elif self.msg_to_process[6:9] == "022":
                self.connect()
                self.response = "17,02,022," + self.tomorrow_forecast()
                self.msg_out_queue.put_nowait(self.response)
                self.logger.debug("Message [%s] received.  Sending response [%s]" % (self.msg_to_process, self.response))                
            # Clear msg-to-process string
            self.msg_to_process = str()
        else:
            pass

    
    def connect(self):
        # Get credentials for login
        self.credentials_file = os.path.join(os.path.dirname(sys.argv[0]), "credentials/nest.txt")
        if os.path.isfile(self.credentials_file):
            self.logger.debug("Credential file found, reading attributes from file")
            self.username = linecache.getline(self.credentials_file, 1)
            self.password = linecache.getline(self.credentials_file, 2)
        else:
            self.logger.debug("Credential file NOT found, continuing with default values")
            self.username = "username"
            self.password = "password"
        # clean up extracted data
        self.username = str(self.username).lstrip()
        self.username = str(self.username).rstrip()
        self.password = str(self.password).lstrip()
        self.password = str(self.password).rstrip()
        # Login to Nest account
        self.logger.debug("Attempting to connect to NEST account")
        try:
            self.nest = nest.Nest(self.username, self.password)
            self.logger.debug("Connection successful")
        except:
            self.nest = None
            self.logger.debug("Could not connect to NEST account")


    def current_conditions(self):
        if self.nest is not None:
            self.logger.debug("Attempting to parse data on current conditons from NEST data")
            try:
                self.structure = self.nest.structures[0]
                self.current_temp = str(int((self.structure.weather.current.temperature * 1.8) + 32))
                self.current_condition = self.structure.weather.current.condition
                self.current_wind_dir = self.structure.weather.current.wind.direction
                self.current_humid = str(int(self.structure.weather.current.humidity))
                self.result = ("%s,%s,%s,%s" % (self.current_condition, self.current_temp, self.current_wind_dir, self.current_humid))
                self.logger.debug("Data successfully obtained.  Returning [%s] to main" % self.result)
                return self.result
            except:
                self.logger.debug("Failure reading tomorrow's forecast data from NEST device")
                return "??,??,??,??"
        else:
            self.logger.debug("Failure reading tomorrow's forecast data from NEST device")
            return "??,??,??,??" 


    def current_forecast(self):
        if self.nest is not None:
            self.logger.debug("Attempting to parse data on today's forecast from NEST data")
            try:
                self.structure = self.nest.structures[0]
                self.forecast = self.structure.weather.daily[0]
                self.forecast_condition = self.forecast.condition
                self.forecast_temp_low = str(int((self.forecast.temperature[0] * 1.8) + 32))
                self.forecast_temp_high = str(int((self.forecast.temperature[1] * 1.8) + 32))
                self.forecast_humid = str(int(self.forecast.humidity))
                self.result = ("%s,%s,%s,%s" % (self.forecast_condition, self.forecast_temp_low, self.forecast_temp_high, self.forecast_humid))
                self.logger.debug("Data successfully obtained.  Returning [%s] to main" % self.result)                
                return self.result
            except:
                self.logger.debug("Failure reading tomorrow's forecast data from NEST device")
                return "??,??,??,??"
        else:
            self.logger.debug("Failure reading tomorrow's forecast data from NEST device")
            return "??,??,??,??"             


    def tomorrow_forecast(self):
        if self.nest is not None:
            self.logger.debug("Attempting to parse data on tomorrow's forecast from NEST data")     
            try:
                self.structure = self.nest.structures[0]
                self.forecast = self.structure.weather.daily[1]
                self.forecast_condition = self.forecast.condition
                self.forecast_temp_low = str(int((self.forecast.temperature[0] * 1.8) + 32))
                self.forecast_temp_high = str(int((self.forecast.temperature[1] * 1.8) + 32))
                self.forecast_humid = str(int(self.forecast.humidity))
                self.result = ("%s,%s,%s,%s" % (self.forecast_condition, self.forecast_temp_low, self.forecast_temp_high, self.forecast_humid))
                self.logger.debug("Data successfully obtained.  Returning [%s] to main" % self.result)                       
                return self.result
            except:
                self.logger.debug("Failure reading tomorrow's forecast data from NEST device")
                return "??,??,??,??" 
        else:
            self.logger.debug("Failure reading tomorrow's forecast data from NEST device")
            return "??,??,??,??"             
        

    def run(self):
        """ Actual process loop.  Runs whenever start() method is called """
        # Configure logging
        self.configure_local_logger()
        # Get credentials for login
        self.connect()
        # Main process loop
        self.main_loop = True
        while self.main_loop is True:
            # Process incoming messages
            self.process_in_msg_queue()

            # Process tasks in internal work queue
            if self.close_pending is False:
                self.process_work_queue()

            # Close process
            if (self.close_pending is True or
                    datetime.datetime.now() > self.last_hb + datetime.timedelta(seconds=30)):
                self.main_loop = False

            # Pause before next process run
            time.sleep(0.097)

        # Shut down logger before exiting process
        self.kill_logger()
