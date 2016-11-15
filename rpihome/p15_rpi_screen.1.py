#!/usr/bin/python3
""" p15_rpi_screen.py: Wake / sleep control for the RPI Home main control screen.  
     
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import logging
import multiprocessing
import platform
import subprocess
import time


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"



# Main gui process loop **********************************************************************************************
def screen_func(msg_in_queue, msg_out_queue, log_queue, log_configurer):
    log_configurer(log_queue)
    name = multiprocessing.current_process().name
    logger = logging.getLogger("main")
    logger.log(logging.DEBUG, "Logging handler for p15_RPI_screen process started")

    msg_in = str()
    close_pending = False
    last_hb = time.time()

    while True:
        # Monitor message queue for new messages
        try:
            msg_in = msg_in_queue.get_nowait()  
        except:
            pass

        # Process incoming message
        if len(msg_in) != 0:
            if msg_in[3:5] == "15":
                
                if msg_in[6:9] == "001":
                    # Process heartbeat message
                    last_hb = time.time()
                if msg_in[6:9] == "150":
                    # Process screen command message
                    command = msg_in[10:]
                    if platform.system().lower() != "windows":
                        try:
                            output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
                            logging.log(logging.DEBUG, "Sending command [ %s ] to terminal" % str(command))
                        except:
                            logging.log(logging.DEBUG, "Command [ %s ] failed" % str(command))
                    else:
                        logging.log(logging.DEBUG, "Error sending command [ %s ] to terminal.  On windows machine, not RPI" % str(command))
                if msg_in[6:9] == "999":
                    # process kill message
                    logging.log(logging.DEBUG, "Kill code received - Shutting down: %s" % msg_in)
                    close_pending = True
            else:
                msg_out_queue.put_nowait(msg_in)
            pass
            msg_in = str()            

        # Only close down process once incoming message queue is empty
        if (close_pending is True and len(msg_in) == 0 and msg_in_queue.empty() is True) or (time.time() > (last_hb + 30)):
            break    

        # Pause before re-checking queue
        time.sleep(0.21)        