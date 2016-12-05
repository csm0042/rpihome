import datetime
import unittest
import sys

if __name__ == "__main__": sys.path.append("..")
from rpihome.modules.schedule import Condition, OnRange, Day, Week


class Test_Schedule(unittest.TestCase):
    def setUp(self):
        self.condition = Condition()
        self.on_range = OnRange()
        self.week = Week()

    def test_schedule_condition(self):
        self.condition = Condition(condition="user1", state="true")
        self.assertEqual(self.condition.condition, "user1")
        self.assertEqual(self.condition.state, "true")

    def test_schedule_on_range(self):
        self.condition = [Condition(condition="user1", state="true")]
        self.on_range = [OnRange(ontime=datetime.time(7,30), offtime=datetime.time(7,45), condition=self.condition)]
        self.assertEqual(self.on_range[0].on_time, datetime.time(7,30))
        self.assertEqual(self.on_range[0].off_time, datetime.time(7,45))
        self.assertEqual(self.on_range[0].condition[0].condition, "user1")
        self.assertEqual(self.on_range[0].condition[0].state, "true")
        self.assertEqual(len(self.on_range[0].condition), 1)

    def test_schedule_day(self):
        self.condition1_1 = Condition(condition="user1", state="true")
        self.condition1_2 = Condition(condition="user2", state="false")
        self.condition1_3 = Condition(condition="user3", state="false")
        self.cond_array1 = [self.condition1_1, self.condition1_2, self.condition1_3]
        self.on_range1 = OnRange(ontime=datetime.time(6,30), offtime=datetime.time(7,0), condition=self.cond_array1)
        self.condition2_1 = Condition(condition="user1", state="true")
        self.condition2_2 = Condition(condition="user2", state="true")
        self.condition2_3 = Condition(condition="user3", state="false")
        self.cond_array2 = [self.condition2_1, self.condition2_2, self.condition2_3]
        self.on_range2 = OnRange(ontime=datetime.time(6,30), offtime=datetime.time(7,0), condition=self.cond_array2)
        self.condition3_1 = Condition(condition="user1", state="true")
        self.condition3_2 = Condition(condition="user2", state="false")
        self.condition3_3 = Condition(condition="user3", state="true")                
        self.cond_array3 = [self.condition3_1, self.condition3_2, self.condition3_3]
        self.on_range3 = OnRange(ontime=datetime.time(6,30), offtime=datetime.time(7,0), condition=self.cond_array3)
        self.on_range_array = [self.on_range1, self.on_range2, self.on_range3]
        self.day = Day(date=datetime.date(2016,12,5), onrange=self.on_range_array)

        self.assertEqual(len(self.day.on_range), 3)
        self.assertEqual(len(self.day.on_range[0].condition), 3)

        
if __name__ == "__main__":
    unittest.main()