#!/usr/bin/python3
""" schedule.py:
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
class Condition(object):
    """ A class consisting of a conditoin to be checked and the desired state to pass """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.__andor = str()
        self.__condition = str()
        self.__state = str()
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "andor":
                    self.andor = value                
                if key == "condition":
                    self.condition = value
                if key == "state":
                    self.state = value

    @property
    def andor(self):
        """ Returns the condition type to be checked """
        return self.__andor

    @andor.setter
    def andor(self, value):
        """ Sets the condition type to be checked """
        if isinstance(value, str):
            self.__andor = value

    @property
    def condition(self):
        """ Returns the condition to be checked """
        return self.__condition

    @condition.setter
    def condition(self, value):
        """ Sets the condition to be checked """
        if isinstance(value, str):
            self.__condition = value

    @property
    def state(self):
        """ Returns the desired state to be checked against """
        return self.__state

    @state.setter
    def state(self, value):
        """ Sets the desired state to be checked against """
        if isinstance(value, str):
            self.__state = value


class OnRange(object):
    """ Single on/off range with aux conditions """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.__on_time = datetime.time()
        self.__off_time = datetime.time()
        self.__condition = []
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "on_time":
                    self.on_time = value
                if key == "off_time":
                    self.off_time = value
                if key == "condition":
                    self.condition = value

    @property
    def on_time(self):
        """ Returns on time for a single on/off value pair """
        return self.__on_time

    @on_time.setter
    def on_time(self, value):
        """ Sets on time for a single on/off value pair """
        if isinstance(value, datetime.time):
            self.__on_time = value

    @property
    def off_time(self):
        """ Returns off time for a single on/off value pair' """
        return self.__off_time

    @off_time.setter
    def off_time(self, value):
        """ Sets off time for a single on/off value pair """
        if isinstance(value, datetime.time):
            self.__off_time = value

    @property
    def condition(self):
        """ Returns the condition array for a single on/off value pair """
        return self.__condition

    @condition.setter
    def condition(self, value):
        """ Sets the condition array for a single on/off value pair """
        if isinstance(value, list):
            self.__condition = value
        elif isinstance(value, Condition):
            self.__condition = [value]

    def add_condition(self, andor=None, condition=None, state=None):
        """ Adds a condition to the list of conditions associated with a given on/off time pair """
        self.__condition.append(Condition(andor=andor, condition=condition, state=state))

    def clear_all_conditions(self):
        """ Clears condition list for a given on/off time pair """
        self.__condition.clear()

    def remove_condition(self, index):
        """ Removes a specific condition from the condition list based on its position in the list (index) """
        try:
            self.__condition.pop(index)
        except:
            pass


class Day(object):
    """ Single day schedule """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.date = datetime.datetime.now().date()
        self.__range = []
        # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "date":
                    self.date = value
                if key == "range":
                    self.range = value

    @property
    def date(self):
        """ Returns entire week's schedule' """
        return self.__date

    @date.setter
    def date(self, value):
        """ Sets entire week's schedule' """
        if isinstance(value, datetime.date):
            self.__date = value

    @property
    def range(self):
        """ Returns entire week's schedule' """
        return self.__range

    @range.setter
    def range(self, value):
        """ Sets entire week's schedule' """
        if isinstance(value, list):
            self.__range = value
        elif isinstance(value, OnRange):
            self.__range = [value]

    def add_range(self, on_time, off_time):
        """ Adds a condition to the list of conditions associated with a given on/off time pair """
        self.__range.append(OnRange(on_time=on_time, off_time=off_time))

    def clear_all_ranges(self):
        """ Clears condition list for a given on/off time pair """
        self.__range.clear()

    def remove_range(self, index):
        """ Removes a specific condition from the condition list based on its position in the list (index) """
        try:
            self.__range.pop(index)
        except:
            pass       

    def add_range_with_conditions(self, on_time, off_time, conditions=None):      
        self.__range.append(OnRange(on_time=on_time, off_time=off_time))
        self.index = len(self.__range) - 1
        # Add single conditions passed in as a tuple
        if isinstance(conditions, tuple):
            self.logger.debug("single condition passed in with on and off time")
            if len(conditions) == 3:
                self.__range[self.index].add_condition(andor=conditions[0],
                                                       condition=conditions[1],
                                                       state=conditions[2])
        # Add multiple conditions passed in as an array of tuples
        if isinstance(conditions, list):
            self.logger.debug("Multiple conditions passed in with on and off time")
            for i, j in enumerate(conditions):
                if isinstance(j, tuple):
                    if len(j) == 3:
                        self.logger.debug("Adding condition: %s %s = %s", j[0], j[1], j[2])
                        self.__range[self.index].add_condition(andor=j[0],
                                                               condition=j[1],
                                                               state=j[2])


