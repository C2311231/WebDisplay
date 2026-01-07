import core.system_modules.device_manager.device as device
import pkgutil
import importlib
import device_modules

class LocalDevice(device.Device):
    modules = {}
    __mapper_args__ = {
        "polymorphic_identity": "local",
    }
    
    def __init__(self, system):
        self.system = system
        self.load_modules()
        
    def load_modules(self):
        for _, module_name, _ in pkgutil.iter_modules(device_modules.__path__):
            module = importlib.import_module(f"{device_modules.__name__}.{module_name}")

            if hasattr(module, "register"):
                module_id, module = module.register(self, self.system)
                
                if module_id in self.modules:
                    raise ValueError(f"Module with id {module_id} is already registered.")

                if not isinstance(module, module):
                    raise TypeError(f"{module_id} does not inherit module")

                self.modules[module_id] = module
            else:
                raise ValueError(f"Module {module_name} does not have a register function.")
                
                
    def get_module(self, module_id: str):
        if module_id not in self.modules:
            raise KeyError(f"Module with id {module_id} not found.")
        return self.modules.get(module_id)
    
    def get_all_modules(self):
        return self.modules
    
    def module_exists(self, module_id: str) -> bool:
        return module_id in self.modules
    
    