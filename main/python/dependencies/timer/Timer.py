import threading
from time import sleep
from main.python.dependencies.Dependency import Dependency
from main.python.dependencies.timer.TimerTime import TimerTime

class Timer(Dependency):

    activeTimers = set()

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
    def conclude(memoryParser):
        [t.stopTimer() for t in Timer.activeTimers]

    @staticmethod
    def getName():
        return "Timer"
