import pyttsx3 as pyTTS
import speech_recognition as sr
from main.python.dependencies.Dependency import Dependency


class SmartAssistant(Dependency):

    assistants = {}
    currentAssistant = None

    def __init__(self, name, rate, volume, voice, wakeWords):
        self.name = name
        self.rate = int(rate)
        self.volume = float(volume)
        self.voice = int(voice)
        self.wakeWords = wakeWords
        SmartAssistant.assistants[name] = self

    @staticmethod
    def setCurrentAssistant(assistantName):
        SmartAssistant.currentAssistant = SmartAssistant.assistants[assistantName.title()]

    @staticmethod
    def getCurrentAssistant():
        return SmartAssistant.currentAssistant

    @staticmethod
    def getAssistants():
        return SmartAssistant.assistants

    @staticmethod
    def createAssistant(memory, name, speechRate, volume, voice, wakeWords=None):
        if wakeWords is None:
            wakeWords = {name.lower()}
        assist = SmartAssistant(name, speechRate, volume, voice, wakeWords)
        assistList = []
        for name in SmartAssistant.getAssistants():
            assistList.append(name)
        memory.changeInMemory("assistantNames", assistList)
        memory.appendToMemorySection('{}SpeechRate'.format(name), assist.getSpeechRate(), "Assistant Data")
        memory.appendToMemorySection('{}Volume'.format(name), assist.getVolume(), "Assistant Data")
        memory.appendToMemorySection('{}Voice'.format(name), assist.getVoice(), "Assistant Data")
        memory.appendToMemorySection('{}WakeWords'.format(name), assist.getWakeWords(), "Assistant Data")

    @staticmethod
    def delAssistant(memory, name):
        assist = SmartAssistant.assistants[name]
        SmartAssistant.assistants.pop(name)
        del assist
        assistList = []
        for name in SmartAssistant.getAssistants():
            assistList.append(name)
        memory.changeInMemory("assistantNames", assistList)
        memory.deleteFromMemory('{}SpeechRate'.format(name))
        memory.deleteFromMemory('{}Volume'.format(name))
        memory.deleteFromMemory('{}Voice'.format(name))
        memory.deleteFromMemory('{}WakeWords'.format(name))

    def getSpeechRate(self):
        return self.rate

    def getVolume(self):
        return self.volume

    def getVoice(self):
        return self.voice

    def getWakeWords(self):
        return self.wakeWords

    def say(self, text):
        engine = pyTTS.init()
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        engine.setProperty('voice', engine.getProperty('voices')[self.voice].id)
        engine.say(text)
        engine.runAndWait()

    def getAudio(self):
        # r = sr.Recognizer()
        # with sr.Microphone() as source:
        #    audio = r.listen(source)
        #    input = ""
        #    try:
        #        input = r.recognize_google(audio).lower()
        #        print(input)
        #    except Exception as e:
        #        pass
        #    return input
        return input("input: ").lower()

    @staticmethod
    def init(memory):
        for name in memory.searchMemory("assistantNames"):
            rate = memory.searchMemory('{}SpeechRate'.format(name))
            volume = memory.searchMemory('{}Volume'.format(name))
            voice = memory.searchMemory('{}Voice'.format(name))
            wakeWords = memory.searchMemory('{}WakeWords'.format(name))
            SmartAssistant(name, rate, volume, voice, wakeWords)
        SmartAssistant.setCurrentAssistant(memory.searchMemory("defaultAssistant"))

    @staticmethod
    def getName():
        return "Smart Assistant"
