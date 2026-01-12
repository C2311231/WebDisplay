"""
Events Module Event Class

Part of WebDisplay
Device Events Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system as system
import core.system_modules.device_manager.device as device
import core.system_modules.device_manager.device_modules.screens.screen as screen
import core.system_modules.device_manager.device_modules.content.content as content
from datetime import datetime

# TODO Turn Criteria into its own class for better structure and validation
# TODO Use Criteria classes to dynamicaly generate ui and serialize/deserialize criteria

class Event:
    def __init__(self, system: system.system, device: device.Device, screen: screen.Screen, content: content.Content, priority: int, criteria: dict):
        self.system = system
        self.device = device
        self.screen = screen
        self.content = content
        self.priority = priority
        self.criteria = criteria
        self.last_occurence = None
        self.overide = False
        self.itterations = 0
        self.enabled = True
        
    def is_active(self) -> bool:
        return self.evaluate_criteria() or self.overide
        
    def is_enabled(self) -> bool:
        return self.enabled
    
    def is_overide(self) -> bool:
        return self.overide
    
    def enable(self) -> None:
        self.enabled = True
        
    def disable(self) -> None:
        self.enabled = False
        
    def trigger(self, manual_overide: bool) -> None:
        self.last_occurence = datetime.now()
        self.overide = manual_overide
        self.itterations += 1
        self.content.start_content(self.screen)
        
    def stop(self) -> None:
        self.content.stop_display()
        self.overide = False
        
    def evaluate_criteria(self, criteria = None) -> bool:
        if criteria is None:
            criteria = self.criteria
        now = datetime.now()
        for criterion, value in criteria.items():
            if criterion == "always":
                return True

            elif criterion == "date_range":
                start_date = datetime.strptime(value["start_date"], "%Y-%m-%d")
                end_date = datetime.strptime(value["end_date"], "%Y-%m-%d")
                if not (start_date <= now <= end_date):
                    return False
                
            elif criterion == "time_range":
                start_time = datetime.strptime(value["start_time"], "%H:%M").time()
                end_time = datetime.strptime(value["end_time"], "%H:%M").time()
                current_time = now.time()
                if not (start_time <= current_time <= end_time):
                    return False
                
            elif criterion == "days_of_week":
                current_day = now.strftime("%A")
                if current_day not in value:
                    return False
                
            elif criterion == "before_time":
                before_time = datetime.strptime(value, "%H:%M").time()
                current_time = now.time()
                if not (current_time < before_time):
                    return False
                
            elif criterion == "after_time":
                after_time = datetime.strptime(value, "%H:%M").time()
                current_time = now.time()
                if not (current_time > after_time):
                    return False
                
            elif criterion == "before_date":
                before_date = datetime.strptime(value, "%Y-%m-%d")
                if not (now < before_date):
                    return False
                
            elif criterion == "after_date":
                after_date = datetime.strptime(value, "%Y-%m-%d")
                if not (now > after_date):
                    return False
                
            elif criterion == "before_weekday":
                weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                current_weekday = now.weekday()
                target_weekday = weekdays.index(value)
                if not (current_weekday < target_weekday):
                    return False
                
            elif criterion == "after_weekday":
                weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                current_weekday = now.weekday()
                target_weekday = weekdays.index(value)
                if not (current_weekday > target_weekday):
                    return False
                
            elif criterion == "durring_weekday":
                weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                current_weekday = now.weekday()
                target_weekday = weekdays.index(value)
                if not (current_weekday == target_weekday):
                    return False
                
            elif criterion == "durring_month":
                current_month = now.month
                if not (current_month == value):
                    return False
                
            elif criterion == "durring_date":
                current_date = now.day
                if not (current_date == value):
                    return False
                
            elif criterion == "durring_day":
                current_day = now.day
                if not (current_day == value):
                    return False

            elif criterion == "before_month":
                current_month = now.month
                if not (current_month < value):
                    return False
                
            elif criterion == "after_month":
                current_month = now.month
                if not (current_month > value):
                    return False
                
            elif criterion == "after_day":
                current_day = now.day
                if not (current_day > value):
                    return False
                
            elif criterion == "before_day":
                current_day = now.day
                if not (current_day < value):
                    return False
                
            elif criterion == "device_active":
                if self.screen.active != value:
                    return False
                
            elif criterion == "and":
                result = all(self.evaluate_criteria({criterion}) for criterion in value)
                if not result:
                    return False
                
            elif criterion == "or":
                result = any(self.evaluate_criteria({criterion}) for criterion in value)
                if not result:
                    return False
                
            elif criterion == "not":
                result = self.evaluate_criteria(value)
                if result:
                    return False
                
            elif criterion == "since_last_occurence":
                if self.last_occurence is not None:
                    delta = now - self.last_occurence
                    if delta.total_seconds() < value:
                        return False
                    
            elif criterion == "before_nth_iteration":
                if self.itterations >= value:
                    return False
                
            elif criterion == "after_nth_iteration":
                if self.itterations <= value:
                    return False
                
            elif criterion == "nth_iteration":
                if self.itterations != value:
                    return False
                
            elif criterion == "every_nth_iteration":
                if self.itterations % value != 0:
                    return False
                    
        return True