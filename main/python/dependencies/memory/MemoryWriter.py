import io
import os
from main.python.assistant import Constants

class MemoryWriter:

    def __init__(self, memoryFile):
        self.memoryFile = memoryFile

    def addToMemory(self, key, values):
        needsNewLine = False
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with io.open(self.memoryFile, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            if "\n" not in lines[len(lines) - 1]:
                needsNewLine = True
        with io.open(self.memoryFile, 'a+', encoding='utf-8') as file:
            MemoryWriter.writeToFile(file, key, values, newLineBefore=needsNewLine)

    def appendToSection(self, key, values, sectionName):
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
                    MemoryWriter.writeToFile(file, key, values)
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
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with io.open(self.memoryFile, 'r+', encoding='utf-8') as file:
            lines = file.readlines()
            file.seek(0)
            for i in lines:
                if '${}$'.format(key) not in i:
                    file.write(i)
                else:
                    MemoryWriter.writeToFile(file, key, values)

    @staticmethod
    def extractValueString(values):
        try:
            values.lower()                          #String
            string = str(values)
            valType = "%%"
        except:
            if "[" in str(values):                  #List
                string = ",".join(values).replace("'", "")
                valType = "[]"
            elif type(values) is set:               #Set
                string = ",".join(values).replace("'", "")
                valType = "{}"
            else:                                   #Num
                string = str(values)
                valType = "##"
        return string, valType

    @staticmethod
    def writeToFile(file, key, values, newLineBefore=False, newLineAfter=True):
        valString, valType = MemoryWriter.extractValueString(values)
        file.write('{}${}$\t\t{}{}{}{}'.format("\n" if newLineBefore else "", key, valType[:1], valString, valType[1:], "\n" if newLineAfter else ""))
