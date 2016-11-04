#!/usr/bin/python3
""" test_rpihome.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import datetime
import unittest

from ..p16_wemo_gateway import wemo_func as wemo_func
from ..p16_wemo_gateway import discover as discover


"""
if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from rpihome import p16_wemo_gateway
    from rpihome.modules import wemo
    from rpihome.modules import sunrise """


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"     


# Test Class for Sunrise / Sunset Module *******************************************************************************************
class TestSunriseSunset(unittest.TestCase):
    def setUp(self):
        self.s = sunrise.sun(lat=38.566, long=-90.409)
        self.utcOffset = -5

    def test_sunrise(self):
        self.sunrise_time = self.s.sunrise(datetime.datetime.now(), self.utcOffset)
        self.sunrise = datetime.datetime.combine(datetime.datetime.today().date(), self.sunrise_time)
        self.sunrise_compare = datetime.datetime.now()   
        print("Sunrise: " + str(self.sunrise))     
        self.assertLessEqual(self.sunrise, self.sunrise_compare)

    def test_sunset(self):
        self.sunset_time = self.s.sunset(datetime.datetime.now(), self.utcOffset)
        self.sunset = datetime.datetime.combine(datetime.datetime.today().date(), self.sunset_time)     
        self.sunset_compare = datetime.datetime.now() 
        print("Sunset: " + str(self.sunset))          
        self.assertGreaterEqual(self.sunset, self.sunset_compare)


# Test Class for Wemo Discovery Module **********************************************************************************************
class TestWemoMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_wemo_discovery(self):
        self.foundDevices = wemo.discover()
        self.assertEqual(len(self.foundDevices), 10)


# Run if called as Main ************************************************************************************************************
if __name__ == '__main__':
    unittest.main()