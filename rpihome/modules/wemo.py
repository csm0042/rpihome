#!/usr/bin/python3
""" wemo.py: Helper Class and methods to find and control wemo devices
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import logging
import pywemo
from rpihome.modules.message import Message


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Wemo Device Helper Class ************************************************************************
class WemoHelper(object):
    def __init__(self, logger):
        self.logger = logger
        self.device_list = []
        self.found = False
        self.state = int()
        self.port = None
        self.device = None
        self.url = str()
        self.msg_in = Message()
        self.msg_out = Message()
        self.msg_to_send = Message()


    def switch_off(self, msg_in):
        """ Searches list for existing wemo device with matching name, then sends off command to
        device if found """
        self.msg_in = Message(raw=msg_in)
        self.found = False
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, send OFF command to device
            if device.name.find(self.msg_in.name) != -1:
                self.found = True
                device.off()
                self.logger.debug("OFF command sent to device: %s" % self.msg_in.name)
        # If match is not found, log error and continue
        if self.found is False:
            self.logger.debug("Could not find device: %s on the network", self.msg_in.name)


    def switch_on(self, msg_in):
        """ Searches list for existing wemo device with matching name, then sends on command
        to device if found """
        self.msg_in = Message(raw=msg_in)
        self.found = False
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, send ON command to device
            if device.name.find(self.msg_in.name) != -1:
                self.found = True
                device.on()
                self.logger.debug("ON command sent to device: %s", self.msg_in.name)
        # If match is not found, log error and continue
        if self.found is False:
            self.logger.debug("Could not find device: %s on the network", self.msg_in.name)


    def query_status(self, msg_in, msg_out):
        """ Searches list for existing wemo device with matching name, then sends "get status-
        update" message to device if found """
        self.msg_in = Message(raw=msg_in)
        self.msg_out_queue = msg_out
        self.found = False
        self.logger.debug("Querrying status for device: %s", self.msg_in.name)
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, get status update from device, then send response message to
            # originating process
            if device.name.find(self.msg_in.name) != -1:
                self.found = True
                self.state = device.get_state(force_update=True)
                self.msg_to_send = Message(source="16", dest=self.msg_in.source, type="163",
                                           name=self.msg_in.name, payload=str(self.state))
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.logger.debug("Response message [%s] sent for device: %s",
                                  self.msg_to_send.raw, self.msg_to_send.name)
            if self.found is False:
                self.logger.debug("Could not find device: %s", self.msg_in.name)


    def discover_device(self, msg_in):
        """ Searches for a wemo device on the network at a particular IP address and appends it to
        the master device list if found """
        self.msg_in = Message(raw=msg_in)
        self.logger.debug("Searching for wemo device at: %s", self.msg_in.payload)
        # Probe device at specified IP address for port it is listening on
        try:
            self.port = None
            self.port = pywemo.ouimeaux_device.probe_wemo(self.msg_in.payload)
        except:
            self.logger.debug("Error discovering port of wemo device at address: %s",
                              self.msg_in.payload)
            self.port = None
        # If port is found, probe device for type and other attributes
        if self.port is not None:
            self.url = 'http://%s:%i/setup.xml' % (self.msg_in.payload, self.port)
            try:
                self.device = None
                self.device = pywemo.discovery.device_from_description(self.url, None)
            except:
                self.logger.debug("Error discovering attributes for device at address: %s, port: %s",
                                  self.msg_in.payload, self.port)
        # If device is found and probe was successful, check existing device list to
        # determine if device is already present in list
        if self.device is not None:
            self.found = False
            for index, device in enumerate(self.device_list):
                if self.msg_in.name == device.name:
                    self.found = True
                    self.logger.debug("Device: %s already exists in device list at address: %s and \
                                      port: %s", self.msg_in.name, self.msg_in.payload, self.port)
            # If not found in list, add it
            if self.found is False:
                self.logger.debug("Found wemo device name: %s at: %s, port: %s", self.msg_in.name,
                                  self.msg_in.payload, self.port)
                self.device_list.append(copy.copy(self.device))
