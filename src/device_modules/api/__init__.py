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
import src.device_modules.api.api_command as api_command
from src.device_modules.api.api_capability import APICapability
import json
from src.device_modules.api.api_response import APIResponse
from src.device import Device

class APIRegistry(src.module.module):
    def __init__(self):
        self.capabilities: dict[str, APICapability] = {}
        
    def register_capability(self, capability: APICapability):
        self.capabilities[capability.name] = capability
        
    def get_capability(self, name) -> APICapability:
        return self.capabilities[name]
    
    def get_capabilities(self):
        return list(self.capabilities.keys())
    
    def parse_json_command(self, data: str):
        try:
            parsed = json.loads(data)
        except:
            return APIResponse("error", error="Invalid JSON")

        #TODO finish json parsing
        

def register(device: Device):
    api_registry = APIRegistry()
    return "api_registry", api_registry