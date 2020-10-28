from main.python.dependencies.DependencyManager import DependencyManager
from main.python.assistant import InputParser

DependencyManager.initDependencies()

powered = True
while powered:
    woke = False
    userInput = DependencyManager.getCurrentAssistant().getAudio()
    if userInput is not None:
        for wake in DependencyManager.getCurrentAssistant().getWakeWords():
            if wake in userInput:
                woke = True
    if woke:
        powered = InputParser.parseInput(userInput, DependencyManager.getCurrentAssistant())

DependencyManager.concludeDependencies()