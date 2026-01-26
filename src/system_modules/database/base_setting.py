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

from src.system import system
import json

class SettingBase():
    # Device settings will be stored with domain of "device.<device_id>...."
    def __init__(self, setting_name: str, default_value: str | None, value_type: str, description: str, validation_data: dict, user_facing: bool):
        self.setting_name = setting_name
        self.default_value = default_value
        self.type = value_type
        self.description = description
        self.validation_data = validation_data
        self.user_facing = user_facing
        self.value = default_value
        
    def get_value(self) -> str | bool | int | dict | float | None:
        try:
            self.validate(self.value)
            return self.get_correct_type(self.value)
        except ValueError:
            pass
    
    def set_value(self, value: str) -> None:
        self.value = value
        
    def get_correct_type(self, data) -> str | bool | int | dict | float | None:
        if self.type in ["string", "ip", "enum"]:
            return data
        
        elif self.type == "json":
           return json.loads(data)
    
        elif self.type == "bool":
            return bool(data)
        
        elif self.type == "int":
            return int(data)
        
        elif self.type == "float":
            return float(data)
    
        else:
            return None
            
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