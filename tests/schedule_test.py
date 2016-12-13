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



# Define test class *******************************************************************************
class Test_Schedule(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        pass

    def test_class_Condition(self):
        self.logger.debug("[test_class_Condition] Testing initial creation and load")
        self.condition = Condition(andor="and", condition="user1", state="true")
        self.assertEqual(self.condition.andor, "and")
        self.assertEqual(self.condition.condition, "user1")
        self.assertEqual(self.condition.state, "true")
        self.logger.debug("[test_class_Condition] Testing manual minipulation of previously loaded condition attributes")
        self.condition.andor = "or"
        self.condition.condition = "user2"
        self.condition.state = "false"
        self.assertEqual(self.condition.andor, "or")
        self.assertEqual(self.condition.condition, "user2")
        self.assertEqual(self.condition.state, "false")

    def test_class_OnRange(self):
        self.logger.debug("[test_class_OnRange] Setting up tags for testing")
        self.dt = datetime.datetime.now()
        self.on_dtime = self.dt + datetime.timedelta(minutes=-30)
        self.off_dtime = self.dt + datetime.timedelta(minutes=30)
        self.logger.debug("[test_class_OnRange] Testing initial creation and load")
        self.condition = Condition(andor="and", condition="user1", state="true")
        self.onRange = OnRange(on_time=self.on_dtime.time(), off_time=self.off_dtime.time(), condition=self.condition)
        self.assertEqual(self.onRange.on_time, self.on_dtime.time())
        self.assertEqual(self.onRange.off_time, self.off_dtime.time())
        self.assertEqual(len(self.onRange.condition), 1)
        self.assertEqual(self.onRange.condition[0].andor, "and")
        self.assertEqual(self.onRange.condition[0].condition, "user1")
        self.assertEqual(self.onRange.condition[0].state, "true")
        self.logger.debug("[test_class_OnRange] Testing manual minipulation of previously loaded on and off times")
        self.onRange.on_time = self.on_dtime + datetime.timedelta(minutes=10)
        self.onRange.off_time = self.off_dtime + datetime.timedelta(minutes=10)
        self.assertEqual(self.onRange.on_time, (self.on_dtime + datetime.timedelta(minutes=10)).time())
        self.assertEqual(self.onRange.off_time, (self.off_dtime + datetime.timedelta(minutes=10)).time())
        self.onRange.on_time = (self.on_dtime + datetime.timedelta(minutes=9)).time()
        self.onRange.off_time = (self.off_dtime + datetime.timedelta(minutes=9)).time()
        self.assertEqual(self.onRange.on_time, (self.on_dtime + datetime.timedelta(minutes=9)).time())
        self.assertEqual(self.onRange.off_time, (self.off_dtime + datetime.timedelta(minutes=9)).time())
        self.logger.debug("[test_class_OnRange] Testing manual minipulation of previously loaded condition")
        self.onRange.condition = Condition(andor="or", condition="user2", state="false")
        self.assertEqual(len(self.onRange.condition), 1)
        self.assertEqual(self.onRange.condition[0].andor, "or")
        self.assertEqual(self.onRange.condition[0].condition, "user2")
        self.assertEqual(self.onRange.condition[0].state, "false")
        self.onRange.condition = [Condition(andor="and", condition="user1", state="true"), Condition(andor="or", condition="user2", state="false")]
        self.assertEqual(len(self.onRange.condition), 2)
        self.assertEqual(self.onRange.condition[0].andor, "and")
        self.assertEqual(self.onRange.condition[0].condition, "user1")
        self.assertEqual(self.onRange.condition[0].state, "true")
        self.assertEqual(self.onRange.condition[1].andor, "or")
        self.assertEqual(self.onRange.condition[1].condition, "user2")
        self.assertEqual(self.onRange.condition[1].state, "false")
        self.logger.debug("[test_class_OnRange] Testing condition, add, remove, and clear methods")
        self.onRange.add_condition(andor="or", condition="user3", state="true")
        self.assertEqual(len(self.onRange.condition), 3)
        self.assertEqual(self.onRange.condition[0].andor, "and")
        self.assertEqual(self.onRange.condition[0].condition, "user1")
        self.assertEqual(self.onRange.condition[0].state, "true")
        self.assertEqual(self.onRange.condition[1].andor, "or")
        self.assertEqual(self.onRange.condition[1].condition, "user2")
        self.assertEqual(self.onRange.condition[1].state, "false")
        self.assertEqual(self.onRange.condition[2].andor, "or")
        self.assertEqual(self.onRange.condition[2].condition, "user3")
        self.assertEqual(self.onRange.condition[2].state, "true")
        self.onRange.remove_condition(1)
        self.assertEqual(len(self.onRange.condition), 2)
        self.assertEqual(self.onRange.condition[0].andor, "and")
        self.assertEqual(self.onRange.condition[0].condition, "user1")
        self.assertEqual(self.onRange.condition[0].state, "true")
        self.assertEqual(self.onRange.condition[1].andor, "or")
        self.assertEqual(self.onRange.condition[1].condition, "user3")
        self.assertEqual(self.onRange.condition[1].state, "true")
        self.onRange.clear_all_conditions()
        self.assertEqual(len(self.onRange.condition), 0)

    def test_class_Day(self):
        self.logger.debug("[test_class_Day] Setting up tags for testing")
        self.dt = datetime.datetime.now()
        self.on_dtime = self.dt + datetime.timedelta(minutes=-30)
        self.off_dtime = self.dt + datetime.timedelta(minutes=30)
        self.logger.debug("[test_class_Day] Testing initial creation and load")
        self.condition = Condition(andor="and", condition="user1", state="true")
        self.onRange = OnRange(on_time=self.on_dtime.time(), off_time=self.off_dtime.time(), condition=self.condition) 
        self.day = Day(date=datetime.datetime.now().date(), on_range=self.onRange)
        self.assertEqual(len(self.day.on_range), 1)
        self.assertEqual(self.day.on_range[0].on_time, self.on_dtime.time())
        self.assertEqual(self.day.on_range[0].off_time, self.off_dtime.time())
        self.assertEqual(len(self.day.on_range[0].condition), 1)
        self.assertEqual(self.day.on_range[0].condition[0].andor, "and")
        self.assertEqual(self.day.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.day.on_range[0].condition[0].state, "true")
        self.logger.debug("[test_class_Day] Testing manual minipulation of previously loaded on-range values")
        self.day.on_range[0].on_time = self.dt.time()
        self.assertEqual(self.day.on_range[0].on_time, self.dt.time())
        self.day.on_range[0].off_time = self.dt.time()
        self.assertEqual(self.day.on_range[0].off_time, self.dt.time())
        self.day.on_range[0].condition[0].andor = "and"
        self.assertEqual(self.day.on_range[0].condition[0].andor, "and")
        self.day.on_range[0].condition[0].condition = "test2"
        self.assertEqual(self.day.on_range[0].condition[0].condition, "test2")
        self.day.on_range[0].condition[0].state = "True"
        self.assertEqual(self.day.on_range[0].condition[0].state, "true") 
        self.logger.debug("[test_class_Day] Testing adding, deleting, and clearing on-ranges from on-range list")
        self.condition2 = Condition(andor="or", condition="user2", state="false")
        self.day.add_range(on_time=self.dt + datetime.timedelta(seconds=-15), 
                           off_time=self.dt + datetime.timedelta(seconds=15),
                           condition=self.condition2)
        self.assertEqual(len(self.day.on_range), 2)
        self.assertEqual(self.day.on_range[0].on_time, self.dt.time())
        self.assertEqual(self.day.on_range[0].off_time, self.dt.time())
        self.day.on_range[0].condition[0].andor = "and"
        self.assertEqual(self.day.on_range[0].condition[0].andor, "and")
        self.day.on_range[0].condition[0].condition = "test2"
        self.assertEqual(self.day.on_range[0].condition[0].condition, "test2")
        self.day.on_range[0].condition[0].state = "True"
        self.assertEqual(self.day.on_range[0].condition[0].state, "true")
        self.assertEqual(self.day.on_range[1].on_time, (self.dt + datetime.timedelta(seconds=-15)).time())
        self.assertEqual(self.day.on_range[1].off_time, (self.dt + datetime.timedelta(seconds=15)).time())
        self.day.on_range[1].condition[0].andor = "or"
        self.assertEqual(self.day.on_range[1].condition[0].andor, "or")
        self.day.on_range[1].condition[0].condition = "user2"
        self.assertEqual(self.day.on_range[1].condition[0].condition, "user2")
        self.day.on_range[1].condition[0].state = "false"
        self.assertEqual(self.day.on_range[1].condition[0].state, "false")
        self.day.remove_range(0)
        self.assertEqual(len(self.day.on_range), 1)
        self.assertEqual(self.day.on_range[0].on_time, (self.dt + datetime.timedelta(seconds=-15)).time())
        self.assertEqual(self.day.on_range[0].off_time, (self.dt + datetime.timedelta(seconds=15)).time())
        self.day.on_range[0].condition[0].andor = "or"
        self.assertEqual(self.day.on_range[0].condition[0].andor, "or")
        self.day.on_range[0].condition[0].condition = "user2"
        self.assertEqual(self.day.on_range[0].condition[0].condition, "user2")
        self.day.on_range[0].condition[0].state = "false"
        self.assertEqual(self.day.on_range[0].condition[0].state, "false")
        self.day.clear_all_ranges()
        self.assertEqual(len(self.day.on_range),0)

    def print_current_week(self):
        print(str(self.week.monday.on_range[0].on_time) + " - " + str(id(self.week.monday)))
        print(str(self.week.tuesday.on_range[0].on_time) + " - " + str(id(self.week.tuesday)))
        print(str(self.week.wednesday.on_range[0].on_time) + " - " + str(id(self.week.wednesday)))
        print(str(self.week.thursday.on_range[0].on_time) + " - " + str(id(self.week.thursday)))
        print(str(self.week.friday.on_range[0].on_time) + " - " + str(id(self.week.friday)))
        print(str(self.week.saturday.on_range[0].on_time) + " - " + str(id(self.week.saturday)))
        print(str(self.week.sunday.on_range[0].on_time) + " - " + str(id(self.week.sunday)))        

    def test_class_Week(self):
        self.logger.debug("[test_class_Week] Setting up tags for testing")
        self.dt = datetime.datetime.now()
        self.logger.debug("[test_class_Week] Testing initial creation and load") 
        self.week = Week(monday=Day(date=datetime.date(2016,12,12),
                                    on_range=OnRange(on_time=datetime.time(12, 0),
                                                     off_time=datetime.time(14, 0),
                                                     condition=Condition(andor="and",
                                                                         condition="user1",
                                                                         state="true"))),
                         tuesday=Day(date=datetime.date(2016,12,12),
                                     on_range=OnRange(on_time=datetime.time(12, 0),
                                                      off_time=datetime.time(14, 0),
                                                      condition=Condition(andor="and",
                                                                          condition="user1",
                                                                          state="true"))),
                         wednesday=Day(date=datetime.date(2016,12,12),
                                       on_range=OnRange(on_time=datetime.time(12, 0),
                                                        off_time=datetime.time(14, 0),
                                                        condition=Condition(andor="and",
                                                                            condition="user1",
                                                                            state="true"))),
                         thursday=Day(date=datetime.date(2016,12,12),
                                      on_range=OnRange(on_time=datetime.time(12, 0),
                                                       off_time=datetime.time(14, 0),
                                                       condition=Condition(andor="and",
                                                                           condition="user1",
                                                                           state="true"))),
                         friday=Day(date=datetime.date(2016,12,12),
                                    on_range=OnRange(on_time=datetime.time(12, 0),
                                                     off_time=datetime.time(14, 0),
                                                     condition=Condition(andor="and",
                                                                         condition="user1",
                                                                         state="true"))),
                         saturday=Day(date=datetime.date(2016,12,12),
                                      on_range=OnRange(on_time=datetime.time(12, 0),
                                                       off_time=datetime.time(14, 0),
                                                       condition=Condition(andor="and",
                                                                           condition="user1",
                                                                           state="true"))),
                         sunday=Day(date=datetime.date(2016,12,12),
                                    on_range=OnRange(on_time=datetime.time(12, 0),
                                                     off_time=datetime.time(14, 0),
                                                     condition=Condition(andor="and",
                                                                         condition="user1",
                                                                         state="true"))))
        self.assertEqual(len(self.week.monday.on_range), 1)
        self.assertEqual(len(self.week.monday.on_range[0].condition), 1)
        self.assertEqual(self.week.monday.on_range[0].on_time, datetime.time(12,0))
        self.assertEqual(self.week.monday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.week.tuesday.on_range), 1)
        self.assertEqual(len(self.week.tuesday.on_range[0].condition), 1)
        self.assertEqual(self.week.tuesday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.tuesday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.wednesday.on_range), 1)
        self.assertEqual(len(self.week.wednesday.on_range[0].condition), 1)
        self.assertEqual(self.week.wednesday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.wednesday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.week.thursday.on_range), 1)
        self.assertEqual(len(self.week.thursday.on_range[0].condition), 1)
        self.assertEqual(self.week.thursday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.thursday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.friday.on_range), 1)
        self.assertEqual(len(self.week.friday.on_range[0].condition), 1)
        self.assertEqual(self.week.friday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.friday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.saturday.on_range), 1)
        self.assertEqual(len(self.week.saturday.on_range[0].condition), 1)
        self.assertEqual(self.week.saturday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.saturday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.sunday.on_range), 1)
        self.assertEqual(len(self.week.sunday.on_range[0].condition), 1)
        self.assertEqual(self.week.sunday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.sunday.on_range[0].off_time, datetime.time(14, 0))

        self.week.tuesday.on_range[0].on_time = datetime.time(11,0)
        self.assertEqual(len(self.week.monday.on_range), 1)
        self.assertEqual(len(self.week.monday.on_range[0].condition), 1)
        self.assertEqual(self.week.monday.on_range[0].on_time, datetime.time(12,0))
        self.assertEqual(self.week.monday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.week.tuesday.on_range), 1)
        self.assertEqual(len(self.week.tuesday.on_range[0].condition), 1)
        self.assertEqual(self.week.tuesday.on_range[0].on_time, datetime.time(11, 0))
        self.assertEqual(self.week.tuesday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.wednesday.on_range), 1)
        self.assertEqual(len(self.week.wednesday.on_range[0].condition), 1)
        self.assertEqual(self.week.wednesday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.wednesday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.week.thursday.on_range), 1)
        self.assertEqual(len(self.week.thursday.on_range[0].condition), 1)
        self.assertEqual(self.week.thursday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.thursday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.friday.on_range), 1)
        self.assertEqual(len(self.week.friday.on_range[0].condition), 1)
        self.assertEqual(self.week.friday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.friday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.saturday.on_range), 1)
        self.assertEqual(len(self.week.saturday.on_range[0].condition), 1)
        self.assertEqual(self.week.saturday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.saturday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.sunday.on_range), 1)
        self.assertEqual(len(self.week.sunday.on_range[0].condition), 1)
        self.assertEqual(self.week.sunday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.sunday.on_range[0].off_time, datetime.time(14, 0))

        self.week.saturday = Day(date=datetime.date(2016,12,17), on_range=OnRange(on_time=datetime.time(10,0), off_time=datetime.time(22,0), condition=Condition(andor="or", condition="user2", state="false")))
        self.assertEqual(len(self.week.monday.on_range), 1)
        self.assertEqual(len(self.week.monday.on_range[0].condition), 1)
        self.assertEqual(self.week.monday.on_range[0].on_time, datetime.time(12,0))
        self.assertEqual(self.week.monday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.week.tuesday.on_range), 1)
        self.assertEqual(len(self.week.tuesday.on_range[0].condition), 1)
        self.assertEqual(self.week.tuesday.on_range[0].on_time, datetime.time(11, 0))
        self.assertEqual(self.week.tuesday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.wednesday.on_range), 1)
        self.assertEqual(len(self.week.wednesday.on_range[0].condition), 1)
        self.assertEqual(self.week.wednesday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.wednesday.on_range[0].off_time, datetime.time(14, 0))
        self.assertEqual(len(self.week.thursday.on_range), 1)
        self.assertEqual(len(self.week.thursday.on_range[0].condition), 1)
        self.assertEqual(self.week.thursday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.thursday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.friday.on_range), 1)
        self.assertEqual(len(self.week.friday.on_range[0].condition), 1)
        self.assertEqual(self.week.friday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.friday.on_range[0].off_time, datetime.time(14, 0))        
        self.assertEqual(len(self.week.saturday.on_range), 1)
        self.assertEqual(len(self.week.saturday.on_range[0].condition), 1)
        self.assertEqual(self.week.saturday.on_range[0].on_time, datetime.time(10, 0))
        self.assertEqual(self.week.saturday.on_range[0].off_time, datetime.time(22, 0))        
        self.assertEqual(len(self.week.sunday.on_range), 1)
        self.assertEqual(len(self.week.sunday.on_range[0].condition), 1)
        self.assertEqual(self.week.sunday.on_range[0].on_time, datetime.time(12, 0))
        self.assertEqual(self.week.sunday.on_range[0].off_time, datetime.time(14, 0)) 
                          





if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.debug("\n\nStarting log\n")
    unittest.main()
