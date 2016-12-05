import datetime


class Condition(object):
    def __init__(self, **kwargs):
        self.condition = str()
        self.state = str()
        # Process input variables if present    
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "condition":
                    self.condition = value
                if key == "state":
                    self.state = value


class OnRange(object):
    def __init__(self, **kwargs):
        self.on_time = datetime.time()
        self.off_time = datetime.time()
        self.condition = [Condition()]
        # Process input variables if present    
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "ontime":
                    self.on_time = value
                if key == "offtime":
                    self.off_time = value
                if key == "condition":
                    self.condition = value


class Day(object):
    def __init__(self, **kwargs):
        self.date = datetime.datetime.now().date()
        self.on_range = [OnRange()]
        # Process input variables if present    
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "date":
                    self.date = value
                if key == "onrange":
                    self.on_range = value       


class Week(object):
    def __init__(self, **kwargs):
        self.day = [Day()] * 7
         # Process input variables if present    
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "day":
                    self.day = value
                if key == "monday":
                    self.monday = value
                if key == "tuesday":
                    self.tuesday = value
                if key == "wednesday":
                    self.wednesday = value
                if key == "thursday":
                    self.thursday = value
                if key == "friday":
                    self.friday = value
                if key == "saturday":
                    self.saturday = value
                if key == "sunday":
                    self.sunday = value

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, value):
        self.__day = value

    @property
    def monday(self):
        return self.__day[0]

    @monday.setter
    def monday(self, value):
        self.__day[0] = value

    @property
    def tuesday(self):
        return self.__day[1]

    @tuesday.setter
    def tuesday(self, value):
        self.__day[1] = value 

    @property
    def wednesday(self):
        return self.__day[2]

    @wednesday.setter
    def wednesday(self, value):
        self.__day[2] = value 

    @property
    def thursday(self):
        return self.__day[3]

    @thursday.setter
    def thursday(self, value):
        self.__day[3] = value 

    @property
    def friday(self):
        return self.__day[4]

    @friday.setter
    def friday(self, value):
        self.__day[4] = value 

    @property
    def saturday(self):
        return self.__day[5]

    @saturday.setter
    def saturday(self, value):
        self.__day[5] = value

    @property
    def sunday(self):
        return self.__day[6]

    @sunday.setter
    def sunday(self, value):
        self.__day[6] = value                                              

        