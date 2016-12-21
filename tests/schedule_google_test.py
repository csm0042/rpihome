#!/usr/bin/python3
""" schedule_google_test.py:   
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import logging
import unittest
import sys

if __name__ == "__main__": sys.path.append("..")
from rpihome.modules.schedule_google import GoogleSheetsInterface, GoogleSheetToSched


# Define test class *******************************************************************************
class Test_Schedule(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger(__name__)
        pass

    def test_google_sheets_read(self):
        self.google_sheets_reader = GoogleSheetsInterface()
        self.records = self.google_sheets_reader.read_data()
        print(self.records)
        #self.schedule_builder = GoogleSheetToSched(self.logger)
        #3self.schedule_builder.main(self.records)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    logger.debug("\n\nStarting log\n")
    unittest.main()        