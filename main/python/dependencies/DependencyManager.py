from main.python.dependencies.ActiveDependencies import ActiveDependencies
from main.python.assistant import Constants

class DependencyManager:

    @staticmethod
    def initDependencies():
        for dependency in ActiveDependencies:
            dependency.value.init(DependencyManager.getDependency('memory')(Constants.MEMORY_FILE))

    @staticmethod
    def concludeDependencies():
        for dependency in ActiveDependencies:
            dependency.value.conclude(DependencyManager.getDependency('memory')(Constants.MEMORY_FILE))

    @staticmethod
    def getDependency(dependency):
        for d in ActiveDependencies:
            if str(dependency).upper() == d.name:
                return d.value
        return None
