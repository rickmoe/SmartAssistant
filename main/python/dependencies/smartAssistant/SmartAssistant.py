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
    def setCurrentAssistant(assistant):
        SmartAssistant.currentAssistant = assistant

    @staticmethod
    def getCurrentAssistant():
        return SmartAssistant.currentAssistant

    @staticmethod
    def getAssistants():
        return SmartAssistant.assistants

    def delAssistant(self):
        SmartAssistant.assistants.pop(self.name)
        del self

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
        #r = sr.Recognizer()
        #with sr.Microphone() as source:
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
    def init(memoryParser):
        for name in memoryParser.searchMemory("assistantNames"):
            rate = memoryParser.searchMemory('{}SpeechRate'.format(name))
            volume = memoryParser.searchMemory('{}Volume'.format(name))
            voice = memoryParser.searchMemory('{}Voice'.format(name))
            wakeWords = memoryParser.searchMemory('{}WakeWords'.format(name))
            SmartAssistant(name, rate, volume, voice, wakeWords)
        SmartAssistant.setCurrentAssistant(SmartAssistant.assistants[memoryParser.searchMemory("defaultAssistant")])

    @staticmethod
    def getName():
        return "Smart Assistant"
