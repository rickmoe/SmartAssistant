from main.python.dependencies.DependencyManager import DependencyManager
from main.python.dependencies.calendar.Event import Event
from main.python.dependencies.calendar.Time import Time
from main.python.assistant import Constants

def parseInput(input, assistant):
    if "hello" in input:
        assistant.say("yo, what's up dawg?")
    elif "goodbye" in input:
        assistant.say("goodbye")
        return False
    elif ("what's the date" in input) or ("what is the date" in input) or ("what's today's date" in input) or ("what is today's date" in input):
        assistant.say('it\'s {}'.format(Time.getCurrentTime().getDate()))
    elif ("what's the time" in input) or ("what is the time" in input) or ("what time is it" in input):
        assistant.say('it\'s currently {}'.format(Time.getCurrentTime().getTime()))
    elif "event" in input or "calendar" in input:
        calendar = DependencyManager.getCurrentCalendar()
        if "what" in input or "how many" in input:
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
        elif "add" in input or "create" in input or "make" in input:
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
                DependencyManager.createCalendar(calendarName)
                assistant.say('created a new calendar called {}'.format(calendarName))
        elif "delete" in input or "remove" in input or "cancel" in input:
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
                    DependencyManager.getCalendars()['{}.txt'.format(calendarName)].delCalendar()
                    assistant.say('deleted {}'.format(calendarName))
                except:
                    assistant.say('could not find a calendar named {}'.format(calendarName))
        elif "set" in input or "switch" in input:
            calendarName = input.split(" to ")[1]
            try:
                DependencyManager.setCurrentCalendar('{}.txt'.format(calendarName))
                assistant.say('set the current calendar to {}'.format(calendarName))
            except:
                assistant.say('could not find a calendar named {}'.format(calendarName))

    elif "assistant" in input:
        if "set" in input or "switch" in input:
            assistantName = input.split(" to ")[1]
            try:
                DependencyManager.setCurrentAssistant(assistantName)
                assistant.say("ok. goodbye.")
                DependencyManager.getCurrentAssistant().say("hello, i'm {}.".format(assistantName))
            except:
                assistant.say('i couldn\'t find an assistant named {}'.format(assistantName))
        elif "add" in input or "create" in input or "make" in input:
            name = promptAssistantName(input, assistant)
            assistant.say("on a scale from 0 to 10, how fast do you want them to talk?")
            speechRate = max(0, min(10, promptNum(assistant.getAudio(), assistant)))
            speechRate = int(convertRange(speechRate, 0, 10, Constants.ASSISTANT_MIN_SPEECH_RATE, Constants.ASSISTANT_MAX_SPEECH_RATE))
            assistant.say("on a scale from 0 to 10, how loud do you want them to be?")
            volume = max(0, min(10, promptNum(assistant.getAudio(), assistant)))
            volume = convertRange(volume, 0, 10, Constants.ASSISTANT_MIN_VOLUME, Constants.ASSISTANT_MAX_VOLUME)
            assistant.say("do you want them to have a male or female voice? say 0 for male and 1 for female.")
            voice = max(0, min(1, promptNum(assistant.getAudio(), assistant)))
            DependencyManager.createAssistant(name, speechRate, volume, voice)
            assistant.say('done! say hello {}.'.format(name))
            DependencyManager.getAssistants()[name].say('hello, i am {}, your personal assistant.'.format(name))
        elif "delete" in input:
            name = promptAssistantName(input, assistant)
            try:
                DependencyManager.delAssistant(name)
                assistant.say('successfully deleted {}'.format(name))
            except:
                assistant.say('could not find an assistant named {}'.format(name))
    elif "timer" in input:
        hours, minutes, seconds = promptTimerTime(assistant, input)
        DependencyManager.getDependency('timer')(hours, minutes, seconds).startTimer()
        str = 'set a timer for {}{} {} {}{} {} {}{}.'.format((hours + " hour") if int(hours) != 0 else "", "s" if (int(hours) != 1 and int(hours) != 0) else "",
                "and" if int(hours) != 0 and int(minutes) != 0 and int(seconds == 0) else "",
                (minutes + " minute") if int(minutes) != 0 else "", "s" if (int(minutes) != 1 and int(minutes) != 0) else "",
                "and" if (int(hours) != 0 or int(minutes) != 0) and int(seconds != 0) else "",
                (seconds + " second") if int(seconds) != 0 else "", "s" if (int(seconds) != 1 and int(seconds) != 0) else "")
        assistant.say(str)
    else:
        assistant.say("sorry, I didn't get that")
    return True

def promptTimerTime(assistant, input):
    while True:
        hours, minutes, seconds = getHoursMinutesSeconds(input)
        if hours != 0 or minutes != 0 or seconds != 0:
            return hours, minutes, seconds
        assistant.say("for how long?")
        input = assistant.getAudio()

def getHoursMinutesSeconds(input):
    hours, minutes, seconds = 0, 0, 0
    if "hour" in input:
        temp = input.split(" hour")[0].split()
        hours = temp[len(temp) - 1]
    if "minute" in input:
        temp = input.split(" minute")[0].split()
        minutes = temp[len(temp) - 1]
    if "second" in input:
        temp = input.split(" second")[0].split()
        seconds = temp[len(temp) - 1]
    return hours, minutes, seconds

def promptCalendarTitle(assistant):
    title = ""
    while title == "":
        assistant.say("what's the calendar's name?")
        title = assistant.getAudio()
    return title

def promptEventTitle(userInput, assistant):
    while getName(userInput) is not "":
        assistant.say("what would you like to name it?")
        userIn = assistant.getAudio().title()
        return userIn if userIn is not "" else ""
    return getName(userInput)

def promptAssistantName(userInput, assistant):
    while getName(userInput) is "":
        assistant.say("what would you like to name them?")
        return assistant.getAudio().title()
    return getName(userInput)

def promptNum(userInput, assistant):
    while True:
        try:
            speechRate = int(userInput)
            return speechRate
        except:
            assistant.say("please state a valid number")
            userInput = assistant.getAudio()

def getName(userInput):
    if " called " in userInput:
        return userInput.split("called ")[1].split()[0].title()
    elif " named " in userInput:
        return userInput.split("named ")[1].split()[0].title()
    return ""

def convertRange(val, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    return (val - min1) * range2 / range1 + min2

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
        if ordinal in input and isDigit[input.find(ordinal) - 1]:
            if isDigit[input.find(ordinal) - 2]:
                day = int(input[input.find(ordinal) - 2:input.find(ordinal)])
            else:
                day = int(input[input.find(ordinal) - 1:input.find(ordinal)])
    if day == 0:
        return None
    else:
        t = Time.getCurrentTime()
        if t.getDay() <= day:
            t.setDay(day)
            return t
        else:
            t.addTime(1, 0, 0, 0, 0)
            t.setDay(day)
            return t

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
