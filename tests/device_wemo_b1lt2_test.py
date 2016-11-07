from unittest import TestCase
import datetime
import multiprocessing
from rpihome.rules.device_wemo_b1lt2 import Wemo_b1lt2


class Test_wemo_b1lt2(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)    
        self.device = Wemo_b1lt2("b1lt2", "192.168.86.28", self.testQueue) 

    def test_wemo_b1lt2(self):
        self.testData = []
        # Before early wake time - with and without kids
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,39)), [True, True, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,39)), [True, True, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,39)), [True, False, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,39)), [True, False, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,39)), [False, False, False], False))
        # Just after early wake time - with and without kids
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,41)), [True, True, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,41)), [True, True, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,41)), [True, False, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,41)), [True, False, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(5,41)), [False, False, False], False))
        # Before late wake time - with and without kids
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,19)), [True, True, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,19)), [True, True, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,19)), [True, False, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,19)), [True, False, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,19)), [False, False, False], False)) 
        # After late wake time - with and without kids
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,21)), [True, True, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,21)), [True, True, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,21)), [True, False, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,21)), [True, False, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,21)), [False, False, False], False)) 
        # Before early leave time - with and without kids 
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,39)), [True, True, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,39)), [True, True, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,39)), [True, False, True], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,39)), [True, False, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,39)), [False, False, False], False))
        # After early leave time - with and without kids
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,41)), [True, True, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,41)), [True, True, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,41)), [True, False, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,41)), [True, False, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(6,41)), [False, False, False], False))
        # Before late leave time
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,9)), [True, True, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,9)), [True, True, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,9)), [True, False, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,9)), [True, False, False], True))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,9)), [False, False, False], False))
        # After late leave time
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,11)), [True, True, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,11)), [True, True, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,11)), [True, False, True], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,11)), [True, False, False], False))
        self.testData.append((datetime.datetime.combine(datetime.date(2016,10,31), datetime.time(7,11)), [False, False, False], False))                              

        for index, data in enumerate(self.testData):
            self.device.check_rules(datetime=data[0], homeArray=data[1])
            self.assertEqual(self.device.state, data[2])
       