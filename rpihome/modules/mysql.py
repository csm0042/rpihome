#!/usr/bin/python3
""" mysql.py: Class and methods to connect to and query a mySQL database
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import logging
import mysql.connector
import mysql.connector.errorcode as errorcode


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Define mySQL interface Class ****************************************************************************************
class MySQLinterface(object):
    """ The Occupancy task is uses a combination of a mySQL database and standard ARP commands to determine if a device
    is present on a network.  A list of devices and their MAC IDs is first obtained from a table in the mySQL database,
    then those addresses are compared against the results of an ARP command.  If a match is found, the device is
    considered "present", otherwise it's considered not-present in the system.  Each time this check is performed, the
    result of the check is written back to each device record in the mySQL table along with a timestamp indicating the
    last time the check was performed"""

    def __init__(self, **kwargs):
        """ Declare instance elements and set default values"""
        self._host = "localhost"
        self._database = "db"
        self._user = "user"
        self._password = "password"
        self._connected = False
        self.db = mysql.connector.connect()
        self.query_to_run = str()
        self.results = []

        # Update default elements based on any parameters passed in
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "host":
                    self.host = value
                if key == "database":
                    self.database = value
                if key == "user":
                    self.user = value
                if key == "password":
                    self.password = value

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = str(value)

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        self._database = str(value)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = str(value)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = str(value)

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        if value is True or str(value).lower == "true":
            self._connected = True
        elif value is False or str(value).lower == "false":
            self._connected = False
        pass
#

    def connect(self):
        """ Establishes an active connection to the mySQL database using the parameters passed in """
        try:
            self.db = mysql.connector.connect(host=self.host, database=self.database,
                                              user=self.user, password=self.password)
            self.connected = True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.connected = False
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.connected = False
            else:
                self.connected = False
            pass
        return self.db
#

    def query(self):
        """ Runs a query passed in from external program """
        logging.info(self.query_to_run)
        self.results = []

        if self.connected is True:
            cursor = self.db.cursor()
            cursor.execute(self.query_to_run)
            try:
                self.results = cursor.fetchall()
                logging.info(self.results)
            except:
                pass
            self.db.commit()
            cursor.close()
        else:
            logging.info("connection error")

        return self.results
#

    def close(self):
        """ Closes connection to the mySQL database when called """
        try:
            self.db.close()
            self.connected = False
        except:
            logging.info("error attempting to close database")
        return True


# Run as Script when called as Main ***********************************************************************************
if __name__ == "__main__":
    host="192.168.42.201"
    database="mauehome"
    user="python"
    password="python"

    record = ()
    record_list = []
    db_interface = MySQLinterface(host=host, database=database, user=user, password=password)
    db = db_interface.connect()

    if db_interface.connected is True:
        db_interface.query_to_run = "SELECT name, address, status, lastupdate FROM users"
        result_list = db_interface.query()
        print(result_list)
    else:
        print("could not connect")
