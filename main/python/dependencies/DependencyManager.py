from main.python.dependencies.ActiveDependencies import ActiveDependencies
from main.python.dependencies.memory.MemoryParser import MemoryParser
from main.python.dependencies.memory.MemoryWriter import MemoryWriter
from main.python.dependencies.calendar.Calendar import Calendar
from main.python.dependencies.smartAssistant.SmartAssistant import SmartAssistant
from main.python.dependencies.timer.Timer import Timer
from main.python.assistant import Constants

class DependencyManager:

    memoryParser = None

    @staticmethod
    def initDependencies():
        DependencyManager.memoryParser = MemoryParser(Constants.MEMORY_FILE)
        for dependency in ActiveDependencies:
            dependency.value.init(DependencyManager.getMemoryParser())

    @staticmethod
    def concludeDependencies():
        for dependency in ActiveDependencies:
            dependency.value.conclude(DependencyManager.getMemoryParser())

    @staticmethod
    def getDependency(dependency):
        for d in ActiveDependencies:
            if str(dependency).upper() == d.name:
                return d.value
        return None

    @staticmethod
    def getMemoryParser():
        return DependencyManager.memoryParser

    @staticmethod
    def getCurrentCalendar():
        return Calendar.currentCalendar

    @staticmethod
    def getCalendars():
        return Calendar.getCalendars()

    @staticmethod
    def setCurrentCalendar(calendarName):
        Calendar.setCurrentCalendar(Calendar.calendars[calendarName])

    @staticmethod
    def createCalendar(calendarName):
        Calendar(calendarName)

    @staticmethod
    def getCurrentAssistant():
        return SmartAssistant.currentAssistant

    @staticmethod
    def setCurrentAssistant(assistantName):
        SmartAssistant.setCurrentAssistant(SmartAssistant.assistants[assistantName.title()])

    @staticmethod
    def getAssistants():
        return SmartAssistant.getAssistants()

    @staticmethod
    def getActiveTimers():
        return Timer.activeTimers

    @staticmethod
    def createAssistant(name, speechRate, volume, voice, wakeWords=None):
        assist = SmartAssistant.createAssistant(name, speechRate, volume, voice, wakeWords)
        assistList = []
        for key in DependencyManager.getAssistants():
            assistList.append(key)
        DependencyManager.changeInMemory("assistantNames", assistList)
        DependencyManager.appendToMemorySection('{}SpeechRate'.format(name), assist.getSpeechRate(), "Assistant Data")
        DependencyManager.appendToMemorySection('{}Volume'.format(name), assist.getVolume(), "Assistant Data")
        DependencyManager.appendToMemorySection('{}Voice'.format(name), assist.getVoice(), "Assistant Data")
        DependencyManager.appendToMemorySection('{}WakeWords'.format(name), assist.getWakeWords(), "Assistant Data")

    @staticmethod
    def delAssistant(name):
        assist = DependencyManager.getAssistants()[name]
        assist.delAssistant()
        a = DependencyManager.getAssistants()
        assistList = []
        for key in a:
            assistList.append(key)
        DependencyManager.changeInMemory("assistantNames", assistList)
        DependencyManager.deleteFromMemory('{}SpeechRate'.format(name))
        DependencyManager.deleteFromMemory('{}Volume'.format(name))
        DependencyManager.deleteFromMemory('{}Voice'.format(name))
        DependencyManager.deleteFromMemory('{}WakeWords'.format(name))

    @staticmethod
    def addToMemory(key, values):
        MemoryWriter(Constants.MEMORY_FILE).addToMemory(key, values)

    @staticmethod
    def deleteFromMemory(key):
        MemoryWriter(Constants.MEMORY_FILE).deleteFromMemory(key)

    @staticmethod
    def changeInMemory(key, values):
        MemoryWriter(Constants.MEMORY_FILE).changeValue(key, values)

    @staticmethod
    def appendToMemorySection(key, values, sectionName):
        MemoryWriter(Constants.MEMORY_FILE).appendToSection(key, values, sectionName)
