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

class EventManager(core.module.module):
    def __init__(self, system: core.system.system, device: device.Device):
        self.system = system
        self.device = device
        self.events: list[event.Event] = []
        
    def register_event(self, name: str, handler, content: content.Content, priority: int, criteria) -> None:
        self.events.append(event.Event(self.system, self.device, name, handler, content, priority, criteria))



def register(system: core.system.system, device: device.Device) -> tuple[str, core.module.module]:
    return "event_manager", EventManager(system, device)