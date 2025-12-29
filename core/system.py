import pkgutil
import importlib
import system_modules
import time

class system:
    def __init__(self):
        self.modules = {}
        self._last_update_time = time.time()
        self.load_modules()
    
    def load_modules(self):
        for _, module_name, _ in pkgutil.iter_modules(system_modules.__path__):
            module = importlib.import_module(f"{system_modules.__name__}.{module_name}")

            if hasattr(module, "register"):
                module_id, module = module.register(self)
                
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
    
    def update_modules(self):
        for module_id, module in self.modules.items():
            if hasattr(module, "update"):
                module.update(time.time()-self._last_update_time)
            self._last_update_time = time.time()
    
    def start_modules(self):
        for module_id, module in self.modules.items():
            if hasattr(module, "start"):
                module.start()
                
    def shutdown_modules(self):
        for module_id, module in self.modules.items():
            if hasattr(module, "shutdown"):
                module.shutdown()