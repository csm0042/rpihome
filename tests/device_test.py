from unittest import TestCase
import datetime
import multiprocessing
from rpihome.devices.device import Device


class TestDevice(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)            
        self.device = Device("test-name", self.testQueue)

    def test_name(self):
        self.device.name = "new-test-name"
        self.assertEqual(self.device.name, "new-test-name")

    def test_state(self):
        self.device.state = True
        self.assertEqual(self.device.state, True) 
        self.device.state = None
        self.assertEqual(self.device.state, True)          
        self.device.state = False
        self.assertEqual(self.device.state, False)               

    def test_state_mem(self):
        self.device.state_mem = False
        self.assertEqual(self.device.state_mem, False)
        self.device.state_mem = True
        self.assertEqual(self.device.state_mem, True)
        self.device.state_mem = None
        self.assertEqual(self.device.state_mem, None)

    def test_status(self):
        self.device.status = 1
        self.assertEqual(self.device.status, 1)
        self.device.status = 0
        self.assertEqual(self.device.status, 0)
        self.device.status = "n"
        self.assertIsInstance(self.device.status, int)
        self.assertEqual(self.device.status, 0)

    def test_statusChangeTS(self):
        self.datetimeCompare = datetime.datetime.now()
        self.device.statusChangeTS = self.datetimeCompare
        self.assertIsInstance(self.device.statusChangeTS, datetime.datetime)
        self.assertEqual(self.device.statusChangeTS, self.datetimeCompare)        

    def test_dt(self):
        self.datetimeCompare = datetime.datetime.now()
        self.device.dt = self.datetimeCompare
        self.assertIsInstance(self.device.dt, datetime.datetime)
        self.assertEqual(self.device.dt, self.datetimeCompare) 

    def test_online(self):
        self.device.online = True
        self.assertEqual(self.device.online, True) 
        self.device.online = None
        self.assertEqual(self.device.online, True)          
        self.device.online = False
        self.assertEqual(self.device.online, False)         
        self.assertIsInstance(self.device.online, bool)

    def test_home(self):
        self.device.home = True
        self.assertEqual(self.device.home, True) 
        self.device.home = None
        self.assertEqual(self.device.home, True)          
        self.device.home = False
        self.assertEqual(self.device.home, False)         
        self.assertIsInstance(self.device.home, bool)

    def test_home(self):
        self.device.homeNew = True
        self.assertEqual(self.device.homeNew, True) 
        self.device.homeNew = None
        self.assertEqual(self.device.homeNew, None)          
        self.device.homeNew = False
        self.assertEqual(self.device.homeNew, False)         
        self.assertIsInstance(self.device.homeNew, bool)   

    def test_homeArray(self):
        self.homeArray = [True, True, True] 
        self.homeTime = [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()]      
        self.assertIsInstance(self.homeArray[1], bool)
        self.assertIsInstance(self.homeTime[1], datetime.datetime)
