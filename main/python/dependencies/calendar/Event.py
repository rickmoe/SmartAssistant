class Event:

    def __init__(self, eventName, startTime):
        self.name = eventName
        self.startTime = startTime

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setStart(self, time):
        self.startTime = time

    def getStart(self):
        return self.startTime
