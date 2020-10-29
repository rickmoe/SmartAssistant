from main.python.dependencies.Dependency import Dependency
from main.python.dependencies.memory.MemoryParser import MemoryParser
from main.python.dependencies.memory.MemoryWriter import MemoryWriter

class Memory(Dependency):

    def __init__(self, memoryFile):
        self.memoryFile = memoryFile
        self.updateMemory()
        self.memory = {}

    def updateMemory(self):
        self.memory = MemoryParser(self.memoryFile).parseData()

    def addToMemory(self, key, values):
        MemoryWriter(self.memoryFile).addToMemory(key, values)

    def deleteFromMemory(self, key):
        MemoryWriter(self.memoryFile).deleteFromMemory(key)

    def changeInMemory(self, key, values):
        MemoryWriter(self.memoryFile).changeValue(key, values)

    def appendToMemorySection(self, key, values, sectionName):
        MemoryWriter(self.memoryFile).appendToSection(key, values, sectionName)

    def searchMemory(self, string):
        self.updateMemory()
        return self.memory[string]
