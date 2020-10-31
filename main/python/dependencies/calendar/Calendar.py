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
    memory = None

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
    def setDefaultCalendar(memory, calendarName):
        memory.changeInMemory("defaultCalendar", '{}.txt'.format(calendarName))

    @staticmethod
    def setCurrentCalendar(calendarName):
        Calendar.currentCalendar = Calendar.calendars[calendarName]

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
    def init(memory):
        Calendar.dependencyKeyWords = {'event', 'calendar'}
        Calendar.keyWordList = [['default'],
                                ['what', 'how many'],
                                ['add', 'create', 'make'],
                                ['delete', 'get rid of', 'remove', 'cancel'],
                                ['set', 'switch']]
        Calendar.keyWordMethods = [Calendar.respondSetDefault,
                                   Calendar.respondList,
                                   Calendar.respondAdd,
                                   Calendar.respondDel,
                                   Calendar.respondSet]
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\calendars")
        for file in glob.glob("*.txt"):
            file = file.split(".tx")[0]
            Calendar(file)
        Calendar.setCurrentCalendar(memory.searchMemory("defaultCalendar"))
        Calendar.memory = memory

    @staticmethod
    def getName():
        return "Calendar"

    @staticmethod
    def respondSetDefault(input, assistant):
        calendarName = input.split(" to ")[1]
        try:
            currentCalendarName = Calendar.getCurrentCalendar().filename
            Calendar.setCurrentCalendar('{}.txt'.format(calendarName))
            Calendar.setDefaultCalendar(Calendar.memory, calendarName)
            assistant.say('{} is now your default calendar.'.format(calendarName))
            Calendar.setCurrentCalendar(currentCalendarName)
        except:
            assistant.say('i couldn\'t find a calendar named {}'.format(calendarName))

    @staticmethod
    def respondList(input, assistant):
        calendar = Calendar.getCurrentCalendar()
        if "today" in input:
            t = Time.getCurrentTime()
            matchingEvents = calendar.checkForEvents(t.getMonth(), t.getDay(), t.getYear())
            assistant.say("you have {} {} today.".format(len(matchingEvents), "event" if len(matchingEvents) == 1 else "events"))
            for event in matchingEvents:
                assistant.say("at {} you have {}.".format(event.getStart().getTime(), event.getName()))
        elif "tomorrow" in input:
            t = Time.getCurrentTime()
            t.addTime(0, 1, 0, 0, 0)
            matchingEvents = calendar.checkForEvents(t.getMonth(), t.getDay(), t.getYear())
            assistant.say("you have {} {} tomorrow.".format(len(matchingEvents), "event" if len(matchingEvents) == 1 else "events"))
            for event in matchingEvents:
                assistant.say("at {} you have {}.".format(event.getStart().getTime(), event.getName()))
        elif getDate(input) is not None:
            t = getDate(input)
            matchingEvents = calendar.checkForEvents(t.getMonth(), t.getDay(), t.getYear())
            dateStr = t.getDate() if Time.getCurrentTime().getYear() != t.getYear() else t.getMonthDay()
            assistant.say("you have {} {} on {}.".format(len(matchingEvents), "event" if len(matchingEvents) == 1 else "events", dateStr))
            for event in matchingEvents:
                assistant.say("at {} you have {}.".format(event.getStart().getTime(), event.getName()))
        elif getDay(input) is not None:
            t = getDay(input)
            matchingEvents = calendar.checkForEvents(t.getMonth(), t.getDay(), t.getYear())
            assistant.say("you have {} {} on the {}{}.".format(len(matchingEvents), "event" if len(matchingEvents) == 1 else "events", t.getDay(), t.getDaySuffix()))
            for event in matchingEvents:
                assistant.say("at {} you have {}.".format(event.getStart().getTime(), event.getName()))
        elif getWeekday(input) is not None:
            t = getWeekday(input)
            matchingEvents = calendar.checkForEvents(t.getMonth(), t.getDay(), t.getYear())
            assistant.say("you have {} {} on {}.".format(len(matchingEvents), "event" if len(matchingEvents) == 1 else "events", t.getWeekday()))
            for event in matchingEvents:
                assistant.say("at {} you have {}.".format(event.getStart().getTime(), event.getName()))
        else:
            events = calendar.getEvents()
            assistant.say("you have {} {}.".format(len(events), "event" if len(events) == 1 else "events"))
            for event in events:
                assistant.say("on {} you have {}.".format(event.getStart().getDateTime(), event.getName()))

    @staticmethod
    def respondAdd(input, assistant):
        calendar = Calendar.getCurrentCalendar()
        if "event" in input:
            hour, minute = getTime(input, assistant)
            if "today" in input:
                t = Time.getCurrentTime()
                t.setTime(hour, minute)
                title = promptEventTitle(input, assistant)
                calendar.addEvent(Event(title, t))
                assistant.say('added {} to your calendar at {} today'.format(title, t.getTime()))
            elif "tomorrow" in input:
                t = Time.getCurrentTime()
                t.addTime(0, 1, 0, 0, 0)
                t.setTime(hour, minute)
                title = promptEventTitle(input, assistant)
                calendar.addEvent(Event(title, t))
                assistant.say('added {} to your calendar at {} tomorrow'.format(title, t.getTime()))
            elif getDate(input) is not None:
                t = getDate(input)
                t.setTime(hour, minute)
                title = promptEventTitle(input, assistant)
                calendar.addEvent(Event(title, t))
                assistant.say('added {} to your calendar at {} on {}'.format(title, t.getTime(), t.getDate()))
            elif getDay(input) is not None:
                t = getDay(input)
                t.setTime(hour, minute)
                title = promptEventTitle(input, assistant)
                calendar.addEvent(Event(title, t))
                assistant.say('added {} to your calendar at {} on {}'.format(title, t.getTime(), t.getMonthDay()))
            elif getWeekday(input) is not None:
                t = getWeekday(input)
                t.setTime(hour, minute)
                title = promptEventTitle(input, assistant)
                calendar.addEvent(Event(title, t))
                assistant.say('added {} to your calendar at {} on {}'.format(title, t.getTime(), t.getWeekday()))
            else:
                t = promptForDate(assistant)
                t.setTime(hour, minute)
                title = promptEventTitle(input, assistant)
                calendar.addEvent(Event(title, t))
                assistant.say('added {} to your calendar at {} on {}'.format(title, t.getTime(), t.getDate()))
        else:
            calendarName = promptCalendarTitle(assistant)
            Calendar(calendarName)
            assistant.say('created a new calendar called {}'.format(calendarName))

    @staticmethod
    def respondDel(input, assistant):
        calendar = Calendar.getCurrentCalendar()
        if "event" in input:
            if "today" in input:
                t = Time.getCurrentTime()
                delCount = calendar.delEvent(t.getMonth(), t.getDay(), t.getYear())
                assistant.say('deleted {} events'.format(delCount))
            elif "tomorrow" in input:
                t = Time.getCurrentTime()
                t.addTime(0, 1, 0, 0, 0)
                delCount = calendar.delEvent(t.getMonth(), t.getDay(), t.getYear())
                assistant.say('deleted {} events'.format(delCount))
            elif getDate(input) is not None:
                t = getDate(input)
                delCount = calendar.delEvent(t.getMonth(), t.getDay(), t.getYear())
                assistant.say('deleted {} events'.format(delCount))
            elif getDay(input) is not None:
                t = getDay(input)
                delCount = calendar.delEvent(t.getMonth(), t.getDay(), t.getYear())
                assistant.say('deleted {} events'.format(delCount))
            elif getWeekday(input) is not None:
                t = getWeekday(input)
                delCount = calendar.delEvent(t.getMonth(), t.getDay(), t.getYear())
                assistant.say('deleted {} events'.format(delCount))
            elif getName(input) is not "":
                title = getName(input)
                delCount = calendar.delEvent(title)
                assistant.say('deleted {} events'.format(delCount))
            else:
                title = promptEventTitle(input, assistant)
                delCount = calendar.delEvent(title)
                assistant.say('deleted {} events'.format(delCount))
        else:
            calendarName = promptCalendarTitle(assistant)
            try:
                Calendar.getCalendars()['{}.txt'.format(calendarName)].delCalendar()
                assistant.say('deleted {}'.format(calendarName))
            except:
                assistant.say('could not find a calendar named {}'.format(calendarName))

    @staticmethod
    def respondSet(input, assistant):
        calendarName = input.split(" to ")[1]
        try:
            Calendar.setCurrentCalendar('{}.txt'.format(calendarName))
            assistant.say('set the current calendar to {}'.format(calendarName))
        except:
            assistant.say('could not find a calendar named {}'.format(calendarName))

