"""
Database Module Setting Class

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
- Database storing implementation of SettingBase class.
"""

from src.system import system
from src.system_modules.database.dbsetting import dbSetting
from src.system_modules.database import base_setting
from sqlalchemy.orm import DeclarativeBase

class Setting(base_setting.SettingBase):
    # Device settings will be stored with domain of "device.<device_id>...."
    def __init__(self, database_manager, domain: str, version: str, setting_name: str, default_value: str, value_type: str, description: str, validation_data: dict, user_facing: bool):
        self.domain = domain
        self.version = version
        self.database_manager = database_manager
        super().__init__(setting_name, default_value, value_type, description, validation_data, user_facing=user_facing)
        self.db_setting = self.database_manager.get_session().query(dbSetting).filter_by(setting_name=self.setting_name).first()
        
        ## TODO Add migration capabilities later
        
    def get_value(self) -> str | bool | int | dict | float | None:
        if self.db_setting:
            self.value = self.db_setting.value
        
        return super().get_value()
               
    def set_value(self, value: str) -> None:
        if self.db_setting is None:
            self.db_setting = dbSetting(domain=self.domain, setting_name=self.setting_name, value=value, version=self.version) # type: ignore
            self.database_manager.get_session().add(self.db_setting)
        else:
            self.db_setting.value = value
        self.database_manager.get_session().commit()
        
    def push_to_db(self):
        if self.db_setting is None:
            self.db_setting = dbSetting(domain=self.domain, setting_name=self.setting_name, value=self.default_value, version=self.version) # type: ignore
            self.database_manager.get_session().add(self.db_setting)

        return self