from unittest import TestCase
import datetime
import multiprocessing
from rpihome.modules.sun import Sun
from rpihome.modules.dst import USdst
from rpihome.rules.device_wemo_fylt1 import Wemo_fylt1


class Test_wemo_fylt1(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)          
        self.device = Wemo_fylt1("fylt1", "192.168.86.21", self.testQueue)
        self.utcOffset = datetime.timedelta(hours=0)         
        self.dst = USdst()

    def test_wemo_fylt1(self):
        self.testData = []
        # Before DST begins (sunrise around 6:34 am on 3/1)
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,30)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(6,40)), False))        
        # After DST begins (sunrise around 7:14 am on 3/15)
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,15), datetime.time(7,10)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,15), datetime.time(7,20)), False))        
        # Before DST ends (sunrise around 7:26am on 10/31)
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,20)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,30)), False))        
        # After DST ends (sunrise around 6:42 am on 11/15)
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,15), datetime.time(6,40)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,15), datetime.time(6,50)), False))        

        # Before DST begins (sunset around 5:53 pm on 3/1)
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(17,50)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(18,0)), True))
        # After DST begins (sunset around 7:07 pm on 3/15)  
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,15), datetime.time(19,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,15), datetime.time(19,10)), True))        
        # Before DST ends (sunset around 6:04 pm on 10/31)  
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(18,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(18,10)), True))
        # After DST ends (sunset around 4:49 pm on 11/15)                                  
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,15), datetime.time(16,40)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,15), datetime.time(16,50)), True))

        # Perform tests with data set
        for index, data in enumerate(self.testData):
            # Calculate if DST is active or not
            if self.dst.is_active(datetime=data[0]) is True:
                self.utcOffset = datetime.timedelta(hours=-5)
            else:
                self.utcOffset = datetime.timedelta(hours=-6)
            # Check rules
            self.device.check_rules(datetime=data[0], utcOffset=self.utcOffset, sunriseOffset=datetime.timedelta(minutes=0), sunsetOffset=datetime.timedelta(minutes=0))
            if self.device.state != data[1]:
                print("\n\nError\nDateTime: [%s]\nExpected State: [%s]\nActual State: [%s]\nutcOffset: [%s]" % (data[0], data[1], self.device.state, self.utcOffset))            
            self.assertEqual(self.device.state, data[1])
            