def getWeekday(input):
    targetString = ""
    for day in Constants.WEEKDAY_STRINGS:
        if day in input:
            targetString = day
    if targetString is "":
        return None
    else:
        t = Time.getCurrentTime()
        currentWeekday = Constants.WEEKDAY_STRINGS_PROPER.index(t.getWeekday())
        targetWeekday = Constants.WEEKDAY_STRINGS.index(targetString)
        t.addTime(0, (targetWeekday - currentWeekday) % 7, 0, 0, 0)
        return t

def getDay(input):
    day = 0
    isDigit = []
    for i, c in enumerate(input):
        isDigit.append(c in Constants.DIGITS)
    for ordinal in Constants.ORDINAL_INDICATORS:
        poses = set()
        if ordinal in input:
            for i in range(len(input) - 1):
                if input[i:i+2] == ordinal:
                    poses.add(i)
        for pos in poses:
            if isDigit[pos - 1]:
                if isDigit[pos - 2]:
                    day = int(input[pos - 2:pos])
                else:
                    day = int(input[pos - 1:pos])
    if day != 0:
        t = Time.getCurrentTime()
        if t.getDay() <= day:
            t.setDay(day)
            return t
        else:
            t.addTime(1, 0, 0, 0, 0)
            t.setDay(day)
            return t
    return None

