import logging
import pywemo

# Wemo Discovery function *********************************************************************************************
def discover():
    devices = pywemo.discover_devices()
    numOfDevices = len(devices)
    logging.log(logging.DEBUG, "Found %s wemo devices on network" % str(numOfDevices))
    for i, j in enumerate(devices):
        logging.log(logging.DEBUG, "Found Device: %s" % str(j))
    return devices