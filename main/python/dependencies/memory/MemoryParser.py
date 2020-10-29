import os
from main.python.assistant import Constants

class MemoryParser:

    def __init__(self, memoryFile):
        self.memoryFile = memoryFile

    def parseData(self):
        memory = {}
        os.chdir(Constants.RESOURCE_DIRECTORY + "\\memory")
        with open(self.memoryFile, 'r') as file:
            data = file.read()
            separatedData = data.split("\n")
            while len(separatedData) > 0:
                if "//" not in separatedData[0] and separatedData[0] is not "":
                    if "[" in separatedData[0]:         #List
                        memory[separatedData[0].split("$")[1].split("$")[0]] = \
                            separatedData[0].split("[")[1].split("]")[0].split(",")
                    elif "{" in separatedData[0]:       #Set
                        dataSet = set()
                        dataSet.update(separatedData[0].split("{")[1].split("}")[0].split(","))
                        memory[separatedData[0].split("$")[1].split("$")[0]] = dataSet
                    elif "%" in separatedData[0]:       #String
                        memory[separatedData[0].split("$")[1].split("$")[0]] = \
                            str(separatedData[0].split("%")[1].split("%")[0])
                    elif "#" in separatedData[0]:       #Num
                        num = str(separatedData[0].split("#")[1].split("#")[0])
                        if "." in num:
                            num = float(num)
                        else:
                            num = int(num)
                        memory[separatedData[0].split("$")[1].split("$")[0]] = num
                del separatedData[0]
        return memory
