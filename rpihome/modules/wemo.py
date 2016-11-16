#!/usr/bin/python3
""" wemo.py: Helper Class and methods to find and control wemo devices
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import logging
import pywemo


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Wemo Device Helper Class ***************************************************************************************************
class WemoHelper(object):
    def __init__(self):
        self.device_list = []
        self.device_name = str()
        self.found = False
        self.request_from = str()
        self.state = int()
        self.device_address = str()
        self.port = None
        self.device = None
        self.url = str()

    def switch_off(self, msg_in):
        """ Searches list for existing wemo device with matching name, then sends off command to
        device if found """
        self.device_name = str(msg_in[10:]).lower()
        self.found = False
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, send OFF command to device
            if (device.name.lower()).find(self.device_name) != -1:
                self.found = True
                device.off()
                logging.log(logging.DEBUG, "OFF command sent to device: %s" % self.device_name)
        # If match is not found, log error and continue
        if self.found is False:
            logging.log(logging.DEBUG, "Could not find device: %s on the network" %
                            self.device_name)

    def switch_on(self, msg_in):
        """ Searches list for existing wemo device with matching name, then sends on command
        to device if found """
        self.device_name = str(msg_in[10:]).lower()
        self.found = False
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, send ON command to device
            if (device.name.lower()).find(self.device_name) != -1:
                self.found = True
                device.on()
                logging.log(logging.DEBUG, "ON command sent to device: %s" % self.device_name)
        # If match is not found, log error and continue
        if self.found is False:
            logging.log(logging.DEBUG, "Could not find device: %s on the network" %
                            self.device_name)

    def query_status(self, msg_in, msg_out):
        """ Searches list for existing wemo device with matching name, then sends "get status-
        update" message to device if found """
        self.device_name = str(msg_in[10:]).lower()
        self.request_from = str(msg_in[0:2])
        self.found = False
        logging.log(logging.DEBUG, "Querrying status for device: %s" % str(self.device_name))
        # Search list of existing devices on network for matching device name
        for index, device in enumerate(self.device_list):
            # If match is found, get status update from device, then send response message to
            # originating process
            if (device.name.lower()).find(self.device_name) != -1:
                self.found = True
                self.state = device.get_state(force_update=True)
                msg_out.put_nowait("16,%s,163,%s,%s" %
                                   (self.request_from, str(self.state), self.device_name))
                logging.log(logging.DEBUG, "Response message [%s] sent for device: %s" %
                                (str(self.state), self.device_name))
            if self.found is False:
                logging.log(logging.DEBUG, "Could not find device: %s on network" %
                                str(self.device_name))

    def discover_device(self, msg_in):
        """ Searches for a wemo device on the network at a particular IP address and appends it to
        the master device list if found """
        self.device_address = msg_in[10:]
        logging.log(logging.DEBUG, "Searching for wemo device at: %s" %
                        self.device_address)
        # Probe device at specified IP address for port it is listening on
        try:
            self.port = None
            self.port = pywemo.ouimeaux_device.probe_wemo(self.device_address)
        except:
            logging.log(logging.DEBUG, "Error discovering port of wemo device at address: %s" %
                            str(self.device_address))
            self.port = None
        # If port is found, probe device for type and other attributes
        if self.port is not None:
            self.url = 'http://%s:%i/setup.xml' % (self.device_address, self.port)
            try:
                self.device = None
                self.device = pywemo.discovery.device_from_description(self.url, None)
            except:
                logging.log(logging.DEBUG, "Error discovering attributes for device at \
                                address: %s, port: %s" %
                                (str(self.device_address), str(self.port)))
        # If device is found and probe was successful, check existing device list to
        # determine if device is already present in list
        if self.device is not None:
            self.found = False
            for index, device in enumerate(self.device_list):
                if self.device.name == device.name:
                    self.found = True
                    logging.log(logging.DEBUG, "Device: %s already exists in device \
                                    list at address: %s and port: %s" %
                                    (self.device.name, self.device_address, self.port))
            # If not found in list, add it
            if self.found is False:
                logging.log(logging.DEBUG, "Found wemo device name: %s at: %s, port: %s" %
                                (self.device.name, self.device_address, self.port))
                self.device_list.append(copy.copy(self.device))
