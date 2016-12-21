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
from .sun import Sun


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
class GoogleSheetsInterface(object):
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
        self.sun = Sun(lat=38.566, long=-90.410)
        self.split = []
        self.ready = [False, False, False, False, False, False, False]
        self.records_by_day = [None, None, None, None, None, None, None]


    def convert_to_datetimes(self, record):
        self.record_to_convert = record
        # Cycle through all parts of the record, replacing dates and times as appropriate
        for i, j in enumerate(self.record_to_convert):
            # Replace yyyy-mm-dd format with datetime object
            self.regex = r"(\d{4})\-(0?[1-9]|[1][012])\-(0?[1-9]|[12][0-9]|3[01])"
            if re.search(self.regex, j):
                self.logger.debug("Data in fied is a date using a '-' as a separator")
                self.split = j.split("-")
                j = datetime.date(int(self.split[0]),
                                  int(self.split[1]),
                                  int(self.split[2]))
                self.record_to_convert[i] = j
            # Replace yyyy/mm/dd format with datetime object
            self.regex = r"(\d{4})\/(0?[1-9]|[1][012])\/(0?[1-9]|[12][0-9]|3[01])"
            if re.search(self.regex, j):
                self.logger.debug("Data in fied is a date using a '/' as a separator")
                self.split = j.split("/")
                j = datetime.date(int(self.split[0]),
                                  int(self.split[1]),
                                  int(self.split[2]))
                self.record_to_convert[i] = j
            # Replace hh:mm format with datetime object
            self.regex = r"\b([01]?[0-9]|2[0-3]):([0-5][0-9])(:([0-5][0-9]))?"
            if re.search(self.regex, j):
                self.logger.debug("Data in fied is a date using a '/' as a separator")
                self.split = j.split(":")
                j = datetime.time(int(self.split[0]),
                                  int(self.split[1]))
                self.record_to_convert[i] = j
            # Replace sunrise keyword with datetime object
            self.regex = r"\b[Ss]un(-)?[Rr]ise"
            if re.search(self.regex, j):
                self.logger.debug("Data in field is a keyword 'sunrise'")
                j = self.sun.sunrise.time()
                self.record_to_convert[i] = j
            # Replace sunset keyword with datetime object
            self.regex = r"\b[Ss]un(-)?[Ss]et" 
            if re.search(self.regex, j):
                self.logger.debug("Data in field is a keyword 'sunset'")
                j = self.sun.sunset.time()
                self.record_to_convert[i] = j            
        # Return updated record
        return self.self.record_to_convert


    def find_date_specific_date_records(self, raw_records, records_by_day, date):
        self.records_to_search = raw_records
        self.records_by_day = records_by_day
        # Figure out what day of the week was passed in, then set start date to monday of that same week
        if isinstance(date, datetime.date):
            self.iso_day = (datetime.datetime.combine(date, datetime.time(0, 0))).weekday()
        elif isinstance(date, datetime.datetime):
            self.iso_day = date.weekday()
        self.start_date = date + datetime.timedelta(days=-self.iso_day)
        self.end_date = self.start_date + datetime.timedelta(days=6)
        # Search through list of records for any specific date entries that fall between the start and end dates just calculated
        for i, j in enumerate(self.records_to_search):
            if j[0].date() >= self.start_date or j[0].date() <= self.end_date:
                # Determine what day was found
                self.day_ptr = (j[0].date()).weekday()
                # Use that as a pointer to put a copy of that specific record in the proper slot for that day in the list for that week                
                if self.records_by_day[self.day_ptr] is None:
                    self.records_by_day[self.day_ptr] = [j]
                else:
                    self.records_by_day[self.day_ptr].append(copy.copy(j))
        # Mark days with records as "ready"
        for i, j in enumerate(self.records_by_day):
            if j is not None:
                self.ready[i] = True
        # Return updated list
        return self.records_by_day

    
    def find_specific_day_records(self, raw_records, records_by_day):
        self.records_to_search = raw_records
        self.records_by_day = records_by_day
        # Cycle through records looking for specific day keywords
        for i, j in enumerate(self.records_to_search):
            if re.search(r"\b[Mm][Oo][Nn]([Dd][Aa][Yy])?", j):
                if self.ready[0] is False:
                    if self.records_by_day[0] is None:
                        self.records_by_day[0] = [j]
                    else:
                        self.records_by_day[0].append(copy.copy(j))
            elif re.search(r"\b[Tt][Uu][Ee]([Ss][Dd][Aa][Yy])?", j):
                if self.ready[1] is False:
                    if self.records_by_day[1] is None:
                        self.records_by_day[1] = [j]
                    else:
                        self.records_by_day[1].append(copy.copy(j))
            elif re.search(r"\b[Ww][Ee][Dd]([Nn][Ee][Ss][Dd][Aa][Yy])?", j):
                if self.ready[2] is False:
                    if self.records_by_day[2] is None:
                        self.records_by_day[2] = [j]
                    else:
                        self.records_by_day[2].append(copy.copy(j))
            elif re.search(r"[Tt][Hh][Uu]([Rr])?([Ss][Dd][Aa][Yy])?", j):
                if self.ready[3] is False:
                    if self.records_by_day[3] is None:
                        self.records_by_day[3] = [j]
                    else:
                        self.records_by_day[3].append(copy.copy(j))
            elif re.search(r"[Ff][Rr][Ii]([Dd][Aa][Yy])?", j):
                if self.ready[4] is False:
                    if self.records_by_day[4] is None:
                        self.records_by_day[4] = [j]
                    else:
                        self.records_by_day[4].append(copy.copy(j))
            elif re.search(r"[Ss][Aa][Tt]([Uu][Rr][Dd][Aa][Yy])?", j):
                if self.ready[5] is False:
                    if self.records_by_day[5] is None:
                        self.records_by_day[5] = [j]
                    else:
                        self.records_by_day[5].append(copy.copy(j))
            elif re.search(r"[Ss][Uu][Nn]([Dd][Aa][Yy])?", j):
                if self.ready[6] is False:
                    if self.records_by_day[6] is None:
                        self.records_by_day[6] = [j]
                    else:
                        self.records_by_day[6].append(copy.copy(j))
        # Mark days with records as "ready"
        for i, j in enumerate(self.records_by_day):
            if j is not None:
                self.ready[i] = True
        # Return updated list
        return self.records_by_day


    def find_weekday_weekend_records(self, raw_records, records_by_day):
        self.records_to_search = raw_records
        self.records_by_day = records_by_day
        # Cycle through records looking for specific day keywords
        for i, j in enumerate(self.records_to_search):
            if re.search(r"\b[Ww][Ee][Ee][Kk](-)?([Dd][Aa][Yy])([Ss])?", j):
                for k in range(0, 5, 1):
                    if self.ready[k] is False:
                        if self.records_by_day[k] is None:
                            self.records_by_day[k] = [j]
                        else:
                            self.records_by_day[k].append(copy.copy(j))
            elif re.search(r"\b[Ww][Ee][Ee][Kk](-)?([Ee][Nn][Dd])([Ss])?", j):
                for k in range(5, 7, 1):
                    if self.ready[k] is False:
                        if self.records_by_day[k] is None:
                            self.records_by_day[k] = [j]
                        else:
                            self.records_by_day[k].append(copy.copy(j))                
        # Mark days with records as "ready"
        for i, j in enumerate(self.records_by_day):
            if j is not None:
                self.ready[i] = True
        # Return updated list
        return self.records_by_day


