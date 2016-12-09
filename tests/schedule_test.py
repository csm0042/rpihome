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
from rpihome.modules.schedule import Condition, OnRange, Day, Week, GoogleSheetsSchedule, GoogleSheetToSched
from rpihome.devices.device import Device


# Define test class *******************************************************************************
class Test_Schedule(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        self.schedule = Week()
        self.logger.debug("Finished running setup")


    def test_data_structure_before_load(self):
        self.logger.debug("Testing structure of data object immediately after creation")
        self.assertEqual(len(self.schedule.day), 7)
        self.assertEqual(len(self.schedule.day[0].range), 0)
        self.assertEqual(len(self.schedule.monday.range), 0)
        self.assertEqual(len(self.schedule.day[1].range), 0)
        self.assertEqual(len(self.schedule.tuesday.range), 0)
        self.assertEqual(len(self.schedule.day[2].range), 0)
        self.assertEqual(len(self.schedule.wednesday.range), 0)
        self.assertEqual(len(self.schedule.day[3].range), 0)
        self.assertEqual(len(self.schedule.thursday.range), 0) 
        self.assertEqual(len(self.schedule.day[4].range), 0)
        self.assertEqual(len(self.schedule.friday.range), 0)
        self.assertEqual(len(self.schedule.day[5].range), 0)
        self.assertEqual(len(self.schedule.saturday.range), 0)
        self.assertEqual(len(self.schedule.day[6].range), 0)
        self.assertEqual(len(self.schedule.sunday.range), 0)


    def test_range_load(self):
        self.logger.debug("Testing loading of a single range to a single day")
        self.schedule.monday.add_range(on_time=datetime.time(5, 40), off_time=datetime.time(6, 30))
        self.assertEqual(len(self.schedule.day[0].range), 1)
        self.assertEqual(len(self.schedule.monday.range), 1)
        self.assertEqual(len(self.schedule.monday.range[0].condition), 0)
        self.assertEqual(self.schedule.monday.range[0].on_time, datetime.time(5, 40))
        self.assertEqual(self.schedule.monday.range[0].off_time, datetime.time(6, 30))


    def test_condition_load(self):
        self.logger.debug("Testing the addition of a condition to a single day's single on-range")
        self.schedule.monday.add_range(on_time=datetime.time(5, 40), off_time=datetime.time(6, 30))
        self.schedule.monday.range[0].add_condition(condition="user1", state="true")
        self.assertEqual(len(self.schedule.day[0].range), 1)
        self.assertEqual(len(self.schedule.monday.range), 1)
        self.assertEqual(len(self.schedule.monday.range[0].condition), 1)
        self.assertEqual(self.schedule.monday.range[0].on_time, datetime.time(5, 40))
        self.assertEqual(self.schedule.monday.range[0].off_time, datetime.time(6, 30))
        self.assertEqual(self.schedule.monday.range[0].condition[0].condition, "user1")
        self.assertEqual(self.schedule.monday.range[0].condition[0].state, "true")


    def test_load_multiple_ranges_single_day(self):
        self.logger.debug("Testing data loading multiple ranges for a single day")
        self.schedule.monday.add_range(on_time=datetime.time(5, 40), off_time=datetime.time(6, 30))
        self.schedule.monday.range[0].add_condition(andor="and", condition="user1", state="true")
        self.schedule.monday.range[0].add_condition(andor="and", condition="user2", state="true")
        self.schedule.monday.range[0].add_condition(andor="or", condition="user3", state="true")
        self.schedule.monday.add_range(on_time=datetime.time(6, 30), off_time=datetime.time(7, 0))
        self.schedule.monday.range[1].add_condition(andor="and", condition="user1", state="true")
        self.schedule.monday.range[1].add_condition(andor="and", condition="user2", state="false")
        self.schedule.monday.range[1].add_condition(andor="and", condition="user3", state="false")
        self.assertEqual(len(self.schedule.monday.range), 2)
        self.assertEqual(len(self.schedule.monday.range[0].condition), 3)
        self.assertEqual(len(self.schedule.monday.range[1].condition), 3)
        self.assertEqual(self.schedule.monday.range[0].on_time, datetime.time(5, 40))
        self.assertEqual(self.schedule.monday.range[0].off_time, datetime.time(6, 30))
        self.assertEqual(self.schedule.monday.range[1].on_time, datetime.time(6, 30))
        self.assertEqual(self.schedule.monday.range[1].off_time, datetime.time(7, 0))


    def test_complex_load_single_day(self):
        self.logger.debug("testing complex loading of on/off range data with conditions for a single day")
        self.schedule.monday.date = datetime.date(2016, 12, 5)
        self.schedule.monday.add_range_with_conditions(on_time=datetime.time(5, 40),
                                                       off_time=datetime.time(6, 30),
                                                       conditions=[("and", "user1", "true"),
                                                                   ("and", "user2", "true"),
                                                                   ("or", "user3", "true")])
        self.schedule.monday.add_range_with_conditions(on_time=datetime.time(6, 30),
                                                       off_time=datetime.time(7, 0),
                                                       conditions=[("and", "user1", "true"),
                                                                   ("and", "user2", "false"),
                                                                   ("and", "user3", "false")])
        self.assertEqual(self.schedule.monday.date, datetime.date(2016, 12, 5))
        self.assertEqual(len(self.schedule.monday.range), 2)
        self.assertEqual(len(self.schedule.monday.range[0].condition), 3)
        self.assertEqual(len(self.schedule.monday.range[1].condition), 3)
        self.assertEqual(self.schedule.monday.range[0].on_time, datetime.time(5, 40))
        self.assertEqual(self.schedule.monday.range[0].off_time, datetime.time(6, 30))
        self.assertEqual(self.schedule.monday.range[0].condition[0].andor, "and")
        self.assertEqual(self.schedule.monday.range[0].condition[0].condition, "user1")
        self.assertEqual(self.schedule.monday.range[0].condition[0].state, "true")
        self.assertEqual(self.schedule.monday.range[0].condition[1].andor, "and")
        self.assertEqual(self.schedule.monday.range[0].condition[1].condition, "user2")
        self.assertEqual(self.schedule.monday.range[0].condition[1].state, "true")
        self.assertEqual(self.schedule.monday.range[0].condition[2].andor, "or")
        self.assertEqual(self.schedule.monday.range[0].condition[2].condition, "user3")
        self.assertEqual(self.schedule.monday.range[0].condition[2].state, "true")                
        self.assertEqual(self.schedule.monday.range[1].on_time, datetime.time(6, 30))
        self.assertEqual(self.schedule.monday.range[1].off_time, datetime.time(7, 0))
        self.assertEqual(self.schedule.monday.range[1].condition[0].andor, "and")
        self.assertEqual(self.schedule.monday.range[1].condition[0].condition, "user1")
        self.assertEqual(self.schedule.monday.range[1].condition[0].state, "true")
        self.assertEqual(self.schedule.monday.range[1].condition[1].andor, "and")
        self.assertEqual(self.schedule.monday.range[1].condition[1].condition, "user2")
        self.assertEqual(self.schedule.monday.range[1].condition[1].state, "false")
        self.assertEqual(self.schedule.monday.range[1].condition[2].andor, "and")
        self.assertEqual(self.schedule.monday.range[1].condition[2].condition, "user3")
        self.assertEqual(self.schedule.monday.range[1].condition[2].state, "false")


    def test_google_sheets_read(self):
        self.google_sheets_reader = GoogleSheetsSchedule()
        self.records = self.google_sheets_reader.read_data()
        self.schedule_builder = GoogleSheetToSched(self.logger)
        self.schedule_builder.main(self.records)

            


        
        


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.debug("\n\nStarting log\n")
    unittest.main()
