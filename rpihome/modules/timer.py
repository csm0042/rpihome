import time


class Timer(object):
    def __init__(self):
        self.start = float()
        self.acc = float()
        self.pre = float()
        self.en = bool()
        self.tt = bool()
        self.dn = bool()        

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        if isinstance(value, float) is True:
            self.__start = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.start (should be type: float)") 

    @property
    def pre(self):
        return self.__pre

    @pre.setter
    def pre(self, value):
        if isinstance(value, float) is True:
            self.__pre = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.pre (should be type: float)") 

    @acc.setter
    def acc(self, value):
        if isinstance(value, float) is True:
            self.__acc = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.acc (should be type: float)")                              

    @property
    def en(self):
        return self.__en

    @en.setter
    def en(self, value):
        if isinstance(value, bool) is True:
            self.__en = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.en (should be type: bool)")  

    @property
    def tt(self):
        return self.__tt

    @tt.setter
    def tt(self, value):
        if isinstance(value, bool) is True:
            self.__tt = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.tt (should be type: bool)") 

    @property
    def dn(self):
        return self.__dn

    @dn.setter
    def dn(self, value):
        if isinstance(value, bool) is True:
            self.__dn = value
        else:
            logging.log(logging.DEBUG, "Improper type attmpted to load into self.dn (should be type: bool)")              


    def ton(self, enable, **kwargs):
        """ When enabled, times for the preset length of time.  When that time has elapsed, the dn bit is turned on (True) and remains on for as long as the timer remains enabled.  The timing (tt) bit will be on when the timer is enabled but not yet done.  The enable (en) bit simply echos the state of the timer enable input """
        # Process input variables if present   
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "pre":
                    self.pre = value  
        # Timer control      
        if enable is True:
            if self.en is False:
                self.start = time.time()
                self.en = True
                self.tt = True
                self.acc = 0.0
            elif self.en is True:
                self.acc = time.time() - self.start                
                if self.acc >= self.pre:
                    self.dn = True
                    self.tt = False
                else:
                    self.dn = False
                    self.tt = True                                       

