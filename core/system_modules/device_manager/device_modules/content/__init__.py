"""
Content Module Manager

Part of WebDisplay
Device Content Module

License: MIT license

Author: C2311231

Notes:
"""

import core.module as device_module
import core.system as system
from core.system_modules.device_manager.device_modules.content.content.content import Content
from core.system_modules.database.base_setting import SettingBase

class ContentManager(device_module.module):
    def __init__(self, device_module: device_module.module, system: system.system):
        self.device_module = device_module
        self.system = system
        self.content: list[Content] = []
        self.content_types: dict[str, type[Content]] = {}
        
    def get_all_content(self) -> list[Content]:
        return self.content
    
    def register_content(self, content: Content) -> None:
        self.content.append(content)
        
    def register_content_type(self, name: str, content_type: type[Content]) -> None:
        if name in self.content_types:
            raise ValueError(f"Content type {name} is already registered.")
        
        if not issubclass(content_type, Content):
            raise ValueError(f"Content type {name} must be a subclass of Content.")
        
        self.content_types[name] = content_type
    
    
def register(system, device):
    return "content_manager", ContentManager(device, system)