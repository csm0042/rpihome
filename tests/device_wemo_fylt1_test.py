from unittest import TestCase
import datetime
import multiprocessing
from rpihome.modules.sun import Sun
from rpihome.rules.device_wemo_fylt1 import Wemo_fylt1


class Test_wemo_fylt1(TestCase):
    def setUp(self):
        self.s = Sun(lat=38.566, long=-90.409)
        self.utcOffset = datetime.timedelta(hours=-5)
        self.testQueue = multiprocessing.Queue(-1)    
        self.device = Wemo_fylt1("fylt1", self.testQueue)

    def test_before_sunrise(self):
        self.sunrise_time = self.s.sunrise(datetime.datetime.now(), self.utcOffset)
        self.sunrise = datetime.datetime.combine(datetime.datetime.today().date(), self.sunrise_time)
        self.test_time = datetime.datetime.combine(datetime.datetime.today().date(), datetime.time(5,0))       
        self.device.check_rules(datetime=self.test_time, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))
        self.assertEqual(self.device.state, True)

    def test_just_after_sunrise(self):
        self.sunrise_time = self.s.sunrise(datetime.datetime.now(), self.utcOffset)
        self.sunrise = datetime.datetime.combine(datetime.datetime.today().date(), self.sunrise_time)
        self.test_time = datetime.datetime.combine(datetime.datetime.today().date(), datetime.time(7,45))      
        self.device.check_rules(datetime=self.test_time, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))      
        self.assertEqual(self.device.state, False) 

    def test_just_before_sunset(self):
        self.sunset_time = self.s.sunset(datetime.datetime.now(), self.utcOffset)
        self.sunset = datetime.datetime.combine(datetime.datetime.today().date(), self.sunset_time)
        self.test_time = datetime.datetime.combine(datetime.datetime.today().date(), datetime.time(17,30))
        self.device.check_rules(datetime=self.test_time, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0)) 
        self.assertEqual(self.device.state, False)        

    def test_after_sunset(self):
        self.sunset_time = self.s.sunset(datetime.datetime.now(), self.utcOffset)
        self.sunset = datetime.datetime.combine(datetime.datetime.today().date(), self.sunset_time)
        self.test_time = datetime.datetime.combine(datetime.datetime.today().date(), datetime.time(18,30))               
        self.device.check_rules(datetime=self.test_time, utcOffset=datetime.timedelta(hours=-5), sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))      
        self.assertEqual(self.device.state, True) 