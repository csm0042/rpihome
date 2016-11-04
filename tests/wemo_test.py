from unittest import TestCase
from rpihome.modules.wemo import discover


class TestDiscover(TestCase):
    def test_discover(self):
        self.devices = discover()
        self.assertEqual(len(self.devices), 0)

