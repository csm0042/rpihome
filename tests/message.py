import unittest
import sys

if __name__ == "__main__": sys.path.append("..")
from rpihome.modules.message import Message


class Test_Message(unittest.TestCase):
    def setUp(self):
        self.message = Message()

    def test_message_set_from_raw(self):
        self.message.raw = "02,11,103,fylt1,"
        self.assertEqual(self.message.source, "02")
        self.assertEqual(self.message.dest, "11")
        self.assertEqual(self.message.type, "103")
        self.assertEqual(self.message.device, "fylt1")
        self.assertEqual(self.message.payload, "")

    def test_message_raw_from_part1(self):
        self.message.source = "01"
        self.message.dest = "23"
        self.message.type = "456"
        self.message.device = "bylt1"
        self.message.payload = ""
        self.assertEqual(self.message.raw, "01,23,456,bylt1,")

    def test_message_raw_from_part2(self):
        self.message.source = "01"
        self.message.dest = "23"
        self.message.type = "456"
        self.message.device = ""
        self.message.payload = "hello"
        self.assertEqual(self.message.raw, "01,23,456,,hello")        

if __name__ == "__main__":
    unittest.main()
