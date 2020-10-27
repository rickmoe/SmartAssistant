import os
from main.python.dependencies.calendar.Event import Event
from main.python.dependencies.calendar.Time import Time
from main.python.assistant import Constants


class CalendarEventParser:

    def __init__(self, filename):
        self.filename = filename
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\calendars")
        with open(filename, 'r') as file:
            self.data = file.read()
        self.events = []
        self.parseData()

    def parseData(self):
        self.events = []
        separatedData = self.data.split("\n")
        while len(separatedData) > 0:
            if "//" not in separatedData[0]:
                if "," in separatedData[0]:
                    data = separatedData[0].split("%")[1].split("%")[0].split(",")
                    t = Time(data[0], data[1], data[2], data[3], data[4])
                    self.events.append(Event(separatedData[0].split("$")[1].split("$")[0], t))
                else:
                    pass    # Should not be single variable types in calendar files
            del separatedData[0]

    def getEvents(self):
        return self.events
