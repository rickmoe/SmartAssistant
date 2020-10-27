from datetime import datetime
from main.python.assistant import Constants

class Time:

    def __init__(self, month, day, year, hour, minute):
        self.setDateTime(month, day, year, hour, minute)

    def getInstance(self):
        return self

    def getDay(self):
        return self.day

    def setDay(self, day):
        self.day = int(day)

    def getMonth(self):
        return self.month

    def setMonth(self, month):
        self.month = int(month)

    def getYear(self):
        return self.year

    def setYear(self, year):
        self.year = int(year)

    def getHour(self):
        return self.hour

    def setHour(self, hour):
        self.hour = int(hour)

    def getMinute(self):
        return self.minute

    def setMinute(self, minute):
        self.minute = int(minute)

    def getDateTimeCSV(self):
        return '{},{}'.format(self.getDateCSV(), self.getTimeCSV())

    def getDateTime(self):
        return '{} at {}'.format(self.getDate(), self.getTime())

    def setDateTime(self, month, day, year, hour, minute):
        self.setDate(month, day, year)
        self.setTime(hour, minute)

    def getTimeCSV(self):
        return '{},{}'.format(self.getHour(), self.getMinute())

    def getTime(self):
        return '{}:{:02d} {}'.format(self.getHour() % 12 if self.getHour() % 12 != 0 else 12, self.getMinute(), "am" if self.getHour() < 12 else "pm")

    def setTime(self, hour, minute):
        self.setHour(hour)
        self.setMinute(minute)

    def getMonthDay(self):
        return '{} {}{}'.format(Constants.MONTH_STRINGS_PROPER[self.getMonth() - 1], self.getDay(), self.getDaySuffix())

    def getDateCSV(self):
        return '{},{},{}'.format(self.getMonth(), self.getDay(), self.getYear())

    def getDate(self):
        return '{}, {} {}{}, {}'.format(self.getWeekday(), Constants.MONTH_STRINGS_PROPER[self.getMonth() - 1], self.getDay(), self.getDaySuffix(), self.getYear())

    def setDate(self, month, day, year):
        self.setMonth(month)
        self.setDay(day)
        self.setYear(year)

    @staticmethod
    def getCurrentTime():
        today = datetime.now()
        return Time(today.month, today.day, today.year, today.hour, today.minute)

    def isLeapYear(self):
        if (self.getYear() % 400) == 0:
            return True
        elif (self.getYear() % 4) == 0 and (self.getYear() % 100) != 0:
            return True
        else:
            return False

    def getDaySuffix(self):
        if 10 < self.getDay() < 14:
            return "th"
        elif (self.getDay() % 10) == 1:
            return "st"
        elif (self.getDay() % 10) == 2:
            return "nd"
        elif (self.getDay() % 10) == 3:
            return "rd"
        else:
            return "th"

    def getWeekday(self):
        # Uses Zeller's Rule
        # @see http://mathforum.org/dr.math/faq/faq.calendar.html
        k = self.getDay()
        m = (self.getMonth() - 2) % 12 if self.month is not 2 else 12
        D = (self.getYear() - (0 if self.getMonth() > 2 else 1)) % 100
        C = (self.getYear() - (0 if self.getMonth() > 2 else 1)) - D
        f = k + int((13 * m - 1) / 5) + D + int(D / 4) + int(C / 4) - 2 * C
        return Constants.WEEKDAY_STRINGS_PROPER[f % 7]

    @staticmethod
    def getMonthOfNextDayInstance(day):
        t = Time.getCurrentTime()
        if day < t.getDay():
            t.addTime(1, 0, 0, 0, 0)
        return t.getMonth()

    @staticmethod
    def getYearOfNextMonthInstance(month):
        t = Time.getCurrentTime()
        if month < t.getMonth():
            t.addTime(0, 0, 1, 0, 0)
        return t.getYear()

    def addTime(self, months, days, years, hours, minutes):
        self.setMinute(self.getMinute() + minutes)
        self.setHour(self.getHour() + hours + int(self.getMinute() / 60))
        self.setMinute(self.getMinute() % 60)
        self.setDay(self.getDay() + days + int(self.getHour() / 24))
        self.setHour(self.getHour() % 24)
        while self.getDay() > (Constants.DAYS_IN_MONTH_LEAP if self.isLeapYear() else Constants.DAYS_IN_MONTH_NON_LEAP)[self.getMonth() - 1]:
            print('{} || {}'.format(self.getDay(), (
                Constants.DAYS_IN_MONTH_LEAP if self.isLeapYear() else Constants.DAYS_IN_MONTH_NON_LEAP)[self.getMonth() - 1]))
            deltaDays = (Constants.DAYS_IN_MONTH_LEAP if self.isLeapYear() else Constants.DAYS_IN_MONTH_NON_LEAP)[self.getMonth() - 1]
            self.setMonth(self.getMonth() + 1)
            self.setDay(self.getDay() - deltaDays)
            self.setYear(self.getYear() + (1 if self.getMonth() > 12 else 0))
            self.setMonth(self.getMonth() - (12 if self.getMonth() > 12 else 0))
        self.setMonth(self.getMonth() + months)
        while self.getMonth() > 12:
            self.setYear(self.getYear() + (1 if self.getMonth() > 12 else 0))
            self.setMonth(self.getMonth() - (12 if self.getMonth() > 12 else 0))
        self.setYear(self.getYear() + years)
