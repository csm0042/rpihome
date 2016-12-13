from unittest import TestCase
import datetime
import multiprocessing
if __name__ == "__main__": sys.path.append("..")
from rpihome.devices.device import Device
from rpihome.modules.schedule import Day, Week, OnRange, Condition


class TestDevice(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)            
        self.device = Device("test-name", self.testQueue)

    def test_device_name(self):
        self.device.name = "new-test-name"
        self.assertEqual(self.device.name, "new-test-name")

    def test_device_state(self):
        self.device.state = True
        self.assertEqual(self.device.state, True) 
        self.device.state = None
        self.assertEqual(self.device.state, True)          
        self.device.state = False
        self.assertEqual(self.device.state, False)               

    def test_device_state_mem(self):
        self.device.state_mem = False
        self.assertEqual(self.device.state_mem, False)
        self.device.state_mem = True
        self.assertEqual(self.device.state_mem, True)
        self.device.state_mem = None
        self.assertEqual(self.device.state_mem, None)

    def test_device_status(self):
        self.device.status = 1
        self.assertEqual(self.device.status, 1)
        self.device.status = 0
        self.assertEqual(self.device.status, 0)
        self.device.status = "n"
        self.assertIsInstance(self.device.status, int)
        self.assertEqual(self.device.status, 0)

    def test_device_statusChangeTS(self):
        self.datetimeCompare = datetime.datetime.now()
        self.device.statusChangeTS = self.datetimeCompare
        self.assertIsInstance(self.device.statusChangeTS, datetime.datetime)
        self.assertEqual(self.device.statusChangeTS, self.datetimeCompare)        

    def test_device_dt(self):
        self.datetimeCompare = datetime.datetime.now()
        self.device.dt = self.datetimeCompare
        self.assertIsInstance(self.device.dt, datetime.datetime)
        self.assertEqual(self.device.dt, self.datetimeCompare) 

    def test_device_online(self):
        self.device.online = True
        self.assertEqual(self.device.online, True) 
        self.device.online = None
        self.assertEqual(self.device.online, None)          
        self.device.online = False
        self.assertEqual(self.device.online, False)         
        self.assertIsInstance(self.device.online, bool)

    def test_device_home(self):
        self.device.home = True
        self.assertEqual(self.device.home, True) 
        self.device.home = None
        self.assertEqual(self.device.home, None)          
        self.device.home = False
        self.assertEqual(self.device.home, False)         
        self.assertIsInstance(self.device.home, bool)

    def test_device_homeNew(self):
        self.device.homeNew = True
        self.assertEqual(self.device.homeNew, True) 
        self.device.homeNew = None
        self.assertEqual(self.device.homeNew, None)          
        self.device.homeNew = False
        self.assertEqual(self.device.homeNew, False)         
        self.assertIsInstance(self.device.homeNew, bool)   

    def test_device_homeArray(self):
        self.homeArray = [True, True, True] 
        self.homeTime = [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()]      
        self.assertIsInstance(self.homeArray[1], bool)
        self.assertIsInstance(self.homeTime[1], datetime.datetime)


    def test_check_rules(self):
        # Create condition(s)
        self.condition = Condition(condition="user1", state="true")
        # Create two time ranges to use on different days
        self.on_range_1 = OnRange(ontime=datetime.time(6,30), offtime=datetime.time(7,0), condition=self.condition)
        self.on_range_2 = OnRange(ontime=datetime.time(5,40), offtime=datetime.time(6,30), condition=self.condition)
        # Create each day's schedule
        self.monday = Day(date=datetime.date(2016,12,5), onrange=self.on_range_1)
        self.tuesday = Day(date=datetime.date(2016,12,6), onrange=self.on_range_1)
        self.wednesday = Day(date=datetime.date(2016,12,7), onrange=self.on_range_1)
        self.thursday = Day(date=datetime.date(2016,12,8), onrange=self.on_range_2)
        self.friday = Day(date=datetime.date(2016,12,9), onrange=self.on_range_2)
        # Create overall week's schedule
        self.schedule = Week(monday=self.monday, tuesday=self.tuesday, wednesday=self.wednesday, thursday=self.thursday, friday=self.friday)
        self.test_data = []
        self.test_data.append((
            datetime.datetime.combine(datetime.date(2016,12,5), datetime.time(6,29)),
            [True, True, True], False))
        self.test_data.append((
            datetime.datetime.combine(datetime.date(2016,12,5), datetime.time(6,31)),
            [True, True, True], True))
        self.test_data.append((
            datetime.datetime.combine(datetime.date(2016,12,5), datetime.time(6,59)),
            [True, True, True], True))
        self.test_data.append((
            datetime.datetime.combine(datetime.date(2016,12,5), datetime.time(7,1)),
            [True, True, True], False))
        self.test_data.append((
            datetime.datetime.combine(datetime.date(2016,12,5), datetime.time(6,45)),
            [True, True, True], True))
        self.test_data.append((
            datetime.datetime.combine(datetime.date(2016,12,5), datetime.time(6,45)),
            [False, True, True], False))
        # Check each data set against it's anticipated result
        for i, j in enumerate(self.test_data):
            self.device.check_custom_rules(datetime=j[0],
                                           homeArray=j[1],
                                           utcOffset=datetime.timedelta(hours=-6), 
                                           sunriseOffset=datetime.timedelta(minutes=0),
                                           sunsetOffset=datetime.timedelta(minutes=0),
                                           schedule=self.schedule)
            self.assertEqual(self.device.state, j[2])          
