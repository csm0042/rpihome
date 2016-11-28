#!/usr/bin/python3
""" p13_home_away.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
import multiprocessing
import platform
import os, sys
import time
import modules.message as message
import home.home_user1 as home_user1
import home.home_user2 as home_user2
import home.home_user3 as home_user3


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Set up local logging ****************************************************************************
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
logfile = os.path.join(os.path.dirname(sys.argv[0]), ("logs/" + __name__ + ".log"))
handler = logging.handlers.TimedRotatingFileHandler(logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
formatter = logging.Formatter('%(processName)-16s,  %(asctime)-24s,  %(levelname)-8s, %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug("Logging handler for %s started", __name__)


# Process Class ***********************************************************************************
class HomeProcess(multiprocessing.Process):
    """ WEMO gateway process class and methods """
    def __init__(self, **kwargs):
        # Set default input parameter values
        self.name = "undefined"
        self.msg_in_queue = multiprocessing.Queue(-1)
        self.msg_out_queue = multiprocessing.Queue(-1)    
        # Update default elements based on any parameters passed in
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "msgin":
                    self.msg_in_queue = value
                if key == "msgout":
                    self.msg_out_queue = value
        # Initialize parent class 
        multiprocessing.Process.__init__(self, name=self.name)
        # Create remaining class elements
        self.work_queue = multiprocessing.Queue(-1)
        self.msg_in = message.Message()
        self.msg_to_process = message.Message()
        self.msg_to_send = message.Message()
        self.user1 = home_user1.HomeUser1(self.msg_out_queue)
        self.user2 = home_user2.HomeUser2(self.msg_out_queue)
        self.user3 = home_user3.HomeUser3(self.msg_out_queue)
        self.last_hb = datetime.datetime.now()
        self.in_msg_loop = bool()
        self.main_loop = bool()
        self.close_pending = False


    def process_in_msg_queue(self):
        """ Method to cycle through incoming message queue, filtering out heartbeats and
        mis-directed messages.  Messages corrected destined for this process are loaded
        into the work queue """
        self.in_msg_loop = True
        while self.in_msg_loop is True:
            try:
                self.msg_in = message.Message(raw=self.msg_in_queue.get_nowait())
            except:
                self.in_msg_loop = False
            if len(self.msg_in.raw) > 4:
                logger.debug("Processing message [%s] from incoming message queue" % self.msg_in.raw)                
                if self.msg_in.dest == "13":
                    if self.msg_in.type == "001":
                        self.last_hb = datetime.datetime.now()
                    elif self.msg_in.type == "999":
                        logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Moving message [%s] over to internal work queue", self.msg_in.raw)                        
                else:
                    self.msg_out_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Redirecting message [%s] back to main" % self.msg_in.raw)
                # Resetting message for next check of queue                
                self.msg_in = message.Message()
            else:
                self.in_msg_loop = False


    def process_work_queue(self):
        """ Method to perform work from the work queue """
        # Get next message from internal queue or timeout trying to do so
        try:
            self.msg_to_process = message.Message(raw=self.work_queue.get_nowait())
        except:
            pass
        # If there is a message to process, do so
        if len(self.msg_to_process.raw) > 4:
            logger.debug("Processing message [%s] from internal work queue" % self.msg_to_process.raw)
            # 130 = Set Home-Away mode set to away (override)
            if self.msg_to_process.type == "130":
                # Mode 0 == away override
                if self.msg_to_process.payload == "0":
                    if self.msg_to_process.name == "user1":
                        self.user1.mode = 0
                    if self.msg_to_process.name == "user2":
                        self.user2.mode = 0
                    if self.msg_to_process.name == "user3":
                        self.user3.mode = 0
                # Mode 1 == home override
                if self.msg_to_process.payload == "1":
                    if self.msg_to_process.name == "user1":
                        self.user1.mode = 1
                    if self.msg_to_process.name == "user2":
                        self.user2.mode = 1
                    if self.msg_to_process.name == "user3":
                        self.user3.mode = 1
                # Mode 2 == auto by schedule
                if self.msg_to_process.payload == "2":
                    if self.msg_to_process.name == "user1":
                        self.user1.mode = 2
                    if self.msg_to_process.name == "user2":
                        self.user2.mode = 2
                    if self.msg_to_process.name == "user3":
                        self.user3.mode = 2   
                # Mode 3 == auto by arp & ping
                if self.msg_to_process.payload == "3":
                    if self.msg_to_process.name == "user1":
                        self.user1.mode = 3
                    if self.msg_to_process.name == "user2":
                        self.user2.mode = 3
                    if self.msg_to_process.name == "user3":
                        self.user3.mode = 3
                # Mode 4 == auto by ping with delay
                if self.msg_to_process.payload == "4":
                    if self.msg_to_process.name == "user1":
                        self.user1.mode = 4
                    if self.msg_to_process.name == "user2":
                        self.user2.mode = 4
                    if self.msg_to_process.name == "user3":
                        self.user3.mode = 4
                # Mode 5 == auto by schedule with ping
                if self.msg_to_process.payload == "5":
                    if self.msg_to_process.name == "user1":
                        self.user1.mode = 5
                    if self.msg_to_process.name == "user2":
                        self.user2.mode = 5
                    if self.msg_to_process.name == "user3":
                        self.user3.mode = 5
            # Clear msg-to-process string
            self.msg_to_process = message.Message()
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
        pass