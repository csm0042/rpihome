#!/usr/bin/python3
""" schedule_google.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
from __future__ import print_function
import datetime
import logging
import httplib2
import re
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Class Definitions *******************************************************************************
class GoogleSheetsSchedule(object):
    """ Class and methods necessary to read a schedule from a google sheets via google's api' """
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None
        self.home_dir = str()
        self.credential_dir = str()
        self.store = str()
        self.credentials = str()
        self.path = str()
        self.CLIENT_SECRET_FILE = str()
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Device Schedule via Google Sheets API'


    def get_credentials(self):
        """
        Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid, the OAuth2 flow is completed to obtain the new credentials. 
        Returns: Credentials, the obtained credential.
        """
        self.home_dir = os.path.expanduser('~')
        self.credential_dir = os.path.join(self.home_dir, '.credentials')
        if not os.path.exists(self.credential_dir):
            self.logger.debug("Creating directory: %s", self.credential_dir)
            os.makedirs(self.credential_dir)
        self.credential_path = os.path.join(self.credential_dir,
                                    'sheets.googleapis.com-python-quickstart.json')
        self.logger.debug("Setting credential path to: %s", self.credential_path)
        self.store = Storage(self.credential_path)
        self.logger.debug("Setting store to: %s", self.store)
        self.credentials = self.store.get()
        self.logger.debug("Getting credentials from store")
        if not self.credentials or self.credentials.invalid:
            self.logger.debug("Credentials not in store")
            self.path = os.path.dirname(sys.argv[0])
            self.logger.debug("System path is: %s", self.path)
            self.CLIENT_SECRET_FILE = os.path.join(self.path, "client_secret.json")
            self.logger.debug("Looking for json file at: %s", self.CLIENT_SECRET_FILE)
            self.flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            self.flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                self.credentials = tools.run_flow(self.flow, self.store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                self.credentials = tools.run(self.flow, self.store)
            self.logger.debug('Storing credentials to ' + self.credential_path)
        self.logger.debug("Returning credentials to main program")
        return self.credentials


    def read_data(self, sheet_id=None, sheet_range=None):
        """
        Returns all data from a specific sheet using the google sheets API
        """
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        self.service = discovery.build('sheets', 'v4',
                                       http=self.http,
                                       discoveryServiceUrl=self.discoveryUrl)
        # Set sheet name and range to read
        if sheet_id is not None:
            self.spreadsheetId = sheet_id
        else:
            self.spreadsheetId = '1LJpDC0wMv3eXQtJvHNav_Yty4PQcylthOxXig3_Bwu8'
        self.logger.debug("Using sheet id: %s", self.spreadsheetId)
        if sheet_range is not None:
            self.rangeName = sheet_range
        else:
            self.rangeName = "fylt1!A3:L"
        self.logger.debug("Reading data from range: %s", self.rangeName)
        # Read data from sheet/range specified
        self.result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=self.rangeName).execute()
        self.values = self.result.get('values', [])
        self.logger.debug("Read from table: %s", self.values)

        if not self.values:
            self.logger.debug("No data found.  Returning NONE to main")
            return None
        else:
            self.logger.debug("Returning data to main")
            return self.values


class GoogleSheetToSched(object):
    """ class and methods used to covert a list of records from a specifically formatted google sheet, into a schedule for the current calendar Week
    """
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.split = []


    def convert_objects(self, record):
        self.record = record
        # Cycle through all parts of the record, replacing dates and times as appropriate
        for i, j in enumerate(self.record):
            # Replace yyyy-mm-dd format with datetime object
            self.regex = r"(\d{4})\-(0?[1-9]|[1][012])\-(0?[1-9]|[12][0-9]|3[01])"
            if re.search(self.regex, j):
                self.logger.debug("Data in fied is a date using a '-' as a separator")
                self.split = j.split("-")
                j = datetime.date(int(self.split[0]),
                                  int(self.split[1]),
                                  int(self.split[2]))
                record[i] = j
            # Replace yyyy/mm/dd format with datetime object
            self.regex = r"(\d{4})\/(0?[1-9]|[1][012])\/(0?[1-9]|[12][0-9]|3[01])"
            if re.search(self.regex, j):
                self.logger.debug("Data in fied is a date using a '/' as a separator")
                self.split = j.split("/")
                j = datetime.date(int(self.split[0]),
                                  int(self.split[1]),
                                  int(self.split[2]))
                record[i] = j
            # Replace hh:mm format with datetime object
            self.regex = r"\b([01]?[0-9]|2[0-3]):([0-5][0-9])"
            if re.search(self.regex, j):
                self.logger.debug("Data in fied is a date using a '/' as a separator")
                self.split = j.split(":")
                j = datetime.time(int(self.split[0]),
                                  int(self.split[1]))
                record[i] = j              

        return self.record


        
        

    def main(self, records):
        """ Don't really know what to call this yet, but this will be the main decoder sequence' """
        self.records = records
        self.logger.debug("\n\nDecoding starting for record set:\n%s", self.records)
        # First step is to convert all dates in the leading column of the data to datetime objects
        for index, record in enumerate(self.records):
            self.record = self.convert_date(record)
            self.records[index] = self.record
        self.logger.debug("\n\nUpdated record-set:\n%s", self.records)
        # Next step is to determine the week start and end dates of this current week.  This information will be used to filter out specific date assignments outside of this range
        self.dt_now = datetime.datetime.now()
        self.day = self.dt_now.weekday()
        self.dt_monday = self.dt_now + datetime.timedelta(days=-self.day)
        self.logger.debug("week starts on: %s", self.dt_monday.date())
        self.dt_sunday = self.dt_monday + datetime.timedelta(days=6)
        self.logger.debug("week ends on: %s", self.dt_sunday.date())
        # Now search the record list and remove any items that have specific dates in their day data fields, but don't fall within the range of the current week being considered
        for index, record in enumerate(self.records):
            if isinstance(record[0], datetime.date):
                if record[0] < self.dt_monday.date() or record[0] > self.dt_sunday.date():
                    self.logger.debug("Record [%s] falls outside of range and will be discarded", record)
                    self.records.pop(index)
        self.logger.debug("Updated record list: %s", self.records)
        # We are now left with only data from the schedule that in some way applies to this week.  Now we apply the records to each day based on a pre-defined priority

