import os
import glob
from multipledispatch import dispatch
from main.python.dependencies.Dependency import Dependency
from main.python.dependencies.calendar.CalendarEventParser import CalendarEventParser
from main.python.dependencies.calendar.CalendarEventWriter import CalendarEventWriter
from main.python.dependencies.calendar.Event import Event
from main.python.dependencies.calendar.Time import Time
from main.python.assistant import Constants

class Calendar(Dependency):

    calendars = {}
    currentCalendar = None

    def __init__(self, filename):
        self.filename = '{}.txt'.format(filename)
        self.createFile(self.filename)
        Calendar.calendars[self.filename] = self
        self.events = []
        self.readEvents()

    @staticmethod
    def createFile(path):
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\calendars")
        try:
            with open(path, 'r+') as file:
                data = file.read()
        except FileNotFoundError:
            with open(path, 'w+') as file:
                data = file.read()

    def delCalendar(self):
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\calendars")
        if os.path.exists(self.filename):
            os.remove(self.filename)

    @staticmethod
    def setCurrentCalendar(calendar):
        Calendar.currentCalendar = calendar

    @staticmethod
    def getCurrentCalendar():
        return Calendar.currentCalendar

    @staticmethod
    def getCalendars():
        return Calendar.calendars

    def getEvents(self):
        self.readEvents()
        return self.events

    @dispatch(Event)
    def addEvent(self, event):
        CalendarEventWriter(self.filename).addEvent(event)

    @dispatch(Event)
    def delEvent(self, event):
        CalendarEventWriter(self.filename).delEvent(event)
        self.readEvents()

    @dispatch(str)
    def delEvent(self, eventName):
        delCount = 0
        for event in self.getEvents():
            if eventName == event.getName():
                self.delEvent(event)
                delCount += 1
        return delCount

    @dispatch(Time)
    def delEvent(self, time):
        delCount = 0
        for event in self.getEvents():
            if time.getDateTime() == event.getStart().getDateTime():
                self.delEvent(event)
                delCount += 1
        return delCount

    @dispatch(int, int, int)
    def delEvent(self, month, day, year):
        if day is 0:
            day = Time.getCurrentTime().getDay()
        if month is 0:
            month = Time.getMonthOfNextDayInstance(day)
        if year is 0:
            year = Time.getYearOfNextMonthInstance(month)
        delCount = 0
        for event in self.getEvents():
            if event.getStart().getDateCSV() == '{},{},{}'.format(month, day, year):
                self.delEvent(event)
                delCount += 1
        return delCount

    def readEvents(self):
        parser = CalendarEventParser(self.filename)
        self.events = parser.getEvents()

    @staticmethod
    def isSameDate(t1, t2):
        if t1.getMonth() == t2.getMonth() and t1.getDay() == t2.getDay() and t1.getYear() == t2.getYear():
            return True
        else:
            return False

    def checkForEvents(self, month, day, year):
        events = []
        t = Time(month, day, year, 0, 0)
        for event in self.getEvents():
            startTime = event.getStart()
            if Calendar.isSameDate(t, startTime):
                events.append(event)
        return events

    @staticmethod
    def init(memoryParser):
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\calendars")
        for file in glob.glob("*.txt"):
            file = file.split(".tx")[0]
            Calendar(file)
        Calendar.setCurrentCalendar(Calendar.calendars[memoryParser.searchMemory("defaultCalendar")])

    @staticmethod
    def getName():
        return "Calendar"
