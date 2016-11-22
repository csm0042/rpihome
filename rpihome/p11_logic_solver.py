#!/usr/bin/python3
""" logic.py: Decision making engine for the RPi Home application
""" 

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import logging
import multiprocessing
import os, sys
import time
import modules.dst as dst
import modules.message as message
import rules.device_rpi as device_rpi
import rules.device_wemo_fylt1 as device_wemo_fylt1
import rules.device_wemo_bylt1 as device_wemo_bylt1
import rules.device_wemo_ewlt1 as device_wemo_ewlt1
import rules.device_wemo_cclt1 as device_wemo_cclt1
import rules.device_wemo_lrlt1 as device_wemo_lrlt1
import rules.device_wemo_drlt1 as device_wemo_drlt1
import rules.device_wemo_br1lt1 as device_wemo_br1lt1
import rules.device_wemo_br1lt2 as device_wemo_br1lt2
import rules.device_wemo_br2lt1 as device_wemo_br2lt1
import rules.device_wemo_br2lt2 as device_wemo_br2lt2
import rules.device_wemo_br3lt1 as device_wemo_br3lt1
import rules.device_wemo_br3lt2 as device_wemo_br3lt2


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Set up local logging ****************************************************************************
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
logfile = os.path.join(os.path.dirname(sys.argv[0]), ("logs/" + __name__ + ".log"))
handler = logging.handlers.TimedRotatingFileHandler(logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
formatter = logging.Formatter('%(processName)-16s,  %(asctime)-24s,  %(levelname)-8s, %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug("Logging handler for %s started", __name__)


# Process Class ***********************************************************************************
class LogicProcess(multiprocessing.Process):
    """ WEMO gateway process class and methods """
    def __init__(self, **kwargs):
        # Set default input parameter values
        self.name = "undefined"
        self.msg_in_queue = multiprocessing.Queue(-1)
        self.msg_out_queue = multiprocessing.Queue(-1)   
        # Update default elements based on any parameters passed in
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "msgin":
                    self.msg_in_queue = value
                if key == "msgout":
                    self.msg_out_queue = value
        # Initialize parent class    
        multiprocessing.Process.__init__(self, name=self.name)
        # Create remaining class elements
        self.work_queue = multiprocessing.Queue(-1)
        self.msg_in = message.Message()
        self.msg_to_process = message.Message()
        self.msg_to_send = message.Message()
        self.last_hb = datetime.datetime.now()
        self.last_forecast_update = datetime.datetime.now() + datetime.timedelta(minutes=-15)
        self.dst = dst.USdst()
        self.utc_offset = datetime.timedelta(hours=0)
        self.in_msg_loop = bool()
        self.main_loop = bool()
        self.close_pending = False
        #self.create_devices()
        self.create_home_flags()


    def create_devices(self):
        """ Create devices in home """
        self.rpi_screen = device_rpi.RPImain("rpi", self.msg_out_queue)
        self.wemo_fylt1 = device_wemo_fylt1.Wemo_fylt1("fylt1", "192.168.86.21", self.msg_out_queue, logger)
        self.wemo_bylt1 = device_wemo_bylt1.Wemo_bylt1("bylt1", "192.168.86.22", self.msg_out_queue, logger)
        self.wemo_ewlt1 = device_wemo_ewlt1.Wemo_ewlt1("ewlt1", "192.168.86.23", self.msg_out_queue, logger)
        self.wemo_cclt1 = device_wemo_cclt1.Wemo_cclt1("cclt1", "192.168.86.24", self.msg_out_queue, logger)
        self.wemo_lrlt1 = device_wemo_lrlt1.Wemo_lrlt1("lrlt1", "192.168.86.25", self.msg_out_queue, logger)
        self.wemo_drlt1 = device_wemo_drlt1.Wemo_drlt1("drlt1", "192.168.86.26", self.msg_out_queue, logger)
        self.wemo_br1lt1 = device_wemo_br1lt1.Wemo_br1lt1(
            "br1lt1", "192.168.86.27", self.msg_out_queue, logger)
        self.wemo_br1lt2 = device_wemo_br1lt2.Wemo_br1lt2(
            "br1lt2", "192.168.86.28", self.msg_out_queue, logger)
        self.wemo_br2lt1 = device_wemo_br2lt1.Wemo_br2lt1(
            "br2lt1", "192.168.86.29", self.msg_out_queue, logger)
        self.wemo_br2lt2 = device_wemo_br2lt2.Wemo_br2lt2(
            "br2lt2", "192.168.86.30", self.msg_out_queue, logger)
        self.wemo_br3lt1 = device_wemo_br3lt1.Wemo_br3lt1(
            "br3lt1", "192.168.86.31", self.msg_out_queue, logger)
        self.wemo_br3lt2 = device_wemo_br3lt2.Wemo_br3lt2(
            "br3lt2", "192.168.86.32", self.msg_out_queue, logger)


    def create_home_flags(self):
        """ Create an array of home/away values and an array of datetimes indicating when users
        got home """
        self.homeArray = [False, False, False]
        self.homeTime = [datetime.datetime.now() + datetime.timedelta(minutes=-15),
                         datetime.datetime.now() + datetime.timedelta(minutes=-15),
                         datetime.datetime.now() + datetime.timedelta(minutes=-15)]


    def update_forecast(self):
        """ Requests a forecast update from the nest module """
        self.msg_to_send = message.Message(source="11", dest="17", type="020")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        logger.debug("Requesting current weather status update from NEST [%s]", self.msg_to_send.raw)
        self.msg_to_send = message.Message(source="11", dest="17", type="021")        
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        logger.debug("Requesting current weather status update from NEST [%s]", self.msg_to_send.raw)
        self.msg_to_send = message.Message(source="11", dest="17", type="022")        
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        logger.debug("Requesting current weather status update from NEST [%s]", self.msg_to_send.raw)       
        self.last_forecast_update = datetime.datetime.now()


    def process_in_msg_queue(self):
        """ Method to cycle through incoming message queue, filtering out heartbeats and
        mis-directed messages.  Messages corrected destined for this process are loaded
        into the work queue """
        self.in_msg_loop = True
        while self.in_msg_loop is True:
            try:
                self.msg_in = message.Message(raw=self.msg_in_queue.get_nowait())
            except:
                self.in_msg_loop = False
            if len(self.msg_in.raw) > 4:
                logger.debug("Processing message [%s] from incoming message queue" % self.msg_in.raw)                
                if self.msg_in.dest == "11":
                    if self.msg_in.type == "001":
                        self.last_hb = datetime.datetime.now()
                    elif self.msg_in.type == "999":
                        logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Moving message [%s] over to internal work queue", self.msg_in.raw)                        
                    self.msg_in = str()
                else:
                    self.msg_out_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Redirecting message [%s] back to main" % self.msg_in.raw)                    
                self.msg_in = message.Message()
            else:
                self.in_msg_loop = False


    def process_work_queue(self):
        """ Method to perform work from the work queue """
        # Get next message from internal queue or timeout trying to do so
        try:
            self.msg_to_process = message.Message(raw=self.work_queue.get_nowait())
        except:
            pass
        # If there is a message to process, do so
        if len(self.msg_to_process.raw) > 4:
            logger.debug("Processing message [%s] from internal work queue" % self.msg_to_process.raw)
            # Process user "home/away" messages
            if self.msg_to_process.type == "100":
                if self.msg_to_process.name == "user1":
                    if self.msg_to_process.payload == "0":
                        self.homeArray[0] = False
                        logger.debug("User1 is no longer home")
                    elif self.msg_to_process.payload == "1":
                        self.homeArray[0] = True
                        logger.debug("User1 is home")
                if self.msg_to_process.name == "user2":
                    if self.msg_to_process.payload == "0":
                        self.homeArray[1] = False
                        logger.debug("User2 is no longer home")
                    elif self.msg_to_process.payload == "1":
                        self.homeArray[1] = True
                        logger.debug("User2 is home")
                if self.msg_to_process.name == "user3":
                    if self.msg_to_process.payload == "0":
                        self.homeArray[2] = False
                        logger.debug("User3 is no longer home")
                    elif self.msg_to_process.payload == "1":
                        self.homeArray[2] = True
                        logger.debug("User3 is home")
            # Process device create messages                                        
            elif self.msg_to_process.type == "168":
                self.create_devices()
            else:
                pass
            # Clear message once all possibilities are checked
            self.msg_to_process = message.Message()
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
        pass
