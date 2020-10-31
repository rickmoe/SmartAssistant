import pyttsx3 as pyTTS
import speech_recognition as sr
from main.python.dependencies.Dependency import Dependency
from main.python.assistant import Constants

class SmartAssistant(Dependency):

    assistants = {}
    currentAssistant = None
    memory = None

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
    def setDefaultAssistant(memory, assistantName):
        memory.changeInMemory("defaultAssistant", assistantName.title())

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
        for assistName in SmartAssistant.getAssistants():
            assistList.append(assistName)
        memory.changeInMemory("assistantNames", assistList)
        memory.deleteFromMemory('{}SpeechRate'.format(name))
        memory.deleteFromMemory('{}Volume'.format(name))
        memory.deleteFromMemory('{}Voice'.format(name))
        memory.deleteFromMemory('{}WakeWords'.format(name))

    def getAssistantName(self):
        return self.name

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
        SmartAssistant.dependencyKeyWords = {'assistant'}
        SmartAssistant.keyWordList = [['default'],
                                      ['set', 'switch'],
                                      ['add', 'create', 'make'],
                                      ['delete', 'get rid of']]
        SmartAssistant.keyWordMethods = [SmartAssistant.respondSetDefault,
                                         SmartAssistant.respondSetAssistant,
                                         SmartAssistant.respondAddAssistant,
                                         SmartAssistant.respondDelAssistant]
        for name in memory.searchMemory("assistantNames"):
            rate = memory.searchMemory('{}SpeechRate'.format(name))
            volume = memory.searchMemory('{}Volume'.format(name))
            voice = memory.searchMemory('{}Voice'.format(name))
            wakeWords = memory.searchMemory('{}WakeWords'.format(name))
            SmartAssistant(name, rate, volume, voice, wakeWords)
        SmartAssistant.setCurrentAssistant(memory.searchMemory("defaultAssistant"))
        SmartAssistant.memory = memory

    @staticmethod
    def getName():
        return "Smart Assistant"

    @staticmethod
    def respondSetDefault(input, assistant):
        assistantName = input.split(" to ")[1]
        try:
            SmartAssistant.setCurrentAssistant(assistantName)
            SmartAssistant.setDefaultAssistant(SmartAssistant.memory, assistantName)
            assistant.say('{} is now your default assistant.'.format(assistantName))
            SmartAssistant.setCurrentAssistant(assistant.getAssistantName())
        except:
            assistant.say('i couldn\'t find an assistant named {}'.format(assistantName))

    @staticmethod
    def respondSetAssistant(input, assistant):
        assistantName = input.split(" to ")[1]
        try:
            SmartAssistant.setCurrentAssistant(assistantName)
            assistant.say("ok. goodbye.")
            SmartAssistant.getCurrentAssistant().say("hello, i'm {}.".format(assistantName))
        except:
            assistant.say('i couldn\'t find an assistant named {}'.format(assistantName))

    @staticmethod
    def respondAddAssistant(input, assistant):
        name = promptAssistantNameAdd(input, assistant)
        assistant.say("on a scale from 0 to 10, how fast do you want them to talk?")
        speechRate = max(0, min(10, promptNum(assistant.getAudio(), assistant)))
        speechRate = int(convertRange(speechRate, 0, 10, Constants.ASSISTANT_MIN_SPEECH_RATE, Constants.ASSISTANT_MAX_SPEECH_RATE))
        assistant.say("on a scale from 0 to 10, how loud do you want them to be?")
        volume = max(0, min(10, promptNum(assistant.getAudio(), assistant)))
        volume = convertRange(volume, 0, 10, Constants.ASSISTANT_MIN_VOLUME, Constants.ASSISTANT_MAX_VOLUME)
        assistant.say("do you want them to have a male or female voice? say 0 for male and 1 for female.")
        voice = max(0, min(1, promptNum(assistant.getAudio(), assistant)))
        SmartAssistant.createAssistant(SmartAssistant.memory, name, speechRate, volume, voice)
        assistant.say('done! say hello {}.'.format(name))
        SmartAssistant.getAssistants()[name].say('hello, i am {}, your personal assistant.'.format(name))

    @staticmethod
    def respondDelAssistant(input, assistant):
        name = promptAssistantNameDel(input, assistant)
        try:
            SmartAssistant.delAssistant(SmartAssistant.memory, name)
            assistant.say('successfully deleted {}'.format(name))
        except:
            assistant.say('could not find an assistant named {}'.format(name))

def promptAssistantNameAdd(input, assistant):
    while getName(input) is "":
        assistant.say("what would you like to name them?")
        return assistant.getAudio().title()
    return getName(input)

def promptAssistantNameDel(input, assistant):
    while getName(input) is "":
        assistant.say("what's their name?")
        return assistant.getAudio().title()
    return getName(input)

def getName(userInput):
    if " called " in userInput:
        return userInput.split("called ")[1].split()[0].title()
    elif " named " in userInput:
        return userInput.split("named ")[1].split()[0].title()
    return ""

def convertRange(val, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    return (val - min1) * range2 / range1 + min2

def promptNum(input, assistant):
    while True:
        try:
            speechRate = int(input)
            return speechRate
        except:
            assistant.say("please state a valid number")
            input = assistant.getAudio()
