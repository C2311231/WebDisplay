import core.module
import core.system_modules.api.api_command as api_command

class APIRegistry(core.module.module):
    def __init__(self):
        self.commands = []

    def register_command(self, capability: str, capability_version: int, name: str, handler, description: str, example: str = "") -> None:
        self.commands.append(api_command.APICommand(capability, capability_version, name, handler, description, example))
        
    def get_commands(self) -> list[api_command.APICommand]:
        return self.commands

    def get_command(self, capability: str, capability_version: int, name: str) -> api_command.APICommand | None:
        for command in self.commands:
            if command.capability == capability and command.name == name and command.capability_version == capability_version:
                return command
        return None
    
def register(system_manager):
    api_registry = APIRegistry()
    return "api_registry", api_registry