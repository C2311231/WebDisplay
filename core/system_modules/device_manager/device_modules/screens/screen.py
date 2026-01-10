import core.system
import core.system_modules.device_manager.device as device
class Screen():
    
    # TODO Store these settings in the database
    def __init__(self, system: core.system.system, device: device.Device, screen_name: str, screen_id: int, input: str, resolution_x: int, resolution_y: int, volume: float, sound_device: str, screen_type: str, scale: float):
        self.system = system
        self.device = device
        self.screen_id = screen_id
        self.input = input
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.scale = scale
        self.screen_name = screen_name
        self.volume = volume
        self.sound_device = sound_device
        self.screen_type = screen_type
        
        
    