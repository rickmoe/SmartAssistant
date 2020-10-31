from main.python.dependencies.DependencyManager import DependencyManager

def parseInput(input, assistant):
    for dependency in DependencyManager.getDependencies():
        actionTaken = False
        keywords = DependencyManager.getDependencies()[dependency].getDependencyKeyWords()
        if keywords is None or any(keyword in input for keyword in keywords):
            actionTaken = DependencyManager.getDependencies()[dependency].parseInput(input, assistant)
        if actionTaken:
            break
    else:
        assistant.say("sorry, I didn't get that")
