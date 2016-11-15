#!/usr/bin/python3
""" main.py:
    Main entry-point into the RPiHome application.
    When run, this application will create a log message queue and start a listener service which will monitor that queue
    and write to a file any log messages it finds.  This queue is shared with any sub-processes that are later called and
    allows all parts of this application to share a single log-file in a multi-processing-safe manner.
    Once the log queue and listener process are started, the GUI is started.  
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import logging
import multiprocessing
import os
import sys
import time
if __name__ == "__main__":
    sys.path.append("..")

from rpihome.modules.log_path import LogFilePath
from rpihome.modules.multiprocess_logging import listener_configurer, worker_configurer

from p01_log_handler import listener_process
from p02_gui import MainWindow
from p11_logic_solver import LogicProcess
from p13_home_away import home_func
from p15_rpi_screen import screen_func
from p16_wemo_gateway import WemoProcess
from p17_nest_gateway import nest_func


# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Process Generator Helper Function ***************************************************************
def create_process(name, func_name, args):
    process = multiprocessing.Process(name=name, target=func_name, args=args)
    process.daemon = True
    process.start()
    return process


# Main Routine ************************************************************************************
def main():
    # Decide what processes to enable
    enable = [True, True, True, False, False, False, False, False, False, False, False, True,
              False, True, False, True, True, False]

    # Get Nest login info if necessary
    if enable[17] is True:
        nestUsername = input("NEST Username: ")
        nestPassword = input("NEST Password: ")

    # Define queues for InterruptedError-process communication
    p00_queue = multiprocessing.Queue(-1)
    if enable[1] is True:
        p01_queue = multiprocessing.Queue(-1)
    if enable[2] is True:
        p02_queue = multiprocessing.Queue(-1)
    if enable[11] is True:
        p11_queue = multiprocessing.Queue(-1)
    if enable[13] is True:
        p13_queue = multiprocessing.Queue(-1)
    if enable[15] is True:
        p15_queue = multiprocessing.Queue(-1)
    if enable[16] is True:
        p16_queue = multiprocessing.Queue(-1)
    if enable[17] is True:
        p17_queue = multiprocessing.Queue(-1)

    # Set location of log file and crate subfolder if necessary
    name = "main"
    logfilepathgen = LogFilePath()
    logfile = logfilepathgen.return_path_and_name_combined(
        name=name, path=os.path.dirname(sys.argv[0]))
    process_path = os.path.dirname(sys.argv[0])

    # Start global log handler process - This process retrieves log messages from the shared log
    # queue and writes them to a file
    if enable[1] is True:
        p01_process_alive_mem = None
        p01_process = create_process(
            "p01_log_handler", listener_process, (
                p01_queue, p00_queue, listener_configurer, logfile))
        p01_process_modtime = os.path.getmtime(os.path.join(process_path, "p01_log_handler.py"))


    # Start gui process to spawn the user interface
    if enable[2] is True:
        p02_process_alive_mem = None
        p02_process = MainWindow(
            "p02_gui", p02_queue, p00_queue, p01_queue, worker_configurer, logfile, enable)
        p02_process.start()
        p02_process_modtime = os.path.getmtime(os.path.join(process_path, "p02_gui.py"))
   

    # Start logic solver process - this process runs the automation engine that decides when to turn various devices on/off
    if enable[11] is True:      
        p11_process_alive_mem = None    
        p11_process = LogicProcess(
            "p11_logic_solver", p11_queue, p00_queue, p01_queue, worker_configurer)
        p11_process.start()
        p11_process_modtime = os.path.getmtime(os.path.join(process_path, "p11_logic_solver.py"))
    

    # Start home/away detection process 
    # This process monitors various triggers and sends sleep and wake commands when necessary to the RPI screen
    if enable[13] is True:                
        p13_process_alive_mem = None
        p13_process = create_process("p13_home_away", home_func, (p13_queue, p00_queue, p01_queue, worker_configurer))
        p13_process_modtime = os.path.getmtime(os.path.join(process_path, "p13_home_away.py"))    

    # Start motion detector process 
    # This process monitors various triggers and sends sleep and wake commands when necessary to the RPI screen 
    if enable[14] is True:                  
        p14_process_alive_mem = None
        p14_process = create_process("p14_motion", motion_func, (p14_queue, p00_queue, p01_queue, worker_configurer))
        p14_process_modtime = os.path.getmtime(os.path.join(process_path, "p14_motion.py"))    

    # Start screen wake/sleep process 
    # This process monitors various triggers and sends sleep and wake commands when necessary to the RPI screen
    if enable[15] is True:             
        p15_process_alive_mem = None
        p15_process = create_process("p15_rpi_screen", screen_func, (p15_queue, p00_queue, p01_queue, worker_configurer))
        p15_process_modtime = os.path.getmtime(os.path.join(process_path, "p15_rpi_screen.py"))

    # Start wemo gateway process - This process controls the interface to/from wemo devices on the
    # network
    if enable[16] is True:
        p16_process_alive_mem = None
        #p16_process = create_process("p16_wemo_gw", wemo_func, (p16_queue, p00_queue, p01_queue,
        #worker_configurer))
        p16_process = WemoProcess("p16_wemo_gateway", p16_queue, p00_queue, p01_queue,
                                  worker_configurer)
        p16_process.start()
        p16_process_modtime = os.path.getmtime(os.path.join(process_path, "p16_wemo_gateway.py"))

    # Start nest gateway process - This process controls the interface to/from nest thermostats
    # on the network
    if enable[17] is True:
        p17_process_alive_mem = None
        p17_process = create_process("p17_nest_gw", nest_func, (p17_queue, p00_queue, p01_queue, worker_configurer, nestUsername, nestPassword))
        p17_process_modtime = os.path.getmtime(os.path.join(process_path, "p17_nest_gateway.py"))    

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
        if len(msg_in) != 0 and msg_in[3:5] == "00":               
            if msg_in[6:9] == "999":
                logging.log(logging.DEBUG, "Kill code received - Shutting down: %s" % msg_in)
                close_pending = True 

        # If message is destined for process p01, forward.  If message is kill-code for that process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "01" and enable[1] is True:
            p01_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                if p01_process.is_alive() is False:
                    p01_process = create_process("p01_log_handler", listener_process, (p01_queue, p00_queue, listener_configurer, name, logfile))
            if msg_in[6:9] == "999":
                if p01_process.is_alive() is True:
                    p01_process.join()

        # If message is destined for process p02, forward.  If message is kill-code for that process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "02" and enable[2] is True:
            if p02_process.is_alive() is True:
                p02_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                if p02_process.is_alive() is False:
                    p02_process = MainWindow("p02_gui", p02_queue, p00_queue, p01_queue, worker_configurer, logfile, enable)
                    p02_process.start()           
            if msg_in[6:9] == "999":
                if p02_process.is_alive() is True:                
                    p02_process.join()

        # If message is destined for process p11, forward.  If message is kill-code for that process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "11" and enable[11] is True:
            if p11_process.is_alive() is True:            
                p11_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                if p11_process.is_alive() is False:
                    p11_process = LogicProcess("p11_logic_solver", p11_queue, p00_queue, p01_queue, worker_configurer)
                    p11_process.start()       
            if msg_in[6:9] == "999":
                if p11_process.is_alive() is True:                
                    p11_process.join()

        # If message is destined for process p13, forward.  If message is kill-code for that process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "13" and enable[13] is True:
            if p13_process.is_alive() is True:            
                p13_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                if p13_process.is_alive() is False:
                    p13_process = create_process("p13_home_away", home_func, (p13_queue, p00_queue, p01_queue, worker_configurer))           
            if msg_in[6:9] == "999":
                if p13_process.is_alive() is True:                
                    p13_process.join()
 
        # If message is destined for process p15, forward.  If message is kill-code for that process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "15" and enable[15] is True:
            if p15_process.is_alive() is True:            
                p15_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                if p15_process.is_alive() is False:
                    p15_process = create_process("p15_rpi_screen", screen_func, (p15_queue, p00_queue, p01_queue, worker_configurer))
            if msg_in[6:9] == "999":
                if p15_process.is_alive() is True:                
                    p15_process.join()

        # If message is destined for process p16, forward.  If message is kill-code for that
        # process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "16" and enable[16] is True:
            if p16_process.is_alive() is True:            
                p16_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                if p16_process.is_alive() is False:
                    p16_process = WemoProcess("p16_wemo_gateway", p16_queue, p00_queue, p01_queue,
                                              worker_configurer)
                    p16_process.start()
                    #p16_process = create_process("p16_wemo_gw", wemo_func, (p16_queue, p00_queue,
                    #p01_queue, worker_configurer))
            if msg_in[6:9] == "999":
                if p16_process.is_alive() is True:                
                    p16_process.join()
        
        # If message is destined for process p17, forward.  If message is kill-code for that
        # process, join process
        elif len(msg_in) != 0 and msg_in[3:5] == "17" and enable[17] is True:
            if p17_process.is_alive() is True:            
                p17_queue.put_nowait(msg_in)
            if msg_in[6:9] == "900":
                if p17_process.is_alive() is False:
                    p17_process = create_process("p17_nest_gw", nest_func, (p17_queue, p00_queue, p01_queue, worker_configurer, nestUsername, nestPassword))
            if msg_in[6:9] == "999":
                if p17_process.is_alive() is True:                
                    p17_process.join()   
        
        msg_in = str()                       


        # If process is stopped, clear any messages in it's queue so it doesn't restart later with stale data
        if enable[2] is True:
            if p02_process.is_alive() is False:
                try:
                    discarded_msg = p02_queue.get_nowait()  
                except:
                    pass
        if enable[11] is True:
            if p11_process.is_alive() is False:
                try:
                    discarded_msg = p11_queue.get_nowait()  
                except:
                    pass 
        if enable[13] is True:                     
            if p13_process.is_alive() is False:
                try:
                    discarded_msg = p13_queue.get_nowait()  
                except:
                    pass  
        if enable[15] is True:                     
            if p15_process.is_alive() is False:
                try:
                    discarded_msg = p15_queue.get_nowait()  
                except:
                    pass 
        if enable[16] is True:                      
            if p16_process.is_alive() is False:
                try:
                    discarded_msg = p16_queue.get_nowait()  
                except:
                    pass 
        if enable[17] is True:                     
            if p17_process.is_alive() is False:
                try:
                    discarded_msg = p17_queue.get_nowait()  
                except:
                    pass       

        # Monitor processes as they are spawned / die and send messages to gui to update display
        if enable[1] is True:
            if p01_process.is_alive() != p01_process_alive_mem: 
                if p01_process.is_alive() is True:
                    p02_queue.put_nowait("01,02,002")
                    p01_process_alive_mem = True
                elif p01_process.is_alive() is False:
                    p02_queue.put_nowait("01,02,003")
                    p01_process_alive_mem = False 
        if enable[11] is True:                    
            if p11_process.is_alive() != p11_process_alive_mem: 
                if p11_process.is_alive() is True:
                    p02_queue.put_nowait("11,02,002")
                    p11_process_alive_mem = True
                elif p11_process.is_alive() is False:
                    p02_queue.put_nowait("11,02,003")
                    p11_process_alive_mem = False 
        if enable[13] is True:                    
            if p13_process.is_alive() != p13_process_alive_mem: 
                if p13_process.is_alive() is True:
                    p02_queue.put_nowait("13,02,002")
                    p13_process_alive_mem = True
                elif p13_process.is_alive() is False:
                    p02_queue.put_nowait("13,02,003")
                    p13_process_alive_mem = False   
        if enable[15] is True:                    
            if p15_process.is_alive() != p15_process_alive_mem: 
                if p15_process.is_alive() is True:
                    p02_queue.put_nowait("15,02,002")
                    p15_process_alive_mem = True
                elif p15_process.is_alive() is False:
                    p02_queue.put_nowait("15,02,003")
                    p15_process_alive_mem = False 
        if enable[16] is True:                        
            if p16_process.is_alive() != p16_process_alive_mem: 
                if p16_process.is_alive() is True:
                    p02_queue.put_nowait("16,02,002")
                    p16_process_alive_mem = True
                elif p16_process.is_alive() is False:
                    p02_queue.put_nowait("16,02,003")
                    p16_process_alive_mem = False  
        if enable[17] is True:                    
            if p17_process.is_alive() != p17_process_alive_mem: 
                if p17_process.is_alive() is True:
                    p02_queue.put_nowait("17,02,002")
                    p17_process_alive_mem = True
                elif p17_process.is_alive() is False:
                    p02_queue.put_nowait("17,02,003")
                    p17_process_alive_mem = False                                                                                                                                       


        # If the source-code for one of the processes changes, automatically bounce process
        if enable[1] is True:
            if p01_process.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p01_log_handler.py")) != p01_process_modtime:
                    logging.log(logging.DEBUG, "p01 process file has changed.  Restarting process using new file")
                    p01_queue.put_nowait("00,01,999")
                    p01_process.join()
                    time.sleep(1)
                    p01_process = create_process("p01_log_handler", listener_process, (p01_queue, p00_queue, listener_configurer, name, logfile))
                    p01_process_modtime = os.path.getmtime(os.path.join(process_path, "p01_log_handler.py"))

        if enable[11] is True:
            if p11_process.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p11_logic_solver.py")) != p11_process_modtime:
                    logging.log(logging.DEBUG, "p11 process file has changed.  Restarting process using new file")
                    p11_queue.put_nowait("00,11,999")
                    p11_process.join()
                    time.sleep(1)
                    p11_process = create_process("p11_logic_solver", logic_func, (p11_queue, p00_queue, p01_queue, worker_configurer))
                    p11_process_modtime = os.path.getmtime(os.path.join(process_path, "p11_logic_solver.py"))

        if enable[13] is True:
            if p13_process.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p13_home_away.py")) != p13_process_modtime:
                    logging.log(logging.DEBUG, "p13 process file has changed.  Restarting process using new file")
                    p13_queue.put_nowait("00,13,999")
                    p13_process.join()
                    time.sleep(1)
                    p13_process = create_process("p13_home_away", home_func, (p13_queue, p00_queue, p01_queue, worker_configurer))
                    p13_process_modtime = os.path.getmtime(os.path.join(process_path, "p13_home_away.py"))

        if enable[15] is True:
            if p15_process.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p15_rpi_screen.py")) != p15_process_modtime:
                    logging.log(logging.DEBUG, "p15 process file has changed.  Restarting process using new file")
                    p15_queue.put_nowait("00,15,999")
                    p15_process.join()
                    time.sleep(1)
                    p15_process = create_process("p15_rpi_screen", screen_func, (p15_queue, p00_queue, p01_queue, worker_configurer))
                    p15_process_modtime = os.path.getmtime(os.path.join(process_path, "p15_rpi_screen.py"))

        if enable[16] is True:
            if p16_process.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p16_wemo_gateway.py")) != p16_process_modtime:
                    logging.log(logging.DEBUG, "p16 process file has changed.  Restarting process using new file")
                    p16_queue.put_nowait("00,16,999")
                    p16_process.join()
                    time.sleep(1)
                    p16_process = WemoProcess(p16_queue, p00_queue, p01_queue,
                                              worker_configurer)
                    p16_process.start()
                    #p16_process = create_process("p16_wemo_gw", wemo_func, (p16_queue, p00_queue,
                    #p01_queue, worker_configurer))
                    p16_process_modtime = os.path.getmtime(os.path.join(process_path,
                                                                        "p16_wemo_gateway.py"))  

        if enable[17] is True:
            if p17_process.is_alive() is True:
                if os.path.getmtime(os.path.join(process_path, "p17_nest_gateway.py")) != p17_process_modtime:
                    logging.log(logging.DEBUG, "p17 process file has changed.  Restarting process using new file")
                    p17_queue.put_nowait("00,17,999")
                    p17_process.join()
                    time.sleep(1)
                    p17_process = create_process("p17_nest_gw", nest_func, (p17_queue, p00_queue, p01_queue, worker_configurer))
                    p17_process_modtime = os.path.getmtime(os.path.join(process_path, "p17_nest_gateway.py"))                                                                                              

        # Send periodic heartbeats to child processes so they don't time-out and shutdown
        if time.time() > (last_hb + 5) and close_pending is False:
            if enable[1] is True:
                if p01_process.is_alive() is True:
                    p01_queue.put_nowait("00,01,001")
            if enable[2] is True:
                if p02_process.is_alive() is True:
                    p02_queue.put_nowait("00,02,001")
            if enable[11] is True:
                if p11_process.is_alive() is True:
                    p11_queue.put_nowait("00,11,001")
            if enable[13] is True:
                if p13_process.is_alive() is True:
                    p13_queue.put_nowait("00,13,001")
            if enable[15] is True:
                if p15_process.is_alive() is True:
                    p15_queue.put_nowait("00,15,001")
            if enable[16] is True:
                if p16_process.is_alive() is True:
                    p16_queue.put_nowait("00,16,001")
            if enable[17] is True:
                if p17_process.is_alive() is True:
                    p17_queue.put_nowait("00,17,001")             
            last_hb = time.time()


        # If a close is pending, wait until all messages from the queue have been processed before ending the program     
        if close_pending is True and p00_queue.empty() is True:            
            break            

        # Wait before next loop iteration
        time.sleep(0.011)



# Run as Script ******************************************************************************************************
if __name__ == "__main__":
    main()
    