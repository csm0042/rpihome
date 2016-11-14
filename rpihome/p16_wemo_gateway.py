#!/usr/bin/python3
""" p16_wemo_gateway.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
import multiprocessing
import os
import time
from rpihome.modules.wemo import WemoHelper


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
class WemoProcess(multiprocessing.Process):
    """ WEMO gateway process class and methods """
    def __init__(self, name, msg_in_queue, msg_out_queue, log_queue, log_configurer):
        multiprocessing.Process.__init__(self, name=name)
        self.configure_logger(name, log_queue, log_configurer)
        self.handlers = []
        self.msg_in_queue = msg_in_queue
        self.msg_out_queue = msg_out_queue
        self.work_queue = multiprocessing.Queue(-1)
        self.msg_in = str()
        self.msg_to_process = str()
        self.wemo = WemoHelper(self.logger)
        self.last_hb = datetime.datetime.now()
        self.in_msg_loop = bool()
        self.main_loop = bool()
        self.close_pending = False


    def configure_logger(self, name, log_queue, log_configurer):
        """ Method to configure multiprocess logging """
        log_configurer(log_queue)
        self.logger = logging.getLogger(name)
        self.logger.debug("Logging handler for %s process started" % name)


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
                if self.msg_in[3:5] == "16":
                    if self.msg_in[6:9] == "001":
                        self.last_hb = datetime.datetime.now()
                        self.logger.debug("heartbeat received")
                    elif self.msg_in[6:9] == "999":
                        self.logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in)
                    self.msg_in = str()
                else:
                    self.msg_out_queue.put_nowait(self.msg_in)
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
            # Process wemo off commands
            if self.msg_to_process[6:9] == "160":
                self.wemo.switch_off(self.msg_to_process)
            # Process wemo on command
            if self.msg_to_process[6:9] == "161":
                self.wemo.switch_on(self.msg_to_process)
            # Process wemo state-request message
            if self.msg_to_process[6:9] == "162":
                self.wemo.query_status(self.msg_to_process, self.msg_out_queue)
            # Process "find device" message
            if self.msg_to_process[6:9] == "169":
                self.wemo.discover_device(self.msg_to_process)
            # Clear msg-to-process string
            self.msg_to_process = str()
        else:
            pass

    def run(self):
        """ Actual process loop.  Runs whenever start() method is called """
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
