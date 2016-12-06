#!/usr/bin/python3
""" schedule_test.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import logging
import multiprocessing
import unittest
import sys

if __name__ == "__main__": sys.path.append("..")
from rpihome.modules.schedule import Condition, OnRange, Day, Week
from rpihome.devices.device import Device


# Define test class *******************************************************************************
class Test_Schedule(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("\n\nStarting log\n")
        self.condition = Condition()
        self.on_range = OnRange()
        self.week = Week(logger=self.logger)
        self.dt = datetime.datetime.now()
        self.home_array = [True, True, True]
        self.utc_offset = datetime.timedelta(hours=-6)
        self.schedule = Week()
        self.test_queue = multiprocessing.Queue(-1)
        self.device = Device("test_device", self.test_queue, logger=self.logger)
        self.on_range_array = []

    def test_schedule_day(self):
        self.schedule = Week()
        self.on_range_array = []

        self.on_range = OnRange(ontime=datetime.time(6, 30),
                                offtime=datetime.time(7, 0),
                                condition=[Condition(condition="user1", state="true"),
                                           Condition(condition="user2", state="false"),
                                           Condition(condition="user3", state="false")])
        self.on_range_array.append(copy.copy(self.on_range))

        self.on_range = OnRange(ontime=datetime.time(5, 40),
                                offtime=datetime.time(6, 30),
                                condition=[Condition(condition="user1", state="true"),
                                           Condition(condition="user2", state="true")])
        self.on_range_array.append(copy.copy(self.on_range))

        self.on_range = OnRange(ontime=datetime.time(5, 40),
                                offtime=datetime.time(6, 30),
                                condition=[Condition(condition="user1", state="true"),
                                           Condition(condition="user3", state="true")])
        self.on_range_array.append(copy.copy(self.on_range))

        self.schedule.monday.on_range = self.on_range_array

        # Check combo 1 - all three home, before lights turn on
        self.dt = datetime.datetime.combine(datetime.date(2016, 12, 5), datetime.time(5, 39))
        self.home_array = [True, True, True]
        self.utc_offset = datetime.timedelta(hours=-6)
        self.device.check_custom_rules(datetime=self.dt,
                                       homeArray=self.home_array,
                                       utcOffset=self.utc_offset,
                                       schedule=self.schedule)
        self.assertEqual(self.device.state, False)

        # Check combo 1 - all three home, after lights turn on
        self.dt = datetime.datetime.combine(datetime.date(2016, 12, 5), datetime.time(5, 41))
        self.home_array = [True, True, True]
        self.utc_offset = datetime.timedelta(hours=-6)
        self.device.check_custom_rules(datetime=self.dt,
                                       homeArray=self.home_array,
                                       utcOffset=self.utc_offset,
                                       schedule=self.schedule)
        self.assertEqual(self.device.state, True)

        # Check combo 1 - all three home, before lights turn off
        self.dt = datetime.datetime.combine(datetime.date(2016, 12, 5), datetime.time(6, 29))
        self.home_array = [True, True, True]
        self.utc_offset = datetime.timedelta(hours=-6)
        self.device.check_custom_rules(datetime=self.dt,
                                       homeArray=self.home_array,
                                       utcOffset=self.utc_offset,
                                       schedule=self.schedule)
        self.assertEqual(self.device.state, True)

        # Check combo 1 - all three home, after lights turn off
        self.dt = datetime.datetime.combine(datetime.date(2016, 12, 5), datetime.time(6, 31))
        self.home_array = [True, True, True]
        self.utc_offset = datetime.timedelta(hours=-6)
        self.device.check_custom_rules(datetime=self.dt,
                                       homeArray=self.home_array,
                                       utcOffset=self.utc_offset,
                                       schedule=self.schedule)
        self.assertEqual(self.device.state, False)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    unittest.main()
