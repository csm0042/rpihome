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

if __name__ == "__main__":
    sys.path.append("..")
    
from rpihome.modules.log_path import LogFilePath
from rpihome.modules.multiprocess_logging import listener_configurer, worker_configurer
from rpihome.p01_log_handler import listener_process
from rpihome.p02_gui import MainWindow
from rpihome.p11_logic_solver import LogicProcess
from rpihome.p13_home_away import HomeProcess
from rpihome.p15_rpi_screen import RpiProcess
from rpihome.p16_wemo_gateway import WemoProcess
from rpihome.p17_nest_gateway import NestProcess




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
        self.msg_in = str()
        self.msg_to_process = str()
        self.last_hb = datetime.datetime.now()
        self.in_msg_loop = True
        self.main_loop = True
        self.work_queue = multiprocessing.Queue(-1)
        self.close_pending = False
        self.process_path = os.path.dirname(sys.argv[0])
        self.logfile = LogFilePath().return_path_and_name_combined(
            name="p01", path=self.process_path)
        self.enable = [
            True, True, True, False, False, False, False, False, False, False, False, True, False,
            True, False, True, True, True]
        self.nest_username = str()
        self.nest_password = str()
        # Spawn individual processes
        self.create_process_queues()
        self.create_remote_log_handler_process()
        self.configure_remote_logger()
        self.create_gui_process()
        self.create_logic_process()
        self.create_home_process()
        self.create_screen_process()
        self.create_wemo_process()
        self.create_nest_process()
        self.update_gui()
        self.init_complete = True


    def create_process_queues(self):
        """ Create queues used for inter-process communication """
        self.p00_queue = multiprocessing.Queue(-1)
        self.p01_queue = multiprocessing.Queue(-1)


    def configure_remote_logger(self):
        """ Method to configure multiprocess logging """
        self.logger = logging.getLogger(self.name)        
        handler = logging.handlers.QueueHandler(self.p01_queue)
        self.logger.addHandler(handler)
        self.logger.debug("Logging handler for %s process started", "p00_main")


    def configure_local_logger(self):
        """ Method to configure local logging """
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.handlers.TimedRotatingFileHandler(self.logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
        formatter = logging.Formatter('%(processName)-16s |  %(asctime)-24s |  %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.debug("Logging handler for %s process started", self.name)        


    def kill_local_logger(self):
        """ Shut down logger when process exists """
        self.handlers = list(self.logger.handlers)
        for i in iter(self.handlers):
            self.logger.removeHandler(i)
            i.flush()
            i.close()


    def create_remote_log_handler_process(self):
        """ Creates a separate process to run the multiprocess logger.  This Process
        monitors a shared queue and writes those log messages to a file """
        self.p01_alive_mem = None
        self.p01 = multiprocessing.Process(name="p01_log_handler",
                                           target=listener_process,
                                           args=(self.p01_queue, self.p00_queue,
                                                 listener_configurer, self.logfile))
        self.p01.start()
        self.p01_modtime = os.path.getmtime(os.path.join(self.process_path, "p01_log_handler.py"))
            


    def create_gui_process(self):
        """ Spawns a process specific to the user interface """
        self.p02_alive_mem = None
        self.p02_queue = multiprocessing.Queue(-1)
        self.p02 = MainWindow(name="p02_gui",
                              msgin=self.p02_queue,
                              msgout=self.p00_queue,
                              logfile=(LogFilePath().return_path_and_name_combined(
                                  name="p02",
                                  path=self.process_path)),
                              displayfile=(LogFilePath().return_path_and_name_combined(
                                  name="p11",
                                  path=self.process_path)),
                              enable=self.enable,
                              logremote=False)
        self.p02.start()
        self.p02_modtime = os.path.getmtime(os.path.join(self.process_path, "p02_gui.py"))


    def create_logic_process(self):
        """ Spawns a process for the logic solver """
        self.p11_alive_mem = None
        self.p11_queue = multiprocessing.Queue(-1)
        self.p11 = LogicProcess(name="p11_logic_solver",
                                msgin=self.p11_queue,
                                msgout=self.p00_queue,
                                logfile=(LogFilePath().return_path_and_name_combined(
                                    name="p11",
                                    path=self.process_path)),
                                    logremote=False)
        self.p11.start()
        self.p11_modtime = os.path.getmtime(os.path.join(self.process_path, "p11_logic_solver.py"))


    def create_home_process(self):
        """ Spawns a process for the home/away monitor """
        self.p13_alive_mem = None
        self.p13_queue = multiprocessing.Queue(-1)
        self.p13 = HomeProcess(name="p13_home_away",
                                msgin=self.p13_queue,
                                msgout=self.p00_queue,
                                logfile=(LogFilePath().return_path_and_name_combined(
                                    name="p13",
                                    path=self.process_path)),
                                    logremote=False)
        self.p13.start()        
        self.p13_modtime = os.path.getmtime(os.path.join(self.process_path, "p13_home_away.py"))


    def create_screen_process(self):
        """ Spawns a process for the home/away monitor """
        self.p15_alive_mem = None
        self.p15_queue = multiprocessing.Queue(-1)
        self.p15 = RpiProcess(name="p15_rpi_screen",
                                msgin=self.p15_queue,
                                msgout=self.p00_queue,
                                logfile=(LogFilePath().return_path_and_name_combined(
                                    name="p15",
                                    path=self.process_path)),
                                    logremote=False)
        self.p15.start()         
        self.p15_modtime = os.path.getmtime(os.path.join(self.process_path, "p15_rpi_screen.py"))


    def create_wemo_process(self):
        """ Spawns a process for the wemo communication gateway """
        self.p16_alive_mem = None
        self.p16_queue = multiprocessing.Queue(-1)
        self.p16 = WemoProcess(name="p16_wemo_gateway",
                                msgin=self.p16_queue,
                                msgout=self.p00_queue,
                                logfile=(LogFilePath().return_path_and_name_combined(
                                    name="p16",
                                    path=self.process_path)),
                                    logremote=False)
        self.p16.start()          
        self.p16_modtime = os.path.getmtime(os.path.join(self.process_path, "p16_wemo_gateway.py"))


    def create_nest_process(self):
        """ Spawns a process for the NEST communication gateway """
        self.p17_alive_mem = None
        self.p17_queue = multiprocessing.Queue(-1)
        self.p17 = NestProcess(name="p17_nest_gateway",
                                msgin=self.p17_queue,
                                msgout=self.p00_queue,
                                logfile=(LogFilePath().return_path_and_name_combined(
                                    name="p17",
                                    path=self.process_path)),
                                    logremote=False)
        self.p17.start()
        self.p17_modtime = os.path.getmtime(os.path.join(self.process_path, "p17_nest_gateway.py"))


    def process_in_msg_queue(self):
        """ Method to cycle through incoming message queue, filtering out heartbeats and
        mis-directed messages.  Messages corrected destined for this process are loaded
        into the work queue """
        self.in_msg_loop = True
        while self.in_msg_loop is True:
            try:
                self.msg_in = self.p00_queue.get_nowait()
            except:
                self.in_msg_loop = False
            if len(self.msg_in) != 0:
                if self.msg_in[3:5] == "00":
                    if self.msg_in[6:9] == "001":
                        self.last_hb = datetime.datetime.now()
                        self.logger.debug("heartbeat received")
                    elif self.msg_in[6:9] == "999":
                        self.logger.debug("Kill code received - Shutting down")
                        self.close_pending = True
                        self.in_msg_loop = False
                    else:
                        self.work_queue.put_nowait(self.msg_in)
                    self.msg_in = str()
                # Message forwarding to p01
                elif self.msg_in[3:5] == "01":
                    self.p01_queue.put_nowait(self.msg_in)
                    if self.msg_in[6:9] == "900" or self.msg_in[6:9] == "999":
                        self.work_queue.put_nowait(self.msg_in)
                # Message forwarding to p01
                elif self.msg_in[3:5] == "02":
                    self.p02_queue.put_nowait(self.msg_in)
                    if self.msg_in[6:9] == "900" or self.msg_in[6:9] == "999":
                        self.work_queue.put_nowait(self.msg_in)
                # Message forwarding to p11
                elif self.msg_in[3:5] == "11":
                    self.p11_queue.put_nowait(self.msg_in)
                    if self.msg_in[6:9] == "900" or self.msg_in[6:9] == "999":
                        self.work_queue.put_nowait(self.msg_in)
                # Message forwarding to p13
                elif self.msg_in[3:5] == "13":
                    self.p13_queue.put_nowait(self.msg_in)
                    if self.msg_in[6:9] == "900" or self.msg_in[6:9] == "999":
                        self.work_queue.put_nowait(self.msg_in)
                # Message forwarding to p15
                elif self.msg_in[3:5] == "15":
                    self.p15_queue.put_nowait(self.msg_in)
                    if self.msg_in[6:9] == "900" or self.msg_in[6:9] == "999":
                        self.work_queue.put_nowait(self.msg_in)
                # Message forwarding to p16
                elif self.msg_in[3:5] == "16":
                    self.p16_queue.put_nowait(self.msg_in)
                    if self.msg_in[6:9] == "900" or self.msg_in[6:9] == "999":
                        self.work_queue.put_nowait(self.msg_in)
                # Message forwarding to p17
                elif self.msg_in[3:5] == "17":
                    self.p17_queue.put_nowait(self.msg_in)
                    if self.msg_in[6:9] == "900" or self.msg_in[6:9] == "999":
                        self.work_queue.put_nowait(self.msg_in)
                self.msg_in = str()
            else:
                self.in_msg_loop = False


    def process_work_queue(self):
        """ Method to perform work from the work queue """
        try:
            self.msg_to_process = self.work_queue.get_nowait()
        except:
            pass
        # If there is a message to process, do so
        if len(self.msg_to_process) != 0:
            # Start / Stop p01 process
            if self.msg_to_process[3:5] == "01":
                if self.msg_to_process[6:9] == "900":
                    if self.p01.is_alive() is False:
                        self.create_remote_log_handler_process()
                elif self.msg_to_process[6:9] == "999":
                    if self.p01.is_alive():                    
                        self.p01.join()
            # Start / Stop p11 process
            elif self.msg_to_process[3:5] == "11":
                if self.msg_to_process[6:9] == "900":
                    if self.p11.is_alive() is False:                    
                        self.create_logic_process()
                elif self.msg_to_process[6:9] == "999":
                    if self.p11.is_alive():                    
                        self.p11.join()
            # Start / Stop p13 process
            elif self.msg_to_process[3:5] == "13":
                if self.msg_to_process[6:9] == "900":
                    if self.p13.is_alive() is False:                    
                        self.create_home_process()
                elif self.msg_to_process[6:9] == "999":
                    if self.p13.is_alive():
                        self.p13.join()
            # Start / Stop p15 process
            elif self.msg_to_process[3:5] == "15":
                if self.msg_to_process[6:9] == "900":
                    if self.p15.is_alive() is False:                    
                        self.create_screen_process()
                elif self.msg_to_process[6:9] == "999":
                    if self.p15.is_alive():                    
                        self.p15.join()   
            # Start / Stop p16 process
            elif self.msg_to_process[3:5] == "16":
                if self.msg_to_process[6:9] == "900":
                    if self.p16.is_alive() is False:                    
                        self.create_wemo_process()
                elif self.msg_to_process[6:9] == "999":
                    if self.p16.is_alive():                    
                        self.p16.join()
            # Start / Stop p17 process
            elif self.msg_to_process[3:5] == "17":
                if self.msg_to_process[6:9] == "900":
                    if self.p17.is_alive() is False:                    
                        self.create_nest_process()
                elif self.msg_to_process[6:9] == "999":
                    if self.p17.is_alive():
                        self.p17.join()                                      
            # Clear msg-to-process string
            self.msg_to_process = str()
        else:
            pass


    def send_heartbeats(self):
        """ Send periodic heartbeats to child processes so they don't time-out and shutdown """
        self.p01_queue.put_nowait("00,01,001")
        self.p02_queue.put_nowait("00,02,001")
        self.p11_queue.put_nowait("00,11,001")
        self.p13_queue.put_nowait("00,13,001")
        self.p15_queue.put_nowait("00,15,001")
        self.p16_queue.put_nowait("00,16,001")
        self.p17_queue.put_nowait("00,17,001")
        self.last_hb = datetime.datetime.now()


    def update_gui(self):
        """ Monitor processes as they are spawned / die and send messages to gui to
        update display """
        if self.p01.is_alive() != self.p01_alive_mem:
            if self.p01.is_alive() is True:
                self.p02_queue.put_nowait("01,02,002")
                self.p01_alive_mem = True
            elif self.p01.is_alive() is False:
                self.p02_queue.put_nowait("01,02,003")
                self.p01_alive_mem = False
        if self.p11.is_alive() != self.p11_alive_mem:
            if self.p11.is_alive() is True:
                self.p02_queue.put_nowait("11,02,002")
                self.p11_alive_mem = True
            elif self.p11.is_alive() is False:
                self.p02_queue.put_nowait("11,02,003")
                self.p11_alive_mem = False
        if self.p13.is_alive() != self.p13_alive_mem:
            if self.p13.is_alive() is True:
                self.p02_queue.put_nowait("13,02,002")
                self.p13_alive_mem = True
            elif self.p13.is_alive() is False:
                self.p02_queue.put_nowait("13,02,003")
                self.p13_alive_mem = False
        if self.p15.is_alive() != self.p15_alive_mem:
            if self.p15.is_alive() is True:
                self.p02_queue.put_nowait("15,02,002")
                self.p15_alive_mem = True
            elif self.p15.is_alive() is False:
                self.p02_queue.put_nowait("15,02,003")
                self.p15_alive_mem = False
        if self.p16.is_alive() != self.p16_alive_mem:
            if self.p16.is_alive() is True:
                self.p02_queue.put_nowait("16,02,002")
                self.p16_alive_mem = True
            elif self.p16.is_alive() is False:
                self.p02_queue.put_nowait("16,02,003")
                self.p16_alive_mem = False
        if self.p17.is_alive() != self.p17_alive_mem:
            if self.p17.is_alive() is True:
                self.p02_queue.put_nowait("17,02,002")
                self.p17_alive_mem = True
            elif self.p17.is_alive() is False:
                self.p02_queue.put_nowait("17,02,003")
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
        self.kill_local_logger()



# Main Routine ************************************************************************************
def main():
    """ Main function called when run """
    p00 = MainProcess()
    p00.run()


# Run as Script ***********************************************************************************
if __name__ == "__main__":
    main()
