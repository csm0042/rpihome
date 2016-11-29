import logging
import tkinter as tk
from tkinter import font
from rpihome.modules.message import Message


class OnIndOffButtonFrame(object):
    def __init__(self, parent_frame, **kwargs):
        self.parent_frame = parent_frame
        self.msg_to_send = Message()
        # Update default elements based on any parameters passed in
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "name":
                    self.name = value
                if key == "resource_dir":
                    self.resource_dir = value
                if key == "on_button_text":
                    self.on_button_text = value
                if key == "ind_button_text":
                    self.ind_button_text = value
                if key == "off_button_text":
                    self.off_button_text = value
                if key == "on_button_img":
                    self.on_button_img = value
                if key == "ind_on_button_img":
                    self.ind_on_button_img = value
                if key == "ind_off_button_img":
                    self.ind_off_button_img = value                    
                if key == "off_button_img":
                    self.off_button_img = value                    
                if key == "msg_out_queue":
                    self.msg_out_queue = value
        # Create muti-button widget
        self.create_frame()
        self.create_on_button()
        self.create_ind_button()
        self.create_off_button()


    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        self.__frame = value

    @property
    def on_button(self):
        return self.__on_button

    @on_button.setter
    def on_button(self, value):
        self.__on_button = value

    @property
    def ind_button(self):
        return self.__ind_button

    @ind_button.setter
    def ind_button(self, value):
        self.__ind_button = value 

    @property
    def off_button(self):
        return self.__off_button

    @off_button.setter
    def off_button(self, value):
        self.__off_button = value

    def create_frame(self):
        self.frame = tk.Frame(self.parent_frame)
        self.frame.config(background="black")                              

    def create_on_button(self):
        self.on_button = tk.Button(self.frame)
        self.on_button.config(anchor="se")
        self.on_button.config(background="black")
        self.on_button.config(borderwidth=0)
        self.on_button.config(command=self.on_action)
        self.on_button.config(compound="center")
        self.on_button.config(foreground="black")
        self.on_button.config(highlightthickness=0)
        self.on_button.config(justify="right")
        self.on_button.config(relief="flat")
        self.on_button.config(text=self.on_button_text)
        self.on_button.config(height=44, width=108)
        self.on_button.config(font=font.Font(family="Helvetica", size=10, weight="bold"))
        self.on_button.config(image=self.on_button_img)
        self.on_button.pack(side="left", padx=0, pady=0)

    def create_ind_button(self):
        self.ind_button = tk.Button(self.frame)
        self.ind_button.config(anchor="se")
        self.ind_button.config(background="black")
        self.ind_button.config(borderwidth=0)
        self.ind_button.config(command=self.ind_action)
        self.ind_button.config(compound="center")
        self.ind_button.config(foreground="black") 
        self.ind_button.config(highlightthickness=0) 
        self.ind_button.config(justify="center")
        self.ind_button.config(relief="flat")
        self.ind_button.config(text=self.ind_button_text)
        self.ind_button.config(height=44, width=108)
        self.ind_button.config(font=font.Font(family="Helvetica", size=10, weight="bold"))
        self.ind_button.config(image=self.ind_off_button_img)
        self.ind_button.pack(side="left", padx=0, pady=0)

    def create_off_button(self):
        self.off_button = tk.Button(self.frame)
        self.off_button.config(anchor="se")
        self.off_button.config(background="black")
        self.off_button.config(borderwidth=0)
        self.off_button.config(command=self.off_action)
        self.off_button.config(compound="center")
        self.off_button.config(foreground="black")
        self.off_button.config(highlightthickness=0)
        self.off_button.config(justify="right")
        self.off_button.config(relief="flat")
        self.off_button.config(text=self.off_button_text)
        self.off_button.config(height=44, width=108)
        self.off_button.config(font=font.Font(family="Helvetica", size=10, weight="bold"))
        self.off_button.config(image=self.off_button_img)
        self.off_button.pack(side="left", padx=0, pady=0)     


    def on_action(self):
        logging.debug("On button pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name=self.name, payload="on")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        logging.debug("Sending message [%s]", self.msg_to_send.raw)
        self.set_indicator_green()

    def ind_action(self):
        logging.debug("Ind button pressed")
        self.msg_to_send = Message(source="02", dest="16", type="162", name=self.name)
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        logging.debug("Sending message [%s]", self.msg_to_send.raw)

    def off_action(self):
        logging.debug("Off button pressed")
        self.msg_to_send = Message(source="02", dest="16", type="161", name=self.name, payload="off")
        self.msg_out_queue.put_nowait(self.msg_to_send.raw)
        logging.debug("Sending message [%s]", self.msg_to_send.raw)
        self.set_indicator_red()


    def set_indicator_green(self):
        self.ind_button.config(image=self.ind_on_button_img)
        logging.debug("Setting color of status indicator for [%s] to green", self.name)

    def set_indicator_red(self):
        self.ind_button.config(image=self.ind_off_button_img)
        logging.debug("Setting color of status indicator for [%s] to red", self.name)
