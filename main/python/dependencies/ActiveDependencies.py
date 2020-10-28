from enum import Enum
from main.python.dependencies.calendar.Calendar import Calendar
from main.python.dependencies.smartAssistant.SmartAssistant import SmartAssistant
from main.python.dependencies.timer.Timer import Timer

class ActiveDependencies(Enum):

    CALENDAR = Calendar
    SMART_ASSISTANT = SmartAssistant
    TIMER = Timer
