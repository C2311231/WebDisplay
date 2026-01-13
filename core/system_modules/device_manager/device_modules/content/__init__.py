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

# TODO Create a way to register different content types and their settings


class ContentManager(device_module.module):
    def __init__(self, device_module: device_module.module, system: system.system):
        self.device_module = device_module
        self.system = system
        self.content: list[Content] = []
        self.content_types: dict[str, list[SettingBase]] = {}
        
    def get_all_content(self) -> list[Content]:
        return self.content
    
    def register_content(self, content: Content) -> None:
        self.content.append(content)
        
    def register_content_type(self, name: str, settings: list[SettingBase]) -> None:
        self.content_types[name] = settings
    