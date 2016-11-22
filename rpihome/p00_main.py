#!/usr/bin/python3
""" main.py:
    Main entry-point into the RPiHome application.
    When run, this application will create a log message queue and start a listener service which
    will monitor that queue and write to a file any log messages it finds.  This queue is shared
    with any sub-processes that are later called and allows all parts of this application to share
    a single log-file in a multi-processing-safe manner.  Once the log queue and listener process
    are started, the GUI is started.
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import datetime
import logging
import multiprocessing
import os
import sys
import time

if __name__ == "__main__": sys.path.append("..")
from modules.log_path import LogFilePath
from modules.message import Message
from modules.multiprocess_logging import listener_configurer, worker_configurer
from p02_gui import MainWindow
from p11_logic_solver import LogicProcess
from p13_home_away import HomeProcess
from p15_rpi_screen import RpiProcess
from p16_wemo_gateway import WemoProcess
from p17_nest_gateway import NestProcess


# Set up local logging *********************************************************************
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
logfile = os.path.join(os.path.dirname(sys.argv[0]), ("logs/" + __name__ + ".log"))
handler = logging.handlers.TimedRotatingFileHandler(logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
formatter = logging.Formatter('%(processName)-16s,  %(asctime)-24s,  %(levelname)-8s, %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug("Logging handler for %s started", __name__)


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Main Process Class Definition *******************************************************************
class MainProcess(object):
    """ This class runs the main process of rpihome application """
    def __init__(self):
        """ Regular init stuff """
        self.init_complete = False
        self.name = "p00_main"
        self.handlers = []
        self.msg_in = Message()
        self.msg_to_process = Message()
        self.msg_to_send = Message()
        self.last_hb = datetime.datetime.now()
        self.in_msg_loop = True
        self.main_loop = True
        self.p00_queue = multiprocessing.Queue(-1)
        self.work_queue = multiprocessing.Queue(-1)
        self.close_pending = False
        self.process_path = os.path.dirname(sys.argv[0])
        self.logfile = LogFilePath().return_path_and_name_combined(name="p01", path=self.process_path)
        self.enable = [True, False, True, False, False, False, False, False, False, False, False, True, False, True, False, True, True, True]
        self.nest_username = str()
        self.nest_password = str()
        # Spawn individual processes
        self.create_gui_process()
        self.create_logic_process()
        self.create_home_process()
        self.create_screen_process()
        self.create_wemo_process()
        self.create_nest_process()
        self.update_gui()
        self.init_complete = True


    def create_gui_process(self):
        """ Spawns a process specific to the user interface """
        self.p02_alive_mem = None
        self.p02_queue = multiprocessing.Queue(-1)
        self.p02 = MainWindow(name="p02_gui",
                              msgin=self.p02_queue,
                              msgout=self.p00_queue,
                              displayfile=(LogFilePath().return_path_and_name_combined(
                                  name="p11",
                                  path=self.process_path)),
                              enable=self.enable)
        self.p02.start()
        self.p02_modtime = os.path.getmtime(os.path.join(self.process_path, "p02_gui.py"))


    def create_logic_process(self):
        """ Spawns a process for the logic solver """
        self.p11_alive_mem = None
        self.p11_queue = multiprocessing.Queue(-1)
        self.p11 = LogicProcess(name="p11_logic_solver",
                                msgin=self.p11_queue,
                                msgout=self.p00_queue)
        self.p11.start()
        self.p11_modtime = os.path.getmtime(os.path.join(self.process_path, "p11_logic_solver.py"))


    def create_home_process(self):
        """ Spawns a process for the home/away monitor """
        self.p13_alive_mem = None
        self.p13_queue = multiprocessing.Queue(-1)
        self.p13 = HomeProcess(name="p13_home_away",
                                msgin=self.p13_queue,
                                msgout=self.p00_queue)
        self.p13.start()        
        self.p13_modtime = os.path.getmtime(os.path.join(self.process_path, "p13_home_away.py"))


    def create_screen_process(self):
        """ Spawns a process for the home/away monitor """
        self.p15_alive_mem = None
        self.p15_queue = multiprocessing.Queue(-1)
        self.p15 = RpiProcess(name="p15_rpi_screen",
                                msgin=self.p15_queue,
                                msgout=self.p00_queue)
        self.p15.start()         
        self.p15_modtime = os.path.getmtime(os.path.join(self.process_path, "p15_rpi_screen.py"))


    def create_wemo_process(self):
        """ Spawns a process for the wemo communication gateway """
        self.p16_alive_mem = None
        self.p16_queue = multiprocessing.Queue(-1)
        self.p16 = WemoProcess(name="p16_wemo_gateway",
                                msgin=self.p16_queue,
                                msgout=self.p00_queue)
        self.p16.start()          
        self.p16_modtime = os.path.getmtime(os.path.join(self.process_path, "p16_wemo_gateway.py"))


    def create_nest_process(self):
        """ Spawns a process for the NEST communication gateway """
        self.p17_alive_mem = None
        self.p17_queue = multiprocessing.Queue(-1)
        self.p17 = NestProcess(name="p17_nest_gateway",
                                msgin=self.p17_queue,
                                msgout=self.p00_queue)
        self.p17.start()
        self.p17_modtime = os.path.getmtime(os.path.join(self.process_path, "p17_nest_gateway.py"))


    def process_in_msg_queue(self):
        """ Method to cycle through incoming message queue, filtering out heartbeats and
        mis-directed messages.  Messages corrected destined for this process are loaded
        into the work queue """
        self.in_msg_loop = True
        while self.in_msg_loop is True:
            try:
                self.msg_in = Message(raw=self.p00_queue.get_nowait())
            except:
                self.in_msg_loop = False
            if len(self.msg_in.raw) > 4:
                if self.msg_in.dest == "00":
                    if self.msg_in.type == "001":
                        self.last_hb = datetime.datetime.now()
                        logger.debug("heartbeat received")
                    elif self.msg_in.type == "999":
                        logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Transfered message [%s] to internal work queue", self.msg_in.raw)
                # Message forwarding to p02
                elif self.msg_in.dest == "02":
                    self.p02_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Transfered message [%s] to p02 queue", self.msg_in.raw)
                    if self.msg_in.type == "900" or self.msg_in.type == "999":
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Transfered message [%s] to internal work queue", self.msg_in.raw)
                # Message forwarding to p11
                elif self.msg_in.dest == "11":
                    self.p11_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Transfered message [%s] to p11 queue", self.msg_in.raw)
                    if self.msg_in.type == "900" or self.msg_in.type == "999":
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Transfered message [%s] to internal work queue", self.msg_in.raw)
                # Message forwarding to p13
                elif self.msg_in.dest == "13":
                    self.p13_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Transfered message [%s] to p13 queue", self.msg_in.raw)
                    if self.msg_in.type == "900" or self.msg_in.type == "999":
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Transfered message [%s] to internal work queue", self.msg_in.raw)
                # Message forwarding to p15
                elif self.msg_in.dest == "15":
                    self.p15_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Transfered message [%s] to p15 queue", self.msg_in.raw)
                    if self.msg_in.type == "900" or self.msg_in.type == "999":
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Transfered message [%s] to internal work queue", self.msg_in.raw)
                # Message forwarding to p16
                elif self.msg_in.dest == "16":
                    self.p16_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Transfered message [%s] to p16 queue", self.msg_in.raw)
                    if self.msg_in.type == "900" or self.msg_in.type == "999":
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Transfered message [%s] to internal work queue", self.msg_in.raw)
                # Message forwarding to p17
                elif self.msg_in.dest == "17":
                    self.p17_queue.put_nowait(self.msg_in.raw)
                    logger.debug("Transfered message [%s] to p17 queue", self.msg_in.raw)
                    if self.msg_in.type == "900" or self.msg_in.type == "999":
                        self.work_queue.put_nowait(self.msg_in.raw)
                        logger.debug("Transfered message [%s] to internal work queue", self.msg_in.raw)
                self.msg_in = Message()
            else:
                self.in_msg_loop = False


    def process_work_queue(self):
        """ Method to perform work from the work queue """
        try:
            self.msg_to_process = Message(raw=self.work_queue.get_nowait())
        except:
            pass
        # If there is a message to process, do so
        if len(self.msg_to_process.raw) > 4:
            # Start / Stop p11 process
            if self.msg_to_process.dest == "11":
                if self.msg_to_process.type == "900":
                    if self.p11.is_alive() is False:                    
                        self.create_logic_process()
                elif self.msg_to_process.type == "999":
                    if self.p11.is_alive():                    
                        self.p11.join()
            # Start / Stop p13 process
            elif self.msg_to_process.dest == "13":
                if self.msg_to_process.type == "900":
                    if self.p13.is_alive() is False:                    
                        self.create_home_process()
                elif self.msg_to_process.type == "999":
                    if self.p13.is_alive():
                        self.p13.join()
            # Start / Stop p15 process
            elif self.msg_to_process.dest == "15":
                if self.msg_to_process.type == "900":
                    if self.p15.is_alive() is False:                    
                        self.create_screen_process()
                elif self.msg_to_process.type == "999":
                    if self.p15.is_alive():                    
                        self.p15.join()   
            # Start / Stop p16 process
            elif self.msg_to_process.dest == "16":
                if self.msg_to_process.type == "900":
                    if self.p16.is_alive() is False:                    
                        self.create_wemo_process()
                elif self.msg_to_process.type == "999":
                    if self.p16.is_alive():                    
                        self.p16.join()
            # Start / Stop p17 process
            elif self.msg_to_process.dest == "17":
                if self.msg_to_process.type == "900":
                    if self.p17.is_alive() is False:                    
                        self.create_nest_process()
                elif self.msg_to_process.type == "999":
                    if self.p17.is_alive():
                        self.p17.join()                                      
            # Clear msg-to-process string
            self.msg_to_process = Message()
        else:
            pass


    def send_heartbeats(self):
        """ Send periodic heartbeats to child processes so they don't time-out and shutdown """
        self.p02_queue.put_nowait(Message(source="00", dest="02", type="001").raw)
        self.p11_queue.put_nowait(Message(source="00", dest="11", type="001").raw)
        self.p13_queue.put_nowait(Message(source="00", dest="13", type="001").raw)
        self.p15_queue.put_nowait(Message(source="00", dest="15", type="001").raw)
        self.p16_queue.put_nowait(Message(source="00", dest="16", type="001").raw)
        self.p17_queue.put_nowait(Message(source="00", dest="17", type="001").raw)
        self.last_hb = datetime.datetime.now()


    def update_gui(self):
        """ Monitor processes as they are spawned / die and send messages to gui to
        update display """
        if self.p11.is_alive() != self.p11_alive_mem:
            if self.p11.is_alive() is True:
                self.p02_queue.put_nowait(Message(source="11", dest="02", type="002").raw)
                self.p11_alive_mem = True
            elif self.p11.is_alive() is False:
                self.p02_queue.put_nowait(Message(source="11", dest="02", type="003").raw)
                self.p11_alive_mem = False
        if self.p13.is_alive() != self.p13_alive_mem:
            if self.p13.is_alive() is True:
                self.p02_queue.put_nowait(Message(source="13", dest="02", type="002").raw)
                self.p13_alive_mem = True
            elif self.p13.is_alive() is False:
                self.p02_queue.put_nowait(Message(source="13", dest="02", type="003").raw)
                self.p13_alive_mem = False
        if self.p15.is_alive() != self.p15_alive_mem:
            if self.p15.is_alive() is True:
                self.p02_queue.put_nowait(Message(source="15", dest="02", type="002").raw)
                self.p15_alive_mem = True
            elif self.p15.is_alive() is False:
                self.p02_queue.put_nowait(Message(source="15", dest="02", type="003").raw)
                self.p15_alive_mem = False
        if self.p16.is_alive() != self.p16_alive_mem:
            if self.p16.is_alive() is True:
                self.p02_queue.put_nowait(Message(source="16", dest="02", type="002").raw)
                self.p16_alive_mem = True
            elif self.p16.is_alive() is False:
                self.p02_queue.put_nowait(Message(source="16", dest="02", type="003").raw)
                self.p16_alive_mem = False
        if self.p17.is_alive() != self.p17_alive_mem:
            if self.p17.is_alive() is True:
                self.p02_queue.put_nowait(Message(source="17", dest="02", type="002").raw)
                self.p17_alive_mem = True
            elif self.p17.is_alive() is False:
                self.p02_queue.put_nowait(Message(source="17", dest="02", type="003").raw)
                self.p17_alive_mem = False


    def run(self):
        """ Actual process loop.  Runs whenever start() method is called """
        self.main_loop = True
        while self.main_loop is True:
            # Process incoming messages
            self.process_in_msg_queue()

            # Process tasks in internal work queue
            if self.close_pending is False:
                self.process_work_queue()
                # Send periodic heartbeats to child processes
                if datetime.datetime.now() > (self.last_hb + datetime.timedelta(seconds=5)):
                    self.send_heartbeats()
                # Update gui based on process status
                self.update_gui()

            # Close process
            if self.close_pending is True or (
                    datetime.datetime.now() > (self.last_hb + datetime.timedelta(seconds=30))):
                self.main_loop = False

            # Pause before next process run
            time.sleep(0.011)

        # Shut down logger before exiting process
        pass



# Main Routine ************************************************************************************
def main():
    """ Main function called when run """
    p00 = MainProcess()
    p00.run()


# Run as Script ***********************************************************************************
if __name__ == "__main__":
    main()
