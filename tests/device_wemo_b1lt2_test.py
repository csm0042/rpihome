from unittest import TestCase
import datetime
import multiprocessing
from rpihome.rules.device_wemo_b1lt2 import Wemo_b1lt2


class Test_wemo_b1lt2(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)    
        self.device = Wemo_b1lt2("b1lt2", self.testQueue)

    def test_monday_no_kids_before_alarm(self):
        self.test_date = datetime.date(2016, 10, 24)
        self.test_time = datetime.time(6,19)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, False, False]))
        self.assertEqual(self.device.state, False)    

    def test_monday_no_kids_after_alarm(self):
        self.test_date = datetime.date(2016, 10, 24)
        self.test_time = datetime.time(6,21)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, False, False]))
        self.assertEqual(self.device.state, True)  

    def test_monday_no_kids_before_leave(self):
        self.test_date = datetime.date(2016, 10, 24)
        self.test_time = datetime.time(7,9)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, False, False]))
        self.assertEqual(self.device.state, True)

    def test_monday_no_kids_after_leave(self):
        self.test_date = datetime.date(2016, 10, 24)
        self.test_time = datetime.time(7,11)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, False, False]))
        self.assertEqual(self.device.state, False)     

    def test_monday_yes_kids_before_alarm(self):
        self.test_date = datetime.date(2016, 10, 31)
        self.test_time = datetime.time(5,39)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, True, False]))
        self.assertEqual(self.device.state, False)    

    def test_monday_yes_kids_after_alarm(self):
        self.test_date = datetime.date(2016, 10, 31)
        self.test_time = datetime.time(5,41)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, True, False]))
        self.assertEqual(self.device.state, True)  

    def test_monday_yes_kids_before_leave(self):
        self.test_date = datetime.date(2016, 10, 31)
        self.test_time = datetime.time(6,39)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, True, False]))
        self.assertEqual(self.device.state, True)

    def test_monday_yes_kids_after_leave(self):
        self.test_date = datetime.date(2016, 10, 31)
        self.test_time = datetime.time(6,41)
        self.test_datetime = datetime.datetime.combine(self.test_date, self.test_time) 
        self.device.check_rules(datetime=self.test_datetime, homeArray=([True, True, False]))
        self.assertEqual(self.device.state, False)                       
