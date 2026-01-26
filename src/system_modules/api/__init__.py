"""
API registry manager

Part of WebDisplay
System API Module

License: MIT license

Author: C2311231

Notes:
- Manages the registration and retrieval of API commands.
"""

import src.module
import src.system_modules.api.api_command as api_command
from src.system_modules.api.api_capability import APICapability
import json
from src.system_modules.api.api_response import APIResponse

import src.system as system

class APIRegistry(src.module.module):
    def __init__(self, system: system.system):
        self.capabilities: dict[str, APICapability] = {}
        self.system = system
        
    def register_capability(self, capability: APICapability):
        self.capabilities[capability.name] = capability
        
    def get_capability(self, name) -> APICapability:
        return self.capabilities[name]
    
    def get_capabilities(self):
        return self.capabilities.keys()
    
    def parse_json_command(self, data: str):
        try:
            parsed = json.loads(data)
        except:
            return APIResponse("error", error="Invalid JSON")

        #TODO finish json parsing
        

def register(system_manager):
    api_registry = APIRegistry(system_manager)
    return "api_registry", api_registry