import threading
from time import sleep
from main.python.dependencies.Dependency import Dependency
from main.python.dependencies.timer.TimerTime import TimerTime

class Timer(Dependency):

    activeTimers = set()
    keyWordList = [[]]
    keyWordMethods = []

    def __init__(self, hours, minutes, seconds):
        self.time = TimerTime(hours, minutes, seconds)
        self.stopThread = False

    def startTimer(self):
        t = threading.Thread(target=self.runTimer)
        Timer.activeTimers.add(self)
        self.stopThread = False
        t.start()

    def runTimer(self):
        while not self.time.isDone():
            sleep(1)
            self.time.subtractTime(0, 0, 1)
            if self.stopThread:
                return
        print("Done!")
        Timer.activeTimers.remove(self)

    def stopTimer(self):
        Timer.activeTimers.remove(self)
        self.stopThread = True

    @staticmethod
    def init(memory):
        Timer.dependencyKeyWords = {'timer'}
        Timer.keyWordList = [['set', 'start', 'make', 'create'],
                             ['stop', 'delete', 'get rid of', 'reset']]
        Timer.keyWordMethods = [Timer.createNewTimer,
                                Timer.stopTimers]

    @staticmethod
    def conclude(memoryParser):
        tList = list(Timer.activeTimers)
        [t.stopTimer() for t in tList]

    @staticmethod
    def getName():
        return "Timer"

    @staticmethod
    def createNewTimer(input, assistant):
        hours, minutes, seconds = promptTimerTime(input, assistant)
        Timer(hours, minutes, seconds).startTimer()
        str = 'set a timer for {}{} {} {}{} {} {}{}.'.format((hours + " hour") if int(hours) != 0 else "",
                    "s" if (int(hours) != 1 and int(hours) != 0) else "",
                    "and" if int(hours) != 0 and int(minutes) != 0 and int(seconds == 0) else "",
                    (minutes + " minute") if int(minutes) != 0 else "",
                    "s" if (int(minutes) != 1 and int(minutes) != 0) else "",
                    "and" if (int(hours) != 0 or int(minutes) != 0) and int(seconds != 0) else "",
                    (seconds + " second") if int(seconds) != 0 else "",
                    "s" if (int(seconds) != 1 and int(seconds) != 0) else "")
        assistant.say(str)

    @staticmethod
    def stopTimers(input, assistant):
        tList = list(Timer.activeTimers)
        [t.stopTimer() for t in tList]
        assistant.say('all timers have been stopped')

def promptTimerTime(input, assistant):
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
