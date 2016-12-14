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
from rpihome.modules.schedule import Day, Week, OnRange, Condition


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

    def test_home(self):
        self.device.home = True
        self.assertEqual(self.device.home, True) 
        self.device.home = None
        self.assertEqual(self.device.home, None)          
        self.device.home = False
        self.assertEqual(self.device.home, False)         
        self.assertIsInstance(self.device.home, bool)

    def test_homeNew(self):
        self.device.homeNew = True
        self.assertEqual(self.device.homeNew, True)
        self.device.homeNew = None
        self.assertEqual(self.device.homeNew, None)
        self.device.homeNew = False
        self.assertEqual(self.device.homeNew, False)
        self.assertIsInstance(self.device.homeNew, bool)

    def test_homeArray(self):
        self.homeArray = [True, True, True]
        self.homeTime = [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()]
        self.assertIsInstance(self.homeArray[1], bool)
        self.assertIsInstance(self.homeTime[1], datetime.datetime)

    def test_online(self):
        self.device.online = True
        self.assertEqual(self.device.online, True) 
        self.device.online = None
        self.assertEqual(self.device.online, None)          
        self.device.online = False
        self.assertEqual(self.device.online, False)         
        self.assertIsInstance(self.device.online, bool)        

    def test_dt(self):
        self.dt = datetime.datetime.now()
        self.device.dt = self.dt
        self.assertIsInstance(self.device.dt, datetime.datetime)
        self.assertEqual(self.device.dt, self.dt)

    def test_statusChangeTS(self):
        self.datetimeCompare = datetime.datetime.now()
        self.device.statusChangeTS = self.datetimeCompare
        self.assertIsInstance(self.device.statusChangeTS, datetime.datetime)
        self.assertEqual(self.device.statusChangeTS, self.datetimeCompare)

    def test_utcOffset(self):
        self.device.utcOffset = datetime.timedelta(hours=-6)
        self.assertIsInstance(self.device.utcOffset, datetime.timedelta)
        self.assertEqual(self.device.utcOffset, datetime.timedelta(hours=-6))

    def test_schedule(self):
        self.device.schedule = Week(monday=Day(date=datetime.date(2016,12,12),
                                    on_range=OnRange(on_time=datetime.time(12, 0),
                                                     off_time=datetime.time(14, 0),
                                                     condition=Condition(andor="and",
                                                                         condition="user1",
                                                                         state="true"))),
                         tuesday=Day(date=datetime.date(2016,12,13),
                                     on_range=OnRange(on_time=datetime.time(12, 0),
                                                      off_time=datetime.time(14, 0),
                                                      condition=Condition(andor="and",
                                                                          condition="user1",
                                                                          state="true"))),
                         wednesday=Day(date=datetime.date(2016,12,14),
                                       on_range=OnRange(on_time=datetime.time(12, 0),
                                                        off_time=datetime.time(14, 0),
                                                        condition=Condition(andor="and",
                                                                            condition="user1",
                                                                            state="true"))),
                         thursday=Day(date=datetime.date(2016,12,15),
                                      on_range=OnRange(on_time=datetime.time(12, 0),
                                                       off_time=datetime.time(14, 0),
                                                       condition=Condition(andor="and",
                                                                           condition="user1",
                                                                           state="true"))),
                         friday=Day(date=datetime.date(2016,12,16),
                                    on_range=OnRange(on_time=datetime.time(12, 0),
                                                     off_time=datetime.time(14, 0),
                                                     condition=Condition(andor="and",
                                                                         condition="user1",
                                                                         state="true"))),
                         saturday=Day(date=datetime.date(2016,12,17),
                                      on_range=OnRange(on_time=datetime.time(12, 0),
                                                       off_time=datetime.time(14, 0),
                                                       condition=Condition(andor="and",
                                                                           condition="user1",
                                                                           state="true"))),
                         sunday=Day(date=datetime.date(2016,12,18),
                                    on_range=OnRange(on_time=datetime.time(12, 0),
                                                     off_time=datetime.time(14, 0),
                                                     condition=Condition(andor="and",
                                                                         condition="user1",
                                                                         state="true"))))
        self.assertEqual(self.device.schedule.monday.date, datetime.date(2016, 12, 12))
        self.assertEqual(len(self.device.schedule.monday.on_range), 1)
        self.assertEqual(self.device.schedule.monday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.monday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.monday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[0].state, "true")
        self.assertEqual(self.device.schedule.tuesday.date, datetime.date(2016, 12, 13))
        self.assertEqual(len(self.device.schedule.tuesday.on_range), 1)
        self.assertEqual(self.device.schedule.tuesday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.tuesday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.tuesday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.tuesday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.tuesday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.tuesday.on_range[0].condition[0].state, "true")
        self.assertEqual(self.device.schedule.wednesday.date, datetime.date(2016, 12, 14))
        self.assertEqual(len(self.device.schedule.wednesday.on_range), 1)
        self.assertEqual(self.device.schedule.wednesday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.wednesday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.wednesday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.wednesday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.wednesday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.wednesday.on_range[0].condition[0].state, "true")
        self.assertEqual(self.device.schedule.thursday.date, datetime.date(2016, 12, 15))
        self.assertEqual(len(self.device.schedule.thursday.on_range), 1)
        self.assertEqual(self.device.schedule.thursday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.thursday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.thursday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.thursday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.thursday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.thursday.on_range[0].condition[0].state, "true")
        self.assertEqual(self.device.schedule.friday.date, datetime.date(2016, 12, 16))
        self.assertEqual(len(self.device.schedule.friday.on_range), 1)
        self.assertEqual(self.device.schedule.friday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.friday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.friday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.friday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.friday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.friday.on_range[0].condition[0].state, "true")
        self.assertEqual(self.device.schedule.saturday.date, datetime.date(2016, 12, 17))
        self.assertEqual(len(self.device.schedule.saturday.on_range), 1)
        self.assertEqual(self.device.schedule.saturday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.saturday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.saturday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.saturday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.saturday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.saturday.on_range[0].condition[0].state, "true")
        self.assertEqual(self.device.schedule.sunday.date, datetime.date(2016, 12, 18))
        self.assertEqual(len(self.device.schedule.sunday.on_range), 1)
        self.assertEqual(self.device.schedule.sunday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.sunday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.sunday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.sunday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.sunday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.sunday.on_range[0].condition[0].state, "true")



if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.debug("\n\nStarting log\n")
    unittest.main()     
