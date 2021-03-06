from enum import Enum
from main.python.assistant.BaseDependency import BaseDependency
from main.python.dependencies.calendar.Calendar import Calendar
from main.python.dependencies.memory.Memory import Memory
from main.python.dependencies.smartAssistant.SmartAssistant import SmartAssistant
from main.python.dependencies.timer.Timer import Timer

class ActiveDependencies(Enum):

    MEMORY = Memory
    BASE = BaseDependency
    CALENDAR = Calendar
    SMART_ASSISTANT = SmartAssistant
    TIMER = Timer
