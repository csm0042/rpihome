from unittest import TestCase
import datetime
from rpihome.modules.sunrise import sun


class TestSun(TestCase):
    def setUp(self):
        self.s = sun(lat=38.566, long=-90.409)
        self.utcOffset = -5

    def test_sunrise(self):
        self.sunrise_time = self.s.sunrise(datetime.datetime.now(), self.utcOffset)
        self.sunrise = datetime.datetime.combine(datetime.datetime.today().date(), self.sunrise_time)
        self.sunrise_compare = datetime.datetime.now()
        print("Sunrise: " + str(self.sunrise))
        self.assertLessEqual(self.sunrise, self.sunrise_compare)

    def test_sunset(self):
        self.sunset_time = self.s.sunset(datetime.datetime.now(), self.utcOffset)
        self.sunset = datetime.datetime.combine(datetime.datetime.today().date(), self.sunset_time)
        self.sunset_compare = datetime.datetime.now()
        print("Sunset: " + str(self.sunset))
        self.assertGreaterEqual(self.sunset, self.sunset_compare)
