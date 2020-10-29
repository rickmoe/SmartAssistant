from main.python.dependencies.DependencyManager import DependencyManager
from main.python.assistant import InputParser

DependencyManager.initDependencies()

# print(any(v in string for v in vals))
# print({v for v in vals if v in string})
# print([v for v in vals if v in string])

# DependencyManager.getDependency('timer').getName()

powered = True
while powered:
    woke = False
    userInput = DependencyManager.getDependency('smart_assistant').getCurrentAssistant().getAudio()
    if userInput is not None:
        if any(wake in userInput for wake in DependencyManager.getDependency('smart_assistant').getCurrentAssistant().getWakeWords()):
            powered = InputParser.parseInput(userInput, DependencyManager.getDependency('smart_assistant').getCurrentAssistant())

DependencyManager.concludeDependencies()