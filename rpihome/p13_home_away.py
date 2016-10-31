#!/usr/bin/python3
""" occupancy.py: Human occupancy checker for the RPiHome application.  
    When running, this application will periodically ping a list of specific devices that are identified in the system
    database as the personal cell phones of the home's occupants.  The results of those pings, along with a timestamp
    are written to the database each time to keep it up to date on who's home at any given time. 
    Logging is handled via a common queue and log handler running as a separate process.  
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

    user1home = home_user1.HomeUser1(msg_out_queue)
    user2home = home_user2.HomeUser2(msg_out_queue)
    user3home = home_user3.HomeUser3(msg_out_queue)


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
                        user1home.mode = 0
                    if msg_in[10:] == "user2":
                        user2home.mode = 0
                    if msg_in[10:] == "user3":
                        user3home.mode = 0                       
                # 131 = Home-Away mode set to home (override)
                if msg_in[6:9] == "131":
                    logging.log(logging.DEBUG, "Setting home/away mode for %s to \"home\"" % msg_in[10:])
                    if msg_in[10:] == "user1":
                        user1home.mode = 1
                    if msg_in[10:] == "user2":
                        user2home.mode = 1
                    if msg_in[10:] == "user3":
                        user3home.mode = 1                
                # 132 = Home-Away mode set to auto (by schedule)
                if msg_in[6:9] == "132":
                    logging.log(logging.DEBUG, "Setting home/away mode for %s to auto (by schedule)" % msg_in[10:])
                    if msg_in[10:] == "user1":
                        user1home.mode = 2
                    if msg_in[10:] == "user2":
                        user2home.mode = 2
                    if msg_in[10:] == "user3":
                        user3home.mode = 2 
                # 133 = Home-Away mode set to auto (arp/ping-based)
                if msg_in[6:9] == "133":
                    logging.log(logging.DEBUG, "Setting home/away mode for %s to auto (by arp/ping)" % msg_in[10:])
                    if msg_in[10:] == "user1":
                        user1home.mode = 3
                    if msg_in[10:] == "user2":
                        user2home.mode = 3
                    if msg_in[10:] == "user3":
                        user3home.mode = 3                                  
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
                                

        # Check if user is home
        user1home.by_mode(mode=4, ip="192.168.86.30")     
        user2home.by_mode(mode=4, ip="192.168.86.32")        
        user3home.by_mode(mode=4, ip="192.168.86.33")        



        # Only close down process once incoming message queue is empty
        if (close_pending is True and len(msg_in) == 0 and msg_in_queue.empty() is True) or (time.time() > (last_hb + 30)):
            break                                        
             

        # Pause before re-checking queue
        time.sleep(0.107)  