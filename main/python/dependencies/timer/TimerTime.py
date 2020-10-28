from math import floor

class TimerTime:

    def __init__(self, hours, minutes, seconds):
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.seconds = int(seconds)

    def subtractTime(self, hours, minutes, seconds):
        self.seconds -= seconds
        self.minutes += floor(self.seconds / 60)
        self.seconds %= 60
        self.minutes -= minutes
        self.hours += floor(self.minutes / 60)
        self.minutes %= 60
        self.hours -= hours

    def getTime(self):
        return '{:02d}:{:02d}:{:02d}'.format(self.hours, self.minutes, self.seconds)

    def isDone(self):
        if self.seconds <= 0 and self.minutes <= 0 and self.hours <= 0:
            return True
        return False