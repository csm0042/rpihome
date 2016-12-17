#!/usr/bin/python3
""" device_auto_test.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
import multiprocessing
import sys
import unittest
if __name__ == "__main__": sys.path.append("..")
from rpihome.devices.device_auto import DeviceAuto
from rpihome.modules.schedule import Day, Week, OnRange, Condition
from rpihome.modules.sun import Sun


# Define test class *******************************************************************************
class TestDevice(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.testQueue = multiprocessing.Queue(-1)            
        self.device = DeviceAuto("test-name", self.testQueue)

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
        self.device.homeArray = [True, False, True, False]
        self.assertIsInstance(self.device.homeArray, list)
        self.assertIsInstance(self.device.homeArray[0], bool)
        self.assertEqual(self.device.homeArray[0], True)
        self.assertIsInstance(self.device.homeArray[1], bool)
        self.assertEqual(self.device.homeArray[1], False)
        self.assertIsInstance(self.device.homeArray[2], bool)
        self.assertEqual(self.device.homeArray[2], True)
        self.assertIsInstance(self.device.homeArray[3], bool)
        self.assertEqual(self.device.homeArray[3], False)

    def test_homeTime(self):
        self.device.homeTime = [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()]
        self.assertIsInstance(self.device.homeTime, list)
        self.assertIsInstance(self.device.homeTime[0], datetime.datetime)
        self.assertIsInstance(self.device.homeTime[1], datetime.datetime)
        self.assertIsInstance(self.device.homeTime[2], datetime.datetime)
        self.assertIsInstance(self.device.homeTime[3], datetime.datetime)
        self.assertAlmostEqual(self.device.homeTime[0], datetime.datetime.now())
        self.assertAlmostEqual(self.device.homeTime[1], datetime.datetime.now())
        self.assertAlmostEqual(self.device.homeTime[2], datetime.datetime.now())
        self.assertAlmostEqual(self.device.homeTime[3], datetime.datetime.now())

    def test_dt(self):
        self.dt = datetime.datetime.now()
        self.device.dt = self.dt
        self.assertIsInstance(self.device.dt, datetime.datetime)
        self.assertEqual(self.device.dt, self.dt)

    def test_utcOffset(self):
        self.device.utcOffset = datetime.timedelta(hours=-6)
        self.assertIsInstance(self.device.utcOffset, datetime.timedelta)
        self.assertEqual(self.device.utcOffset, datetime.timedelta(hours=-6))

    def test_sunriseOffset(self):
        self.device.sunriseOffset = datetime.timedelta(hours=-6)
        self.assertIsInstance(self.device.sunriseOffset, datetime.timedelta)
        self.assertEqual(self.device.sunriseOffset, datetime.timedelta(hours=-6))

    def test_sunsetOffset(self):
        self.device.sunsetOffset = datetime.timedelta(hours=-4)
        self.assertIsInstance(self.device.sunsetOffset, datetime.timedelta)
        self.assertEqual(self.device.sunsetOffset, datetime.timedelta(hours=-4))

    def test_timeout(self):
        self.device.timeout = datetime.timedelta(minutes=15)
        self.assertIsInstance(self.device.timeout, datetime.timedelta)
        self.assertEqual(self.device.timeout, datetime.timedelta(minutes=15))

    def test_result(self):
        self.device.result = 3
        self.assertIsInstance(self.device.result, int)
        self.assertEqual(self.device.result, 3)


    def load_schedule(self):
        self.device.schedule = Week(
            monday=Day(
                date=datetime.date(2016,12,12),
                on_range=[OnRange(
                    on_time=datetime.time(12, 0),
                    off_time=datetime.time(14, 0),
                    condition=[Condition(andor="and", condition="user1", state="true"), 
                               Condition(andor="or", condition="user2", state="true"),
                               Condition(andor="or", condition="user3", state="true")]),
                          OnRange(
                    on_time=datetime.time(16, 0),
                    off_time=datetime.time(18, 0),
                    condition=[Condition(andor="and", condition="user1", state="true"), 
                               Condition(andor="and", condition="user2", state="false"),
                               Condition(andor="and", condition="user3", state="false")])]),
            tuesday=Day(
                date=datetime.date(2016,12,13),
                on_range=OnRange(
                    on_time=datetime.time(12, 0),
                    off_time=datetime.time(14, 0),
                    condition=Condition(andor="and", condition="user1", state="true"))),
            wednesday=Day(
                date=datetime.date(2016,12,14),
                on_range=OnRange(
                    on_time=datetime.time(12, 0),
                    off_time=datetime.time(14, 0),
                    condition=Condition(andor="and", condition="user1", state="true"))),
            thursday=Day(
                date=datetime.date(2016,12,15),
                on_range=OnRange(
                    on_time=datetime.time(12, 0),
                    off_time=datetime.time(14, 0),
                    condition=Condition(andor="and", condition="user1", state="true"))),
            friday=Day(
                date=datetime.date(2016,12,16),
                on_range=OnRange(
                    on_time=datetime.time(12, 0),
                    off_time=datetime.time(14, 0),
                    condition=Condition(andor="and", condition="user1", state="true"))),
            saturday=Day(
                date=datetime.date(2016,12,17),
                on_range=OnRange(
                    on_time=datetime.time(12, 0),
                    off_time=datetime.time(14, 0),
                    condition=Condition(andor="and", condition="user1", state="true"))),
            sunday=Day(
                date=datetime.date(2016,12,18),
                on_range=OnRange(
                    on_time=self.sun.sunrise(
                        when=datetime.date(2016,12,18), 
                        offset=datetime.timedelta(hours=-6)),
                    off_time=self.sun.sunset(
                        when=datetime.date(2016,12,18), 
                        offset=datetime.timedelta(hours=-6)),
                    condition=Condition(andor="and", condition="user1", state="true"))))


    def test_schedule(self):
        self.sun = Sun()
        self.load_schedule()
        self.assertEqual(self.device.schedule.monday.date, datetime.date(2016, 12, 12))
        self.assertEqual(len(self.device.schedule.monday.on_range), 2)
        self.assertEqual(self.device.schedule.monday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.device.schedule.monday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.device.schedule.monday.on_range[0].condition), 3)
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[0].state, "true")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[1].andor, "or")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[1].condition, "user2")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[1].state, "true")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[2].andor, "or")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[2].condition, "user3")
        self.assertEqual(self.device.schedule.monday.on_range[0].condition[2].state, "true")
        self.assertEqual(self.device.schedule.monday.on_range[1].on_time, datetime.time(16, 0))
        self.assertEqual(self.device.schedule.monday.on_range[1].off_time, datetime.time(18, 0))
        self.assertEqual(len(self.device.schedule.monday.on_range[1].condition), 3)
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[0].state, "true")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[1].andor, "and")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[1].condition, "user2")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[1].state, "false")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[2].andor, "and")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[2].condition, "user3")
        self.assertEqual(self.device.schedule.monday.on_range[1].condition[2].state, "false")                     
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
        self.assertEqual(self.device.schedule.sunday.on_range[0].on_time, self.sun.sunrise(when=datetime.date(2016,12,18), offset=datetime.timedelta(hours=-6)))
        self.assertEqual(self.device.schedule.sunday.on_range[0].off_time, self.sun.sunset(when=datetime.date(2016,12,18), offset=datetime.timedelta(hours=-6)))
        self.assertEqual(len(self.device.schedule.sunday.on_range[0].condition), 1)
        self.assertEqual(self.device.schedule.sunday.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.device.schedule.sunday.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.device.schedule.sunday.on_range[0].condition[0].state, "true")


    def test_eval_user(self):
        self.sun = Sun()
        self.load_schedule()
        self.homeArray = [False, True, True, True]
        self.result = self.device.eval_user(self.device.schedule.monday.on_range[0].condition[0], self.homeArray[0])
        self.assertEqual(self.result, ("and", False))
        self.result = self.device.eval_user(self.device.schedule.monday.on_range[0].condition[1], self.homeArray[2])
        self.assertEqual(self.result, ("or", True))


    def test_eval_conditions(self):
        self.sun = Sun()
        self.load_schedule()
        self.device.homeArray = [True, True, True, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [False, True, True, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [True, True, False, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)  
        self.device.homeArray = [True, True, True, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [True, True, False, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [False, True, True, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [False, True, False, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [False, True, False, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), False)
        self.device.schedule.monday.on_range[0].condition[1].andor="and"
        self.device.homeArray = [True, True, True, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [True, True, False, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), True)
        self.device.homeArray = [True, True, False, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[0].condition), False)
        # 2nd on-range
        self.device.homeArray = [True, True, True, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), False)
        self.device.homeArray = [False, True, True, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), False)
        self.device.homeArray = [True, True, False, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), False)  
        self.device.homeArray = [True, True, True, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), False)
        self.device.homeArray = [True, True, False, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), True)
        self.device.homeArray = [False, True, True, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), False)
        self.device.homeArray = [False, True, False, True]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), False)
        self.device.homeArray = [False, True, False, False]
        self.assertEqual(self.device.eval_conditions(self.device.schedule.monday.on_range[1].condition), False)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.debug("\n\nStarting log\n")
    unittest.main()