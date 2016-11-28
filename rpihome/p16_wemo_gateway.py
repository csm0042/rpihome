#!/usr/bin/python3
""" p16_wemo_gateway.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
import multiprocessing
import os
import sys
import time
import modules.wemo as wemo
import modules.message as message


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Set up local logging *********************************************************************
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
class WemoProcess(multiprocessing.Process):
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
                logger.debug("Processing message [%s] from incoming message queue",
                                  self.msg_in.raw)
                if self.msg_in.dest == "16":
                    if self.msg_in.type == "001":
                        self.last_hb = datetime.datetime.now()
                    elif self.msg_in.type == "999":
                        logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Moving message [%s] over to internal work queue",
                                          self.msg_in.raw)
                else:
                    self.msg_out_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Redirecting message [%s] back to main", self.msg_in.raw)
                self.msg_in = message.Message()
            else:
                self.msg_in = message.Message()
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
            logger.debug("Processing message [%s] from internal work queue",
                              self.msg_to_process.raw)

            # Discover Device
            if self.msg_to_process.type == "160":
                logger.debug("Message type 160 - attempting to discover device: %s", self.msg_to_process.payload)
                self.device = self.wemo.discover_device(self.msg_to_process.raw)
                if self.device is not None:
                    self.msg_to_send = Message(source="16", dest="11", type="163", name=self.device.name, payload="found")
                    self.msg_out_queue.put_notwait(self.msg_to_send.raw)
                    logger.debug("Sending discovery successful message: [%s]", self.msg_to_send.raw)

            # Set Wemo state
            if self.msg_to_process.type == "161":
                # Process wemo off commands
                if self.msg_to_process.payload == "off":
                    logger.debug("Sending \"off\" command to device: %s", self.msg_to_process.name)
                    self.wemo.switch_off(self.msg_to_process.raw)
                # Process wemo on command
                if self.msg_to_process.payload == "on":
                    logger.debug("Sending \"on\" command to device: %s", self.msg_to_process.name)
                    self.wemo.switch_on(self.msg_to_process.raw)

            # Get Wemo state
            if self.msg_to_process.type == "162":
                logger.debug("Sending \"request state\" command to device: %s", self.msg_to_process.name)
                self.wemo.query_status(self.msg_to_process.raw, self.msg_out_queue)

            # Clear msg-to-process string
            self.msg_to_process = message.Message()
        else:
            self.msg_to_process = message.Message()


    def run(self):
        """ Actual process loop.  Runs whenever start() method is called """
        # Create wemo helper object
        self.wemo = wemo.WemoHelper(logger=logger)
        # Pause briefly
        time.sleep(4)
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
        pass
