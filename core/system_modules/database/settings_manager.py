"""
Database Module Settings Manager

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
"""

from sqlalchemy import func
from .setting import Setting
import core.system
import core.module
from .setting import dbSetting
from .database import DBManager
import uuid

class SettingsManager(core.module.module):
    def __init__(self, system_manager: core.system.system):
        self.system_manager = system_manager
        self.settings = []
        self.required_settings = []
        system_manager.require_modules("database_manager")
        
    def start(self):
        self.validate_required_settings()
        self.database_manager: DBManager = self.system_manager.get_module("database_manager") # type: ignore
        
        self.device_id = self.register_setting(domain = "system", version = "V1", setting_name= "device_id", default_value= str(uuid.uuid4()), type= "string", description = "UUID for system identification", validation_data = {}, user_facing = False)
        self.device_id.push_to_db() # Ensure device id is stored in db for future starts (If not already)
        super().start()
    
    ## Registers a global setting in the database
    ## @param setting_name: Name of the setting
    ## @param default_value: Default value of the setting
    ## @param type: Type of the setting (string, int, bool, float, json, enum, etc.)
    ## @param description: Description of the setting
    def register_setting(self, domain: str, version: str,setting_name: str, default_value: str, type: str, description: str, validation_data: dict, user_facing: bool) -> Setting:
        if type not in ["string", "int", "bool", "float", "ip", "json"]:
            raise ValueError(f"Invalid setting type ({type}) for {setting_name} with default value {default_value}")
        setting = Setting(self.database_manager, domain, version, setting_name=setting_name, default_value=default_value, value_type=type, description=description, validation_data=validation_data, user_facing=user_facing)
        self.settings.append(setting)
        return setting
    
    def register_required_setting(self, setting_name: str) -> None:
        self.required_settings.append(setting_name)
        
    def register_required_settings(self, *setting_names: str) -> None:
        for setting_name in setting_names:
            self.register_required_setting(setting_name)
        
    def validate_required_settings(self) -> None:
        for setting in self.required_settings:
            for registered_setting in self.settings:
                if setting == registered_setting.setting_name:
                    break
                raise ValueError(f"Required setting {setting} not registered in database manager")
            
    def get_setting(self, domain:str, setting_name: str) -> Setting:
        for setting in self.settings:
            if setting.setting_name == setting_name and setting.domain == domain:
                return setting
        raise ValueError(f"Setting {setting_name} not found in database manager")
    
    def get_settings_of_domain(self, domain: str) -> list[Setting]:
        domain_settings = []
        for setting in self.settings:
            if setting.domain == domain:
                domain_settings.append(setting)
        return domain_settings
    
    def get_settings_of_subdomain(self, subdomain: str) -> list[Setting]:
        subdomain_settings = []
        for setting in self.settings:
            if setting.domain.startswith(subdomain):
                subdomain_settings.append(setting)
        return subdomain_settings
            
    # Returns a list of unique subdomains for a given domain prefix one level below the prefix
    # For input of "device." it would give the device IDs of all devices with registered settings
    def get_unique_subdomains(self, domain_prefix: str) -> list[str]:
        prefix_len = len(domain_prefix)
        query = (
            self.database_manager.get_session().query(
                func.substr(
                    dbSetting.domain,
                    prefix_len + 1,  # start after prefix
                    func.instr(func.substr(dbSetting.domain, prefix_len + 1), '.') - 1
                ).label("subdomain")
            )
            .filter(dbSetting.domain.like(f"{domain_prefix}%"))
            .distinct()
        )

        return [row.subdomain for row in query.all()]        
        
def register(system_manager):
    return "settings_manager", SettingsManager(system_manager)