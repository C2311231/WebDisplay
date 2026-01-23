"""
API capability class

Part of WebDisplay
System API Module

License: MIT license

Author: C2311231

Notes:
"""

from core.system_modules.api.api_command import APICommand

class APICapability:
    def __init__(self, capability_name: str, capability_version: int):
        self.name = capability_name
        self.version = capability_version
        self.commands: list[APICommand] = []
        
    def register_command(self, command: APICommand):
         self.commands.append(command)
         
    def get_commands(self) -> list[APICommand]:
        return self.commands