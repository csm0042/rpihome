from unittest import TestCase
import multiprocessing
from rpihome.devices.device_rpi import DeviceRPI


class TestDevice(TestCase):
    """ Test class and methods for the DeviceRPI class """
    def setUp(self):
        self.test_queue = multiprocessing.Queue(-1)
        self.device = DeviceRPI("test-name", self.test_queue)
        self.msg_in = str()

    def test_device_rpi_command(self):
        """ Test command method for rpi screen saver """
        self.device.state = False
        self.device.command()
        try:
            self.msg_in = self.test_queue.get_nowait()
        except:
            pass
        self.assertEqual(self.msg_in, "11,15,150,export DISPLAY=:0; xset s activate")
        self.device.state = True
        self.device.command()
        try:
            self.msg_in = self.test_queue.get_nowait()
        except:
            pass
        self.assertEqual(self.msg_in, "11,15,150,export DISPLAY=:0; xset s reset")

