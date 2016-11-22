#!/usr/bin/python3
""" logic.py: Decision making engine for the RPi Home application
""" 

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import datetime
import logging
import multiprocessing
import time

from rpihome.modules.dst import USdst
from rpihome.modules.message import Message

from rpihome.rules import device_rpi
from rpihome.rules import device_wemo_fylt1
from rpihome.rules import device_wemo_bylt1
from rpihome.rules import device_wemo_ewlt1
from rpihome.rules import device_wemo_cclt1
from rpihome.rules import device_wemo_lrlt1
from rpihome.rules import device_wemo_drlt1
from rpihome.rules import device_wemo_br1lt1
from rpihome.rules import device_wemo_br1lt2
from rpihome.rules import device_wemo_br2lt1
from rpihome.rules import device_wemo_br2lt2
from rpihome.rules import device_wemo_br3lt1
from rpihome.rules import device_wemo_br3lt2


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Process Class ***********************************************************************************
class LogicProcess(multiprocessing.Process):
    """ WEMO gateway process class and methods """
    def __init__(self, **kwargs):
        # Set default input parameter values
        self.name = "undefined"
        self.msg_in_queue = multiprocessing.Queue(-1)
        self.msg_out_queue = multiprocessing.Queue(-1)
        self.logfile = "logfile"
        self.log_remote = False    
        # Update default elements based on any parameters passed in
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "msgin":
                    self.msg_in_queue = value
                if key == "msgout":
                    self.msg_out_queue = value
                if key == "logqueue":
                    self.log_queue = value
                if key == "logfile":
                    self.logfile = value
                if key == "logremote":
                    self.log_remote = value
        # Initialize parent class    
        multiprocessing.Process.__init__(self, name=self.name)
        # Create remaining class elements
        self.work_queue = multiprocessing.Queue(-1)
        self.msg_in = Message()
        self.msg_to_process = Message()
        self.msg_to_send = Message()
        self.last_hb = datetime.datetime.now()
        self.last_forecast_update = datetime.datetime.now() + datetime.timedelta(minutes=-15)
        self.dst = USdst()
        self.utc_offset = datetime.timedelta(hours=0)
        self.in_msg_loop = bool()
        self.main_loop = bool()
        self.close_pending = False
        #self.create_devices()
        self.create_home_flags()


    def configure_local_logger(self):
        """ Method to configure local logging """
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False         
        self.handler = logging.handlers.TimedRotatingFileHandler(self.logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
        self.formatter = logging.Formatter('%(processName)-16s |  %(asctime)-24s |  %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.logger.debug("Logging handler for %s process started", self.name)


    def kill_logger(self):
        """ Shut down logger when process exists """
        self.handlers = list(self.logger.handlers)
        for i in iter(self.handlers):
            self.logger.removeHandler(i)
            i.flush()
            i.close()


    def create_devices(self):
        """ Create devices in home """
        self.rpi_screen = device_rpi.RPImain("rpi", self.msg_out_queue)
        self.wemo_fylt1 = device_wemo_fylt1.Wemo_fylt1("fylt1", "192.168.86.21", self.msg_out_queue, self.logger)
        self.wemo_bylt1 = device_wemo_bylt1.Wemo_bylt1("bylt1", "192.168.86.22", self.msg_out_queue, self.logger)
        self.wemo_ewlt1 = device_wemo_ewlt1.Wemo_ewlt1("ewlt1", "192.168.86.23", self.msg_out_queue, self.logger)
        self.wemo_cclt1 = device_wemo_cclt1.Wemo_cclt1("cclt1", "192.168.86.24", self.msg_out_queue, self.logger)
        self.wemo_lrlt1 = device_wemo_lrlt1.Wemo_lrlt1("lrlt1", "192.168.86.25", self.msg_out_queue, self.logger)
        self.wemo_drlt1 = device_wemo_drlt1.Wemo_drlt1("drlt1", "192.168.86.26", self.msg_out_queue, self.logger)
        self.wemo_br1lt1 = device_wemo_br1lt1.Wemo_br1lt1(
            "br1lt1", "192.168.86.27", self.msg_out_queue, self.logger)
        self.wemo_br1lt2 = device_wemo_br1lt2.Wemo_br1lt2(
            "br1lt2", "192.168.86.28", self.msg_out_queue, self.logger)
        self.wemo_br2lt1 = device_wemo_br2lt1.Wemo_br2lt1(
            "br2lt1", "192.168.86.29", self.msg_out_queue, self.logger)
        self.wemo_br2lt2 = device_wemo_br2lt2.Wemo_br2lt2(
            "br2lt2", "192.168.86.30", self.msg_out_queue, self.logger)
        self.wemo_br3lt1 = device_wemo_br3lt1.Wemo_br3lt1(
            "br3lt1", "192.168.86.31", self.msg_out_queue, self.logger)
        self.wemo_br3lt2 = device_wemo_br3lt2.Wemo_br3lt2(
            "br3lt2", "192.168.86.32", self.msg_out_queue, self.logger)


    def create_home_flags(self):
        """ Create an array of home/away values and an array of datetimes indicating when users
        got home """
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.now() + datetime.timedelta(minutes=-15),
                         datetime.datetime.now() + datetime.timedelta(minutes=-15),
                         datetime.datetime.now() + datetime.timedelta(minutes=-15)]


    def update_forecast(self):
        """ Requests a forecast update from the nest module """
        self.msg_to_send = Message(source="11", dest="17", type="020")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Requesting current weather status update from NEST [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="11", dest="17", type="021")        
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Requesting current weather status update from NEST [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="11", dest="17", type="022")        
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Requesting current weather status update from NEST [%s]", self.msg_to_send.raw)       
        self.last_forecast_update = datetime.datetime.now()


    def process_in_msg_queue(self):
        """ Method to cycle through incoming message queue, filtering out heartbeats and
        mis-directed messages.  Messages corrected destined for this process are loaded
        into the work queue """
        self.in_msg_loop = True
        while self.in_msg_loop is True:
            try:
                self.msg_in = Message(raw=self.msg_in_queue.get_nowait())
            except:
                self.in_msg_loop = False
            if len(self.msg_in.raw) > 4:
                self.logger.debug("Processing message [%s] from incoming message queue" % self.msg_in.raw)                
                if self.msg_in.dest == "11":
                    if self.msg_in.type == "001":
                        self.last_hb = datetime.datetime.now()
                    elif self.msg_in.type == "999":
                        self.logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in.raw)
                        self.logger.debug("Moving message [%s] over to internal work queue", self.msg_in.raw)                        
                    self.msg_in = str()
                else:
                    self.msg_out_queue.put_nowait(self.msg_in.raw)
                    self.logger.debug("Redirecting message [%s] back to main" % self.msg_in.raw)                    
                self.msg_in = Message()
            else:
                self.in_msg_loop = False


    def process_work_queue(self):
        """ Method to perform work from the work queue """
        # Get next message from internal queue or timeout trying to do so
        try:
            self.msg_to_process = Message(raw=self.work_queue.get_nowait())
        except:
            pass
        # If there is a message to process, do so
        if len(self.msg_to_process.raw) > 4:
            self.logger.debug("Processing message [%s] from internal work queue" % self.msg_to_process.raw)
            # Process user "home/away" messages
            if self.msg_to_process.type == "100":
                if self.msg_to_process.name == "user1":
                    if self.msg_to_process.payload == "0":
                        self.homeArray[0] = False
                        self.logger.debug("User1 is no longer home")
                    elif self.msg_to_process.payload == "1":
                        self.homeArray[0] = True
                        self.logger.debug("User1 is home")
                if self.msg_to_process.name == "user2":
                    if self.msg_to_process.payload == "0":
                        self.homeArray[1] = False
                        self.logger.debug("User2 is no longer home")
                    elif self.msg_to_process.payload == "1":
                        self.homeArray[1] = True
                        self.logger.debug("User2 is home")
                if self.msg_to_process.name == "user3":
                    if self.msg_to_process.payload == "0":
                        self.homeArray[2] = False
                        self.logger.debug("User3 is no longer home")
                    elif self.msg_to_process.payload == "1":
                        self.homeArray[2] = True
                        self.logger.debug("User3 is home")
            # Process device create messages                                        
            elif self.msg_to_process.type == "168":
                self.create_devices()
            else:
                pass
            # Clear message once all possibilities are checked
            self.msg_to_process = Message()
        else:
            pass


    def check_dst(self):
        """ Determine DST offset based on current time/date """
        if self.dst.is_active(datetime=datetime.datetime.now()) is True:
            self.utc_offset = datetime.timedelta(hours=-5)
        else:
            self.utc_offset = datetime.timedelta(hours=-6)
        return self.utc_offset


    def run_automation(self):
        """ Run automation rule checks for automatic device output state control """
        self.rpi_screen.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray)
        self.wemo_fylt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_bylt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_ewlt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0),
                                    homeTime=self.homeTime)
        self.wemo_cclt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_lrlt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_drlt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_br1lt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_br1lt2.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_br2lt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_br2lt2.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_br3lt1.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))
        self.wemo_br3lt2.check_rules(datetime=datetime.datetime.now(),
                                    homeArray=self.homeArray,
                                    utcOffset=self.utc_offset,
                                    sunriseOffset=datetime.timedelta(minutes=0),
                                    sunsetOffset=datetime.timedelta(minutes=0))


    def run_commands(self):                                    
        """ Monitor desired command state and send commands to target device when COS occurs """
        self.rpi_screen.command()
        self.wemo_fylt1.command()
        self.wemo_bylt1.command()
        self.wemo_ewlt1.command()
        self.wemo_cclt1.command()
        self.wemo_lrlt1.command()
        self.wemo_drlt1.command()
        self.wemo_br1lt1.command()
        self.wemo_br1lt2.command()
        self.wemo_br2lt1.command()
        self.wemo_br2lt2.command()
        self.wemo_br3lt1.command()
        self.wemo_br3lt2.command()


    def run(self):
        """ Actual process loop.  Runs whenever start() method is called """
        # Configure logging
        self.configure_local_logger()
        # Create devices
        self.create_devices()
        # Main process loop        
        self.main_loop = True
        while self.main_loop is True:
            # Process incoming messages
            self.process_in_msg_queue()

            # Process tasks in internal work queue
            if self.close_pending is False:
                self.process_work_queue()
                self.check_dst()
                self.run_automation()
                self.run_commands()
                if datetime.datetime.now() > self.last_forecast_update + datetime.timedelta(minutes=15):
                    self.update_forecast()

            # Close process
            if (self.close_pending is True or
                    datetime.datetime.now() > self.last_hb + datetime.timedelta(seconds=30)):
                self.main_loop = False

            # Pause before next process run
            time.sleep(0.097)

        # Shut down logger before exiting process
        self.kill_logger()
