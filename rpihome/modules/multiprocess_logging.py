#!/usr/bin/python3
""" multiprocess_logging.py: Support library for multi-process logging
"""

# Import Required Libraries (Standard, Third Party, Local) ************************************************************
import logging
import logging.handlers
import multiprocessing


# Authorship Info *****************************************************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2016, The Maue-Home Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Log Handler Process *****************************************************************************
def listener_configurer(logfile):
    """ Configures logger for the listener process in a multiprocess application """
    root = logging.getLogger()
    hand = logging.handlers.TimedRotatingFileHandler(logfile, when="h", interval=1,
                                                     backupCount=10, encoding=None,
                                                     delay=False, utc=False,
                                                     atTime=None)
    form = logging.Formatter('%(processName)-16s |  %(asctime)-24s |  %(message)s')
    hand.setFormatter(form)
    root.addHandler(hand)

def worker_configurer(queue):
    """ Configures individual processes to log to a shared queue in a multiprocess application """
    hand = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(hand)
    root.setLevel(logging.DEBUG)

