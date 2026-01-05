import core.system_modules.api.api_registry as api_registry
import core.system as system
import core.module as module

def register(system: system.system) -> tuple[str, module.module]:
    return api_registry.register(system)