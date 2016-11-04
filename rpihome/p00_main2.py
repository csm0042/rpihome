#!/usr/bin/python3
""" main.py: Main entry-point into the RPiHome application.  
    When run, this application will create a log message queue and start a listener service which will monitor that queue
    and write to a file any log messages it finds.  This queue is shared with any sub-processes that are later called and
    allows all parts of this application to share a single log-file in a multi-processing-safe manner.
    Once the log queue and listener process are started, the GUI is started.  
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import logging
import multiprocessing
import os
import psutil
import sys
import time

from modules import log_path
from modules import multiprocess_logging

from p01_log_handler import listener
from p02_gui import gui_func
from p11_logic_solver import logic_func
from p12_db_interface import db_func
from p13_home_away import home_func
from p14_motion import motion_func
from p15_rpi_screen import screen_func
from p16_wemo_gateway import wemo_func
from p17_nest_gateway import nest_func


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Class Definition ****************************************************************************************************
class MyProcess(object):
    def __init__(self, name, function, args):
        self.process = self.create(name, function, args)    
        self.alive_mem = None   
        self.modTime = os.path.getmtime(os.path.join((os.path.dirname(sys.argv[0])), name, ".py"))
        self.modTimeLast = self.modtime

    def create(self, name, function, args):
        if self.is_alive() is False:
            self.process = multiprocessing.Process(name=name, target=function, args=args)
            self.process.daemon = True
        return self.process

    def checkModified(self):
        self.modTime = os.path.getmtime(os.path.join((os.path.dirname(sys.argv[0])), name, ".py"))
        if self.modTime != self.modTimeLast:
            pass
            # do stuff to bounce process

    def start(self):
        self.process.start()

    def stop(self):
        if self.process.is_alive() is True:
            self.process.join()    

    def is_alive(self):
        try:
            if self.process.is_alive() is True:
                return True
            else:
                return False
        except:
            return False


def main():
    # Decide what processes to enable
    enable = [True, True, True, False, False, False, False, False, False, False, False, True, False, True, False, True, True, False]

    # Get Nest login info if necessary
    if enable[17] is True:
        nestUsername = input("NEST Username: ")
        nestPassword = input("NEST Password: ")
  


    # Set location of log file and crate subfolder if necessary
    name="main"
    logfilepathgen = log_path.LogFilePath()
    logfile = logfilepathgen.return_path_and_name_combined(name=name, path=os.path.dirname(sys.argv[0]))
    process_path = os.path.dirname(sys.argv[0])

    # Start global log handler process - This process retrieves log messages from the shared log queue and writes them to a file    
    if enable[1] is True: 
        p01_queue = multiprocessing.Queue(-1)        
        p01 = MyProcess("p01_log_handler", listener, (p01_queue, p00_queue, multiprocess_logging.listener_configurer, name, logfile))
        p01.start()

    # Start gui process to spawn the user interface
    if enable[2] is True:  
        p02_queue = multiprocessing.Queue(-1)        
        p02 = MyProcess("p02_gui", gui_func, (p02_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer, logfile, enable))
        p02.start()    

    # Start logic solver process - this process runs the automation engine that decides when to turn various devices on/off
    if enable[11] is True:  
        p11_queue = multiprocessing.Queue(-1)         
        p11 = MyProcess("p11_logic_solver", logic_func, (p11_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
        p11.start()            

    # Start db interface process - This process monitors various triggers and sends sleep and wake commands when necessary to the RPI screen
    if enable[12] is True:  
        p12_queue = multiprocessing.Queue(-1)         
        p12 = MyProcess("p12_db_interface", db_func, (p12_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
        p12.start()                     

    # Start home/away detection process - This process monitors various triggers and sends sleep and wake commands when necessary to the RPI screen
    if enable[13] is True:     
        p13_queue = multiprocessing.Queue(-1)        
        p13 = MyProcess("p13_home_away", home_func, (p13_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
        p13.start()                       

    # Start motion detector process - This process monitors various triggers and sends sleep and wake commands when necessary to the RPI screen 
    if enable[14] is True:   
        p14_queue = multiprocessing.Queue(-1)             
        p14 = MyProcess("p14_motion", motion_func, (p14_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
        p14.start()                       

    # Start screen wake/sleep process - This process monitors various triggers and sends sleep and wake commands when necessary to the RPI screen
    if enable[15] is True: 
        p15_queue = multiprocessing.Queue(-1)           
        p15 = MyProcess("p15_rpi_screen", screen_func, (p15_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
        p15.start()                   

    # Start wemo gateway process - This process controls the interface to/from wemo devices on the network    
    if enable[16] is True: 
        p16_queue = multiprocessing.Queue(-1)            
        p16 = MyProcess("p16_wemo_gateway", wemo_func, (p16_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
        p16.start()              

    # Start nest gateway process - This process controls the interface to/from nest thermostats on the network
    if enable[17] is True:
        p17_queue = multiprocessing.Queue(-1)         
        p17 = MyProcess("p17_nest_gateway", db_func, (p12_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
        p17.start()   

    msg_in = str()
    close_pending = False
    last_hb = time.time()


    while True:
        # Check incoming queue for messages
        try:
            msg_in = p00_queue.get_nowait()     
        except:
            pass

        # If message recevied, check destination and process or forward
        if msg_in[3:5] == "00":               
            if msg_in[6:9] == "999":
                logging.log(logging.DEBUG, "Kill code received - Shutting down: %s" % msg_in)
                close_pending = True 

        # If message is destined for process p01, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "01":
            if enable[1] is True:
                p01_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p01.create("p01_log_handler", listener, (p01_queue, p00_queue, multiprocess_logging.listener_configurer, name, logfile))
                if msg_in[6:9] == "999":
                    p01.stop()

        # If message is destined for process p02, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "02":
            if enable[2] is True:
                if p02.is_alive() is True:
                    p02_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p02.create("p02_gui", gui_func, (p02_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer, logfile))           
                if msg_in[6:9] == "999":
                    p02.stop()

        # If message is destined for process p11, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "11":
            if enable[11] is True:
                if p11.is_alive() is True:            
                    p11_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p11.create("p11_logic_solver", logic_func, (p11_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))           
                if msg_in[6:9] == "999":
                    p11.stop()

        # If message is destined for process p12, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "12":
            if enable[12] is True:
                if p12.is_alive() is True:            
                    p12_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p12.create("p12_db_interface", db_func, (p12_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))           
                if msg_in[6:9] == "999":
                    p12.stop()

        # If message is destined for process p13, forward.  If message is kill-code for that process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "13" and enable[13] is True:
            if p13.is_alive() is True:            
                p13_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                p13.create("p13_home_away", home_func, (p13_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))           
            if msg_in[6:9] == "999":
                p13.stop()
               
        # If message is destined for process p14, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "14":
            if enable[14] is True:
                if p14.is_alive() is True:            
                    p14_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p14.create("p14_motion", motion_func, (p14_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))           
                if msg_in[6:9] == "999":
                    p14.stop()
 
        # If message is destined for process p15, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "15":
            if enable[15] is True:
                if p15.is_alive() is True:            
                    p15_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p15.create("p15_rpi_screen", screen_func, (p15_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                if msg_in[6:9] == "999":
                    p15.stop()

        # If message is destined for process p16, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "16":
            if enable[16] is True:
                if p16.is_alive() is True:            
                    p16_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p16.create("p16_wemo_gw", wemo_func, (p16_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                if msg_in[6:9] == "999":
                    p16.stop()
        
        # If message is destined for process p17, forward.  If message is kill-code for that process, join process
        if msg_in[3:5] == "17":
            if enable[17] is True:
                if p17.is_alive() is True:            
                    p17_queue.put_nowait(msg_in)
                if msg_in[6:9] == "900":
                    p17.create("p17_nest_gw", nest_func, (p17_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer, nestUsername, nestPassword))
                if msg_in[6:9] == "999":
                    p17.stop()   
        
        msg_in = str()   

        # If process is stopped, clear any messages in it's queue so it doesn't restart later with stale data
        if enable[2] is True:
            if p02.is_alive() is False:
                try:
                    discarded_msg = p02_queue.get_nowait()  
                except:
                    pass
        if enable[11] is True:
            if p11.is_alive() is False:
                try:
                    discarded_msg = p11_queue.get_nowait()  
                except:
                    pass 
        if enable[12] is True:                    
            if p12.is_alive() is False:
                try:
                    discarded_msg = p12_queue.get_nowait()  
                except:
                    pass  
        if enable[13] is True:                     
            if p13.is_alive() is False:
                try:
                    discarded_msg = p13_queue.get_nowait()  
                except:
                    pass 
        if enable[14] is True:                     
            if p14.is_alive() is False:
                try:
                    discarded_msg = p14_queue.get_nowait()  
                except:
                    pass  
        if enable[15] is True:                     
            if p15.is_alive() is False:
                try:
                    discarded_msg = p15_queue.get_nowait()  
                except:
                    pass 
        if enable[16] is True:                      
            if p16.is_alive() is False:
                try:
                    discarded_msg = p16_queue.get_nowait()  
                except:
                    pass 
        if enable[17] is True:                     
            if p17.is_alive() is False:
                try:
                    discarded_msg = p17_queue.get_nowait()  
                except:
                    pass   


        # Monitor processes as they are spawned / die and send messages to gui to update display
        if enable[1] is True:
            if p01.is_alive() != p01.alive_mem: 
                if p01.is_alive() is True:
                    p02_queue.put_nowait("01,02,002")
                    p01.alive_mem = True
                elif p01.is_alive() is False:
                    p02_queue.put_nowait("01,02,003")
                    p01.alive_mem = False 
        if enable[11] is True:                    
            if p11.is_alive() != p11.alive_mem: 
                if p11.is_alive() is True:
                    p02_queue.put_nowait("11,02,002")
                    p11.alive_mem = True
                elif p11.is_alive() is False:
                    p02_queue.put_nowait("11,02,003")
                    p11.alive_mem = False 
        if enable[12] is True:            
            if p12.is_alive() != p12.alive_mem: 
                if p12.is_alive() is True:
                    p02_queue.put_nowait("12,02,002")
                    p12.alive_mem = True
                elif p12.is_alive() is False:
                    p02_queue.put_nowait("12,02,003")
                    p12.alive_mem = False 
        if enable[13] is True:                    
            if p13.is_alive() != p13.alive_mem: 
                if p13.is_alive() is True:
                    p02_queue.put_nowait("13,02,002")
                    p13.alive_mem = True
                elif p13.is_alive() is False:
                    p02_queue.put_nowait("13,02,003")
                    p13.alive_mem = False 
        if enable[14] is True:                    
            if p14.is_alive() != p14.alive_mem: 
                if p14.is_alive() is True:
                    p02_queue.put_nowait("14,02,002")
                    p14.alive_mem = True
                elif p14.is_alive() is False:
                    p02_queue.put_nowait("14,02,003")
                    p14.alive_mem = False  
        if enable[15] is True:                    
            if p15.is_alive() != p15.alive_mem: 
                if p15.is_alive() is True:
                    p02_queue.put_nowait("15,02,002")
                    p15.alive_mem = True
                elif p15.is_alive() is False:
                    p02_queue.put_nowait("15,02,003")
                    p15.alive_mem = False 
        if enable[16] is True:                        
            if p16.is_alive() != p16.alive_mem: 
                if p16.is_alive() is True:
                    p02_queue.put_nowait("16,02,002")
                    p16.alive_mem = True
                elif p16.is_alive() is False:
                    p02_queue.put_nowait("16,02,003")
                    p16.alive_mem = False  
        if enable[17] is True:                    
            if p17.is_alive() != p17.alive_mem: 
                if p17.is_alive() is True:
                    p02_queue.put_nowait("17,02,002")
                    p17.alive_mem = True
                elif p17.is_alive() is False:
                    p02_queue.put_nowait("17,02,003")
                    p17.alive_mem = False     


        # If the source-code for one of the processes changes, automatically bounce process
        if enable[1] is True:
            if p01.is_alive() is True:

                if os.path.getmtime(os.path.join(process_path, "p01_log_handler.py")) != p01_process_modtime:
                    logging.log(logging.DEBUG, "p01 process file has changed.  Restarting process using new file")
                    p01_queue.put_nowait("00,01,999")
                    p01_process.join()
                    time.sleep(1)
                    p01.create("p01_log_handler", listener_process, (p01_queue, p00_queue, multiprocess_logging.listener_configurer, name, logfile))
                    p01_process_modtime = os.path.getmtime(os.path.join(process_path, "p01_log_handler.py"))

        if enable[11] is True:
            if p11.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p11_logic_solver.py")) != p11_process_modtime:
                    logging.log(logging.DEBUG, "p11 process file has changed.  Restarting process using new file")
                    p11_queue.put_nowait("00,11,999")
                    p11_process.join()
                    time.sleep(1)
                    p11.create("p11_logic_solver", logic_func, (p11_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                    p11_process_modtime = os.path.getmtime(os.path.join(process_path, "p11_logic_solver.py"))

        if enable[12] is True:
            if p12.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p12_db_interface.py")) != p12_process_modtime:
                    logging.log(logging.DEBUG, "p12 process file has changed.  Restarting process using new file")
                    p12_queue.put_nowait("00,12,999")
                    p12_process.join()
                    time.sleep(1)
                    p12.create("p12_db_interface", db_func, (p12_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                    p12_process_modtime = os.path.getmtime(os.path.join(process_path, "p12_db_interface.py"))

        if enable[13] is True:
            if p13.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p13_home_away.py")) != p13_process_modtime:
                    logging.log(logging.DEBUG, "p13 process file has changed.  Restarting process using new file")
                    p13_queue.put_nowait("00,13,999")
                    p13_process.join()
                    time.sleep(1)
                    p13.create("p13_home_away", home_func, (p13_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                    p13_process_modtime = os.path.getmtime(os.path.join(process_path, "p13_home_away.py"))
        
        if enable[14] is True:
            if p14.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p14_motion.py")) != p14_process_modtime:
                    logging.log(logging.DEBUG, "p14 process file has changed.  Restarting process using new file")
                    p14_queue.put_nowait("00,14,999")
                    p14_process.join()
                    time.sleep(1)
                    p14.create("p14_motion", motion_func, (p14_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                    p14_process_modtime = os.path.getmtime(os.path.join(process_path, "p14_motion.py"))

        if enable[15] is True:
            if p15.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p15_rpi_screen.py")) != p15_process_modtime:
                    logging.log(logging.DEBUG, "p15 process file has changed.  Restarting process using new file")
                    p15_queue.put_nowait("00,15,999")
                    p15_process.join()
                    time.sleep(1)
                    p15.create("p15_rpi_screen", screen_func, (p15_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                    p15_process_modtime = os.path.getmtime(os.path.join(process_path, "p15_rpi_screen.py"))

        if enable[16] is True:
            if p16.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p16_wemo_gateway.py")) != p16_process_modtime:
                    logging.log(logging.DEBUG, "p16 process file has changed.  Restarting process using new file")
                    p16_queue.put_nowait("00,16,999")
                    p16_process.join()
                    time.sleep(1)
                    p16.create("p16_wemo_gw", wemo_func, (p16_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                    p16_process_modtime = os.path.getmtime(os.path.join(process_path, "p16_wemo_gateway.py"))  

        if enable[17] is True:
            if p17.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p17_nest_gateway.py")) != p17_process_modtime:
                    logging.log(logging.DEBUG, "p17 process file has changed.  Restarting process using new file")
                    p17_queue.put_nowait("00,17,999")
                    p17_process.join()
                    time.sleep(1)
                    p17.create("p17_nest_gw", nest_func, (p17_queue, p00_queue, p01_queue, multiprocess_logging.worker_configurer))
                    p17_process_modtime = os.path.getmtime(os.path.join(process_path, "p17_nest_gateway.py"))                                                                                              

        # Send periodic heartbeats to child processes so they don't time-out and shutdown
        if time.time() > (last_hb + 5) and close_pending is False:
            if enable[1] is True:
                if p01.is_alive() is True:
                    p01_queue.put_nowait("00,01,001")
            if enable[2] is True:
                if p02.is_alive() is True:
                    p02_queue.put_nowait("00,02,001")
            if enable[11] is True:
                if p11.is_alive() is True:
                    p11_queue.put_nowait("00,11,001")
            if enable[12] is True:
                if p12.is_alive() is True:
                    p12_queue.put_nowait("00,12,001")
            if enable[13] is True:
                if p13.is_alive() is True:
                    p13_queue.put_nowait("00,13,001")
            if enable[14] is True:
                if p14.is_alive() is True:
                    p14_queue.put_nowait("00,14,001")
            if enable[15] is True:
                if p15.is_alive() is True:
                    p15_queue.put_nowait("00,15,001")
            if enable[16] is True:
                if p16.is_alive() is True:
                    p16_queue.put_nowait("00,16,001")
            if enable[17] is True:
                if p17.is_alive() is True:
                    p17_queue.put_nowait("00,17,001")             
            last_hb = time.time()


        # If a close is pending, wait until all messages from the queue have been processed before ending the program     
        if close_pending is True and p00_queue.empty() is True:            
            break            

        # Wait before next loop iteration
        time.sleep(0.11)



# Run as Script ******************************************************************************************************
if __name__ == "__main__":
    main()
                                                                                                                                                          
                                           
            
        
                 