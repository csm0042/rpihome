from unittest import TestCase
import datetime
from rpihome.modules.dst import USdst


class Test_USdst(TestCase):
    def setUp(self):
        self.dst = USdst() 

    def test_dst_calculation(self):
        self.testData = []
        # Using 2016 data
        self.testData.append((datetime.datetime.combine(datetime.date(2016,1,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,2,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,12), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,13), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,13), datetime.time(3,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,3,14), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,4,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,5,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,6,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,7,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,8,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,9,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,5), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,6), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,6), datetime.time(3,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,11,7), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,12,1), datetime.time(1,0)), False))  
        # Using 2017 data
        self.testData.append((datetime.datetime.combine(datetime.date(2017,1,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,2,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,3,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,3,11), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,3,12), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,3,12), datetime.time(3,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,3,13), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,4,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,5,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,6,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,7,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,8,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,9,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,10,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,11,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,11,4), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,11,5), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,11,5), datetime.time(3,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,11,6), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2017,12,1), datetime.time(1,0)), False)) 
        # Using 2018 data
        self.testData.append((datetime.datetime.combine(datetime.date(2018,1,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,2,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,3,1), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,3,10), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,3,11), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,3,11), datetime.time(3,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,3,12), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,4,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,5,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,6,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,7,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,8,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,9,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,10,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,11,1), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,11,3), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,11,4), datetime.time(1,0)), True))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,11,4), datetime.time(3,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,11,5), datetime.time(1,0)), False))
        self.testData.append((datetime.datetime.combine(datetime.date(2018,12,1), datetime.time(1,0)), False))                                                  

        for index, data in enumerate(self.testData):
            self.assertEqual(self.dst.is_active(datetime=data[0]), data[1])