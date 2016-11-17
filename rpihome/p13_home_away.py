#!/usr/bin/python3
""" p13_home_away.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import datetime
import logging
import multiprocessing
import platform
import time

from rpihome.rules.home_user1 import HomeUser1
from rpihome.rules.home_user2 import HomeUser2
from rpihome.rules.home_user3 import HomeUser3


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Process Class ***********************************************************************************
class HomeProcess(multiprocessing.Process):
    """ WEMO gateway process class and methods """
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
        self.work_queue = multiprocessing.Queue(-1)
        self.msg_in = str()
        self.msg_to_process = str()
        self.user1 = HomeUser1(self.msg_out_queue)
        self.user2 = HomeUser2(self.msg_out_queue)
        self.user3 = HomeUser3(self.msg_out_queue)
        self.last_hb = datetime.datetime.now()
        self.in_msg_loop = bool()
        self.main_loop = bool()
        self.close_pending = False


    def configure_remote_logger(self):
        """ Method to configure multiprocess logging """
        self.logger = logging.getLogger(self.name)        
        self.handler = logging.handlers.QueueHandler(self.log_queue)
        self.logger.addHandler(self.handler)
        self.logger.debug("Logging handler for %s process started", self.name)


    def configure_local_logger(self):
        """ Method to configure local logging """
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
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
                if self.msg_in[3:5] == "13":
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
            # 130 = Home-Away mode set to away (override)
            if self.msg_to_process[6:9] == "130":
                if self.msg_to_process[10:] == "user1":
                    self.user1.mode = 0
                if self.msg_to_process[10:] == "user2":
                    self.user2.mode = 0
                if self.msg_to_process[10:] == "user3":
                    self.user3.mode = 0
            # 131 = Home-Away mode set to home (override)
            if self.msg_to_process[6:9] == "131":
                if self.msg_to_process[10:] == "user1":
                    self.user1.mode = 1
                if self.msg_to_process[10:] == "user2":
                    self.user2.mode = 1
                if self.msg_to_process[10:] == "user3":
                    self.user3.mode = 1
            # 132 = Home-Away mode set to auto (by schedule)
            if self.msg_to_process[6:9] == "132":
                if self.msg_to_process[10:] == "user1":
                    self.user1.mode = 2
                if self.msg_to_process[10:] == "user2":
                    self.user2.mode = 2
                if self.msg_to_process[10:] == "user3":
                    self.user3.mode = 2
            # 133 = Home-Away mode set to auto (arp/ping based)
            if self.msg_to_process[6:9] == "133":
                if self.msg_to_process[10:] == "user1":
                    self.user1.mode = 3
                if self.msg_to_process[10:] == "user2":
                    self.user2.mode = 3
                if self.msg_to_process[10:] == "user3":
                    self.user3.mode = 3
            # 134 = Home-Away mode set to auto (by ping with delay)
            if self.msg_to_process[6:9] == "134":
                if self.msg_to_process[10:] == "user1":
                    self.user1.mode = 4
                if self.msg_to_process[10:] == "user2":
                    self.user2.mode = 4
                if self.msg_to_process[10:] == "user3":
                    self.user3.mode = 4
            # 135 = Home-Away mode set to auto (schedule w/ping)
            if self.msg_to_process[6:9] == "135":
                if self.msg_to_process[10:] == "user1":
                    self.user1.mode = 5
                if self.msg_to_process[10:] == "user2":
                    self.user2.mode = 5
                if self.msg_to_process[10:] == "user3":
                    self.user3.mode = 5
            # Clear msg-to-process string
            self.msg_to_process = str()
        else:
            pass


    def run_automation(self):
        """ Run automation rule determines if user is home or away """
        self.user1.by_mode(
            mode=5, datetime=datetime.datetime.now(), ip="192.168.86.40")
        self.user2.by_mode(
            mode=2, datetime=datetime.datetime.now(), ip="192.168.86.42")
        self.user3.by_mode(
            mode=2, datetime=datetime.datetime.now(), ip="192.168.86.42")


    def run_commands(self):
        """ Monitor home/away state and send commands to target device when COS occurs """
        self.user1.command()
        self.user2.command()
        self.user3.command()


    def run(self):
        """ Actual process loop.  Runs whenever start() method is called """
        # Configure logging
        if self.log_remote is True:
            self.configure_remote_logger()
        else:
            self.configure_local_logger()
        # Main process loop        
        self.main_loop = True
        while self.main_loop is True:
            # Process incoming messages
            self.process_in_msg_queue()

            # Process tasks in internal work queue
            if self.close_pending is False:
                self.process_work_queue()
                self.run_automation()
                self.run_commands()

            # Close process
            if (self.close_pending is True or
                    datetime.datetime.now() > self.last_hb + datetime.timedelta(seconds=30)):
                self.main_loop = False

            # Pause before next process run
            time.sleep(0.097)

        # Shut down logger before exiting process
        self.kill_logger()