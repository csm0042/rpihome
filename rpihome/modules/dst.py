import datetime
import logging

class USdst(object):
    def __init__(self):
        self.dt = datetime.datetime.now()
        self.marchStartsOn = datetime.date(2016,3,1)
        self.marchFirstSun = int()
        self.marchSecondSun = int()
        self.novStartsOn = datetime.date(2016,11,1)
        self.novFirstSun = int()
        self.dstStarts = datetime.datetime(2016,3,13)
        self.dstEnds = datetime.datetime(2016,11,6)

    @property
    def dt(self):
        return self.__dt

    @dt.setter
    def dt(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__dt = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.dt (should be type: datetime.datetime)") 

    @property
    def marchStartsOn(self):
        return self.__marchStartsOn

    @marchStartsOn.setter
    def marchStartsOn(self, value):
        if isinstance(value, datetime.date) is True:
            self.__marchStartsOn = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.marchStartsOn (should be type: datetime.date)") 

    @property
    def marchFirstSun(self):
        return self.__marchFirstSun

    @marchFirstSun.setter
    def marchFirstSun(self, value):
        if isinstance(value, int) is True:
            self.__marchFirstSun = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.marchFirstSun (should be type: int)")

    @property
    def marchSecondSun(self):
        return self.__marchSecondSun

    @marchSecondSun.setter
    def marchSecondSun(self, value):
        if isinstance(value, int) is True:
            self.__marchSecondSun = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.marchSecondSun (should be type: int)")                        

    @property
    def novStartsOn(self):
        return self.__novStartsOn

    @novStartsOn.setter
    def novStartsOn(self, value):
        if isinstance(value, datetime.date) is True:
            self.__novStartsOn = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.novStartsOn (should be type: datetime.date)") 

    @property
    def novFirstSun(self):
        return self.__novFirstSun

    @novFirstSun.setter
    def novFirstSun(self, value):
        if isinstance(value, int) is True:
            self.__novFirstSun = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.novFirstSun (should be type: int)")     

    @property
    def dstStarts(self):
        return self.__dstStarts

    @dstStarts.setter
    def dstStarts(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__dstStarts = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.dstStarts (should be type: datetime.datetime)")                   

    @property
    def dstEnds(self):
        return self.__dstEnds

    @dstEnds.setter
    def dstEnds(self, value):
        if isinstance(value, datetime.datetime) is True:
            self.__dstEnds = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.dstEnds (should be type: datetime.datetime)")                                    


    def is_active(self, **kwargs):
        """ Determines if dst is active based on United States rules.  Defaults to current date/time if no input value given """
        # Update value stored in dt_now to current datetime
        self.dt = datetime.datetime.now()
        # Process input variables if present    
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "datetime":
                    self.dt = value
        # Find date for 2nd Sunday in March
        self.marchStartsOn = datetime.date(self.dt.year, 3, 1)
        self.marchFirstSun = 7 - self.marchStartsOn.weekday()
        self.marchSecondSun = self.marchFirstSun + 7
        # Find date for 1st Sunday in November
        self.novStartsOn = datetime.date(self.dt.year, 11, 1)
        self.novFirstSun = 7 - self.novStartsOn.weekday()
        # Set bounds for dst active
        self.dstStarts = datetime.datetime.combine((datetime.date(self.dt.year, 3, self.marchSecondSun)),(datetime.time(2,0)))
        self.dstEnds = datetime.datetime.combine((datetime.date(self.dt.year, 11, self.novFirstSun)),(datetime.time(2,0)))
        # Determine if date fed into routine falls within bounds
        if self.dstStarts <= self.dt <= self.dstEnds:
            return True
        else:
            return False


if __name__ == "__main__":
    dst_check = USdst()
    dt_to_check = datetime.datetime.combine(datetime.date(2016,3,13), datetime.datetime.now().time())
    print(dst_check.dst_active(datetime=dt_to_check))
