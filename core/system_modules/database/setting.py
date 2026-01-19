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
from sqlalchemy.orm import DeclarativeBase
import json

class Setting(base_setting.SettingBase):
    # Device settings will be stored with domain of "device.<device_id>...."
    def __init__(self, database_manager, domain: str, version: str, setting_name: str, default_value: str, value_type: str, description: str, validation_data: dict, user_facing: bool):
        self.domain = domain
        self.version = version
        self.database_manager = database_manager
        super().__init__(setting_name, default_value, value_type, description, validation_data, user_facing=user_facing)
        self.db_setting = self.database_manager.get_session().query(dbSetting).filter_by(setting_name=self.setting_name).first()
        
        ## TODO Add migration capabilities later
        
    def get_value(self) -> str | bool | int | float | None:
        if self.db_setting:
            try:
                self.validate(self.db_setting.value)
                return self.get_correct_type(self.db_setting.value)
            except ValueError:
                pass
        
        try:
            self.validate(self.default_value)
            return self.get_correct_type(self.default_value)
        except ValueError:
            return None
        
    def get_correct_type(self, data) -> str | bool | int | float | None:
        if self.type in ["string", "ip", "json", "enum"]:
            return self.db_setting.value
    
        elif self.type == "bool":
            return bool(data)
        
        elif self.type == "int":
            return int(data)
        
        elif self.type == "float":
            return float(data)
    
        else:
            return None
        
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
            
            
    def validate(self, data: str | None):
        if data == None:
            raise ValueError("Data must not be None")
        
        data = data.strip(data)
        
        if self.type not in ["string", "int", "bool", "float", "ip", "json", "enum"]:
            raise ValueError(f"Invalid Type: {self.type}")
        
        if self.type == "string":
            if self.validation_data["max_length"] < len(data):
                raise ValueError("Exceeds max string length")
            
            elif self.validation_data["min_length"] > len(data):
                raise ValueError("Below minimum string length")
            
        elif self.type == "int":
            if not data.lstrip("+-").isdigit():
                raise ValueError("Data must be an Integer")
            
            elif self.validation_data["max_value"] < int(data):
                raise ValueError("Integer too large")
        
            elif self.validation_data["min_value"] > int(data):
                raise ValueError("Integer too small")
            
        elif self.type == "bool":
            if not data.lower() in ["true", "false"]:
                raise ValueError("Data must be a boolean")
            
        elif self.type == "float":
            if not data.lstrip("+-").replace(".", "").isdigit():
                raise ValueError("Data must be a float")
            
            elif self.validation_data["max_value"] < float(data):
                raise ValueError("Float too large")
        
            elif self.validation_data["min_value"] > float(data):
                raise ValueError("Float too small")
            
        elif self.type == "ip":
            number_pairs = data.split(".")
            
            if len(number_pairs) != 4:
                raise ValueError("Data must be a valid ip")
            
            for i in number_pairs:
                if not i.isdigit():
                    raise ValueError("IP must only contain . and digits")
                
                if 0 > int(i) or int(i) > 255:
                    raise ValueError("IP sections must be between 0 and 255")
                
        elif self.type == "json":
            try:
                json.loads(data)
            except json.JSONDecodeError:
                raise ValueError("Data is not valid json")
            
        elif self.type == "enum":
            if data not in self.validation_data["options"]:
                raise ValueError(f"Invalid option {data}")