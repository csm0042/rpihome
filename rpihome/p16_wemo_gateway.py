#!/usr/bin/python3
""" p16_wemo_gateway.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import logging
import multiprocessing
import pywemo
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


# Wemo Gateway Process loop *******************************************************************************************
def wemo_func(msg_in_queue, msg_out_queue, log_queue, log_configurer):
    log_configurer(log_queue)
    name = multiprocessing.current_process().name
    logger = logging.getLogger("main")
    logger.log(logging.DEBUG, "Logging handler for p16_wemo_gateway process started")

    msg_in = str()
    close_pending = False
    last_hb = time.time()
    devices = pywemo.discover_devices()
    numOfDevices = len(devices)
    logging.log(logging.DEBUG, "Found %s wemo devices on network" % str(numOfDevices))
    for i, j in enumerate(devices):
        logging.log(logging.DEBUG, "Found Device: %s" % str(j))

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
                elif msg_in[6:9] == "160":
                    device, found = find_device_match(msg_in[10:], devices)
                    if found is True:
                        device.off()
                        logging.log(logging.DEBUG, "OFF command sent to device: %s" % msg_in[10:])
                    else:
                        logging.log(logging.DEBUG, "Could not find device %s on the network" % msg_in[10:])
                    pass  
                # Process wemo on command                       
                elif msg_in[6:9] == "161":
                    device, found = find_device_match(msg_in[10:], devices)
                    if found is True:
                        device.on()
                        logging.log(logging.DEBUG, "ON command sent to device: %s" % msg_in[10:])   
                    else:
                        logging.log(logging.DEBUG, "Could not find device %s on the network" % msg_in[10:])
                    pass 
                # Process wemo state-request message
                elif msg_in[6:9] == "162":
                    #logging.log(logging.DEBUG, "Requesting current status of device: %s" % msg_in[10:])
                    device, found = find_device_match(msg_in[10:], devices)
                    if found is True:
                        state = device.get_state(force_update=True)
                        state_response = "16," + msg_in[0:2] + ",163," + str(state) + "," + msg_in[10:]
                        msg_out_queue.put_nowait(state_response)
                        logging.log(logging.DEBUG, "Response message [%s] sent for device: %s" % (state_response, msg_in[10:]))   
                    else:
                        pass  
                # Process "kill process" message
                elif msg_in[6:9] == "999":
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


def find_device_match(name, device_list):
    found = False
    lower_name = name.lower()
    for index, device in enumerate(device_list):
        lower_dev_name = device.name.lower()
        if lower_dev_name.find(lower_name) != -1:
            return device, True
    return None, False
