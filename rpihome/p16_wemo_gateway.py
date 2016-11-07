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
from modules.wemo import WemoHelper


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Wemo Gateway Process loop *******************************************************************************************
def wemo_func(msg_in_queue, msg_out_queue, log_queue, log_configurer):
    log_configurer(log_queue)
    name = multiprocessing.current_process().name
    logger = logging.getLogger("main")
    logger.log(logging.DEBUG, "Logging handler for p16_wemo_gateway process started")

    msg_in = str()
    close_pending = False
    last_hb = time.time()
    wemo = WemoHelper()    


    # Main process loop
    while True:
        # Monitor message queue for new messages
        try:
            msg_in = msg_in_queue.get_nowait()  
        except:
            pass

        # Process incoming messages
        if len(msg_in) != 0:
            if msg_in[3:5] == "16":
                # Process heartbeat message
                if msg_in[6:9] == "001":
                    #logging.log(logging.DEBUG, "Heartbeat received: %s" % msg_in)
                    last_hb = time.time()
                
                # Process wemo off commands
                if msg_in[6:9] == "160":
                    wemo.switch_off(msg_in)
 
                # Process wemo on command                       
                if msg_in[6:9] == "161":
                    wemo.switch_on(msg_in)                    

                # Process wemo state-request message
                if msg_in[6:9] == "162":
                    wemo.query_status(msg_in, msg_out_queue)   

                # Process "find device" message
                if msg_in[6:9] == "169":
                    wemo.discover_device(msg_in)
  
                # Process "kill process" message
                if msg_in[6:9] == "999":
                    logging.log(logging.DEBUG, "Kill code received - Shutting down: %s" % msg_in)
                    close_pending = True
            # Send mis-routed messages back to main
            else:
                msg_out_queue.put_nowait(msg_in)
            pass
            # Clear incoming message string to ready routine for next message
            msg_in = str()

        # Only close down process once incoming message queue is empty
        if (close_pending is True and len(msg_in) == 0 and msg_in_queue.empty() is True) or (time.time() > (last_hb + 30)):
            break

        # Pause before re-checking queue
        time.sleep(0.097)


if __name__ == "__main__":
    print("Called as main")
