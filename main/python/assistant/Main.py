from main.python.dependencies.DependencyManager import DependencyManager
from main.python.assistant import InputParser

DependencyManager.initDependencies()

# print(any(v in string for v in vals))
# print({v for v in vals if v in string})
# print([v for v in vals if v in string])

while DependencyManager.getDependency('base').getPowered():
    userInput = DependencyManager.getDependency('smart_assistant').getCurrentAssistant().getAudio()
    if userInput is not None and any(wake in userInput for wake in DependencyManager.getDependency('smart_assistant').getCurrentAssistant().getWakeWords()):
        InputParser.parseInput(userInput, DependencyManager.getDependency('smart_assistant').getCurrentAssistant())

DependencyManager.concludeDependencies()