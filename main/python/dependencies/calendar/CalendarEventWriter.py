import io
import os
from main.python.assistant import Constants


class CalendarEventWriter:

    def __init__(self, filename):
        self.filename = filename

    def addEvent(self, event):
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\calendars")
        with io.open(self.filename, 'a+', encoding='utf-8') as file:
            file.write('${}$\t\t%{}%\n'.format(event.getName(), event.getStart().getDateTimeCSV()))

    def delEvent(self, event):
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\calendars")
        with open(self.filename, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for i in lines:
                if '${}$'.format(event.getName()) not in i or '%{}%'.format(event.getStart().getDateTimeCSV()) not in i:
                    file.write(i)
            file.truncate()