class Week(object):
    """ Weekly schedule with on/off times and extra conditions for a single device """
    def __init__(self, logger=None, **kwargs):
        self.logger = logger or logging.getLogger(__name__)
        self.__day = [Day()] * 7
         # Process input variables if present
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "day":
                    self.day = value
                if key == "monday":
                    self.monday = value
                if key == "tuesday":
                    self.tuesday = value
                if key == "wednesday":
                    self.wednesday = value
                if key == "thursday":
                    self.thursday = value
                if key == "friday":
                    self.friday = value
                if key == "saturday":
                    self.saturday = value
                if key == "sunday":
                    self.sunday = value

    @property
    def day(self):
        """ Returns entire week's schedule' """
        return self.__day

    @day.setter
    def day(self, value):
        """ Sets entire week's schedule' """
        if isinstance(value, list):
            self.__day = value

    @property
    def monday(self):
        """ Returns the day's schedule for Monday """
        return self.__day[0]

    @monday.setter
    def monday(self, value):
        """ Set's the schedule for Monday """
        if isinstance(value, Day):
            self.__day[0] = value

    @property
    def tuesday(self):
        """ Returns the day's schedule for Tuesday """
        return self.__day[1]

    @tuesday.setter
    def tuesday(self, value):
        """ Set's the schedule for Tuesday """
        if isinstance(value, Day):
            self.__day[1] = value

    @property
    def wednesday(self):
        """ Returns the day's schedule for Wednesday """
        return self.__day[2]

    @wednesday.setter
    def wednesday(self, value):
        """ Set's the schedule for Wednesday """
        if isinstance(value, Day):
            self.__day[2] = value

    @property
    def thursday(self):
        """ Returns the day's schedule for Thursday """
        return self.__day[3]

    @thursday.setter
    def thursday(self, value):
        """ Set's the schedule for thursday """
        if isinstance(value, Day):
            self.__day[3] = value

    @property
    def friday(self):
        """ Returns the day's schedule for Friday """
        return self.__day[4]

    @friday.setter
    def friday(self, value):
        """ Set's the schedule for Friday """
        if isinstance(value, Day):
            self.__day[4] = value

    @property
    def saturday(self):
        """ Returns the day's schedule for Satruday """
        return self.__day[5]

    @saturday.setter
    def saturday(self, value):
        """ Set's the schedule for Saturday """
        if isinstance(value, Day):
            self.__day[5] = value

    @property
    def sunday(self):
        """ Returns the day's schedule for Sunday """
        return self.__day[6]

    @sunday.setter
    def sunday(self, value):
        """ Set's the schedule for Sunday """
        if isinstance(value, Day):
            self.__day[6] = value


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
        self.date = datetime.date


    def convert_date(self, record):
        self.record = record
        self.regex1 = r"(\d{4})\-(0?[1-9]|[1][012])\-(0?[1-9]|[12][0-9]|3[01])"
        self.regex2 = r"(\d{4})\/(0?[1-9]|[1][012])\/(0?[1-9]|[12][0-9]|3[01])"
        if re.search(self.regex1, self.record[0]):
            self.logger.debug("Data in day field is a date using a '-' as a separator")
            self.split_date = self.record[0].split("-")
            self.record[0] = datetime.date(int(self.split_date[0]),
                                           int(self.split_date[1]),
                                           int(self.split_date[2]))
            self.logger.debug("Updating to datetime.date data type: %s", self.record[0])
        elif re.search(self.regex2, self.record[0]):
            self.logger.debug("Data in day field is a date using a '/' as a separator")
            self.split_date = self.record[0].split("/")
            self.record[0] = datetime.date(int(self.split_date[0]),
                                           int(self.split_date[1]),
                                           int(self.split_date[2]))
            self.logger.debug("Updating to datetime.date data type: %s", self.record[0])
        else:
            self.logger.debug("Data in day field is not a specific date")
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


                

