import logging
import os

def configure_local_logger(name, location):
    """ Method to configure local logging """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    logfile = os.path.join(location, (name + ".log"))
    handler = logging.handlers.TimedRotatingFileHandler(logfile, when="h", interval=1, backupCount=24, encoding=None, delay=False, utc=False, atTime=None)
    formatter = logging.Formatter('%(processName)-16s ,  %(asctime)-24s ,  %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug("Logging handler for %s started", name)
    return logger


def kill_logger(self):
    """ Shut down logger when process exists """
    handlers = list(logger.handlers)
    for i in iter(handlers):
        logger.removeHandler(i)
        i.flush()
        i.close()