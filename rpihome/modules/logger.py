import logging
import logging.handlers
import os
import sys

class MyLogger(object):
    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.clean_handlers()
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False
        self.logfile = os.path.join(os.path.dirname(sys.argv[0]), ("logs/" + self.name + ".log"))
        self.handler = logging.handlers.TimedRotatingFileHandler(self.logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
        self.formatter = logging.Formatter('%(processName)-16s,  %(asctime)-24s,  %(levelname)-8s, %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def logger(self):
        return self.logger

    def clean_handlers(self):
        handlers = list(self.logger.handlers)
        for h in iter(handlers):
            self.logger.removeHandler(h)
            h.flush()
            h.close()

    def __del__(self):
        print("Starting logger clean-up for %s" % self.name)
        self.clean_handlers()
        print("Logger clean-up complete for %s" % self.name)
