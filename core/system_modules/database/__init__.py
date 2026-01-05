import core.system_modules.database.settings_manager as settings_manager
import core.module

def register(system) -> tuple[str, core.module.module]:
    return settings_manager.register(system)