from unittest import TestCase
from rpihome.modules.wemo import discover


class TestDiscover(TestCase):
    def test_discover(self):
        self.devices = discover()
        self.assertGreater(len(self.devices), 0)

