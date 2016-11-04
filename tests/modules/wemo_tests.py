#!/usr/bin/python3
""" wemo_tests.py:
"""

# Import Required Libraries (Standard, Third Party, Local) *************************************************************
import unittest
from rpihome.modules.wemo import discover


# Authorship Info ******************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Test Class for Wemo Discovery Module *********************************************************************************
class TestWemoMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_wemo_discovery(self):
        self.foundDevices = discover()
        self.assertEqual(len(self.foundDevices), 10)


# Run if called as Main ************************************************************************************************
if __name__ == '__main__':
    unittest.main()