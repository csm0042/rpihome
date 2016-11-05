#!/usr/bin/python3
""" logic.py: Decision making engine for the RPi Home application  
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time

from rules import device_rpi
from rules import device_wemo_fylt1
from rules import device_wemo_bylt1
from rules import device_wemo_ewlt1
from rules import device_wemo_cclt1
from rules import device_wemo_lrlt1
from rules import device_wemo_drlt1
from rules import device_wemo_b1lt1
from rules import device_wemo_b1lt2
from rules import device_wemo_b2lt1
from rules import device_wemo_b2lt2
from rules import device_wemo_b3lt1
from rules import device_wemo_b3lt2


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Logic Solver Process loop **********************************************************************************************
def logic_func(msg_in_queue, msg_out_queue, log_queue, log_configurer):
    log_configurer(log_queue)
    name = multiprocessing.current_process().name
    logger = logging.getLogger("main")
    logger.log(logging.DEBUG, "Logging handler for p11_logic_solver process started")

    msg_in = str()
    close_pending = False
    last_hb = time.time() 
    update_index = 0

    print("Waiting 5 seconds for wemo discovery process to complete")
    time.sleep(5)
    print("Running logic solver")

    # Create devices
    rpi_screen = device_rpi.RPImain("rpi", msg_out_queue)
    wemo_fylt1 = device_wemo_fylt1.Wemo_fylt1("fylt1", msg_out_queue)
    wemo_bylt1 = device_wemo_bylt1.Wemo_bylt1("bylt1", msg_out_queue)
    wemo_ewlt1 = device_wemo_ewlt1.Wemo_ewlt1("ewlt1", msg_out_queue)
    wemo_cclt1 = device_wemo_cclt1.Wemo_cclt1("cclt1", msg_out_queue)
    wemo_lrlt1 = device_wemo_lrlt1.Wemo_lrlt1("lrlt1", msg_out_queue)
    wemo_drlt1 = device_wemo_drlt1.Wemo_drlt1("drlt1", msg_out_queue)
    wemo_b1lt1 = device_wemo_b1lt1.Wemo_b1lt1("b1lt1", msg_out_queue)
    wemo_b1lt2 = device_wemo_b1lt2.Wemo_b1lt2("b1lt2", msg_out_queue)
    wemo_b2lt1 = device_wemo_b2lt1.Wemo_b2lt1("b2lt1", msg_out_queue)
    wemo_b2lt2 = device_wemo_b2lt2.Wemo_b2lt2("b2lt2", msg_out_queue)
    wemo_b3lt1 = device_wemo_b3lt1.Wemo_b3lt1("b3lt1", msg_out_queue)
    wemo_b3lt2 = device_wemo_b3lt2.Wemo_b3lt2("b3lt2", msg_out_queue)


    # create home array
    homeArray = [False, False, False] 
    # create home time array (logs when a person first gets home)
    baseTime = datetime.datetime.now() + datetime.timedelta(minutes=-15)
    homeTime = [baseTime, baseTime, baseTime]

    while True:
        # Monitor message queue for new messages
        try:
            msg_in = msg_in_queue.get_nowait()  
        except:
            pass

        # Process incoming message(s)
        if len(msg_in) != 0:
            if msg_in[3:5] == "11":
                if msg_in[6:9] == "001":
                    #logging.log(logging.DEBUG, "Heartbeat received: %s" % msg_in)
                    last_hb = time.time()
                elif msg_in[6:9] == "100":
                    if msg_in[10:] == "user1":
                        homeArray[0] = False
                        logging.log(logging.INFO, "User1 is no longer home")
                    elif msg_in[10:] == "user2":
                        homeArray[1] = False
                        logging.log(logging.INFO, "User2 is no longer home")
                    elif msg_in[10:] == "user3":
                        homeArray[2] = False  
                        logging.log(logging.INFO, "User3 is no longer home")                  
                elif msg_in[6:9] == "101":
                    if msg_in[10:] == "user1":
                        homeArray[0] = True
                        homeTime[0] = datetime.datetime.now()
                        logging.log(logging.INFO, "User1 is home")
                    elif msg_in[10:] == "user2":
                        homeArray[1] = True
                        homeTime[1] = datetime.datetime.now()
                        logging.log(logging.INFO, "User2 is home")
                    elif msg_in[10:] == "user3":
                        homeArray[2] = True
                        homeTime[2] = datetime.datetime.now() 
                        logging.log(logging.INFO, "User3 is home")  
                    else:
                        pass
                    msg_out_queue.put_nowait("02,11,166,%s,%s" % (msg_in[10:11], msg_in[12:]))
                elif msg_in[6:9] == "163":
                    if msg_in[10:11] == "0":
                        if msg_in[12:] == "fylt1":
                            pass
                        elif msg_in[12:] == "bylt1":
                            pass
                        elif msg_in[12:] == "ewlt1":
                            pass
                        elif msg_in[12:] == "cclt1":
                            pass
                        elif msg_in[12:] == "lrlt1":
                            pass
                        elif msg_in[12:] == "drlt1":
                            pass
                        elif msg_in[12:] == "b1lt1":
                            pass
                        elif msg_in[12:] == "b1lt2":
                            pass
                        elif msg_in[12:] == "b2lt1":
                            pass
                        elif msg_in[12:] == "b2lt2":
                            pass
                        elif msg_in[12:] == "b3lt1":
                            pass
                        elif msg_in[12:] == "b3lt2":
                            pass
                    elif msg_in[10:11] == "1":
                        if msg_in[12:] == "fylt1":
                            pass
                        elif msg_in[12:] == "bylt1":
                            pass
                        elif msg_in[12:] == "ewlt1":
                            pass
                        elif msg_in[12:] == "cclt1":
                            pass
                        elif msg_in[12:] == "lrlt1":
                            pass
                        elif msg_in[12:] == "drlt1":
                            pass
                        elif msg_in[12:] == "b1lt1":
                            pass
                        elif msg_in[12:] == "b1lt2":
                            pass
                        elif msg_in[12:] == "b2lt1":
                            pass
                        elif msg_in[12:] == "b2lt2":
                            pass
                        elif msg_in[12:] == "b3lt1":
                            pass
                        elif msg_in[12:] == "b3lt2":
                            pass
                elif msg_in[6:9] == "999":
                    logging.log(logging.DEBUG, "Kill code received - Shutting down: %s" % msg_in)
                    close_pending = True
            else:
                msg_out_queue.put_nowait(msg_in)
            pass  
            msg_in = str()


        # UPDATE ON AND OFF TIME RULES
        rpi_screen.check_rules(homeArray=homeArray)        
        wemo_fylt1.check_rules(homeArray=homeArray, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))
        wemo_bylt1.check_rules(homeArray=homeArray, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))
        wemo_ewlt1.check_rules(homeArray=homeArray, homeTime=homeTime, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))
        wemo_cclt1.check_rules(homeArray=homeArray, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))  
        wemo_lrlt1.check_rules(homeArray=homeArray, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))
        wemo_drlt1.check_rules(homeArray=homeArray, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))      
        wemo_b1lt1.check_rules(homeArray=homeArray)        
        wemo_b1lt2.check_rules(homeArray=homeArray)
        wemo_b2lt1.check_rules(homeArray=homeArray)        
        wemo_b2lt2.check_rules(homeArray=homeArray) 
        wemo_b3lt1.check_rules(homeArray=homeArray)        
        wemo_b3lt2.check_rules(homeArray=homeArray) 

        # Send commands when change-of-state detected in desired output state
        wemo_fylt1.command()
        wemo_bylt1.command()
        rpi_screen.command()
        wemo_ewlt1.command()
        wemo_cclt1.command()
        wemo_lrlt1.command()
        wemo_drlt1.command()
        wemo_b1lt1.command()
        wemo_b1lt2.command()
        wemo_b2lt1.command()
        wemo_b2lt2.command()
        wemo_b3lt1.command()
        wemo_b3lt2.command()     
   
                               
         # Only close down process once incoming message queue is empty
        if (close_pending is True and len(msg_in) == 0 and msg_in_queue.empty() is True) or (time.time() > (last_hb + 30)):
            break 

        # Pause before re-checking queue
        time.sleep(0.97)