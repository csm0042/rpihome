#!/usr/bin/python3
""" p13_home_away.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import datetime
import httplib2
import logging
import multiprocessing
import platform
import time

from rules import home_user1
from rules import home_user2
from rules import home_user3


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Home / Away Process loop **********************************************************************************************
def home_func(msg_in_queue, msg_out_queue, log_queue, log_configurer):
    log_configurer(log_queue)
    name = multiprocessing.current_process().name
    logger = logging.getLogger("main")
    logger.log(logging.DEBUG, "Logging handler for p13_home_away process started")

    msg_in = str()
    close_pending = False
    last_hb = time.time()

    user1 = home_user1.HomeUser1(msg_out_queue)
    user2 = home_user2.HomeUser2(msg_out_queue)
    user3 = home_user3.HomeUser3(msg_out_queue)


    while True:
        # Monitor message queue for new messages
        try:
            msg_in = msg_in_queue.get_nowait()  
        except:
            pass

        # Process incoming message
        if len(msg_in) != 0:
            # 13 = This process ID
            if msg_in[3:5] == "13":
                # 001 = Heartbeat message from main
                if msg_in[6:9] == "001":
                    #logging.log(logging.DEBUG, "Heartbeat received: %s" % msg_in)
                    last_hb = time.time()
                # 130 = Home-Away mode set to away (override)
                if msg_in[6:9] == "130":
                    logging.log(logging.DEBUG, "Setting home/away mode for %s to \"away\"" % msg_in[10:])
                    if msg_in[10:] == "user1":
                        user1.mode = 0
                    if msg_in[10:] == "user2":
                        user2.mode = 0
                    if msg_in[10:] == "user3":
                        user3.mode = 0                       
                # 131 = Home-Away mode set to home (override)
                if msg_in[6:9] == "131":
                    logging.log(logging.DEBUG, "Setting home/away mode for %s to \"home\"" % msg_in[10:])
                    if msg_in[10:] == "user1":
                        user1.mode = 1
                    if msg_in[10:] == "user2":
                        user2.mode = 1
                    if msg_in[10:] == "user3":
                        user3.mode = 1                
                # 132 = Home-Away mode set to auto (by schedule)
                if msg_in[6:9] == "132":
                    logging.log(logging.DEBUG, "Setting home/away mode for %s to auto (by schedule)" % msg_in[10:])
                    if msg_in[10:] == "user1":
                        user1.mode = 2
                    if msg_in[10:] == "user2":
                        user2.mode = 2
                    if msg_in[10:] == "user3":
                        user3.mode = 2 
                # 133 = Home-Away mode set to auto (arp/ping-based)
                if msg_in[6:9] == "133":
                    logging.log(logging.DEBUG, "Setting home/away mode for %s to auto (by arp/ping)" % msg_in[10:])
                    if msg_in[10:] == "user1":
                        user1.mode = 3
                    if msg_in[10:] == "user2":
                        user2.mode = 3
                    if msg_in[10:] == "user3":
                        user3.mode = 3                                  
                # 999 = Shutdown command from main
                if msg_in[6:9] == "999":
                    logging.log(logging.DEBUG, "Kill code received - Shutting down: %s" % msg_in)
                    close_pending = True
            else:
                # Re-route message back to main
                msg_out_queue.put_nowait(msg_in)
            pass
            # Clear message string to prevent processing it multiple times
            msg_in = str()            
                                

        # Determine if user is home
        user1.by_mode(mode=4, ip="192.168.86.30")     
        user2.by_mode(mode=2, ip="192.168.86.32")        
        user3.by_mode(mode=2, ip="192.168.86.33")        



        # Only close down process once incoming message queue is empty
        if (close_pending is True and len(msg_in) == 0 and msg_in_queue.empty() is True) or (time.time() > (last_hb + 30)):
            break                                        
             

        # Pause before re-checking queue
        time.sleep(0.107)  