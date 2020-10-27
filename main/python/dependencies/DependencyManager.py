from main.python.dependencies.memory.MemoryParser import MemoryParser
from main.python.dependencies.memory.MemoryWriter import MemoryWriter
from main.python.dependencies.calendar.Calendar import initCalendars, Calendar
from main.python.dependencies.smartAssistant.SmartAssistant import initSmartAssistants, SmartAssistant
from main.python.assistant import Constants

class DependencyManager:

    memoryParser = None

    @staticmethod
    def initDependencies():
        DependencyManager.memoryParser = MemoryParser(Constants.MEMORY_FILE)
        initCalendars(DependencyManager.memoryParser)
        initSmartAssistants(DependencyManager.memoryParser)

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
    def createAssistant(name, speechRate, volume, voice, wakeWords=None):
        if wakeWords is None:
            wakeWords = [name.lower()]
        assist = SmartAssistant(name, speechRate, volume, voice, wakeWords)
        a = DependencyManager.getAssistants()
        assistList = []
        for key in a:
            assistList.append(key)
        assistList.append(name)
        DependencyManager.changeInMemory("assistantNames", assistList)
        DependencyManager.appendToMemorySection('{}SpeechRate'.format(name), speechRate, "Assistant Data")
        DependencyManager.appendToMemorySection('{}Volume'.format(name), volume, "Assistant Data")
        DependencyManager.appendToMemorySection('{}Voice'.format(name), voice, "Assistant Data")
        DependencyManager.appendToMemorySection('{}WakeWords'.format(name), wakeWords, "Assistant Data")

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