from time import sleep
from main.python.dependencies.timer.TimerTime import TimerTime

class Timer:

    activeTimers = []

    def __init__(self, hours, minutes, seconds):
        self.time = TimerTime(hours, minutes, seconds)
        global stopThread

    def startTimer(self):
        global stopThread
        stopThread = False
        Timer.activeTimers.append(self)
        while not self.time.isDone():
            sleep(1)
            self.time.subtractTime(0, 0, 1)
            if stopThread:
                return
        print("Done!")
        Timer.activeTimers.remove(self)

    def stopTimer(self):
        Timer.activeTimers.remove(self)
        global stopThread
        stopThread = True