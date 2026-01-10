
# TODO Store Content in Database
class Content:
    def __init__(self, system, device_manager):
        self.device_manager = device_manager
        self.system = system
        
    def display(self, screen):
        pass
    
    def stop_display(self):
        pass
    
    def get_status(self):
        pass
    
    def update_content(self, content_data: dict):
        pass
    
    def preview(self):
        pass