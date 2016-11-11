from unittest import TestCase
import datetime
import multiprocessing
from rpihome.devices.device_rpi import DeviceRPI


class TestDevice(TestCase):
    def setUp(self):
        self.testQueue = multiprocessing.Queue(-1)            
        self.device = DeviceRPI("test-name", self.testQueue)
        self.msg_in = str()

    def test_device_rpi_command(self):
        self.device.state = False
        self.device.command()
        try:
            self.msg_in = self.testQueue.get_nowait()  
        except:
            pass
        print(self.msg_in)
        self.assertEqual(self.msg_in, "11,15,150,export DISPLAY=:0; xset s activate")
        
        self.device.state = True
        self.device.command()        
        try:
            self.msg_in = self.testQueue.get_nowait()  
        except:
            pass
        print(self.msg_in)
        self.assertEqual(self.msg_in, "11,15,150,export DISPLAY=:0; xset s reset")        

