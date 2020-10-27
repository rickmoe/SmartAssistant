import os
from main.python.assistant import Constants

class MemoryParser:

    def __init__(self, memoryFile):
        self.memory = {}
        self.parseData(memoryFile)

    def parseData(self, memoryFile):
        data = []
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with open(memoryFile, 'r') as file:
            data = file.read()
            separatedData = data.split("\n")
            while len(separatedData) > 0:
                if "//" not in separatedData[0] and separatedData[0] is not "":
                    if "," in separatedData[0]:
                        self.memory[separatedData[0].split("$")[1].split("$")[0]] = \
                            separatedData[0].split("%")[1].split("%")[0].split(",")
                    else:
                        self.memory[separatedData[0].split("$")[1].split("$")[0]] = \
                            separatedData[0].split("%")[1].split("%")[0]
                del separatedData[0]

    def searchMemory(self, string):
        return self.memory[string]