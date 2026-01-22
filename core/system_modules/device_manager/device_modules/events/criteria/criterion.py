"""
Criterion File for Event System

Part of WebDisplay
Device Event Module

License: MIT license

Author: C2311231

Notes:
"""
from __future__ import annotations
import core.system as system
import core.system_modules.device_manager.device as device
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import core.system_modules.device_manager.device_modules.events.event as event

class Criterion:
    def __init__(self, system: system.system, device: device.Device, event: "event.Event") -> None:
        self.name = "base_criterion"
        self.device = device
        self.system = system
        self.event = event

    def evaluate(self) -> bool:
        # Placeholder for criterion evaluation logic
        return False

    @classmethod
    def get_ui_schema(cls) -> dict:
        # Placeholder for UI definition of the criterion
        return {}
    
    def get_state_definition(self) -> dict:
        return {
            "name": self.name,
            "type": "base",
        }
    
class AlwaysCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", value) -> None:
        super().__init__(system, device, event)
        self.name = "Always"
        self.value = value

    def evaluate(self) -> bool:
        return self.value
    
    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "Label": "Always",
            "type": "always",
            "description": "This criterion is always the selected value. (True/False)",
            "params": {
                "value": {"value": True, "type": "boolean", "description": "The value to always return."}
            }
        }
        
    def get_state_definition(self) -> dict:
        return {"value": True}
    
    
class AllCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", criteria: list[Criterion]) -> None:
        super().__init__(system, device, event)
        self.name = "All"
        self.criteria = criteria

    def evaluate(self) -> bool:
        return all(criterion.evaluate() for criterion in self.criteria)
    
    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "all",
            "description": "All of the following criteria must be met.",
            "params": {
                "criteria": {"value": [], "type": "criteria_list", "description": "Sub-criteria to evaluate."}
            }
        }
    
    def get_state_definition(self) -> dict:
        return {
            "criteria": [criterion.get_state_definition() for criterion in self.criteria]
        }
        
class AnyCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", criteria: list[Criterion]) -> None:
        super().__init__(system, device, event)
        self.name = "Any"
        self.criteria = criteria

    def evaluate(self) -> bool:
        return any(criterion.evaluate() for criterion in self.criteria)
    
    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "any",
            "description": "At least one of the following criteria must be met.",
            "params": {
                "criteria": {"value": [], "type": "criteria_list", "description": "Sub-criteria to evaluate."}
            }
        }
        
    def get_state_definition(self) -> dict:
        return {
            "criteria": [criterion.get_state_definition() for criterion in self.criteria]
        }
        
class NotCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", criterion: Criterion) -> None:
        super().__init__(system, device, event)
        self.name = "Not"
        self.criterion = criterion

    def evaluate(self) -> bool:
        return not self.criterion.evaluate()
    
    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "not",
            "description": "The following criterion must NOT be met.",
            "params": {
                "criterion": {"value": None, "type": "criterion", "description": "Sub-criterion to evaluate."}
            }
        }
        
    def get_state_definition(self) -> dict:
        return {
            "criterion": self.criterion.get_state_definition()
        }
        
class DateRangeCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", start_date: str, end_date: str) -> None:
        super().__init__(system, device, event)
        self.name = "Date Range"
        self.start_date = start_date
        self.end_date = end_date

    def evaluate(self) -> bool:
        now = datetime.now()
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d")
        return start_date <= now <= end_date

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "date_range",
            "description": "The event is active during a specific date range.",
            "params": {
                "start_date": {"value": "", "type": "date", "description": "The start date of the range (YYYY-MM-DD)."},
                "end_date": {"value": "", "type": "date", "description": "The end date of the range (YYYY-MM-DD)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        
class TimeRangeCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", start_time: str, end_time: str) -> None:
        super().__init__(system, device, event)
        self.name = "Time Range"
        self.start_time = start_time
        self.end_time = end_time

    def evaluate(self) -> bool:
        now = datetime.now().time()
        start_time = datetime.strptime(self.start_time, "%H:%M").time()
        end_time = datetime.strptime(self.end_time, "%H:%M").time()
        return start_time <= now <= end_time

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "time_range",
            "description": "The event is active during a specific time range each day.",
            "params": {
                "start_time": {"value": "", "type": "time", "description": "The start time of the range (HH:MM)."},
                "end_time": {"value": "", "type": "time", "description": "The end time of the range (HH:MM)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "start_time": self.start_time,
            "end_time": self.end_time
        }
        
class DayOfWeekCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", day: str) -> None:
        super().__init__(system, device, event)
        self.name = "Days of Week"
        self.day = day

    def evaluate(self) -> bool:
        now = datetime.now()
        current_day = now.strftime("%A")
        return current_day == self.day

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "days_of_week",
            "description": "The event is active on a specific day of the week.",
            "params": {
                "day": {"value": [], "type": "enum", "options": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                        "description": "The day of the week when the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "day": self.day
        }
        
class BeforeTimeCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", before_time: str) -> None:
        super().__init__(system, device, event)
        self.name = "Before Time"
        self.before_time = before_time

    def evaluate(self) -> bool:
        now = datetime.now().time()
        before_time = datetime.strptime(self.before_time, "%H:%M").time()
        return now < before_time

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "before_time",
            "description": "The event is active before a specific time each day.",
            "params": {
                "before_time": {"value": "", "type": "time", "description": "The time before which the event is active (HH:MM)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "before_time": self.before_time
        }
        
class AfterTimeCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", after_time: str) -> None:
        super().__init__(system, device, event)
        self.name = "After Time"
        self.after_time = after_time

    def evaluate(self) -> bool:
        now = datetime.now().time()
        after_time = datetime.strptime(self.after_time, "%H:%M").time()
        return now > after_time

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "after_time",
            "description": "The event is active after a specific time each day.",
            "params": {
                "after_time": {"value": "", "type": "time", "description": "The time after which the event is active (HH:MM)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "after_time": self.after_time
        }
        
class ScreenActiveCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event") -> None:
        super().__init__(system, device, event)
        self.name = "Screen Active"

    def evaluate(self) -> bool:
        screen = self.event.screen
        if screen:
            return screen.active
        return False

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "screen_active",
            "description": "The event is active when the associated screen is already active.",
            "params": {}
        }

    def get_state_definition(self) -> dict:
        return {}
    
class BeforeDateCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", before_date: str) -> None:
        super().__init__(system, device, event)
        self.name = "Before Date"
        self.before_date = before_date

    def evaluate(self) -> bool:
        now = datetime.now()
        before_date = datetime.strptime(self.before_date, "%Y-%m-%d")
        return now < before_date

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "before_date",
            "description": "The event is active before a specific date.",
            "params": {
                "before_date": {"value": "", "type": "date", "description": "The date before which the event is active (YYYY-MM-DD)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "before_date": self.before_date
        }
        
class AfterDateCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", after_date: str) -> None:
        super().__init__(system, device, event)
        self.name = "After Date"
        self.after_date = after_date

    def evaluate(self) -> bool:
        now = datetime.now()
        after_date = datetime.strptime(self.after_date, "%Y-%m-%d")
        return now > after_date

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "after_date",
            "description": "The event is active after a specific date.",
            "params": {
                "after_date": {"value": "", "type": "date", "description": "The date after which the event is active (YYYY-MM-DD)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "after_date": self.after_date
        }
        
class BeforeWeekdayCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", before_weekday: int) -> None:
        super().__init__(system, device, event)
        self.name = "Before Weekday"
        self.before_weekday = before_weekday

    def evaluate(self) -> bool:
        now = datetime.now()
        current_weekday = now.weekday()  # Monday is 0 and Sunday is 6
        return current_weekday < self.before_weekday

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "before_weekday",
            "description": "The event is active before a specific day of the week.",
            "params": {
                "before_weekday": {"value": None, "type": "enum", "options": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                   "description": "The day of the week before which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "before_weekday": self.before_weekday
        }
        
class AfterWeekdayCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", after_weekday: int) -> None:
        super().__init__(system, device, event)
        self.name = "After Weekday"
        self.after_weekday = after_weekday

    def evaluate(self) -> bool:
        now = datetime.now()
        current_weekday = now.weekday()  # Monday is 0 and Sunday is 6
        return current_weekday > self.after_weekday

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "after_weekday",
            "description": "The event is active after a specific day of the week.",
            "params": {
                "after_weekday": {"value": None, "type": "enum", "options": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                  "description": "The day of the week after which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "after_weekday": self.after_weekday
        }
        
class DurringWeekdayCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", weekday: int) -> None:
        super().__init__(system, device, event)
        self.name = "Durring Weekday"
        self.weekday = weekday

    def evaluate(self) -> bool:
        now = datetime.now()
        current_weekday = now.weekday()  # Monday is 0 and Sunday is 6
        return current_weekday == self.weekday

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "durring_weekday",
            "description": "The event is active on a specific day of the week.",
            "params": {
                "weekday": {"value": None, "type": "enum", "options": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                            "description": "The day of the week when the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "weekday": self.weekday
        }
        
class DurringMonthCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", month: int) -> None:
        super().__init__(system, device, event)
        self.name = "Durring Month"
        self.month = month

    def evaluate(self) -> bool:
        now = datetime.now()
        current_month = now.month
        return current_month == self.month

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "durring_month",
            "description": "The event is active during a specific month.",
            "params": {
                "month": {"value": None, "type": "enum", "options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 
                          "description": "The month when the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "month": self.month
        }
        
class DurringDateCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", date: int) -> None:
        super().__init__(system, device, event)
        self.name = "Durring Date"
        self.date = date

    def evaluate(self) -> bool:
        now = datetime.now()
        current_day = now.day
        return current_day == self.date

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "durring_date",
            "description": "The event is active on a specific date of the month.",
            "params": {
                "date": {"value": 1, "type": "integer", "description": "The date of the month when the event is active (1-31)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "date": self.date
        }

class DurringDayCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", day: int) -> None:
        super().__init__(system, device, event)
        self.name = "Durring Day"
        self.day = day

    def evaluate(self) -> bool:
        now = datetime.now()
        current_day = now.day
        return current_day == self.day

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "durring_day",
            "description": "The event is active on a specific day of the month.",
            "params": {
                "day": {"value": 1, "type": "integer", "description": "The day of the month when the event is active (1-31)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "day": self.day
        }
        
class BeforeMonthCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", before_month: int) -> None:
        super().__init__(system, device, event)
        self.name = "Before Month"
        self.before_month = before_month

    def evaluate(self) -> bool:
        now = datetime.now()
        current_month = now.month
        return current_month < self.before_month

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "before_month",
            "description": "The event is active before a specific month.",
            "params": {
                "before_month": {"value": None, "type": "enum", "options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 
                                 "description": "The month before which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "before_month": self.before_month
        }
        
class AfterMonthCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", after_month: int) -> None:
        super().__init__(system, device, event)
        self.name = "After Month"
        self.after_month = after_month

    def evaluate(self) -> bool:
        now = datetime.now()
        current_month = now.month
        return current_month > self.after_month

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "after_month",
            "description": "The event is active after a specific month.",
            "params": {
                "after_month": {"value": None, "type": "enum", "options": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 
                                 "description": "The month after which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "after_month": self.after_month
        }
        
class AfterDayCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", after_day: int) -> None:
        super().__init__(system, device, event)
        self.name = "After Day"
        self.after_day = after_day

    def evaluate(self) -> bool:
        now = datetime.now()
        current_day = now.day
        return current_day > self.after_day

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "after_day",
            "description": "The event is active after a specific day of the month.",
            "params": {
                "after_day": {"value": 1, "type": "integer", "description": "The day of the month after which the event is active (1-31)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "after_day": self.after_day
        }
        
class BeforeDayCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", before_day: int) -> None:
        super().__init__(system, device, event)
        self.name = "Before Day"
        self.before_day = before_day

    def evaluate(self) -> bool:
        now = datetime.now()
        current_day = now.day
        return current_day < self.before_day

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "before_day",
            "description": "The event is active before a specific day of the month.",
            "params": {
                "before_day": {"value": 1, "type": "integer", "description": "The day of the month before which the event is active (1-31)."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "before_day": self.before_day
        }
        
class SinceLastOccurenceCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", since_seconds: int) -> None:
        super().__init__(system, device, event)
        self.name = "Since Last Occurence"
        self.since_seconds = since_seconds

    def evaluate(self) -> bool:
        if self.event.last_occurence is not None:
            now = datetime.now()
            elapsed = (now - self.event.last_occurence).total_seconds()
            return elapsed >= self.since_seconds
        return True  # If never occurred, consider it valid

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "since_last_occurence",
            "description": "The event is active if a certain amount of time has passed since its last occurrence.",
            "params": {
                "since_seconds": {"value": 0, "type": "integer", "description": "The number of seconds that must have passed since the last occurrence."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "since_seconds": self.since_seconds
        }
        
class BeforeNthIterationCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", before_nth: int) -> None:
        super().__init__(system, device, event)
        self.name = "Before Nth Iteration"
        self.before_nth = before_nth

    def evaluate(self) -> bool:
        return self.event.itterations < self.before_nth

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "before_nth_iteration",
            "description": "The event is active before it has been triggered a certain number of times.",
            "params": {
                "before_nth": {"value": 1, "type": "integer", "description": "The number of iterations before which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "before_nth": self.before_nth
        }
        
# The following three may be removed later as they may not actually be useful in practice
# (If the event is only active after n-iterations, it will never reach the nth iteration because it won't trigger)
# Only possibly useful if combined with other criteria or used with manual triggers

class AfterNthIterationCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", after_nth: int) -> None:
        super().__init__(system, device, event)
        self.name = "After Nth Iteration"
        self.after_nth = after_nth

    def evaluate(self) -> bool:
        return self.event.itterations > self.after_nth

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "after_nth_iteration",
            "description": "The event is active after it has been triggered a certain number of times.",
            "params": {
                "after_nth": {"value": 1, "type": "integer", "description": "The number of iterations after which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "after_nth": self.after_nth
        }
        
class NthIterationCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", nth: int) -> None:
        super().__init__(system, device, event)
        self.name = "Nth Iteration"
        self.nth = nth

    def evaluate(self) -> bool:
        return self.event.itterations == self.nth

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "nth_iteration",
            "description": "The event is active on its Nth iteration.",
            "params": {
                "nth": {"value": 1, "type": "integer", "description": "The iteration number on which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "nth": self.nth
        }
        
class EveryNthIterationCriterion(Criterion):
    def __init__(self, system: system.system, device: device.Device, event: "event.Event", every_nth: int) -> None:
        super().__init__(system, device, event)
        self.name = "Every Nth Iteration"
        self.every_nth = every_nth

    def evaluate(self) -> bool:
        return self.event.itterations % self.every_nth == 0

    @classmethod
    def get_ui_schema(cls) -> dict:
        return {
            "type": "every_nth_iteration",
            "description": "The event is active on every Nth iteration.",
            "params": {
                "every_nth": {"value": 1, "type": "integer", "description": "The interval of iterations on which the event is active."}
            }
        }

    def get_state_definition(self) -> dict:
        return {
            "every_nth": self.every_nth
        }

def get_all_available_criteria() -> dict[str, type[Criterion]]:
    return {
        "always": AlwaysCriterion,
        "all": AllCriterion,
        "any": AnyCriterion,
        "not": NotCriterion,
        "date_range": DateRangeCriterion,
        "time_range": TimeRangeCriterion,
        "day_of_week": DayOfWeekCriterion,
        "before_time": BeforeTimeCriterion,
        "after_time": AfterTimeCriterion,
        "screen_active": ScreenActiveCriterion,
        "before_date": BeforeDateCriterion,
        "after_date": AfterDateCriterion,
        "before_weekday": BeforeWeekdayCriterion,
        "after_weekday": AfterWeekdayCriterion,
        "durring_weekday": DurringWeekdayCriterion,
        "durring_month": DurringMonthCriterion,
        "durring_date": DurringDateCriterion,
        "durring_day": DurringDayCriterion,
        "before_month": BeforeMonthCriterion,
        "after_month": AfterMonthCriterion,
        "before_day": BeforeDayCriterion,
        "after_day": AfterDayCriterion,
        "since_last_occurence": SinceLastOccurenceCriterion,
        "before_nth_iteration": BeforeNthIterationCriterion,
        "after_nth_iteration": AfterNthIterationCriterion,
        "nth_iteration": NthIterationCriterion,
        "every_nth_iteration": EveryNthIterationCriterion
    }