#!/usr/bin/python3
""" p01_log_handler.py: Logging process for the rpihome application suite
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import logging
import logging.handlers
import multiprocessing
import time


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Log Handler Process *************************************************************************************************
def listener_process(msg_in_queue, msg_out_queue, log_configurer, logfile):
    log_configurer(logfile)
    close_pending = False
    msg_in = None
    last_hb = time.time()

    # Main process loop    
    while True:
        # Check incoming process message queue and pull next message from the stack if present
        try:
            msg_in = msg_in_queue.get_nowait()  
        except:
            pass
        
        # Process incoming message when message is type "str"
        if isinstance(msg_in, str):
            # Check if data in string
            if len(msg_in) != 0:
                # Check if message is destined for this process based on pseudo-process-id
                if msg_in[3:5] == "01":
                    # If message is a heartbeat, update heartbeat snapshot
                    if msg_in[6:9] == "001":
                        last_hb = time.time()
                    # If message is a kill-code, set the close_pending flag so the process can close out gracefully 
                    elif msg_in[6:9] == "999":
                        logging.log(logging.DEBUG, "Kill code received - Shutting down %s" % msg_in)
                        close_pending = True
                else:
                    # If message isn't destined for this process, drop it into the queue for the main process so it can re-forward it to the proper recipient.
                    msg_out_queue.put_nowait(msg_in)
                    self.logger.debug("Redirecting message [%s] back to main", msg_in)                     
                pass
                msg_in = None
        
        # Process incoming message when message is type "LogRecord"
        if isinstance(msg_in, logging.LogRecord):
            # Get log handler, then pass it the log message from the queue
            logger = logging.getLogger(msg_in.name)
            logger.handle(msg_in)
            msg_in = None

        # Only close down process once incoming message queue is empty
        if (close_pending is True and msg_in == None and msg_in_queue.empty() is True) or (time.time() > (last_hb + 30)):
            break
        
        # Delay before re-running loop
        time.sleep(0.013)








