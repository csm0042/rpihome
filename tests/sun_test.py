from unittest import TestCase
import datetime
from rpihome.modules.sun import Sun


class TestSun(TestCase):
    def setUp(self):
        self.s = Sun(lat=38.566, long=-90.409)
        self.utcOffset = datetime.timedelta(hours=-5)

    def test_sunrise(self):
        self.sunrise_time = self.s.sunrise(datetime.datetime.now(), self.utcOffset)
        self.sunrise = datetime.datetime.combine(datetime.datetime.today().date(), self.sunrise_time)
        self.sunrise_compare = datetime.datetime.now()
        self.assertEqual(self.sunrise.date(), datetime.datetime.now().date())
        

    def test_sunset(self):
        self.sunset_time = self.s.sunset(datetime.datetime.now(), self.utcOffset)
        self.sunset = datetime.datetime.combine(datetime.datetime.today().date(), self.sunset_time)
        self.sunset_compare = datetime.datetime.now()
        self.assertEqual(self.sunset.date(), datetime.datetime.now().date())
