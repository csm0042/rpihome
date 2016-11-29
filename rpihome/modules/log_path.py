#!/usr/bin/python3
""" log_path.py: Support library for determining where to put the log-file when running a project
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import logging
import os
import sys


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Create log file path / folder support function ***********************************************************************
class LogFilePath(object):
    def __init__(self, logger=None):
        # Configure logger
        self.logger = logger or logging.getLogger(__name__)      
        # Init tags         
        self.name = "undefined"
        self.current_path = str()
        self.one_up_path = str()
        log_file_path = str()
        log_file_name = str()


    def create_log_file(self, path, name):
        self.path = path
        self.name = name
        self.logpath = str()
        self.logname = str()
        # Search existing paths to determine where logs should go
        if os.path.isdir(os.path.join(self.path, "logs")):
            self.logpath = os.path.join(self.path, "logs")
        else:
            self.one_up_path = os.path.split(self.path)[0]
            if os.path.isdir(os.path.join(self.one_up_path, "logs")):
                self.logpath = os.path.join(self.one_up_path, "logs")
            else:
                self.logpath = os.path.dirname(sys.argv[0])
            pass
        # Make log directory if it doesn't already exist
        try:
            os.stat(self.logpath)
        except:
            os.mkdir(self.logpath)
        # Define log file name
        self.logname = self.name + ".log"
        # Return result
        return self.logpath, self.logname


    def return_path(self, **kwargs):
        # If arguments were passed, replace default values as necessary
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "path":
                    self.path = value
        # Call method to calculate and create (if necessary) log file and path
        self.log_file_path, self.log_file_name = self.create_log_file(self.path, self.name)
        # Return path to main program
        return self.log_file_path


    def return_name(self, **kwargs):
        # If arguments were passed, replace default values as necessary
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "path":
                    self.path = value
        # Call method to calculate and create (if necessary) log file and path
        self.log_file_path, self.log_file_name = self.create_log_file(self.path, self.name)
        # Return path to main program
        return self.log_file_name


    def return_path_and_name_separate(self, **kwargs):
        # If arguments were passed, replace default values as necessary
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "path":
                    self.path = value
        # Call method to calculate and create (if necessary) log file and path
        self.log_file_path, self.log_file_name = self.create_log_file(self.path, self.name)
        # Return path to main program
        return self.log_file_path, self.log_file_name


    def return_path_and_name_combined(self, **kwargs):
        # If arguments were passed, replace default values as necessary
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "path":
                    self.path = value
        # Call method to calculate and create (if necessary) log file and path
        self.log_file_path, self.log_file_name = self.create_log_file(self.path, self.name)
        # Return path to main program
        return os.path.join(self.log_file_path, self.log_file_name)