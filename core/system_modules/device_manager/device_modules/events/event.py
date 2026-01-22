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
import core.system_modules.device_manager.device_modules.content.content.content as content
import core.system_modules.device_manager.device_modules.events.criteria.criterion as criteria
from datetime import datetime

class Event:
    def __init__(self, system: system.system, device: device.Device, name: str, screen: screen.Screen, content: content.Content, priority: int, criteria: list[criteria.Criterion]):
        self.system = system
        self.device = device
        self.name = name
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
        
    def trigger(self, manual_overide: bool = False) -> None:
        self.last_occurence = datetime.now()
        self.overide = manual_overide
        self.itterations += 1
        self.context = self.content.start_content(self.screen)
        
    def stop(self) -> None:
        self.content.stop_display(self.context)
        self.overide = False
        
    def evaluate_criteria(self) -> bool:
        for criterion in self.criteria:
            if not criterion.evaluate():
                return False
        return True