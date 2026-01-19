"""
Database Setting Base Class

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
- Base class for database settings
- Provides methods for serialization, deserialization, and validation
"""

from core.system import system
from core.system_modules.database.dbsetting import dbSetting


class SettingBase():
    # Device settings will be stored with domain of "device.<device_id>...."
    def __init__(self, setting_name: str, default_value: str | None, value_type: str, description: str, validation_data: dict, user_facing: bool):
        self.setting_name = setting_name
        self.default_value = default_value
        self.type = value_type
        self.description = description
        self.validation_data = validation_data
        self.user_facing = user_facing
        
        ## TODO Add migration and validation capabilities later

    def get_value(self) -> str | bool | int | float | None:
        if self.db_setting is None:
            return self.default_value
        return self.db_setting.value
    
    def set_value(self, value: str) -> None:
        if self.db_setting is None:
            self.db_setting = dbSetting(domain=self.domain, setting_name=self.setting_name, value=value, version=self.version) # type: ignore
        else:
            self.db_setting.value = value
            
    ## TODO Add validation, serialization, and deserialization methods later