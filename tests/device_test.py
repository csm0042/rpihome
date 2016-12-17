#!/usr/bin/python3
""" device_test.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
import multiprocessing
import sys
import unittest
if __name__ == "__main__": sys.path.append("..")
from rpihome.devices.device import Device



# Define test class *******************************************************************************
class TestDevice(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.testQueue = multiprocessing.Queue(-1)            
        self.device = Device("test-name", self.testQueue)

    def test_name(self):
        self.device.name = "new-test-name"
        self.assertEqual(self.device.name, "new-test-name")

    def test_state(self):
        self.device.state = True
        self.assertEqual(self.device.state, True) 
        self.device.state = None
        self.assertEqual(self.device.state, True)          
        self.device.state = False
        self.assertEqual(self.device.state, False)               

    def test_state_mem(self):
        self.device.state_mem = False
        self.assertEqual(self.device.state_mem, False)
        self.device.state_mem = True
        self.assertEqual(self.device.state_mem, True)
        self.device.state_mem = None
        self.assertEqual(self.device.state_mem, None)

    def test_status(self):
        self.device.status = 1
        self.assertEqual(self.device.status, 1)
        self.device.status = 0
        self.assertEqual(self.device.status, 0)
        self.device.status = "n"
        self.assertIsInstance(self.device.status, int)
        self.assertEqual(self.device.status, 0)      

    def test_statusChangeTS(self):
        self.datetimeCompare = datetime.datetime.now()
        self.device.statusChangeTS = self.datetimeCompare
        self.assertIsInstance(self.device.statusChangeTS, datetime.datetime)
        self.assertEqual(self.device.statusChangeTS, self.datetimeCompare)      

    def test_online(self):
        self.device.online = True
        self.assertEqual(self.device.online, True) 
        self.device.online = None
        self.assertEqual(self.device.online, None)          
        self.device.online = False
        self.assertEqual(self.device.online, False)         
        self.assertIsInstance(self.device.online, bool)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.debug("\n\nStarting log\n")
    unittest.main()     
