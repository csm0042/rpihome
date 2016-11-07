from unittest import TestCase
import datetime
import multiprocessing
from rpihome.modules.sun import Sun
from rpihome.modules.dst import USdst
from rpihome.rules.device_wemo_ewlt1 import Wemo_ewlt1


class Test_wemo_ewlt1(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)          
        self.device = Wemo_ewlt1("ewlt1", "192.168.86.23", self.testQueue)
        self.utcOffset = datetime.timedelta(hours=0)         
        self.dst = USdst()


    def test_wemo_ewlt1_user1_before_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,25)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, True)


    def test_wemo_ewlt1_user1_before_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user1_after_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,40)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user1_after_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user1_before_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,47)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user1_before_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)    


    def test_wemo_ewlt1_user1_after_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,58))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, True)


    def test_wemo_ewlt1_user1_after_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,59))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [True, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)       


    def test_wemo_ewlt1_user2_before_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,25)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,28)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,28))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, True)


    def test_wemo_ewlt1_user2_before_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user2_after_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,40)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,44)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,44))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user2_after_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user2_before_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,47)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,48)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,48))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user2_before_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,5)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)    


    def test_wemo_ewlt1_user2_after_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,58))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,57)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,57))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, True)


    def test_wemo_ewlt1_user2_after_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,59))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, True, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)  


    def test_wemo_ewlt1_user3_before_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,25)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,27)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,27))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, True)


    def test_wemo_ewlt1_user3_before_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user3_after_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,40)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,44))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user3_after_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user3_before_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,47)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,48))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_user3_before_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)    


    def test_wemo_ewlt1_user3_after_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,58))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,50))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, True)


    def test_wemo_ewlt1_user3_after_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,59))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, True]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)     


    def test_wemo_ewlt1_none_before_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,25)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_none_before_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_none_after_sunrise_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,40)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_none_after_sunrise_not_home_recently(self):
        """ (sunrise around 6:34 am on 3/1) """  
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,45))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_none_before_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,47)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_none_before_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,49))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)    


    def test_wemo_ewlt1_none_after_sunset_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,58))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)


    def test_wemo_ewlt1_none_after_sunset_not_home_recently(self):
        """ (sunset around 5:53 pm on 3/1) """
        self.dt = datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,59))
        self.sunriseOffset = datetime.timedelta(minutes=0)
        self.sunsetOffset = datetime.timedelta(minutes=0)
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,51)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(14,18)), 
                         datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(15,5))]
        # Calculate if DST is active or not
        if self.dst.is_active(datetime=self.dt) is True:
            self.utcOffset = datetime.timedelta(hours=-5)
        else:
            self.utcOffset = datetime.timedelta(hours=-6)
        # Update device state based on input conditions
        self.device.check_rules(datetime=self.dt, utcOffset=self.utcOffset, sunriseOffset=self.sunriseOffset, sunsetOffset=self.sunsetOffset, homeArray=self.homeArray, homeTime=self.homeTime)
        # Perform check
        self.assertEqual(self.device.state, False)                               