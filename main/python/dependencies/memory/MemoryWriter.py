import io
import os
from main.python.assistant import Constants

class MemoryWriter:

    def __init__(self, memoryFile):
        self.memoryFile = memoryFile

    def addToMemory(self, key, values):
        valString = MemoryWriter.extractValueString(values)
        needsNewLine = False
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with io.open(self.memoryFile, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            if "\n" not in lines[len(lines) - 1]:
                needsNewLine = True
        with io.open(self.memoryFile, 'a+', encoding='utf-8') as file:
            if needsNewLine:
                file.write("\n")
            file.write('${}$\t\t%{}%'.format(key, valString))

    def appendToSection(self, key, values, sectionName):
        valString = MemoryWriter.extractValueString(values)
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with io.open(self.memoryFile, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            atSection = False
            for i in lines:
                if not atSection:
                    file.write(i)
                    if "//" in i and sectionName in i:
                        atSection = True
                elif "//" in i:
                    file.write('${}$\t\t%{}%\n'.format(key, valString))
                    file.write(i)
                    atSection = False
                else:
                    file.write(i)

    def deleteFromMemory(self, key):
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with open(self.memoryFile, 'r+') as file:
            lines = file.readlines()
            file.seek(0)
            for i in lines:
                if '${}$'.format(key) not in i:
                    file.write(i)
            file.truncate()

    def changeValue(self, key, values):
        valString = MemoryWriter.extractValueString(values)
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with io.open(self.memoryFile, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            for i in lines:
                if '${}$'.format(key) not in i:
                    file.write(i)
                else:
                    file.write('${}$\t\t%{}%\n'.format(key, valString))

    @staticmethod
    def extractValueString(values):
        string = ""
        try:
            values.lower()
            string = str(values)
        except:
            if "[" not in str(values):
                string = str(values)
            else:
                string = str(values[0])
                for v in values:
                    if v not in string:
                        string += ',{}'.format(v)
        return string