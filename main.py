import core.system as system
system_manager = system.system()
system_manager.load_modules()
system_manager.validate_required_modules()
system_manager.start_modules()

## Start program loop
system_manager.core_loop()