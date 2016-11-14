#!/usr/bin/python3
""" p16_wemo_gateway.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import pywemo
import time
from rpihome.modules.wemo import WemoHelper


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"



class WemoProcessHelper(object):
    def __init__(self, msg_in_queue, msg_out_queue, logger):
        self.msg_in_queue = msg_in_queue
        self.msg_out_queue = msg_out_queue
        self.logger = logger
        self.msg_in = str()
        self.msg_to_process = str()
        self.work_queue = multiprocessing.Queue(-1)
        self.wemo = WemoHelper(self.logger)
        self.last_hb = datetime.datetime.now()
        self.run1 = bool()
        self.run2 = bool()
        self.close_pending = False
        
    def process_in_msg_queue(self):
        self.run1 = True
        while self.run1 is True:
            try:
                self.msg_in = self.msg_in_queue.get_nowait()
            except:
                self.run1 = False
            if len(self.msg_in) != 0:
                if self.msg_in[3:5] == "16":
                    if self.msg_in[6:9] == "001":
                        self.last_hb = datetime.datetime.now()
                        self.logger.log(logging.DEBUG, "heartbeat received")
                    else:
                        self.work_queue.put_nowait(self.msg_in)
                    self.msg_in = str()
                else:
                    self.msg_out_queue.put_nowait(self.msg_in)
                self.msg_in = str()
            else:
                self.run1 = False

    def process_work_queue(self):
        # Get next message from internal queue or timeout trying to do so
        try:
            self.msg_to_process = self.work_queue.get_nowait()
        except:
            self.run2 = False
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
                #time.sleep(5)
            # Process "kill process" message
            if self.msg_to_process[6:9] == "999":
                self.logger.log(logging.DEBUG, "Kill code received - Shutting down: %s"
                                % self.msg_to_process)
                self.close_pending = True
            # Clear msg-to-process string
            self.msg_to_process = str()
        else:
            self.run2 = False



# Wemo Gateway Process loop ***********************************************************************
def wemo_func(msg_in_queue, msg_out_queue, log_queue, log_configurer):
    log_configurer(log_queue)
    logger = logging.getLogger("main")
    logger.log(logging.DEBUG, "Logging handler for p16_wemo_gateway process started")

    process_helper = WemoProcessHelper(msg_in_queue, msg_out_queue, logger)

    while True:
        # Process incoming messages
        process_helper.process_in_msg_queue()

        # Process tasks in internal work queue
        process_helper.process_work_queue()

        # Close process
        if ((process_helper.close_pending is True and msg_in_queue.empty() is True) or
                datetime.datetime.now() > process_helper.last_hb + datetime.timedelta(seconds=30)):
            break

        # Pause before next process run
        time.sleep(0.097)



if __name__ == "__main__":
    print("Called as main")
