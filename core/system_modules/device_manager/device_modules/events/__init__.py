"""
Device Event Manager

Part of WebDisplay
Device Event Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system
import core.module
import core.system_modules.device_manager.device_modules.events.event as event
import core.system_modules.device_manager.device as device
import core.system_modules.device_manager.device_modules.content.content.content as content
from .criteria import criterion

class EventManager(core.module.module):
    def __init__(self, system: core.system.system, device: device.Device):
        self.system = system
        self.device = device
        self.events: list[event.Event] = []
        self.criteria = criterion.get_all_available_criteria()
        
    def register_event(self, name: str, handler, content: content.Content, priority: int, criteria) -> None:
        self.events.append(event.Event(self.system, self.device, name, handler, content, priority, criteria))
        
    def get_all_events(self) -> list[event.Event]:
        return self.events
    
    def clear_events(self) -> None:
        self.events = []
        
    def update(self, delta_time) -> None:
        for ev in self.events:
            pass
            # TODO Complete event updating and triggering logic, ensuring that only a single event is on per screen and that priority is respected.
            # Also check for overides and conditions.
            
    def register_criteria(self, name: str, handler: type[criterion.Criterion]) -> None:
        if name in self.criteria:
            raise ValueError(f"Criterion {name} is already registered.")

        if not issubclass(handler, criterion.Criterion):
            raise ValueError(f"Criterion {name} must be a subclass of Criterion.")

        self.criteria[name] = handler

    def get_registered_criteria(self) -> dict[str, type[criterion.Criterion]]:
        return self.criteria

def register(system: core.system.system, device: device.Device) -> tuple[str, core.module.module]:
    return "event_manager", EventManager(system, device)