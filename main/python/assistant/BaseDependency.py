from main.python.dependencies.Dependency import Dependency
from main.python.dependencies.calendar.Time import Time

class BaseDependency(Dependency):

    powered = None
    dependencyKeyWords = None       # Overrides keyword check
    keyWordList = [[]]
    keyWordMethods = []

    @staticmethod
    def init(memory):
        BaseDependency.powered = True
        BaseDependency.keyWordList = [['hello', 'hi', 'yo', "what's up"],
                                      ['goodbye', 'bye'],
                                      ["what's the date", "what is the date", "what's today's date", "what is today's date", "what day is it"],
                                      ["what's the time", "what is the time", "what time is it"]]
        BaseDependency.keyWordMethods = [BaseDependency.respondHello,
                                         BaseDependency.respondGoodbye,
                                         BaseDependency.sayDate,
                                         BaseDependency.sayTime]

    @staticmethod
    def getName():
        return "Base"

    @staticmethod
    def getPowered():
        return BaseDependency.powered

    @staticmethod
    def setPowered(state):
        BaseDependency.powered = state

    @staticmethod
    def respondHello(input, assistant):
        assistant.say("yo, what's up dawg?")

    @staticmethod
    def respondGoodbye(input, assistant):
        assistant.say("goodbye")
        BaseDependency.setPowered(False)

    @staticmethod
    def sayDate(input, assistant):
        assistant.say('it\'s {}'.format(Time.getCurrentTime().getDate()))

    @staticmethod
    def sayTime(input, assistant):
        assistant.say('it\'s currently {}'.format(Time.getCurrentTime().getTime()))
