class Dependency:

    dependencyKeyWords = set()
    keyWordList = [[]]
    keyWordMethods = []

    @staticmethod
    def init(memory):
        pass

    @staticmethod
    def conclude(memory):
        pass

    @staticmethod
    def getName():
        pass

    @classmethod
    def parseInput(cls, input, assistant):
        for i in range(len(cls.keyWordList)):
            if any(key in input for key in cls.keyWordList[i]):
                cls.keyWordMethods[i](input, assistant)
                return True
        return False

    @classmethod
    def getDependencyKeyWords(cls):
        return cls.dependencyKeyWords
