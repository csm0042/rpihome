#!/usr/bin/python3
""" gui.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ****************************************
import copy
import datetime
import linecache
import logging
import multiprocessing
import os
import sys
import time
import tkinter as tk
from tkinter import font
from tkinter import messagebox

from modules.message import Message

# Authorship Info *********************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Application GUI Class Definition ****************************************************************
class MainWindow(multiprocessing.Process):
    """ GUI process class and methods """
    def __init__(self, **kwargs):
        # Set default input parameter values
        self.name = "undefined"
        self.msg_in_queue = multiprocessing.Queue(-1)
        self.msg_out_queue = multiprocessing.Queue(-1)
        self.logfile = "logfile"
        self.enable = [True]*18
        self.log_remote = False
        self.display_file = None
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
                if key == "enable":
                    self.enable = value
                if key == "logremote":
                    self.log_remote = value
                if key == "displayfile":
                    self.display_file = value
        # Initialize parent class
        multiprocessing.Process.__init__(self, name=self.name)
        # Create remaining class elements
        self.text = str()
        self.msg_in = Message()
        self.msg_to_send = Message()
        self.close_pending = False
        self.last_hb = time.time()
        self.index = 0
        self.time_to_go = datetime.time(6,30)
        self.last_update = datetime.datetime.now() + datetime.timedelta(seconds=30)
        self.datetime_to_go = str()
        self.time_remaining = str()
        self.scanWemo = True
        self.current_conditions = ["??"] * 4
        self.current_forecast = ["??"] * 4
        self.tomorrow_forecast = ["??"] * 4
        # Initialize pointer for alarm display window
        if os.path.isfile(self.display_file):
            self.line = sum(1 for line in open(self.display_file)) - 50
            if self.line < 1:
                self.line = 1
        else:
            self.line = 1
        # Set location of resource directory
        self.basepath = os.path.dirname(sys.argv[0])
        self.resourceDir = os.path.join(self.basepath, "resources/")


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


    def run(self):
        """ Generate window and schedule after and close handlers """
        # Configure logging
        self.configure_local_logger()
        # Create all parts of application window
        self.logger.debug("Begining generation of application window")
        self.draw_window()
        self.logger.debug("Finished generation of application window")
        # Schedule "after" process to run once main loop has started
        self.window.after(500, self.after_tasks)
        self.logger.debug("Scheduled initial \"after\" task")
        # Start handler for window exit button
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.logger.debug("Added \"on-close\" handler")
        # Run mainloop() to activate gui and begin monitoring its inputs
        self.logger.debug("Started gui mainloop")
        self.window.mainloop()             


    def draw_window(self):
        """ Called to draw a complete application.  It does this by calling methods to create
        individaual sections as necessary """
        # Create initial application object
        self.gen_main_window()
        # Define fonts and images
        self.define_fonts()
        self.define_images()
        # Begin dividing aplication window into sections
        self.divide_main_window()
        self.divide_frame01()
        self.divide_frame02()
        self.divide_frame03()
        self.divide_frame04()
        self.divide_frame05()
        self.divide_frame06()
        self.divide_frame0102()
        self.divide_frame0302()
        self.divide_frame0402()
        self.divide_frame0602()
        # Begin adding widgets to frames
        self.top_divider_bar1()
        self.bottom_divider_bar1()
        self.top_divider_bar2()
        self.bottom_divider_bar2()
        # Top Window selector buttons
        self.frame0201_buttons()
        # Top window content
        self.status_window()
        self.alarm_log_window()
        self.frame0203b.pack_forget()
        self.frame0203b_packed = False
        # Bottom window selector buttons
        self.frame0501_buttons()
        # Bottom window content
        self.frame0503a_content()
        self.frame0503b_content()
        self.frame050301b.pack_forget()
        self.frame050301b_packed = False
        self.frame0503c_content()
        self.frame050301c.pack_forget()
        self.frame050301c_packed = False
        self.frame0503d_content()
        self.frame050301d.pack_forget()
        self.frame050301d_packed = False                    
    

    def gen_main_window(self):
        """ Method to create the main tkinter window """
        self.window = tk.Tk()   
        self.window.title("RPi Home")
        self.window.geometry("%sx%s+%s+%s" % (840, 810, 1, 1))
        self.window.config(background="black") 
        self.logger.debug("Main application window created")


    def define_fonts(self):
        """ Method to define fonts used throughout the application """
        self.helv04bold = font.Font(family="Helvetica", size=4, weight="bold")
        self.helv06bold = font.Font(family="Helvetica", size=6, weight="bold")
        self.helv08bold = font.Font(family="Helvetica", size=8, weight="bold")
        self.helv10bold = font.Font(family="Helvetica", size=10, weight="bold")
        self.helv12bold = font.Font(family="Helvetica", size=12, weight="bold")
        self.helv14bold = font.Font(family="Helvetica", size=14, weight="bold")
        self.helv16bold = font.Font(family="Helvetica", size=16, weight="bold")
        self.helv24bold = font.Font(family="Helvetica", size=24, weight="bold")
        self.helv36 = font.Font(family="Helvetica", size=36, weight="bold")


    def define_images(self):
        """ Method to define image widgets using files from resource directory """
        self.button_elbow_NE_img = (
            tk.PhotoImage(file=self.resourceDir + "Elbow-blue-up-left.png"))
        self.button_elbow_NW_img = (
            tk.PhotoImage(file=self.resourceDir + "Elbow-blue-up-right.png"))
        self.button_elbow_SE_img = (
            tk.PhotoImage(file=self.resourceDir + "Elbow-blue-down-left.png"))
        self.button_elbow_SW_img = (
            tk.PhotoImage(file=self.resourceDir + "Elbow-blue-down-right.png"))
        self.button_green_round_left_img = (
            tk.PhotoImage(file=self.resourceDir + "button_green_round_left.png"))
        self.button_green_round_right_img = (
            tk.PhotoImage(file=self.resourceDir + "button_green_round_right.png"))
        self.button_151_195_225_round_left_img = (
            tk.PhotoImage(file=self.resourceDir + "button_151,195,225_round_left.png"))
        self.button_151_195_225_round_right_img = (
            tk.PhotoImage(file=self.resourceDir + "button_151,195,225_round_right.png")) 
        self.button_red_round_left_img = (
            tk.PhotoImage(file=self.resourceDir + "button_red_round_left.png"))
        self.button_red_round_right_img = (
            tk.PhotoImage(file=self.resourceDir + "button_red_round_right.png"))
        self.button_square_green_img = (
            tk.PhotoImage(file=self.resourceDir + "button-square-green.png"))
        self.button_square_red_img = (
            tk.PhotoImage(file=self.resourceDir + "button-square-red.png"))      


    def divide_main_window(self):
        self.screen1 = tk.Frame(self.window, background="black")
        self.screen1.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        self.logger.debug("Overlayed 1 primary frame over-top of application (root) window")
        self.frame01 = tk.Frame(self.screen1, background="black", height=50, width=800)
        self.frame01.pack(side="top", fill="x", expand=False, padx=0, pady=0)
        self.frame01.pack_propagate(False)
        self.frame02 = tk.Frame(self.screen1, background="black", height=198, width=800)
        self.frame02.pack(side="top", fill="x", expand=False, padx=0, pady=1)
        self.frame02.pack_propagate(False)
        self.frame03 = tk.Frame(self.screen1, background="black", height=50, width=800)
        self.frame03.pack(side="top", fill="x", expand=False, padx=0, pady=0)
        self.frame03.pack_propagate(False)
        self.frame04 = tk.Frame(self.screen1, background="black", height=50, width=800)
        self.frame04.pack(side="top", fill="x", expand=False, padx=0, pady=1)
        self.frame04.pack_propagate(False)
        self.frame05 = tk.Frame(self.screen1, background="black", height=398, width=800)
        self.frame05.pack(side="top", fill="both", expand=True, padx=0, pady=1)
        self.frame05.pack_propagate(False)
        self.frame06 = tk.Frame(self.screen1, background="black", height=50, width=800)
        self.frame06.pack(side="top", fill="x", expand=False, padx=0, pady=0)
        self.frame06.pack_propagate(False)
        self.logger.debug("Overlayed 6 sub-frames, packed top to bottom over-top of primary frame")   


    def divide_frame01(self):
        # split frame 1 into 2 sections along a vertical axis
        self.frame0101 = tk.Frame(self.frame01, background="yellow", height=50, width=105)
        self.frame0101.pack(side="left", fill="none", expand=False, padx=0, pady=0)  
        self.frame0101.pack_propagate(False) 
        self.frame0102 = tk.Frame(self.frame01, background="blue", height=50, width=695)
        self.frame0102.pack(side="left", fill="x", expand=True, padx=1, pady=1)  
        self.frame0102.pack_propagate(False)


    def divide_frame02(self):
        # split frame 2 into 3 sections along a vertical axis
        self.frame0201 = tk.Frame(self.frame02, background="black", height=200, width=85)
        self.frame0201.pack(side="left", fill="y", expand=False, padx=0, pady=0)  
        self.frame0201.pack_propagate(False)  
        self.frame0202 = tk.Frame(self.frame02, background="black", height=200, width=20)
        self.frame0202.pack(side="left", fill="y", expand=False, padx=0, pady=0) 
        self.frame0202.pack_propagate(False) 
        self.frame0203 = tk.Frame(self.frame02, background="black", height=200, width=695)
        self.frame0203.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.frame0203.pack_propagate(False) 


    def divide_frame03(self):
        # split frame 3 into 2 sections along a vertical axis
        self.frame0301 = tk.Frame(self.frame03, background="yellow", height=50, width=105)
        self.frame0301.pack(side="left", fill="none", expand=False, padx=0, pady=0)  
        self.frame0301.pack_propagate(False) 
        self.frame0302 = tk.Frame(self.frame03, background="blue", height=50, width=695)
        self.frame0302.pack(side="left", fill="x", expand=True, padx=1, pady=1)  
        self.frame0302.pack_propagate(False)


    def divide_frame04(self):
        # split frame 4 into 2 sections along a vertical axis
        self.frame0401 = tk.Frame(self.frame04, background="yellow", height=50, width=105)
        self.frame0401.pack(side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame0401.pack_propagate(False)
        self.frame0402 = tk.Frame(self.frame04, background="blue", height=50, width=695)
        self.frame0402.pack(side="left", fill="x", expand=True, padx=1, pady=1)  
        self.frame0402.pack_propagate(False)


    def divide_frame05(self):
        # split frame 5 into 3 sections along a vertical axis
        #self.frame0501 = tk.Frame(self.frame05, background="#2350b5", height=400, width=85)
        self.frame0501 = tk.Frame(self.frame05, background="black", height=400, width=85)
        self.frame0501.pack(side="left", fill="y", expand=False, padx=0, pady=0) 
        self.frame0501.pack_propagate(False)  
        self.frame0502 = tk.Frame(self.frame05, background="black", height=400, width=20)
        self.frame0502.pack(side="left", fill="y", expand=False, padx=0, pady=0) 
        self.frame0502.pack_propagate(False)
        self.frame0503 = tk.Frame(self.frame05, background="black", height=400, width=695)
        self.frame0503.pack(side="left", fill="both", expand=True, padx=0, pady=0)


    def divide_frame06(self):
        # split frame 6 into 2 sections along a vertical axis
        self.frame0601 = tk.Frame(self.frame06, background="yellow", height=50, width=105)
        self.frame0601.pack(side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame0601.pack_propagate(False)
        self.frame0602 = tk.Frame(self.frame06, background="blue", height=50, width=695)
        self.frame0602.pack(side="left", fill="x", expand=True, padx=1, pady=1) 
        self.frame0602.pack_propagate(False)


    def divide_frame0102(self):
        # split frame 0102 into 2 sections along a horizontal axis
        self.frame010201 = tk.Frame(self.frame0102, background="#2350b5", height=17, width=695)
        self.frame010201.pack(side="top", fill="x", expand=True, padx=0, pady=0)  
        self.frame010201.pack_propagate(False)
        self.frame010202 = tk.Frame(self.frame0102, background="black", height=33, width=695)
        self.frame010202.pack(side="top", fill="both", expand=True, padx=0, pady=0) 
        self.frame010202.pack_propagate(False)


    def divide_frame0302(self):
        # split frame 0302 into 2 sections along a horizontal axis
        self.frame030201 = tk.Frame(self.frame0302, background="black", height=31, width=695)
        self.frame030201.pack(anchor="nw", side="top", fill="x", expand=True, padx=0, pady=0) 
        self.frame030201.pack_propagate(False)  
        self.frame030202 = tk.Frame(self.frame0302, background="#2350b5", height=17, width=695)
        self.frame030202.pack(anchor="nw", side="top", fill="both", expand=True, padx=0, pady=0) 
        self.frame030202.pack_propagate(False)


    def divide_frame0402(self):
        # split frame 0102 into 2 sections along a horizontal axis
        self.frame040201 = tk.Frame(self.frame0402, background="#2350b5", height=17, width=695)
        self.frame040201.pack(side="top", fill="x", expand=True, padx=0, pady=0)  
        self.frame040201.pack_propagate(False) 
        self.frame040202 = tk.Frame(self.frame0402, background="black", height=33, width=695)
        self.frame040202.pack(side="top", fill="both", expand=True, padx=0, pady=0) 
        self.frame040202.pack_propagate(False)     


    def divide_frame0602(self):
        # split frame 0302 into 2 sections along a horizontal axis
        self.frame060201 = tk.Frame(self.frame0602, background="black", height=31, width=695)
        self.frame060201.pack(side="top", fill="x", expand=True, padx=0, pady=0)   
        self.frame060202 = tk.Frame(self.frame0602, background="#2350b5", height=17, width=695)
        self.frame060202.pack(side="top", fill="both", expand=True, padx=0, pady=0)   


    def top_divider_bar1(self):
        self.button010101 = tk.Button(self.frame0101, anchor="nw", background="black", borderwidth=0, command=self.action010101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_NW_img, justify="right", relief="flat", text="010101", height=50, width=105)
        self.button010101.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.label010202 = tk.Label(self.frame010202, anchor="e", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="right", relief="flat", text="CURRENT STATUS")
        self.label010202.pack(side="right", fill="both", expand=True, padx=10, pady=7)  


    def bottom_divider_bar1(self):
        self.button030101 = tk.Button(self.frame0301, anchor="sw", background="black", borderwidth=0, command=self.action030101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_SW_img, justify="right", relief="flat", text="030101", height=50, width=105)
        self.button030101.pack(side="left", fill="both", expand=True, padx=0, pady=0)


    def top_divider_bar2(self):
        self.button040101 = tk.Button(self.frame0401, anchor="nw", background="black", borderwidth=0, command=self.action040101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_NW_img, justify="right", relief="flat", text="040101", height=50, width=105)
        self.button040101.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.label040202 = tk.Label(self.frame040202, anchor="ne", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="right", relief="flat", text="SERVICES")
        self.label040202.pack(side="right", fill="none", expand=False, padx=10, pady=7) 
  

    def bottom_divider_bar2(self):
        self.button060101 = tk.Button(self.frame0601, anchor="sw", background="black", borderwidth=0, command=self.action060101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_SW_img, justify="right", relief="flat", text="060101", height=50, width=105)
        self.button060101.pack(side="left", fill="both", expand=True, padx=0, pady=0)


    def frame0201_buttons(self):
        """ FRAME 02 SCREEN SELECTOR BUTTONS """
        self.button020101 = tk.Button(self.frame0201, background="#2350b5", borderwidth=0, command=self.action020101, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="STATUS", height=3, width=10)
        self.button020101.pack(side="top", fill="x", expand=False, padx=0, pady=1)
        self.button020102 = tk.Button(self.frame0201, background="#2350b5", borderwidth=0, command=self.action020102, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="LOGS", height=3, width=10)
        self.button020102.pack(side="top", fill="x", expand=False, padx=0, pady=1)   
        self.button0201xx = tk.Button(self.frame0201, background="#2350b5", borderwidth=0, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", height=3, width=10)
        self.button0201xx.pack(side="top", fill="both", expand=True, padx=0, pady=1)          


    def status_window(self):
        self.frame0203a = tk.Frame(self.frame0203, background="black")
        self.frame0203a.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        # Date and time header
        self.label0203a01 = tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="CURRENT DATE & TIME")
        self.label0203a01.grid(row=0, column=0, rowspan=1, columnspan=8, sticky="w")
        # Date and time text field
        self.text0203a01 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv24bold, foreground="white", highlightthickness=0, height=1, width=24, wrap="word")
        self.text0203a01.grid(row=1, column=0, rowspan=1, columnspan=8, sticky="w")
        
        # Horizontal divider
        self.label0203a03 = tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="  ")
        self.label0203a03.grid(row=2, column=0, rowspan=1, columnspan=8, sticky="w")
        
        # Current condition variable text - condition summary    
        self.label0203a04 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="CURRENT CONDITIONS: ")
        self.label0203a04.grid(row=3, column=0, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a04 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=15, wrap="word")
        self.text0203a04.grid(row=3, column=1, rowspan=1, columnspan=1, sticky="ew") 
        
        # Current condition row label - temp
        self.label0203a05 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="TEMP (F): ")
        self.label0203a05.grid(row=3, column=2, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a05 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a05.grid(row=3, column=3, rowspan=1, columnspan=1, sticky="ew")   
        
        # Current condition row label - winds
        self.label0203a06 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="WINDS: ")
        self.label0203a06.grid(row=3, column=4, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a06 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a06.grid(row=3, column=5, rowspan=1, columnspan=1, sticky="ew")  
        
        # Current condition row label - humidity
        self.label0203a07 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="HUMIDITY: ")
        self.label0203a07.grid(row=3, column=6, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a07 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a07.grid(row=3, column=7, rowspan=1, columnspan=1, sticky="ew")  

        # Horizontal divider
        self.label0203a08 = tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv06bold, foreground="yellow", justify="left", text="  ")
        self.label0203a08.grid(row=4, column=0, rowspan=1, columnspan=8, sticky="w")
        
        # Current condition variable text - condition summary    
        self.label0203a09 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="TODAY'S FORECAST: ")
        self.label0203a09.grid(row=5, column=0, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a09 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=15, wrap="word")
        self.text0203a09.grid(row=5, column=1, rowspan=1, columnspan=1, sticky="ew") 
        
        # Current condition row label - temp
        self.label0203a10 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="LOW (F): ")
        self.label0203a10.grid(row=5, column=2, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a10 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a10.grid(row=5, column=3, rowspan=1, columnspan=1, sticky="ew")   
        
        # Current condition row label - winds
        self.label0203a11 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="HIGH (F): ")
        self.label0203a11.grid(row=5, column=4, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a11 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a11.grid(row=5, column=5, rowspan=1, columnspan=1, sticky="ew")  
        
        # Current condition row label - humidity
        self.label0203a12 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="HUMIDITY: ")
        self.label0203a12.grid(row=5, column=6, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a12 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a12.grid(row=5, column=7, rowspan=1, columnspan=1, sticky="ew")

        # Horizontal divider
        self.label0203a13 = tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv06bold, foreground="yellow", justify="left", text="  ")
        self.label0203a13.grid(row=6, column=0, rowspan=1, columnspan=8, sticky="w")
        
        # Current condition variable text - condition summary    
        self.label0203a14 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="TOMORROW'S FORECAST: ")
        self.label0203a14.grid(row=7, column=0, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a14 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=15, wrap="word")
        self.text0203a14.grid(row=7, column=1, rowspan=1, columnspan=1, sticky="ew") 
        
        # Current condition row label - temp
        self.label0203a15 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="LOW (F): ")
        self.label0203a15.grid(row=7, column=2, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a15 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a15.grid(row=7, column=3, rowspan=1, columnspan=1, sticky="ew")   
        
        # Current condition row label - winds
        self.label0203a16 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="HIGH (F): ")
        self.label0203a16.grid(row=7, column=4, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a16 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a16.grid(row=7, column=5, rowspan=1, columnspan=1, sticky="ew")  
        
        # Current condition row label - humidity
        self.label0203a17 =  tk.Label(self.frame0203a, anchor="w", background="black", font=self.helv10bold, foreground="yellow", justify="left", text="HUMIDITY: ")
        self.label0203a17.grid(row=7, column=6, rowspan=1, columnspan=1, sticky="w")  
        self.text0203a17 = tk.Text(self.frame0203a, background="black", borderwidth=0, font=self.helv12bold, foreground="white", highlightthickness=0, height=1, width=4, wrap="word")
        self.text0203a17.grid(row=7, column=7, rowspan=1, columnspan=1, sticky="ew")        


        # Set flags for packed frame
        self.frame0203a_packed = True
        self.frame0203a.pack_propagate(False)


    def alarm_log_window(self):
        self.frame0203b = tk.Frame(self.frame0203, background="black")
        self.frame0203b.pack(side="top", fill="both", expand=True, padx=0, pady=0)         
        self.text0203b01 = tk.Text(self.frame0203b, background="black", borderwidth=0, font=self.helv08bold, foreground="white", highlightthickness=0, height=10, width=12, wrap="word")
        self.text0203b01.pack(side="left", fill="both", expand=True, padx=0, pady=10)
        self.frame0203b_packed = True
        self.frame0203b.pack_propagate(False)        


    def frame0501_buttons(self):
        """ FRAME 05 SCREEN SELECTOR BUTTONS """
        self.button050101 = tk.Button(self.frame0501, background="#2350b5", borderwidth=0, command=self.action050101, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="SERVICES", height=3, width=10)
        self.button050101.pack(side="top", fill="x", expand=False, padx=0, pady=1)
        self.button050102 = tk.Button(self.frame0501, background="#2350b5", borderwidth=0, command=self.action050102, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="LIGHTING", height=3, width=10)
        self.button050102.pack(side="top", fill="x", expand=False, padx=0, pady=1)
        self.button050103 = tk.Button(self.frame0501, background="#2350b5", borderwidth=0, command=self.action050103, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="HOME/AWAY", height=3, width=10)
        self.button050103.pack(side="top", fill="x", expand=False, padx=0, pady=1) 
        self.button050104 = tk.Button(self.frame0501, background="#2350b5", borderwidth=0, command=self.action050104, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="ENVIRO", height=3, width=10)
        self.button050104.pack(side="top", fill="x", expand=False, padx=0, pady=1)   
        self.button0501xx = tk.Button(self.frame0501, background="#2350b5", borderwidth=0, compound="center", font=self.helv08bold, foreground="black", highlightthickness=0, justify="right", relief="flat", height=3, width=10)
        self.button0501xx.pack(side="top", fill="both", expand=True, padx=0, pady=1)             

    def frame0503a_content(self):
        """ SERVICE CONTROL SCREEN """
        # overlay frame on 0503 for content changing purposes
        self.frame050301a = tk.Frame(self.frame0503, background="black", borderwidth=0, relief="flat", height=300, width=400)
        self.frame050301a.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame050301a_packed = True
        self.frame050301a.pack_propagate(False)
        # Add buttons to frame050301a    
        if self.enable[1] is True:
            self.button050301a01a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a01a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a01b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a01b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="LOG\nHANDLER", height=44, width=108)        
            self.button050301a01c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a01c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a01a.grid(row=1, column=0, padx=0, pady=0)
            self.button050301a01b.grid(row=1, column=1, padx=0, pady=0)        
            self.button050301a01c.grid(row=1, column=2, padx=0, pady=0)
        
        if self.enable[11] is True:
            self.button050301a02a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a02a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a02b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a02b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="LOGIC\nSOLVER", height=44, width=108)  
            self.button050301a02c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a02c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a02a.grid(row=2, column=0, padx=0, pady=0)
            self.button050301a02b.grid(row=2, column=1, padx=0, pady=0)        
            self.button050301a02c.grid(row=2, column=2, padx=0, pady=0)        

        if self.enable[12] is True:
            self.button050301a03a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a03a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a03b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a03b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="DB\nINTERFACE", height=44, width=108)  
            self.button050301a03c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a03c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a03a.grid(row=3, column=0, padx=0, pady=0)
            self.button050301a03b.grid(row=3, column=1, padx=0, pady=0)        
            self.button050301a03c.grid(row=3, column=2, padx=0, pady=0)        
        
        if self.enable[13] is True:
            self.button050301a04a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a04a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a04b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a04b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="HOME\nAWAY", height=44, width=108)  
            self.button050301a04c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a04c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a04a.grid(row=4, column=0, padx=0, pady=0)
            self.button050301a04b.grid(row=4, column=1, padx=0, pady=0)        
            self.button050301a04c.grid(row=4, column=2, padx=0, pady=0)

        if self.enable[14] is True:
            self.button050301a05a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a05a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a05b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a05b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="MOTION\nDETECTION", height=44, width=108)  
            self.button050301a05c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a05c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a05a.grid(row=5, column=0, padx=0, pady=0)
            self.button050301a05b.grid(row=5, column=1, padx=0, pady=0)        
            self.button050301a05c.grid(row=5, column=2, padx=0, pady=0)
        
        if self.enable[15] is True:
            self.button050301a06a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a06a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a06b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a06b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="RPI\nSCREEN", height=44, width=108)  
            self.button050301a06c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a06c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a06a.grid(row=6, column=0, padx=0, pady=0)
            self.button050301a06b.grid(row=6, column=1, padx=0, pady=0)        
            self.button050301a06c.grid(row=6, column=2, padx=0, pady=0)
        
        if self.enable[16] is True:
            self.button050301a07a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a07a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a07b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a07b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="WEMO\nGATEWAY", height=44, width=108)  
            self.button050301a07c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a07c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a07a.grid(row=7, column=0, padx=0, pady=0)
            self.button050301a07b.grid(row=7, column=1, padx=0, pady=0)        
            self.button050301a07c.grid(row=7, column=2, padx=0, pady=0)
        
        if self.enable[17] is True:
            self.button050301a08a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a08a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
            self.button050301a08b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a08b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="NEST\nGATEWAY", height=44, width=108)  
            self.button050301a08c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a08c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
            self.button050301a08a.grid(row=8, column=0, padx=0, pady=0)
            self.button050301a08b.grid(row=8, column=1, padx=0, pady=0)        
            self.button050301a08c.grid(row=8, column=2, padx=0, pady=0)        


    def frame0503b_content(self):
        """ LIGHTING CONTROL SCREEN """
        # overlay frame on 0503 for content changing purposes
        self.frame050301b = tk.Frame(self.frame0503, background="black", borderwidth=0, relief="flat", height=300, width=600)
        self.frame050301b.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame050301b_packed = True
        self.frame050301b.pack_propagate(False)
        # Add text and buttons to frame0404a  
        self.label050301b01 = tk.Label(self.frame050301b, anchor="ne", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="center", relief="flat", text="1ST FLOOR")
        self.label050301b02 = tk.Label(self.frame050301b, anchor="ne", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="center", relief="flat", text="2ND FLOOR")
        self.label050301b01.grid(row=0, column=0, columnspan=3, padx=4, pady=2, sticky="n")
        self.label050301b02.grid(row=0, column=3, columnspan=3, padx=4, pady=2, sticky="n")

        self.button050301b01a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b01a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b01b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b01b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="FRONT\nPATIO", height=44, width=108)  
        self.button050301b01c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b01c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b01a.grid(row=1, column=0, padx=2, pady=2)
        self.button050301b01b.grid(row=1, column=1, padx=2, pady=2)
        self.button050301b01c.grid(row=1, column=2, padx=2, pady=2)                
        
        self.button050301b02a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b02a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b02b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b02b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="BACK\nPATIO", height=44, width=108)        
        self.button050301b02c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b02c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b02a.grid(row=2, column=0, padx=2, pady=2)
        self.button050301b02b.grid(row=2, column=1, padx=2, pady=2)
        self.button050301b02c.grid(row=2, column=2, padx=2, pady=2)

        self.button050301b03a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b03a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b03b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b03b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="ENTRY\nWAY", height=44, width=108)
        self.button050301b03c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b03c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b03a.grid(row=3, column=0, padx=2, pady=2)
        self.button050301b03b.grid(row=3, column=1, padx=2, pady=2)
        self.button050301b03c.grid(row=3, column=2, padx=2, pady=2)

        self.button050301b04a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b04a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b04b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b04b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="COAT\nCORNER", height=44, width=108)        
        self.button050301b04c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b04c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b04a.grid(row=4, column=0, padx=2, pady=2)
        self.button050301b04b.grid(row=4, column=1, padx=2, pady=2)
        self.button050301b04c.grid(row=4, column=2, padx=2, pady=2)

        self.button050301b05a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b05a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b05b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b05b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="LIVING\nROOM", height=44, width=108)        
        self.button050301b05c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b05c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b05a.grid(row=5, column=0, padx=2, pady=2)
        self.button050301b05b.grid(row=5, column=1, padx=2, pady=2)
        self.button050301b05c.grid(row=5, column=2, padx=2, pady=2)

        self.button050301b06a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b06a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b06b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b06b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="DINING\nROOM", height=44, width=108)        
        self.button050301b06c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b06c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b06a.grid(row=6, column=0, padx=2, pady=2)
        self.button050301b06b.grid(row=6, column=1, padx=2, pady=2)
        self.button050301b06c.grid(row=6, column=2, padx=2, pady=2)        

        self.button050301b07a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b07a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b07b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b07b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="ALL 1ST\nFLOOR", height=44, width=108)
        self.button050301b07c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b07c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b07a.grid(row=7, column=0, padx=2, pady=2)
        self.button050301b07b.grid(row=7, column=1, padx=2, pady=2)
        self.button050301b07c.grid(row=7, column=2, padx=2, pady=2)        

        self.button050301b08a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b08a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b08b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b08b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="BEDROOM#1\nOVERHEAD", height=44, width=108)        
        self.button050301b08c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b08c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b08a.grid(row=1, column=3, padx=2, pady=2)
        self.button050301b08b.grid(row=1, column=4, padx=2, pady=2)
        self.button050301b08c.grid(row=1, column=5, padx=2, pady=2)

        self.button050301b09a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b09a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b09b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b09b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="BEDROOM#1\nLAMP", height=44, width=108)        
        self.button050301b09c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b09c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)
        self.button050301b09a.grid(row=2, column=3, padx=2, pady=2)
        self.button050301b09b.grid(row=2, column=4, padx=2, pady=2)
        self.button050301b09c.grid(row=2, column=5, padx=2, pady=2)        
        
        self.button050301b10a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b10a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b10b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b10b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="BEDROOM#2\nOVERHEAD", height=44, width=108)        
        self.button050301b10c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b10c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)   
        self.button050301b10a.grid(row=3, column=3, padx=2, pady=2)
        self.button050301b10b.grid(row=3, column=4, padx=2, pady=2)
        self.button050301b10c.grid(row=3, column=5, padx=2, pady=2)        
        
        self.button050301b11a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b11a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b11b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b11b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="BEDROOM#2\nLAMP", height=44, width=108)        
        self.button050301b11c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b11c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108) 
        self.button050301b11a.grid(row=4, column=3, padx=2, pady=2)
        self.button050301b11b.grid(row=4, column=4, padx=2, pady=2)
        self.button050301b11c.grid(row=4, column=5, padx=2, pady=2)        
        
        self.button050301b12a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b12a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b12b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b12b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="BEDROOM#3\nOVERHEAD", height=44, width=108)
        self.button050301b12c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b12c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108)  
        self.button050301b12a.grid(row=5, column=3, padx=2, pady=2)
        self.button050301b12b.grid(row=5, column=4, padx=2, pady=2)
        self.button050301b12c.grid(row=5, column=5, padx=2, pady=2)        
        
        self.button050301b13a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b13a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b13b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b13b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="BEDROOM#3\nLAMP", height=44, width=108)        
        self.button050301b13c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b13c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108) 
        self.button050301b13a.grid(row=6, column=3, padx=2, pady=2)
        self.button050301b13b.grid(row=6, column=4, padx=2, pady=2)
        self.button050301b13c.grid(row=6, column=5, padx=2, pady=2)          
        
        self.button050301b14a = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b14a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="ON", height=44, width=108)
        self.button050301b14b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b14b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="ALL 2ND\nFLOOR", height=44, width=108)        
        self.button050301b14c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b14c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108) 
        self.button050301b14a.grid(row=7, column=3, padx=2, pady=2)
        self.button050301b14b.grid(row=7, column=4, padx=2, pady=2)
        self.button050301b14c.grid(row=7, column=5, padx=2, pady=2)

    def frame0503c_content(self):
        """ HOME/AWAY CONTROL SCREEN """
        # overlay frame on 0503 for content changing purposes
        self.frame050301c = tk.Frame(self.frame0503, background="black", borderwidth=0, relief="flat", height=300, width=600)
        self.frame050301c.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame050301c_packed = True
        self.frame050301c.pack_propagate(False)
        # Add text and buttons to frame0404a  
        self.label050301c01 = tk.Label(self.frame050301c, anchor="ne", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="center", relief="flat", text="USERS")
        self.label050301c01.grid(row=0, column=0, columnspan=3, padx=4, pady=2, sticky="n")

        self.button050301c01a = tk.Button(self.frame050301c, anchor="se", background="black", borderwidth=0, command=self.action050301c01a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="SET\nHOME", height=44, width=108)
        self.button050301c01b = tk.Button(self.frame050301c, anchor="se", background="black", borderwidth=0, command=self.action050301c01b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="USER1\nHOME", height=44, width=108)  
        self.button050301c01c = tk.Button(self.frame050301c, anchor="se", background="black", borderwidth=0, command=self.action050301c01c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="SET\nAWAY", height=44, width=108)
        self.button050301c01a.grid(row=1, column=0, padx=2, pady=2)
        self.button050301c01b.grid(row=1, column=1, padx=2, pady=2)
        self.button050301c01c.grid(row=1, column=2, padx=2, pady=2)

    def frame0503d_content(self):
        """ HOME/AWAY CONTROL SCREEN """
        # overlay frame on 0503 for content changing purposes
        self.frame050301d = tk.Frame(self.frame0503, background="black", borderwidth=0, relief="flat", height=300, width=600)
        self.frame050301d.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame050301d_packed = True
        self.frame050301d.pack_propagate(False)
        # Add text and buttons to frame0404a  
        self.label050301d01 = tk.Label(self.frame050301d, anchor="ne", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="center", relief="flat", text="INTERNAL ENVIRONMENT")
        self.label050301d02 = tk.Label(self.frame050301d, anchor="ne", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="center", relief="flat", text="EXTERNAL ENVIRONMENT")
        self.label050301d01.grid(row=0, column=0, columnspan=3, padx=4, pady=2, sticky="n")
        self.label050301d02.grid(row=0, column=3, columnspan=3, padx=4, pady=2, sticky="n")

    def update_alarm_window(self):
        # Determine size of logfile (number of lines)
        self.num_lines = sum(1 for line in open(self.display_file))
        # If line index is larger than logfile (meaning log file was reset), reset index to match log-file size
        if self.line > (self.num_lines + 1):
            self.line = self.num_lines
            # Correct for line pointers less than 1
            if self.line < 1:
                self.line = 1
        # Read line from file
        try:
            self.text = linecache.getline(self.display_file, self.line)
        except:
            print("could not access file")
            self.text = str()
        # Processing logfile
        self.iter = 1
        while len(self.text) != 0 and self.iter < 1000:
            if self.text.find("heartbeat") == -1 and self.text.find("[00,11,001,,]") == -1:
                self.text0203b01.insert(tk.END, self.text)
                self.text0203b01.yview_pickplace("end")
            self.line += 1
            self.text = linecache.getline(self.display_file, self.line)
            self.iter += 1
        linecache.clearcache()

    def update_status_window(self):
        self.text0203a01.delete(1.0, tk.END)
        self.dt = datetime.datetime.now()
        self.datetime_to_go = datetime.datetime.combine(self.dt.date(), self.time_to_go)
        self.start_time = self.datetime_to_go + datetime.timedelta(minutes=-60)
        self.end_time = self.datetime_to_go + datetime.timedelta(minutes=30)
        if self.start_time <= self.dt <= self.end_time:
            if self.dt <= self.datetime_to_go:
                self.time_remaining = self.datetime_to_go - self.dt
                self.label0203a01.config(foreground="orange", text="TIME TO GO")
                self.text0203a01.insert(tk.END, ("%s" % self.time_remaining))
                self.text0203a01.config(foreground="orange")
            else:
                self.time_remaining = self.dt - self.datetime_to_go
                self.label0203a01.config(foreground="red", text="WE ARE LATE!!")
                self.text0203a01.insert(tk.END, ("%s" % self.time_remaining))
                self.text0203a01.config(foreground="red")
        else:
            self.label0203a01.config(foreground="yellow", text="CURRENT DATE & TIME")
            self.text0203a01.insert(tk.END, self.dt.strftime("%Y-%m-%d     %I:%M:%S %p"))
            self.text0203a01.config(foreground="white")
        # Current condition display
        self.text0203a04.delete(1.0, tk.END)
        self.text0203a04.insert(tk.END, self.current_conditions[0])
        self.text0203a05.delete(1.0, tk.END)
        self.text0203a05.insert(tk.END, self.current_conditions[1])
        self.text0203a06.delete(1.0, tk.END)
        self.text0203a06.insert(tk.END, self.current_conditions[2])
        self.text0203a07.delete(1.0, tk.END)
        self.text0203a07.insert(tk.END, self.current_conditions[3])
        self.text0203a09.delete(1.0, tk.END)
        self.text0203a09.insert(tk.END, self.current_forecast[0])
        self.text0203a10.delete(1.0, tk.END)
        self.text0203a10.insert(tk.END, self.current_forecast[1])
        self.text0203a11.delete(1.0, tk.END)
        self.text0203a11.insert(tk.END, self.current_forecast[2])
        self.text0203a12.delete(1.0, tk.END)
        self.text0203a12.insert(tk.END, self.current_forecast[3])  
        self.text0203a14.delete(1.0, tk.END)
        self.text0203a14.insert(tk.END, self.tomorrow_forecast[0])
        self.text0203a15.delete(1.0, tk.END)
        self.text0203a15.insert(tk.END, self.tomorrow_forecast[1])
        self.text0203a16.delete(1.0, tk.END)
        self.text0203a16.insert(tk.END, self.tomorrow_forecast[2])
        self.text0203a17.delete(1.0, tk.END)
        self.text0203a17.insert(tk.END, self.tomorrow_forecast[3])              
                 


    def action010101(self):
        self.logger.debug("Button 010101 was pressed")
        pass


    def action020101(self):
        if self.frame0203a_packed is False:
            self.frame0203a.pack(anchor="nw", side="top", fill="both", expand=True, padx=0, pady=0)
            self.frame0203a.pack_propagate(False)
            self.frame0203a_packed = True
            self.label010202.config(text="CURRENT STATUS") 
        pass
        if self.frame0203b_packed is True:
            self.frame0203b.pack_forget()
            self.frame0203b_packed = False

    def action020102(self):
        if self.frame0203b_packed is False:
            self.frame0203b.pack(anchor="nw", side="top", fill="both", expand=True, padx=0, pady=0)
            self.frame0203b.pack_propagate(False)
            self.frame0203b_packed = True
            self.label010202.config(text="SYSTEM LOG")
        pass
        if self.frame0203a_packed is True:
            self.frame0203a.pack_forget()
            self.frame0203a_packed = False


    def action030101(self):
        self.logger.debug("Button 030101 was pressed")
        pass 

    def action040101(self):
        self.logger.debug("Button 040101 was pressed")
        pass
 

    def action050101(self):
        self.scanWemo = False
        self.logger.debug("Button 050101 was pressed")
        if self.frame050301a_packed is False:
            self.frame050301a.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)
            self.frame050301a.pack_propagate(False)
            self.frame050301a_packed = True
            self.label040202.config(text="SYSTEM SERVICES")
        pass           
        if self.frame050301b_packed is True:
            self.frame050301b.pack_forget()
            self.frame050301b_packed = False
        if self.frame050301c_packed is True:
            self.frame050301c.pack_forget()
            self.frame050301c_packed = False 
        if self.frame050301d_packed is True:
            self.frame050301d.pack_forget()
            self.frame050301d_packed = False             
        pass

    def action050102(self):
        self.logger.debug("Button 050102 was pressed")
        self.scanWemo = True
        if self.frame050301b_packed is False:
            self.frame050301b.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)
            self.frame050301b.pack_propagate(False)
            self.frame050301b_packed = True
            self.label040202.config(text="INTERIOR LIGHTING")
        pass           
        if self.frame050301a_packed is True:
            self.frame050301a.pack_forget()
            self.frame050301a_packed = False
        if self.frame050301c_packed is True:
            self.frame050301c.pack_forget()
            self.frame050301c_packed = False 
        if self.frame050301d_packed is True:
            self.frame050301d.pack_forget()
            self.frame050301d_packed = False             
        pass

    def action050103(self):
        self.scanWemo = False
        self.logger.debug("Button 050103 was pressed")
        if self.frame050301c_packed is False:
            self.frame050301c.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)
            self.frame050301c.pack_propagate(False)
            self.frame050301c_packed = True 
            self.label040202.config(text="HOME/AWAY STATUS")
        pass           
        if self.frame050301a_packed is True:
            self.frame050301a.pack_forget()
            self.frame050301a_packed = False
        if self.frame050301b_packed is True:
            self.frame050301b.pack_forget()
            self.frame050301b_packed = False 
        if self.frame050301d_packed is True:
            self.frame050301d.pack_forget()
            self.frame050301d_packed = False                       
        pass   

    def action050104(self):
        self.scanWemo = False
        self.logger.debug("Button 050103 was pressed")
        if self.frame050301d_packed is False:
            self.frame050301d.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)
            self.frame050301d.pack_propagate(False)
            self.frame050301d_packed = True
            self.label040202.config(text="ENVIRONMENTAL CONTROL")
        pass           
        if self.frame050301a_packed is True:
            self.frame050301a.pack_forget()
            self.frame050301a_packed = False
        if self.frame050301b_packed is True:
            self.frame050301b.pack_forget()
            self.frame050301b_packed = False 
        if self.frame050301c_packed is True:
            self.frame050301c.pack_forget()
            self.frame050301c_packed = False                       
        pass              


    # START / CHECK / STOP Controls for: Log handler process
    def action050301a01a(self):
        self.logger.debug("Button 050301a01a was pressed")
        self.msg_to_send = Message(source="02", dest="01", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a01b(self):
        self.logger.debug("Button 050301a01b was pressed")
        self.msg_to_send = Message(source="02", dest="01", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
   
    def action050301a01c(self):
        self.logger.debug("Button 050301a01c was pressed")
        self.msg_to_send = Message(source="02", dest="01", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)            


    # START / CHECK / STOP Controls for: Logic Solver process
    def action050301a02a(self):
        self.logger.debug("Button 050301a02a was pressed")
        self.msg_to_send = Message(source="02", dest="11", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a02b(self):
        self.logger.debug("Button 050301a02b was pressed")
        self.msg_to_send = Message(source="02", dest="11", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)    
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)                

    def action050301a02c(self):
        self.logger.debug("Button 050301a02c was pressed")
        self.msg_to_send = Message(source="02", dest="11", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)            


    # START / CHECK / STOP Controls for: Future process
    def action050301a03a(self):
        self.logger.debug("Button 050301a03a was pressed")
        self.msg_to_send = Message(source="02", dest="12", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a03b(self):
        self.logger.debug("Button 050301a03b was pressed")
        self.msg_to_send = Message(source="02", dest="12", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
     
    def action050301a03c(self):
        self.logger.debug("Button 050301a03c was pressed")
        self.msg_to_send = Message(source="02", dest="12", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Button 050301a03c was pressed - Sending message [%s]", self.msg_to_send.raw)


    # START / CHECK / STOP Controls for: Home / Away process
    def action050301a04a(self):
        self.logger.debug("Button 050301a04a was pressed")
        self.msg_to_send = Message(source="02", dest="13", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a04b(self):
        self.logger.debug("Button 050301a04b was pressed")
        self.msg_to_send = Message(source="02", dest="13", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw) 
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 

    def action050301a04c(self):
        self.logger.debug("Button 050301a04c was pressed")
        self.msg_to_send = Message(source="02", dest="13", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)


    # START / CHECK / STOP Controls for: Future process
    def action050301a05a(self):
        self.logger.debug("Button 050301a05a was pressed")
        self.msg_to_send = Message(source="02", dest="14", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a05b(self):
        self.logger.debug("Button 050301a05b was pressed")
        self.msg_to_send = Message(source="02", dest="14", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw) 
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 

    def action050301a05c(self):
        self.logger.debug("Button 050301a05c was pressed")
        self.msg_to_send = Message(source="02", dest="14", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)


    # START / CHECK / STOP Controls for: Rpi Screen process
    def action050301a06a(self):
        self.logger.debug("Button 050301a06a was pressed")
        self.msg_to_send = Message(source="02", dest="15", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a06b(self):
        self.logger.debug("Button 050301a06b was pressed")
        self.msg_to_send = Message(source="02", dest="15", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw) 
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        

    def action050301a06c(self):
        self.logger.debug("Button 050301a06c was pressed")
        self.msg_to_send = Message(source="02", dest="15", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw) 
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)


    # START / CHECK / STOP Controls for: Wemo Gateway process
    def action050301a07a(self):
        self.logger.debug("Button 050301a07a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw) 
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="02", dest="11", type="168")           
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a07b(self):
        self.logger.debug("Button 050301a07b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw) 
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a07c(self):
        self.logger.debug("Button 050301a07c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)


    # START / CHECK / STOP Controls for: Nest Gateway process
    def action050301a08a(self):
        self.logger.debug("Button 050301a08a was pressed")
        self.msg_to_send = Message(source="02", dest="17", type="900")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw) 
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a08b(self):
        self.logger.debug("Button 050301a08b was pressed")        
        self.msg_to_send = Message(source="02", dest="17", type="???")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301a08c(self):
        self.logger.debug("Button 050301a08c was pressed")
        self.msg_to_send = Message(source="02", dest="17", type="999")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)


    # ON / QUERY / OFF Control for device: fylt1
    def action050301b01a(self):
        self.logger.debug("Button 050301b01a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="fylt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b01b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [fylt1] to green")

    def action050301b01b(self):
        self.logger.debug("Button 050301b01b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="fylt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301b01c(self):
        self.logger.debug("Button 050301b01c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="fylt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b01b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [fylt1] to red")


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b02a(self):
        self.logger.debug("Button 050301b02a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="bylt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b02b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [bylt1] to green")

    def action050301b02b(self):
        self.logger.debug("Button 050301b02b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="bylt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301b02c(self):
        self.logger.debug("Button 050301b02c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="bylt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.button050301b02b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [bylt1] to red")        


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b03a(self):
        self.logger.debug("Button 050301b03a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="ewlt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b03b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [ewlt1] to green")

    def action050301b03b(self):
        self.logger.debug("Button 050301b03b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="ewlt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        

    def action050301b03c(self):
        self.logger.debug("Button 050301b03c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="ewlt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b03b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [ewlt1] to red")   


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b04a(self):
        self.logger.debug("Button 050301b04a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="cclt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b04b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [cclt1] to green")

    def action050301b04b(self):
        self.logger.debug("Button 050301b04b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="cclt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        

    def action050301b04c(self):
        self.logger.debug("Button 050301b04c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="cclt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)         
        self.button050301b04b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [cclt1] to red")          


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b05a(self):
        self.logger.debug("Button 050301b05a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="lrlt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b05b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [lrlt1] to green")

    def action050301b05b(self):
        self.logger.debug("Button 050301b05b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="lrlt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301b05c(self):
        self.logger.debug("Button 050301b05c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="lrlt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b05b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [lrlt1] to red")          


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b06a(self):
        self.logger.debug("Button 050301b06a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="drlt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.button050301b06b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [drlt1] to green")

    def action050301b06b(self):
        self.logger.debug("Button 050301b06b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="drlt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 

    def action050301b06c(self):
        self.logger.debug("Button 050301b06c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="drlt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.button050301b06b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [drlt1] to red")            


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b07a(self):
        self.logger.debug("Button 050301b07a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="lrlt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="161", name="drlt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)   
        self.msg_to_send = Message(source="02", dest="16", type="161", name="cclt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="161", name="ewlt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)   
        self.button050301b03b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [lr1lt1] to green")
        self.button050301b04b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [dr1lt1] to green")
        self.button050301b05b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [cc1lt1] to green")
        self.button050301b06b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [ew1lt1] to green")  

    def action050301b07b(self):
        self.logger.debug("Button 050301b07b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="fylt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)  
        self.msg_to_send = Message(source="02", dest="16", type="162", name="bylt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="162", name="lrlt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="162", name="drlt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="162", name="cclt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="162", name="ewlt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 

    def action050301b07c(self):
        self.logger.debug("Button 050301b07c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="lrlt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="161", name="drlt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="161", name="cclt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.msg_to_send = Message(source="02", dest="16", type="161", name="ewlt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 
        self.button050301b03b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [lr1lt1] to red")
        self.button050301b04b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [dr1lt1] to red")
        self.button050301b05b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [cc1lt1] to red")
        self.button050301b06b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [ew1lt1] to red")


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b08a(self):
        self.logger.debug("Button 050301b08a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b08b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br1lt1] to green")       

    def action050301b08b(self):
        self.logger.debug("Button 050301b08b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br1lt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301b08c(self):
        self.logger.debug("Button 050301b08c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)  
        self.button050301b08b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br1lt1] to red")           


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b09a(self):
        self.logger.debug("Button 050301b09a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt2", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b09b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br1lt2] to green")       

    def action050301b09b(self):
        self.logger.debug("Button 050301b09b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br1lt2")  
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301b09c(self):
        self.logger.debug("Button 050301b09c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt2", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b09b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br1lt2] to red")


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b10a(self):
        self.logger.debug("Button 050301b10a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b10b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br2lt1] to green")

    def action050301b10b(self):
        self.logger.debug("Button 050301b10b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br2lt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301b10c(self):
        self.logger.debug("Button 050301b10c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b10b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br2lt1] to red")  


    # ON / QUERY / OFF Control for device: bylt1
    def action050301b11a(self):
        self.logger.debug("Button 050301b11a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt2", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        
        self.button050301b11b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br2lt2] to green")        

    def action050301b11b(self):
        self.logger.debug("Button 050301b11b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br2lt2")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)        

    def action050301b11c(self):
        self.logger.debug("Button 050301b11c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt2", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b11b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br2lt2] to red")


    # ON / QUERY / OFF Control for device: br3lt1
    def action050301b12a(self):
        self.logger.debug("Button 050301b12a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b12b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br3lt1] to green")

    def action050301b12b(self):
        self.logger.debug("Button 050301b12b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br3lt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)

    def action050301b12c(self):
        self.logger.debug("Button 050301b12c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b12b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br3lt1] to red")             


    # ON / QUERY / OFF Control for device: br3lt2
    def action050301b13a(self):
        self.logger.debug("Button 050301b13a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt2", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b13b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br3lt2] to green")     

    def action050301b13b(self):
        self.logger.debug("Button 050301b13b was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br3lt2")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw) 

    def action050301b13c(self):
        self.logger.debug("Button 050301b13c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt2", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)            
        self.button050301b13b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br3lt2] to red")



    def action050301b14a(self):
        self.logger.debug("Button 050301b14a was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt2", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt2", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt1", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt2", payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)  
        
        self.button050301b08b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br1lt1] to green")
        self.button050301b09b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br1lt2] to green")
        self.button050301b10b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br2lt1] to green")
        self.button050301b11b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br2lt2] to green")
        self.button050301b12b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br3lt1] to green")
        self.button050301b13b.config(image=self.button_square_green_img)
        self.logger.debug("Setting color of status indicator for device [br3lt2] to green")


    def action050301b14b(self):
        self.logger.debug("Button 050301b14b was pressed")
        
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br1lt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br1lt2")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br2lt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br2lt2")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br3lt1")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        
        self.msg_to_send = Message(source="02", dest="16", type="162", name="br3lt2")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)


    def action050301b14c(self):
        self.logger.debug("Button 050301b14c was pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br1lt2", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br2lt2", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt1", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.msg_to_send = Message(source="02", dest="16", type="161", name="br3lt2", payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        self.logger.debug("Sending message [%s]", self.msg_to_send.raw)
        self.button050301b08b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br1lt1] to red") 
        self.button050301b09b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br1lt2] to red")
        self.button050301b10b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br2lt1] to red")
        self.button050301b11b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br2lt2] to red")
        self.button050301b12b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br3lt1] to red")
        self.button050301b13b.config(image=self.button_square_red_img)
        self.logger.debug("Setting color of status indicator for device [br3lt2] to red")    


    def action050301c01a(self):
        self.logger.debug("Button 050301c01a was pressed")
        self.button050301c01b.config(image=self.button_square_green_img)

    def action050301c01b(self):
        self.logger.debug("Button 050301c01b was pressed")

    def action050301c01c(self):
        self.logger.debug("Button 050301c01C was pressed") 
        self.button050301c01b.config(image=self.button_square_red_img)    


    def action060101(self):
        self.logger.debug("Button 060101 was pressed")
        pass        

    def after_tasks(self):
        #self.logger.debug("Running \"after\" task")
        # Process incoming message queue
        try:
            self.msg_in = Message(raw=self.msg_in_queue.get_nowait())    
            #self.logger.debug("Checked in msg queue and found msg: %s" % self.msg_in.raw)   
        except:
            pass
        # Process incoming message
        if len(self.msg_in.raw) > 4:
            self.logger.debug("Processing message [%s] from incoming message queue" % self.msg_in.raw)
            if self.msg_in.dest == "02":
                
                if self.msg_in.type == "001":
                    self.last_hb = time.time()
                
                elif self.msg_in.type == "002":
                    if self.msg_in.source == "01":
                        self.button050301a01b.config(image=self.button_square_green_img)
                    elif self.msg_in.source == "11":
                        self.button050301a02b.config(image=self.button_square_green_img)
                    elif self.msg_in.source == "12":
                        self.button050301a03b.config(image=self.button_square_green_img)
                    elif self.msg_in.source == "13":
                        self.button050301a04b.config(image=self.button_square_green_img)
                    elif self.msg_in.source == "14":
                        self.button050301a05b.config(image=self.button_square_green_img)
                    elif self.msg_in.source == "15":
                        self.button050301a06b.config(image=self.button_square_green_img)
                    elif self.msg_in.source == "16":
                        self.button050301a07b.config(image=self.button_square_green_img)
                    elif self.msg_in.source == "17":
                        self.button050301a08b.config(image=self.button_square_green_img)
        
                elif self.msg_in.type == "003":
                    if self.msg_in.source == "01":
                        self.button050301a01b.config(image=self.button_square_red_img)
                    elif self.msg_in.source == "11":
                        self.button050301a02b.config(image=self.button_square_red_img)
                    elif self.msg_in.source == "12":
                        self.button050301a03b.config(image=self.button_square_red_img)
                    elif self.msg_in.source == "13":
                        self.button050301a04b.config(image=self.button_square_red_img)
                    elif self.msg_in.source == "14":
                        self.button050301a05b.config(image=self.button_square_red_img)
                    elif self.msg_in.source == "15":
                        self.button050301a06b.config(image=self.button_square_red_img)
                    elif self.msg_in.source == "16":
                        self.button050301a07b.config(image=self.button_square_red_img)
                    elif self.msg_in.source == "17":
                        self.button050301a08b.config(image=self.button_square_red_img)

                elif self.msg_in.type == "020":
                    self.current_conditions = (self.msg_in.payload).split(sep=",")
                    self.logger.debug("Current condition response [%s] received from nest gateway", self.msg_in.raw)

                elif self.msg_in.type == "021":
                    self.current_forecast = (self.msg_in.payload).split(sep=",")
                    self.logger.debug("Today's forecast response [%s] received from nest gateway", self.msg_in.raw)                    

                elif self.msg_in.type == "022":
                    self.tomorrow_forecast = (self.msg_in.payload).split(sep=",")      
                    self.logger.debug("Tomorrow's forecast response [%s] received from nest gateway", self.msg_in.raw)                                                 
                
                elif self.msg_in.type == "163":
                    if self.msg_in.payload == "0":
                        if self.msg_in.name == "fylt1":
                            self.button050301b01b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "bylt1":
                            self.button050301b02b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "ewlt1":
                            self.button050301b03b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "cclt1":
                            self.button050301b04b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "lrlt1":
                            self.button050301b05b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "drlt1":
                            self.button050301b06b.config(image=self.button_square_red_img)                        
                        elif self.msg_in.name == "br1lt1":
                            self.button050301b08b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "br1lt2":
                            self.button050301b09b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "br2lt1":
                            self.button050301b10b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "br2lt2":
                            self.button050301b11b.config(image=self.button_square_red_img) 
                        elif self.msg_in.name == "br3lt1":
                            self.button050301b12b.config(image=self.button_square_red_img)
                        elif self.msg_in.name == "br3lt2":
                            self.button050301b13b.config(image=self.button_square_red_img) 
                    elif self.msg_in.payload == "1":
                        if self.msg_in.name == "fylt1":
                            self.button050301b01b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "bylt1":
                            self.button050301b02b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "ewlt1":
                            self.button050301b03b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "cclt1":
                            self.button050301b04b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "lrlt1":
                            self.button050301b05b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "drlt1":
                            self.button050301b06b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "br1lt1":
                            self.button050301b08b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "br1lt2":
                            self.button050301b09b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "br2lt1":
                            self.button050301b10b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "br2lt2":
                            self.button050301b11b.config(image=self.button_square_green_img) 
                        elif self.msg_in.name == "br3lt1":
                            self.button050301b12b.config(image=self.button_square_green_img)
                        elif self.msg_in.name == "br3lt2":
                            self.button050301b13b.config(image=self.button_square_green_img)                                                                            
                                       
                elif self.msg_in.type == "999":
                    self.logger.debug("Kill code received - Shutting down: %s" % self.msg_in.raw)
                    self.close_pending = True
            else:
                self.msg_out_queue.put_nowait(self.msg_in.raw)
                self.logger.debug("Redirecting message [%s] back to main" % self.msg_in.raw)                
            pass  
            self.msg_in = Message()

        # Send periodic querries to field devices to get current status
        if self.close_pending is False and self.scanWemo is True:
            if datetime.datetime.now() > self.last_update + datetime.timedelta(seconds=10):
                self.msg_to_send = Message(source="02", dest="16", type="162", name="fylt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="bylt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="ewlt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="cclt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="lrlt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="drlt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="br1lt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="br1lt2")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="br2lt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="br2lt2")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="br3lt1")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.msg_to_send = Message(source="02", dest="16", type="162", name="br3lt2")
                self.msg_out_queue.put_nowait(self.msg_to_send.raw)
                self.last_update = datetime.datetime.now()
        
              

        # If a close is pending, wait until all messages have been processed before closing down the window
        # Otherwise schedule another run of the "after" process 
        if ((self.close_pending is True) and (len(self.msg_in.raw) == 0) and (self.msg_in_queue.empty() is True)) or (time.time() > (self.last_hb + 30)):
            self.window.destroy()
        else:
            # Update visual aspects of main window (text, etc)
            if self.frame0203a_packed is True:
                self.update_status_window()
            if self.frame0203b_packed is True:
                self.update_alarm_window()
            # Re-schedule after task to run again in another 1000ms
            self.window.after(500, self.after_tasks)
            #self.logger.debug("Re-scheduled next after event")
        pass


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close_pending = True
            # Kill p167(nest gateway)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="17", type="999").raw)
                self.logger.debug("Kill code sent to p17_nest_gateway process")
            except:
                self.logger.debug("Could not send kill-code to p17_nest_gateway process.  Queue already closed")
            # Kill p16 (wemo gateway)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="16", type="999").raw)
                self.logger.debug("Kill code sent to p16_wemo_gateway process") 
            except:
                self.logger.debug("Could not send kill-code to p16_wemo_gateway process.  Queue already closed")           
            # Kill p15 (rpi screen)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="15", type="999").raw)
                self.logger.debug("Kill code sent to p15_rpi_screen process")  
            except:
                self.logger.debug("Could not send kill-code to p15_rpi_screen process.  Queue already closed")                
            # Kill p14 (motion detector)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="14", type="999").raw)
                self.logger.debug("Kill code sent to p14_motion process") 
            except:
                self.logger.debug("Could not send kill-code to p14_motion process.  Queue already closed")                
            # Kill p13 (home / away)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="13", type="999").raw)
                self.logger.debug("Kill code sent to p13_home_away process")   
            except:
                self.logger.debug("Could not send kill-code to p13_home_away process.  Queue already closed")                
            # Kill p12 (db interface)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="12", type="999").raw)
                self.logger.debug("Kill code sent to p12_db_interface process") 
            except:
                self.logger.debug("Could not send kill-code to p12_db_interface process.  Queue already closed")                                                         
            # Kill p11 (logic solver)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="11", type="999").raw)
                self.logger.debug("Kill code sent to p11_logic_solver process")
            except:
                self.logger.debug("Could not send kill-code to p11_logic_solver process.  Queue already closed")                
            # Kill p02 (gui)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="02", type="999").raw)
                self.logger.debug("Kill code sent to p02_gui process")  
            except:
                self.logger.debug("Could not send kill-code to p02_gui process.  Queue already closed")                                                          
            # Kill p00 (main)
            try:
                self.msg_out_queue.put_nowait(Message(source="02", dest="00", type="999").raw)   
                self.logger.debug("Kill code sent to p00_main process")
            except:
                self.logger.debug("Could not send kill-code to p00_main process.  Queue already closed")                
            # Close msg out queue
            self.msg_out_queue.close()
            # Close application main window
            #self.window.destroy()
