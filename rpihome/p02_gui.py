#!/usr/bin/python3
""" gui.py:   
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import copy
import linecache
import logging
import multiprocessing
import os
import platform
import sys
import time
import tkinter as tk
from tkinter import font
from tkinter import messagebox


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The RPi-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"



# Main gui process loop **********************************************************************************************
def gui_func(msg_in_queue, msg_out_queue, log_queue, log_configurer, logfile):
    log_configurer(log_queue)
    name = multiprocessing.current_process().name
    logger = logging.getLogger("main")
    logging.log(logging.DEBUG, "Logging handler for gui process started")

    # Create gui
    gui = MainWindow(msg_in_queue, msg_out_queue, log_queue, logfile)
    logging.log(logging.DEBUG, "creating main window")

    # Schedule "after" process to run oncmsg_oute main window is generated (used for periodic screen updates)
    gui.window.after(500, gui.after_tasks)
    logging.log(logging.DEBUG, "scheduling initial \"after\" task")
    
    # Start handler for window exit button
    gui.window.protocol("WM_DELETE_WINDOW", gui.on_closing)

    # Run mainloop() to activate gui and begin monitoring its inputs
    logging.log(logging.DEBUG, "starting gui mainloop")
    gui.window.mainloop()



# Application GUI Class Definition *************************************************************************************
class MainWindow(object):
    def __init__(self, msg_in_queue, msg_out_queue, log_queue, logfile):
        self.log_queue = log_queue
        self.logfile = logfile
        self.text = str()
        self.msg_in_queue = msg_in_queue
        self.msg_out_queue = msg_out_queue
        self.msg_in = str()
        self.close_pending = False
        self.last_hb = time.time()
        self.index = 0

        self.line = sum(1 for line in open(self.logfile)) - 50
        if self.line < 1:
            self.line = 1

        self.basepath = os.path.dirname(sys.argv[0])  
        self.resourceDir = os.path.join(self.basepath, "resources/")      

        self.helv08bold = ()
        self.helv10bold = ()
        self.helv12bold = ()
        self.helv16bold = ()
        self.helv36 = ()
        self.button_elbow_NE_img = ()
        self.button_elbow_NW_img = ()
        self.button_elbow_SE_img = ()
        self.button_elbow_SW_img = ()
        self.button_green_round_left_img = ()
        self.button_green_round_right_img = ()
        self.button_red_round_left_img = ()
        self.button_red_round_right_img = ()

        self.gen_main_window()
        self.define_fonts()
        self.define_images()
        self.divide_screen()
        self.top_divider_bar1()
        self.alarm_log_window()
        self.bottom_divider_bar1()
        self.top_divider_bar2()
        self.bottom_divider_bar2()
        self.frame0501_buttons()
        self.frame0503a_content()
        self.frame0503b_content()
        self.frame050301b.pack_forget()
        self.frame050301b_packed = False
    
    def gen_main_window(self):
        # CREATE PRIMARY (ROOT) WINDOW
        self.window = tk.Tk()   
        self.window.title("RPi Home")
        self.window.geometry("%sx%s+%s+%s" % (800, 810, 1, 1))
        self.window.config(background="black") 
        logging.log(logging.DEBUG, "Main application window created")


    def define_fonts(self):
        # Define fonts used in the application
        self.helv08bold = font.Font(family="Helvetica", size=8, weight="bold")
        self.helv10bold = font.Font(family="Helvetica", size=10, weight="bold")
        self.helv12bold = font.Font(family="Helvetica", size=12, weight="bold")
        self.helv16bold = font.Font(family="Helvetica", size=16, weight="bold")
        self.helv36 = font.Font(family="Helvetica", size=36, weight="bold")


    def define_images(self):
        # DEFINE IMAGES
        self.button_elbow_NE_img = tk.PhotoImage(file=self.resourceDir + "Elbow-blue-up-left.png")
        self.button_elbow_NW_img = tk.PhotoImage(file=self.resourceDir + "Elbow-blue-up-right.png")
        self.button_elbow_SE_img = tk.PhotoImage(file=self.resourceDir + "Elbow-blue-down-left.png")
        self.button_elbow_SW_img = tk.PhotoImage(file=self.resourceDir + "Elbow-blue-down-right.png")
        self.button_green_round_left_img = tk.PhotoImage(file=self.resourceDir + "button_green_round_left.png")
        self.button_green_round_right_img = tk.PhotoImage(file=self.resourceDir + "button_green_round_right.png")
        self.button_151_195_225_round_left_img = tk.PhotoImage(file=self.resourceDir + "button_151,195,225_round_left.png")
        self.button_151_195_225_round_right_img = tk.PhotoImage(file=self.resourceDir + "button_151,195,225_round_right.png") 
        self.button_red_round_left_img = tk.PhotoImage(file=self.resourceDir + "button_red_round_left.png")
        self.button_red_round_right_img = tk.PhotoImage(file=self.resourceDir + "button_red_round_right.png")
        self.button_square_green_img = tk.PhotoImage(file=self.resourceDir + "button-square-green.png")
        self.button_square_red_img = tk.PhotoImage(file=self.resourceDir + "button-square-red.png")        


    def divide_screen(self):
        self.screen1 = tk.Frame(self.window, background="black")
        self.screen1.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        logging.log(logging.DEBUG, "Overlayed 1 primary frame over-top of application (root) window")

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
        logging.log(logging.DEBUG, "Overlayed 6 sub-frames, packed top to bottom over-top of primary frame")   

        # split frame 1 into 2 sections along a vertical axis
        self.frame0101 = tk.Frame(self.frame01, background="yellow", height=50, width=105)
        self.frame0101.pack(side="left", fill="none", expand=False, padx=0, pady=0)  
        self.frame0101.pack_propagate(False) 
        self.frame0102 = tk.Frame(self.frame01, background="blue", height=50, width=695)
        self.frame0102.pack(side="left", fill="x", expand=True, padx=1, pady=1)  
        self.frame0102.pack_propagate(False)

        # split frame 2 into 3 sections along a vertical axis
        self.frame0201 = tk.Frame(self.frame02, background="#2350b5", height=200, width=85)
        self.frame0201.pack(side="left", fill="y", expand=False, padx=0, pady=0)  
        self.frame0201.pack_propagate(False)  
        self.frame0202 = tk.Frame(self.frame02, background="black", height=200, width=20)
        self.frame0202.pack(side="left", fill="y", expand=False, padx=0, pady=0) 
        self.frame0202.pack_propagate(False) 
        self.frame0203 = tk.Frame(self.frame02, background="black", height=200, width=695)
        self.frame0203.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.frame0203.pack_propagate(False) 

        # split frame 3 into 2 sections along a vertical axis
        self.frame0301 = tk.Frame(self.frame03, background="yellow", height=50, width=105)
        self.frame0301.pack(side="left", fill="none", expand=False, padx=0, pady=0)  
        self.frame0301.pack_propagate(False) 
        self.frame0302 = tk.Frame(self.frame03, background="blue", height=50, width=695)
        self.frame0302.pack(side="left", fill="x", expand=True, padx=1, pady=1)  
        self.frame0302.pack_propagate(False)

        # split frame 4 into 2 sections along a vertical axis
        self.frame0401 = tk.Frame(self.frame04, background="yellow", height=50, width=105)
        self.frame0401.pack(side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame0401.pack_propagate(False)
        self.frame0402 = tk.Frame(self.frame04, background="blue", height=50, width=695)
        self.frame0402.pack(side="left", fill="x", expand=True, padx=1, pady=1)  
        self.frame0402.pack_propagate(False)

        # split frame 5 into 3 sections along a vertical axis
        self.frame0501 = tk.Frame(self.frame05, background="#2350b5", height=400, width=85)
        self.frame0501.pack(side="left", fill="y", expand=False, padx=0, pady=0) 
        self.frame0501.pack_propagate(False)  
        self.frame0502 = tk.Frame(self.frame05, background="black", height=400, width=20)
        self.frame0502.pack(side="left", fill="y", expand=False, padx=0, pady=0) 
        self.frame0502.pack_propagate(False)
        self.frame0503 = tk.Frame(self.frame05, background="black", height=400, width=695)
        self.frame0503.pack(side="left", fill="both", expand=True, padx=0, pady=0)

        # split frame 6 into 2 sections along a vertical axis
        self.frame0601 = tk.Frame(self.frame06, background="yellow", height=50, width=105)
        self.frame0601.pack(side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame0601.pack_propagate(False)
        self.frame0602 = tk.Frame(self.frame06, background="blue", height=50, width=695)
        self.frame0602.pack(side="left", fill="x", expand=True, padx=1, pady=1) 
        self.frame0602.pack_propagate(False)

        # split frame 0102 into 2 sections along a horizontal axis
        self.frame010201 = tk.Frame(self.frame0102, background="#2350b5", height=17, width=695)
        self.frame010201.pack(side="top", fill="x", expand=True, padx=0, pady=0)  
        self.frame010201.pack_propagate(False)
        self.frame010202 = tk.Frame(self.frame0102, background="black", height=33, width=695)
        self.frame010202.pack(side="top", fill="both", expand=True, padx=0, pady=0) 
        self.frame010202.pack_propagate(False)

        # split frame 0302 into 2 sections along a horizontal axis
        self.frame030201 = tk.Frame(self.frame0302, background="black", height=31, width=695)
        self.frame030201.pack(anchor="nw", side="top", fill="x", expand=True, padx=0, pady=0) 
        self.frame030201.pack_propagate(False)  
        self.frame030202 = tk.Frame(self.frame0302, background="#2350b5", height=17, width=695)
        self.frame030202.pack(anchor="nw", side="top", fill="both", expand=True, padx=0, pady=0) 
        self.frame030202.pack_propagate(False)

        # split frame 0102 into 2 sections along a horizontal axis
        self.frame040201 = tk.Frame(self.frame0402, background="#2350b5", height=17, width=695)
        self.frame040201.pack(side="top", fill="x", expand=True, padx=0, pady=0)  
        self.frame040201.pack_propagate(False) 
        self.frame040202 = tk.Frame(self.frame0402, background="black", height=33, width=695)
        self.frame040202.pack(side="top", fill="both", expand=True, padx=0, pady=0) 
        self.frame040202.pack_propagate(False)     

        # split frame 0302 into 2 sections along a horizontal axis
        self.frame060201 = tk.Frame(self.frame0602, background="black", height=31, width=695)
        self.frame060201.pack(side="top", fill="x", expand=True, padx=0, pady=0)   
        self.frame060202 = tk.Frame(self.frame0602, background="#2350b5", height=17, width=695)
        self.frame060202.pack(side="top", fill="both", expand=True, padx=0, pady=0)   


    def top_divider_bar1(self):
        self.button010101 = tk.Button(self.frame0101, anchor="nw", background="black", borderwidth=0, command=self.action010101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_NW_img, justify="right", relief="flat", text="010101", height=50, width=105)
        self.button010101.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.label010202 = tk.Label(self.frame010202, anchor="e", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="right", relief="flat", text="APPLICATION LOG")
        self.label010202.pack(side="right", fill="both", expand=True, padx=10, pady=7)  


    def bottom_divider_bar1(self):
        self.button030101 = tk.Button(self.frame0301, anchor="sw", background="black", borderwidth=0, command=self.action030101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_SW_img, justify="right", relief="flat", text="030101", height=50, width=105)
        self.button030101.pack(side="left", fill="both", expand=True, padx=0, pady=0)


    def top_divider_bar2(self):
        self.button040101 = tk.Button(self.frame0401, anchor="nw", background="black", borderwidth=0, command=self.action040101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_NW_img, justify="right", relief="flat", text="040101", height=50, width=105)
        self.button040101.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        self.label040202 = tk.Label(self.frame040202, anchor="ne", background="black", borderwidth=0, font=self.helv10bold, foreground="yellow", height=1, highlightthickness=0, justify="right", relief="flat", text="CURRENT STATUS")
        self.label040202.pack(side="right", fill="none", expand=False, padx=10, pady=7) 
  

    def bottom_divider_bar2(self):
        self.button060101 = tk.Button(self.frame0601, anchor="sw", background="black", borderwidth=0, command=self.action060101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_elbow_SW_img, justify="right", relief="flat", text="060101", height=50, width=105)
        self.button060101.pack(side="left", fill="both", expand=True, padx=0, pady=0)

    
    def alarm_log_window(self):
        self.text020301 = tk.Text(self.frame0203, background="black", borderwidth=0, font=self.helv08bold, foreground="white", highlightthickness=0, height=10, width=12, wrap="word")
        self.text020301.pack(side="left", fill="both", expand=True, padx=0, pady=10)


    def frame0503a_content(self):
        # overlay frame on 0503 for content changing purposes
        self.frame050301a = tk.Frame(self.frame0503, background="black", borderwidth=0, relief="flat", height=300, width=400)
        self.frame050301a.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)   
        self.frame050301a_packed = True
        self.frame050301a.pack_propagate(False)
        # Add buttons to frame0404a    
        self.button050301a01a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a01a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a01b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a01b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="LOG\nHANDLER", height=44, width=108)        
        self.button050301a01c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a01c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a01a.grid(row=1, column=0, padx=0, pady=0)
        self.button050301a01b.grid(row=1, column=1, padx=0, pady=0)        
        self.button050301a01c.grid(row=1, column=2, padx=0, pady=0)

        self.button050301a02a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a02a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a02b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a02b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="LOGIC\nSOLVER", height=44, width=108)  
        self.button050301a02c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a02c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a02a.grid(row=2, column=0, padx=0, pady=0)
        self.button050301a02b.grid(row=2, column=1, padx=0, pady=0)        
        self.button050301a02c.grid(row=2, column=2, padx=0, pady=0)        
        
        self.button050301a03a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a03a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a03b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a03b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="DB\nINTERFACE", height=44, width=108)  
        self.button050301a03c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a03c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a03a.grid(row=3, column=0, padx=0, pady=0)
        self.button050301a03b.grid(row=3, column=1, padx=0, pady=0)        
        self.button050301a03c.grid(row=3, column=2, padx=0, pady=0)        
        
        self.button050301a04a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a04a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a04b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a04b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="HOME\nAWAY", height=44, width=108)  
        self.button050301a04c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a04c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a04a.grid(row=4, column=0, padx=0, pady=0)
        self.button050301a04b.grid(row=4, column=1, padx=0, pady=0)        
        self.button050301a04c.grid(row=4, column=2, padx=0, pady=0)

        self.button050301a05a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a05a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a05b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a05b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="MOTION\nDETECTION", height=44, width=108)  
        self.button050301a05c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a05c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a05a.grid(row=5, column=0, padx=0, pady=0)
        self.button050301a05b.grid(row=5, column=1, padx=0, pady=0)        
        self.button050301a05c.grid(row=5, column=2, padx=0, pady=0)

        self.button050301a06a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a06a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a06b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a06b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="RPI\nSCREEN", height=44, width=108)  
        self.button050301a06c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a06c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a06a.grid(row=6, column=0, padx=0, pady=0)
        self.button050301a06b.grid(row=6, column=1, padx=0, pady=0)        
        self.button050301a06c.grid(row=6, column=2, padx=0, pady=0)

        self.button050301a07a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a07a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a07b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a07b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="WEMO\nGATEWAY", height=44, width=108)  
        self.button050301a07c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a07c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a07a.grid(row=7, column=0, padx=0, pady=0)
        self.button050301a07b.grid(row=7, column=1, padx=0, pady=0)        
        self.button050301a07c.grid(row=7, column=2, padx=0, pady=0)

        self.button050301a08a = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a08a, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_left_img, justify="right", relief="flat", text="START", height=44, width=108)
        self.button050301a08b = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a08b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="NEST\nGATEWAY", height=44, width=108)  
        self.button050301a08c = tk.Button(self.frame050301a, anchor="se", background="black", borderwidth=0, command=self.action050301a08c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="STOP", height=44, width=108)
        self.button050301a08a.grid(row=8, column=0, padx=0, pady=0)
        self.button050301a08b.grid(row=8, column=1, padx=0, pady=0)        
        self.button050301a08c.grid(row=8, column=2, padx=0, pady=0)        


    def frame0503b_content(self):
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
        self.button050301b14b = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b08b, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_square_red_img, justify="center", relief="flat", text="ALL 2ND\nFLOOR", height=44, width=108)        
        self.button050301b14c = tk.Button(self.frame050301b, anchor="se", background="black", borderwidth=0, command=self.action050301b14c, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, image=self.button_151_195_225_round_right_img, justify="right", relief="flat", text="OFF", height=44, width=108) 
        self.button050301b14a.grid(row=7, column=3, padx=2, pady=2)
        self.button050301b14b.grid(row=7, column=4, padx=2, pady=2)
        self.button050301b14c.grid(row=7, column=5, padx=2, pady=2)         


    def frame0501_buttons(self):
        self.button050101 = tk.Button(self.frame0501, background="#2350b5", borderwidth=0, command=self.action050101, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="SERVICES", height=3, width=10)
        self.button050101.pack(side="top", fill="x", expand=False, padx=0, pady=2)
        self.button050102 = tk.Button(self.frame0501, background="#2350b5", borderwidth=0, command=self.action050102, compound="center", font=self.helv10bold, foreground="black", highlightthickness=0, justify="right", relief="flat", text="WEMO", height=3, width=10)
        self.button050102.pack(side="top", fill="x", expand=False, padx=0, pady=2)
        

    def update_alarm_window(self):
        # Determine size of logfile (number of lines)
        self.num_lines = sum(1 for line in open(self.logfile))
        # If line index is larger than logfile (meaning log file was reset), reset index to match log-file size
        if self.line > (self.num_lines + 1):
            self.line = self.num_lines
            # Correct for line pointers less than 1
            if self.line < 1:
                self.line = 1
        # Read line from file
        try:
            self.text = linecache.getline(self.logfile, self.line)
        except:
            print("could not access file")
            self.text = str()
        # Processing logfile
        self.iter = 1
        while len(self.text) != 0 and self.iter < 1000:
            if (self.text.find("p16_wemo_gw") < 0):
                self.text020301.insert(tk.END, self.text)
                self.text020301.yview_pickplace("end")
            self.line += 1
            self.text = linecache.getline(self.logfile, self.line)
            self.iter += 1
        linecache.clearcache()


    def action010101(self):
        logging.log(logging.DEBUG, "Button 010101 was pressed")
        pass

    def action030101(self):
        logging.log(logging.DEBUG, "Button 030101 was pressed")
        pass 

    def action040101(self):
        logging.log(logging.DEBUG, "Button 040101 was pressed")
        pass

    def action060101(self):
        logging.log(logging.DEBUG, "Button 060101 was pressed")
        pass 

    def action050101(self):
        logging.log(logging.DEBUG, "Button 050101 was pressed")
        if self.frame050301a_packed is False:
            self.frame050301a.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)
            self.frame050301a.pack_propagate(False)
            self.frame050301a_packed = True 
        pass           
        if self.frame050301b_packed is True:
            self.frame050301b.pack_forget()
            self.frame050301b_packed = False
        pass

    def action050102(self):
        logging.log(logging.DEBUG, "Button 050102 was pressed")
        if self.frame050301b_packed is False:
            self.frame050301b.pack(anchor="nw", side="left", fill="none", expand=False, padx=0, pady=0)
            self.frame050301b.pack_propagate(False)
            self.frame050301b_packed = True 
        pass           
        if self.frame050301a_packed is True:
            self.frame050301a.pack_forget()
            self.frame050301a_packed = False
        pass

    def action050301a01a(self):
        logging.log(logging.DEBUG, "Button 050301a01a was pressed")
        self.msg_out_queue.put_nowait("02,01,900")

    def action050301a01b(self):
        logging.log(logging.DEBUG, "Button 050301a01b was pressed")
        self.msg_out_queue.put_nowait("02,01,???")        

    def action050301a01c(self):
        logging.log(logging.DEBUG, "Button 050301a01c was pressed")
        self.msg_out_queue.put_nowait("02,01,999")

    def action050301a02a(self):
        logging.log(logging.DEBUG, "Button 050301a02a was pressed")
        self.msg_out_queue.put_nowait("02,11,900")

    def action050301a02b(self):
        logging.log(logging.DEBUG, "Button 050301a02b was pressed")
        self.msg_out_queue.put_nowait("02,11,???")         

    def action050301a02c(self):
        logging.log(logging.DEBUG, "Button 050301a02c was pressed")
        self.msg_out_queue.put_nowait("02,11,999")

    def action050301a03a(self):
        logging.log(logging.DEBUG, "Button 050301a03a was pressed")
        self.msg_out_queue.put_nowait("02,12,900")

    def action050301a03b(self):
        logging.log(logging.DEBUG, "Button 050301a03b was pressed")
        self.msg_out_queue.put_nowait("02,12,???")         

    def action050301a03c(self):
        logging.log(logging.DEBUG, "Button 050301a03c was pressed")
        self.msg_out_queue.put_nowait("02,12,999")

    def action050301a04a(self):
        logging.log(logging.DEBUG, "Button 050301a04a was pressed")
        self.msg_out_queue.put_nowait("02,13,900")

    def action050301a04b(self):
        logging.log(logging.DEBUG, "Button 050301a04b was pressed")
        self.msg_out_queue.put_nowait("02,13,???")         

    def action050301a04c(self):
        logging.log(logging.DEBUG, "Button 050301a04c was pressed")
        self.msg_out_queue.put_nowait("02,13,999")

    def action050301a05a(self):
        logging.log(logging.DEBUG, "Button 050301a05a was pressed")
        self.msg_out_queue.put_nowait("02,14,900")

    def action050301a05b(self):
        logging.log(logging.DEBUG, "Button 050301a05b was pressed")
        self.msg_out_queue.put_nowait("02,14,???")         

    def action050301a05c(self):
        logging.log(logging.DEBUG, "Button 050301a05c was pressed")
        self.msg_out_queue.put_nowait("02,14,999")

    def action050301a06a(self):
        logging.log(logging.DEBUG, "Button 050301a06a was pressed")
        self.msg_out_queue.put_nowait("02,15,900")

    def action050301a06b(self):
        logging.log(logging.DEBUG, "Button 050301a06b was pressed")
        self.msg_out_queue.put_nowait("02,15,???")         

    def action050301a06c(self):
        logging.log(logging.DEBUG, "Button 050301a06c was pressed")
        self.msg_out_queue.put_nowait("02,15,999")

    def action050301a07a(self):
        logging.log(logging.DEBUG, "Button 050301a07a was pressed")
        self.msg_out_queue.put_nowait("02,16,900")

    def action050301a07b(self):
        logging.log(logging.DEBUG, "Button 050301a07b was pressed")
        self.msg_out_queue.put_nowait("02,16,???")         

    def action050301a07c(self):
        logging.log(logging.DEBUG, "Button 050301a07c was pressed")
        self.msg_out_queue.put_nowait("02,16,999")

    def action050301a08a(self):
        logging.log(logging.DEBUG, "Button 050301a08a was pressed")
        self.msg_out_queue.put_nowait("02,17,900")

    def action050301a08b(self):
        logging.log(logging.DEBUG, "Button 050301a08b was pressed")
        self.msg_out_queue.put_nowait("02,17,???")         

    def action050301a08c(self):
        logging.log(logging.DEBUG, "Button 050301a08c was pressed")
        self.msg_out_queue.put_nowait("02,17,999")        



    def action050301b01a(self):
        logging.log(logging.DEBUG, "Button 050301b01a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,fylt1")
        self.button050301b01b.config(image=self.button_square_green_img)

    def action050301b01b(self):
        logging.log(logging.DEBUG, "Button 050301b01b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,fylt1")

    def action050301b01c(self):
        logging.log(logging.DEBUG, "Button 050301b01C was pressed")
        self.msg_out_queue.put_nowait("02,16,160,fylt1") 
        self.button050301b01b.config(image=self.button_square_red_img)               

    def action050301b02a(self):
        logging.log(logging.DEBUG, "Button 050301b02a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,bylt1")
        self.button050301b02b.config(image=self.button_square_green_img)

    def action050301b02b(self):
        logging.log(logging.DEBUG, "Button 050301b02b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,bylt1")

    def action050301b02c(self):
        logging.log(logging.DEBUG, "Button 050301b02c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,bylt1")  
        self.button050301b02b.config(image=self.button_square_red_img)              

    def action050301b03a(self):
        logging.log(logging.DEBUG, "Button 050301b03a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,ewlt1")
        self.button050301b03b.config(image=self.button_square_green_img)

    def action050301b03b(self):
        logging.log(logging.DEBUG, "Button 050301b03b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,ewlt1")

    def action050301b03c(self):
        logging.log(logging.DEBUG, "Button 050301b03c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,ewlt1")
        self.button050301b03b.config(image=self.button_square_red_img)        

    def action050301b04a(self):
        logging.log(logging.DEBUG, "Button 050301b04a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,cclt1")
        self.button050301b04b.config(image=self.button_square_green_img)

    def action050301b04b(self):
        logging.log(logging.DEBUG, "Button 050301b04b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,cclt1")

    def action050301b04c(self):
        logging.log(logging.DEBUG, "Button 050301b04c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,cclt1")    
        self.button050301b04b.config(image=self.button_square_red_img)            

    def action050301b05a(self):
        logging.log(logging.DEBUG, "Button 050301b05a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,lrlt1")
        self.button050301b05b.config(image=self.button_square_green_img)

    def action050301b05b(self):
        logging.log(logging.DEBUG, "Button 050301b05b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,lrlt1")

    def action050301b05c(self):
        logging.log(logging.DEBUG, "Button 050301b05c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,lrlt1")  
        self.button050301b05b.config(image=self.button_square_red_img)              

    def action050301b06a(self):
        logging.log(logging.DEBUG, "Button 050301b06a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,drlt1")
        self.button050301b06b.config(image=self.button_square_green_img)

    def action050301b06b(self):
        logging.log(logging.DEBUG, "Button 050301b06b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,drlt1")

    def action050301b06c(self):
        logging.log(logging.DEBUG, "Button 050301b06c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,drlt1") 
        self.button050301b06b.config(image=self.button_square_red_img)               

    def action050301b07a(self):
        logging.log(logging.DEBUG, "Button 050301b07a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,lrlt1")
        self.msg_out_queue.put_nowait("02,16,161,drlt1")  
        self.msg_out_queue.put_nowait("02,16,161,cclt1")
        self.msg_out_queue.put_nowait("02,16,161,ewlt1")   
        self.button050301b03b.config(image=self.button_square_green_img)
        self.button050301b04b.config(image=self.button_square_green_img)
        self.button050301b05b.config(image=self.button_square_green_img)
        self.button050301b06b.config(image=self.button_square_green_img)            

    def action050301b07b(self):
        logging.log(logging.DEBUG, "Button 050301b07b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,lrlt1")
        self.msg_out_queue.put_nowait("02,16,162,drlt1")  
        self.msg_out_queue.put_nowait("02,16,162,cclt1")
        self.msg_out_queue.put_nowait("02,16,162,ewlt1") 

    def action050301b07c(self):
        logging.log(logging.DEBUG, "Button 050301b07c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,lrlt1")
        self.msg_out_queue.put_nowait("02,16,160,drlt1")  
        self.msg_out_queue.put_nowait("02,16,160,cclt1")
        self.msg_out_queue.put_nowait("02,16,160,ewlt1") 
        self.button050301b03b.config(image=self.button_square_red_img)
        self.button050301b04b.config(image=self.button_square_red_img)
        self.button050301b05b.config(image=self.button_square_red_img)
        self.button050301b06b.config(image=self.button_square_red_img)


    def action050301b08a(self):
        logging.log(logging.DEBUG, "Button 050301b08a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,b1lt1")
        self.button050301b08b.config(image=self.button_square_green_img)        

    def action050301b08b(self):
        logging.log(logging.DEBUG, "Button 050301b08b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,b1lt1")

    def action050301b08c(self):
        logging.log(logging.DEBUG, "Button 050301b08c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,b1lt1")    
        self.button050301b08b.config(image=self.button_square_red_img)            

    def action050301b09a(self):
        logging.log(logging.DEBUG, "Button 050301b09a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,b1lt2")
        self.button050301b09b.config(image=self.button_square_green_img)         

    def action050301b09b(self):
        logging.log(logging.DEBUG, "Button 050301b09b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,b1lt2")   

    def action050301b09c(self):
        logging.log(logging.DEBUG, "Button 050301b09c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,b1lt2")    
        self.button050301b09b.config(image=self.button_square_red_img)                   

    def action050301b10a(self):
        logging.log(logging.DEBUG, "Button 050301b10a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,b2lt1")
        self.button050301b10b.config(image=self.button_square_green_img)          

    def action050301b10b(self):
        logging.log(logging.DEBUG, "Button 050301b10b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,b2lt1")

    def action050301b10c(self):
        logging.log(logging.DEBUG, "Button 050301b10c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,b2lt1")   
        self.button050301b10b.config(image=self.button_square_red_img)              

    def action050301b11a(self):
        logging.log(logging.DEBUG, "Button 050301b11a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,b2lt2")
        self.button050301b11b.config(image=self.button_square_green_img)         

    def action050301b11b(self):
        logging.log(logging.DEBUG, "Button 050301b11b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,b2lt2") 

    def action050301b11c(self):
        logging.log(logging.DEBUG, "Button 050301b11c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,b2lt2")   
        self.button050301b11b.config(image=self.button_square_red_img)               

    def action050301b12a(self):
        logging.log(logging.DEBUG, "Button 050301b12a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,b3lt1")
        self.button050301b12b.config(image=self.button_square_green_img)         

    def action050301b12b(self):
        logging.log(logging.DEBUG, "Button 050301b12b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,b3lt1")

    def action050301b12c(self):
        logging.log(logging.DEBUG, "Button 050301b12c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,b3lt1")  
        self.button050301b12b.config(image=self.button_square_red_img)               

    def action050301b13a(self):
        logging.log(logging.DEBUG, "Button 050301b13a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,b3lt2")
        self.button050301b13b.config(image=self.button_square_green_img)         

    def action050301b13b(self):
        logging.log(logging.DEBUG, "Button 050301b13b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,b3lt2") 

    def action050301b13c(self):
        logging.log(logging.DEBUG, "Button 050301b13c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,b3lt2")  
        self.button050301b13b.config(image=self.button_square_red_img)               

    def action050301b14a(self):
        logging.log(logging.DEBUG, "Button 050301b14a was pressed")
        self.msg_out_queue.put_nowait("02,16,161,b1lt1")
        self.msg_out_queue.put_nowait("02,16,161,b1lt2")
        self.msg_out_queue.put_nowait("02,16,161,b2lt1")
        self.msg_out_queue.put_nowait("02,16,161,b2lt2")  
        self.msg_out_queue.put_nowait("02,16,161,b3lt1")
        self.msg_out_queue.put_nowait("02,16,161,b3lt2")   
        self.button050301b08b.config(image=self.button_square_green_img)  
        self.button050301b09b.config(image=self.button_square_green_img)
        self.button050301b10b.config(image=self.button_square_green_img)
        self.button050301b11b.config(image=self.button_square_green_img)
        self.button050301b12b.config(image=self.button_square_green_img)
        self.button050301b13b.config(image=self.button_square_green_img)                                                           

    def action050301b14b(self):
        logging.log(logging.DEBUG, "Button 050301b14b was pressed")
        self.msg_out_queue.put_nowait("02,16,162,b1lt1")
        self.msg_out_queue.put_nowait("02,16,162,b1lt2")
        self.msg_out_queue.put_nowait("02,16,162,b2lt1")
        self.msg_out_queue.put_nowait("02,16,162,b2lt2")  
        self.msg_out_queue.put_nowait("02,16,162,b3lt1")
        self.msg_out_queue.put_nowait("02,16,162,b3lt2")  

    def action050301b14c(self):
        logging.log(logging.DEBUG, "Button 050301b14c was pressed")
        self.msg_out_queue.put_nowait("02,16,160,b1lt1")
        self.msg_out_queue.put_nowait("02,16,160,b1lt2")
        self.msg_out_queue.put_nowait("02,16,160,b2lt1")
        self.msg_out_queue.put_nowait("02,16,160,b2lt2")  
        self.msg_out_queue.put_nowait("02,16,160,b3lt1")
        self.msg_out_queue.put_nowait("02,16,160,b3lt2")  
        self.button050301b08b.config(image=self.button_square_red_img)  
        self.button050301b09b.config(image=self.button_square_red_img)
        self.button050301b10b.config(image=self.button_square_red_img)
        self.button050301b11b.config(image=self.button_square_red_img)
        self.button050301b12b.config(image=self.button_square_red_img)
        self.button050301b13b.config(image=self.button_square_red_img)                       




    def after_tasks(self):
        #logging.log(logging.DEBUG, "Running \"after\" task")
        # Process incoming message queue
        try:
            self.msg_in = self.msg_in_queue.get_nowait()    
            #logging.log(logging.DEBUG, "Checked in msg queue and found msg: %s" % self.msg_in)   
        except:
            pass
        

        # Process incoming message
        if len(self.msg_in) != 0:
            if self.msg_in[3:5] == "02":
                
                if self.msg_in[6:9] == "001":
                    #logging.log(logging.DEBUG, "Heartbeat received: %s" % self.msg_in)
                    self.last_hb = time.time()
                
                elif self.msg_in[6:9] == "002":
                    if self.msg_in[0:2] == "01":
                        self.button050301a01b.config(image=self.button_square_green_img)
                    elif self.msg_in[0:2] == "11":
                        self.button050301a02b.config(image=self.button_square_green_img)
                    elif self.msg_in[0:2] == "12":
                        self.button050301a03b.config(image=self.button_square_green_img)
                    elif self.msg_in[0:2] == "13":
                        self.button050301a04b.config(image=self.button_square_green_img)
                    elif self.msg_in[0:2] == "14":
                        self.button050301a05b.config(image=self.button_square_green_img)
                    elif self.msg_in[0:2] == "15":
                        self.button050301a06b.config(image=self.button_square_green_img)
                    elif self.msg_in[0:2] == "16":
                        self.button050301a07b.config(image=self.button_square_green_img)
                    elif self.msg_in[0:2] == "17":
                        self.button050301a08b.config(image=self.button_square_green_img)
                
                elif self.msg_in[6:9] == "003":
                    if self.msg_in[0:2] == "01":
                        self.button050301a01b.config(image=self.button_square_red_img)
                    elif self.msg_in[0:2] == "11":
                        self.button050301a02b.config(image=self.button_square_red_img)
                    elif self.msg_in[0:2] == "12":
                        self.button050301a03b.config(image=self.button_square_red_img)
                    elif self.msg_in[0:2] == "13":
                        self.button050301a04b.config(image=self.button_square_red_img)
                    elif self.msg_in[0:2] == "14":
                        self.button050301a05b.config(image=self.button_square_red_img)
                    elif self.msg_in[0:2] == "15":
                        self.button050301a06b.config(image=self.button_square_red_img)
                    elif self.msg_in[0:2] == "16":
                        self.button050301a07b.config(image=self.button_square_red_img)
                    elif self.msg_in[0:2] == "17":
                        self.button050301a08b.config(image=self.button_square_red_img)
                
                elif self.msg_in[6:9] == "163":
                    if self.msg_in[10:11] == "0":
                        if self.msg_in[12:] == "fylt1":
                            self.button050301b01b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "bylt1":
                            self.button050301b02b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "ewlt1":
                            self.button050301b03b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "cclt1":
                            self.button050301b04b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "lrlt1":
                            self.button050301b05b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "drlt1":
                            self.button050301b06b.config(image=self.button_square_red_img)                        
                        elif self.msg_in[12:] == "b1lt1":
                            self.button050301b08b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "b1lt2":
                            self.button050301b09b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "b2lt1":
                            self.button050301b10b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "b2lt2":
                            self.button050301b11b.config(image=self.button_square_red_img) 
                        elif self.msg_in[12:] == "b3lt1":
                            self.button050301b12b.config(image=self.button_square_red_img)
                        elif self.msg_in[12:] == "b3lt2":
                            self.button050301b13b.config(image=self.button_square_red_img) 
                    elif self.msg_in[10:11] == "1":
                        if self.msg_in[12:] == "fylt1":
                            self.button050301b01b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "bylt1":
                            self.button050301b02b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "ewlt1":
                            self.button050301b03b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "cclt1":
                            self.button050301b04b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "lrlt1":
                            self.button050301b05b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "drlt1":
                            self.button050301b06b.config(image=self.button_square_green_img)                        
                        elif self.msg_in[12:] == "b1lt1":
                            self.button050301b08b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "b1lt2":
                            self.button050301b09b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "b2lt1":
                            self.button050301b10b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "b2lt2":
                            self.button050301b11b.config(image=self.button_square_green_img) 
                        elif self.msg_in[12:] == "b3lt1":
                            self.button050301b12b.config(image=self.button_square_green_img)
                        elif self.msg_in[12:] == "b3lt2":
                            self.button050301b13b.config(image=self.button_square_green_img)                                                                            
                                       
                elif self.msg_in[6:9] == "999":
                    logging.log(logging.DEBUG, "Kill code received - Shutting down: %s" % self.msg_in)
                    self.close_pending = True
            else:
                self.msg_out_queue.put_nowait(self.msg_in)
            pass  
            self.msg_in = str()

        # Send periodic querries to field devices to get current status
        if self.close_pending is False:
            if self.index > 24:
                self.index = 0
            if self.index == 0:
                self.msg_out_queue.put_nowait("02,16,162,fylt1")
            elif self.index == 2:
                self.msg_out_queue.put_nowait("02,16,162,bylt1")
            elif self.index == 4:
                self.msg_out_queue.put_nowait("02,16,162,ewlt1")
            elif self.index == 6:
                self.msg_out_queue.put_nowait("02,16,162,cclt1")
            elif self.index == 8:
                self.msg_out_queue.put_nowait("02,16,162,lrlt1")
            elif self.index == 10:
                self.msg_out_queue.put_nowait("02,16,162,drlt1")
            elif self.index == 12:
                self.msg_out_queue.put_nowait("02,16,162,b1lt1")
            elif self.index == 14:
                self.msg_out_queue.put_nowait("02,16,162,b1lt2")
            elif self.index == 16:
                self.msg_out_queue.put_nowait("02,16,162,b2lt1")
            elif self.index == 18:
                self.msg_out_queue.put_nowait("02,16,162,b2lt2")
            elif self.index == 20:
                self.msg_out_queue.put_nowait("02,16,162,b3lt1")
            elif self.index == 22:
                self.msg_out_queue.put_nowait("02,16,162,b3lt2")
            self.index += 1
        
              

        # If a close is pending, wait until all messages have been processed before closing down the window
        # Otherwise schedule another run of the "after" process 
        if ((self.close_pending is True) and (len(self.msg_in) == 0) and (self.msg_in_queue.empty() is True)) or (time.time() > (self.last_hb + 30)):
            self.window.destroy()
        else:
            # Update visual aspects of main window (text, etc)
            self.update_alarm_window()
            #logging.log(logging.DEBUG, "Log viewer window updated")
            # Re-schedule after task to run again in another 1000ms
            self.window.after(500, self.after_tasks)
            #logging.log(logging.DEBUG, "Re-scheduled next after event")
        pass


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close_pending = True
            # Kill p167(nest gateway)
            try:
                self.msg_out_queue.put_nowait("02,17,999")
                logging.log(logging.DEBUG, "Kill code sent to p17_nest_gateway process")
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p17_nest_gateway process.  Queue already closed")
            # Kill p16 (wemo gateway)
            try:
                self.msg_out_queue.put_nowait("02,16,999")
                logging.log(logging.DEBUG, "Kill code sent to p16_wemo_gateway process") 
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p16_wemo_gateway process.  Queue already closed")           
            # Kill p15 (rpi screen)
            try:
                self.msg_out_queue.put_nowait("02,15,999")
                logging.log(logging.DEBUG, "Kill code sent to p15_rpi_screen process")  
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p15_rpi_screen process.  Queue already closed")                
            # Kill p14 (motion detector)
            try:
                self.msg_out_queue.put_nowait("02,14,999")
                logging.log(logging.DEBUG, "Kill code sent to p14_motion process") 
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p14_motion process.  Queue already closed")                
            # Kill p13 (home / away)
            try:
                self.msg_out_queue.put_nowait("02,13,999")
                logging.log(logging.DEBUG, "Kill code sent to p13_home_away process")   
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p13_home_away process.  Queue already closed")                
            # Kill p12 (db interface)
            try:
                self.msg_out_queue.put_nowait("02,12,999")
                logging.log(logging.DEBUG, "Kill code sent to p12_db_interface process") 
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p12_db_interface process.  Queue already closed")                                                         
            # Kill p11 (logic solver)
            try:
                self.msg_out_queue.put_nowait("02,11,999")
                logging.log(logging.DEBUG, "Kill code sent to p11_logic_solver process")
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p11_logic_solver process.  Queue already closed")                
            # Kill p02 (gui)
            try:
                self.msg_out_queue.put_nowait("02,02,999")
                logging.log(logging.DEBUG, "Kill code sent to p02_gui process")  
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p02_gui process.  Queue already closed")                
            # Kill p01 (log handler)
            try:
                self.msg_out_queue.put_nowait("02,01,999")  
                logging.log(logging.DEBUG, "Kill code sent to p01_logger process")     
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p01_log_handler process.  Queue already closed")                                           
            # Kill p00 (main)
            try:
                self.msg_out_queue.put_nowait("02,00,999")      
                logging.log(logging.DEBUG, "Kill code sent to p00_main process")
            except:
                logging.log(logging.DEBUG, "Could not send kill-code to p00_main process.  Queue already closed")                
            # Close msg out queue
            self.msg_out_queue.close()
            # Close application main window
            #self.window.destroy()