def getDate(input):
    month, day, year = -1, -1, Time.getCurrentTime().getYear()
    for m in Constants.MONTH_STRINGS:
        if m in input:
            month = int(Constants.MONTH_STRINGS.index(m) + 1)
    isDigit = []
    for i, c in enumerate(input):
        isDigit.append(c in Constants.DIGITS)
        if i > 2 and isDigit[i - 1] and isDigit[i - 2] and isDigit[i - 3]:
            year = int(input[i - 3:i + 1])
    for ordinal in Constants.ORDINAL_INDICATORS:
        if ordinal in input and isDigit[input.find(ordinal) - 1] and isDigit[input.find(ordinal) - 2]:
            day = int(input[input.find(ordinal) - 2:input.find(ordinal)])
    if month == -1 or day == -1:
        return None
    else:
        return Time(month, day, year, 0, 0)

def getTime(userInput, assistant):
    stringToSearch = ""
    hoursToAdd = -1
    while stringToSearch is "":
        if " a.m." in userInput:
            temp = userInput.split(" a.m.")[0].split()
            stringToSearch = temp[len(temp) - 1]
            hoursToAdd = 0
        elif " p.m." in userInput:
            temp = userInput.split(" p.m.")[0].split()
            stringToSearch = temp[len(temp) - 1]
            hoursToAdd = 12
        elif ":" in userInput:
            stringToSearch = userInput[max((userInput.find(":") - 2), 0):min(userInput.find(":") + 3, len(userInput))]
        elif " at " in userInput:
            stringToSearch = userInput.split(" at ")[1].split(" ")[0]
        else:
            allDigits = True
            for c in userInput:
                if not (c.isdigit()):
                    allDigits = False
            if allDigits:
                stringToSearch = userInput
            else:
                assistant.say("what time?")
                userInput = assistant.getAudio()
    hour, minute = 0, 0
    if ":" in stringToSearch:
        hour = int(stringToSearch.split(":")[0])
        minute = int(stringToSearch.split(":")[1])
    else:
        for c in stringToSearch:
            if c.isdigit():
                hour = int(c) if hour == 0 else hour * 10 + int(c)
    hour = hour - 12 if hour == 12 else hour
    if hoursToAdd is -1:
        hoursToAdd = 0 if abs(hour - 14) <= abs(hour + 12 - 14) else 12
    hour = hour + hoursToAdd
    return hour, minute

def promptEventTitle(userInput, assistant):
    while getName(userInput) is not "":
        assistant.say("what would you like to name it?")
        userIn = assistant.getAudio().title()
        return userIn if userIn is not "" else ""
    return getName(userInput)

def getName(userInput):
    if " called " in userInput:
        return userInput.split("called ")[1].split()[0].title()
    elif " named " in userInput:
        return userInput.split("named ")[1].split()[0].title()
    return ""

def promptForDate(assistant):
    t = None
    while t is None:
        assistant.say("what day?")
        userInput = assistant.getAudio()
        if "today" in userInput:
            t = Time.getCurrentTime()
        elif "tomorrow" in userInput:
            t = Time.getCurrentTime()
            t.addTime(0, 1, 0, 0, 0)
        elif getDate(userInput) is not None:
            t = getDate(userInput)
        elif getDay(userInput) is not None:
            t = getDay(userInput)
        elif getWeekday(userInput) is not None:
            t = getWeekday(userInput)
    return t

def promptCalendarTitle(assistant):
    title = ""
    while title == "":
        assistant.say("what's the calendar's name?")
        title = assistant.getAudio()
    return title
