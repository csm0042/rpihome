import datetime


class Condition(object):
    condition = str()
    state = str()


class OnRange(object):
    on_time = datetime.time()
    off_time = datetime.time()
    condition = Condition()


class Day(object):
    def __init__(self):
        date = datetime.datetime.now().date()
        on_range = [OnRange()]


class Week(object):
    def __init__(self):
        __day = [Day()] * 7

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

        