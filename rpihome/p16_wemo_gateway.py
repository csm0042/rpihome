#!/usr/bin/python3
""" p16_wemo_gateway.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import logging
import multiprocessing
import os
import sys
import time
import pywemo
from modules.logger_mp import worker_configurer
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


# Process Class ***********************************************************************************
class WemoProcess(multiprocessing.Process):
    """ WEMO gateway process class and methods """
    def __init__(self, in_queue, out_queue, log_queue, **kwargs):
        self.msg_in_queue = in_queue
        self.msg_out_queue = out_queue        
        # Initialize logging
        worker_configurer(log_queue)
        self.logger = logging.getLogger(__name__)      
        # Set default input parameter values
        self.name = "undefined"
        # Update default elements based on any parameters passed in
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
        # Initialize parent class 
        multiprocessing.Process.__init__(self, name=self.name)
        # Create remaining class elements
        self.work_queue_empty = True
        self.work_queue = multiprocessing.Queue(-1)
        self.msg_in = message.Message()
        self.msg_in_empty = True
        self.msg_to_process = message.Message()
        self.msg_to_send = message.Message()
        self.last_hb = datetime.datetime.now()
        self.in_msg_loop = bool()
        self.main_loop = bool()
        self.device = None
        self.device_list = []
        self.index = 0
        self.last_update = datetime.datetime.now()
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
                self.msg_in_empty = False
                self.logger.debug("Processing message [%s] from incoming message queue",
                                  self.msg_in.raw)
                if self.msg_in.dest == "16":
                    if self.msg_in.type == "001":
                        self.last_hb = datetime.datetime.now()
                    elif self.msg_in.type == "999":
                        self.logger.info("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in.raw)
                        self.logger.debug("Moving message [%s] over to internal work queue",
                                          self.msg_in.raw)
                else:
                    self.msg_out_queue.put_nowait(self.msg_in.raw)
                    self.logger.debug("Redirecting message [%s] back to main", self.msg_in.raw)
                self.msg_in = message.Message()
            else:
                self.msg_in_empty = True
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
            self.work_queue_empty = False
            self.logger.debug("Processing message [%s] from internal work queue",
                              self.msg_to_process.raw)

            # Discover Device
            if self.msg_to_process.type == "160":
                self.logger.debug("Message type 160 - attempting to discover device: %s", self.msg_to_process.payload)
                self.device = self.discover_device(self.msg_to_process.name, self.msg_to_process.payload)
                self.msg_to_send = message.Message(source="16", dest=self.msg_to_process.source, type="160A", name=self.msg_to_process.name)
                if self.device is not None:
                    self.msg_to_send.payload = "found"
                else:
                    self.msg_to_send.payload = "not found"
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug("Sending discovery successful message: [%s]", self.msg_to_send.raw)

            # Set Wemo state
            if self.msg_to_process.type == "161":
                # Process wemo off commands
                if self.msg_to_process.payload == "off":
                    self.logger.debug("Sending \"off\" command to device: %s", self.msg_to_process.name)
                    self.switch_off(self.msg_to_process.name)
                # Process wemo on command
                if self.msg_to_process.payload == "on":
                    self.logger.debug("Sending \"on\" command to device: %s", self.msg_to_process.name)
                    self.switch_on(self.msg_to_process.name)

            # Get Wemo state
            if self.msg_to_process.type == "162":
                self.msg_162(self.msg_to_process.name, self.msg_to_process.source)
            
            # Clear msg-to-process string
            self.msg_to_process = message.Message()
        else:
            self.work_queue_empty = True
            self.msg_to_process = message.Message()                

    
    def msg_162(self, name, dest):
        self.logger.debug("Sending \"request state\" command to device: %s", name)
        self.status = self.query_status(name)
        self.msg_to_send = message.Message(source="16", dest=dest, type="162A", name=name)
        if self.status is not None:
            self.logger.debug("Get status query successfully returned value of: %s", self.status)
            self.msg_to_send.payload = self.status
        else:
            self.logger.warning("Device [%s] did not respond to Get status query", name)
            self.msg_to_send.payload = ""
        # send response
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending get-status successful message: [%s]", self.msg_to_send.raw)



    def discover_device(self, name, address):
        """ Searches for a wemo device on the network at a particular IP address and appends it to
        the master device list if found """
        self.logger.debug("Searching for wemo device at: %s", address)
        self.port = None
        self.device = None
        # Probe device at specified IP address for port it is listening on
        try:
            self.port = pywemo.ouimeaux_device.probe_wemo(address)
        except:
            self.logger.warning("Error discovering port of wemo device at address: %s", address)
            self.port = None
        # If port is found, probe device for type and other attributes
        if self.port is not None:
            self.logger.debug("Found wemo device at: %s on port: %s", address, str(self.port))
            self.url = 'http://%s:%i/setup.xml' % (address, self.port)
            try:
                self.device = pywemo.discovery.device_from_description(self.url, None)
            except:
                self.logger.warning("Error discovering attributes for device at address: %s, port: %s", address, str(self.port))
                self.device = None
        else:
            self.logger.warning("No wemo device detected at: %s", address)
        # If device is found and probe was successful, check existing device list to
        # determine if device is already present in list
        if self.port is not None and self.device is not None:
            if self.device.name.find(name) != -1:
                self.logger.debug("Discovery successful for wemo device: %s at: %s, port: %s", name, address, str(self.port))
                # Search device list to determine if device already exists
                for index, device in enumerate(self.device_list):
                    if self.device.name == device.name:
                        self.logger.debug("Device: %s already exists in device list at address: %s and port: %s", self.device.name, address, self.port)
                        self.device_list[index] = copy.copy(device)
                        self.logger.debug("Replacing old device [%s] record in know device list with updated device attributes", self.device.name)
                        break
                else:
                # If not found in list, add it
                    self.logger.debug("Device [%s] not previously discovered.  Adding to known device list", self.device.name)
                    self.device_list.append(copy.copy(self.device))
                    self.logger.debug("Updated device list: %s", str(self.device_list))
                    return self.device
            else:
                self.logger.error("Device name mis-match between found device and configuration")
        else:
            self.logger.warning("Device was not found")
            return None


    def switch_on(self, name):
        """ Searches list for existing wemo device with matching name, then sends on command
        to device if found """
        self.found = False
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, send ON command to device
            if device.name.find(name) != -1:
                self.found = True
                device.on()
                self.logger.debug("ON command sent to device: %s", name)
                return True
        # If match is not found, log error and continue
        if self.found is False:
            self.logger.warning("Could not find device: %s on the network", name)
            return False           


    def switch_off(self, name):
        """ Searches list for existing wemo device with matching name, then sends off command to
        device if found """
        self.found = False
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, send OFF command to device
            if device.name.find(name) != -1:
                self.found = True
                device.off()
                self.logger.debug("OFF command sent to device: %s", name)
                return True
        # If match is not found, log error and continue
        if self.found is False:
            self.logger.warning("Could not find device: %s on the network", name)
            return False


    def query_status(self, name):
        """ Searches list for existing wemo device with matching name, then sends "get status-
        update" message to device if found """
        self.found = False
        self.logger.debug("Querrying status for device: %s", name)
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, get status update from device, then send response message to
            # originating process
            if device.name.find(name) != -1:
                self.found = True
                self.logger.debug("Found device [%s] in existing device list", name)
                self.state = str(device.get_state(force_update=True))
                self.logger.debug("Returning status [%s] to main program", self.state)
                return self.state
        if self.found is False:
            self.logger.warning("Could not find device [%s] in existing device list", name)
            return None          


    def run(self):
        """ Actual process loop.  Runs whenever start() method is called """
        self.logger.info("Main loop started")
        # Main process loop
        self.main_loop = True
        while self.main_loop is True:
            # Process incoming messages
            self.process_in_msg_queue()

            # Process tasks in internal work queue
            if self.close_pending is False:
                self.process_work_queue()

            """
            # Update device status periodically
            if self.close_pending is False:
                if self.msg_in_empty is True and self.work_queue_empty is True:
                    if datetime.datetime.now() > self.last_update + datetime.timedelta(seconds=60):
                        self.last_update = datetime.datetime.now()
                        # Check index pointer against device list length to prevent overflow
                        if len(self.device_list) > 0:
                            if self.index > (len(self.device_list) - 1):
                                self.index = 0
                            # Check one device each scan
                            self.msg_162(self.device_list[self.index].name, "02")
                            self.index += 1
            """

            # Close process
            if self.close_pending is True:
                self.main_loop = False
            elif datetime.datetime.now() > self.last_hb + datetime.timedelta(seconds=30):
                self.logger.critical("Comm timeout - shutting down")
                self.main_loop = False

            # Pause before next process run
            time.sleep(0.097)

        # Send final log message when process exits
        self.logger.info("Shutdown complete")
