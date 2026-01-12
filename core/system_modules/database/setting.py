"""
Database Module Setting Class

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
- Database storing implementation of SettingBase class.
"""
#TODO Remove code duplication from base class

from core.system import system
from core.system_modules.database.dbsetting import dbSetting
from core.system_modules.database import base_setting
from flask_sqlalchemy import SQLAlchemy

class Setting(base_setting.SettingBase):
    # Device settings will be stored with domain of "device.<device_id>...."
    def __init__(self, db: SQLAlchemy, domain: str, version: str, setting_name: str, default_value: str, value_type: str, description: str, validation_data: dict, user_facing: bool):
        self.domain = domain
        self.version = version
        self.db = db
        super().__init__(setting_name, default_value, value_type, description, validation_data, user_facing=user_facing)
        self.db_setting = self.db.query(dbSetting).filter_by(setting_name=self.setting_name).first()
        
        ## TODO Add migration and validation capabilities later
        
    def get_value(self) -> str | None:
        if self.db_setting is None:
            return self.default_value
        return self.db_setting.value
    
    def set_value(self, value: str) -> None:
        if self.db_setting is None:
            self.db_setting = dbSetting(domain=self.domain, setting_name=self.setting_name, value=value, version=self.version) # type: ignore
            self.db.add(self.db_setting)
        else:
            self.db_setting.value = value
        self.db.commit()