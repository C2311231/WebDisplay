"""
Content Module Base Class

Part of WebDisplay
Device Content Module

License: MIT license

Author: C2311231

Notes:
"""

import json
import core.system as system
import core.system_modules.device_manager.device as device
import core.system_modules.device_manager.device_modules.screens as device_manager_screen

# TODO Store Content in Database

class Content:
    def __init__(self, system: system.system, device: device.Device):
        self.device = device
        self.system = system
        
    def start_content(self, screen: device_manager_screen.Screen):
        pass
    
    def stop_display(self):
        pass
    
    def get_status(self) -> dict:
        return {}
    
    def update_content(self, content_data: dict):
        pass
    
    def preview(self) -> str:
        return ""
    
class ContentURL(Content):
    def __init__(self, system: system.system, device: device.Device, url: str):
        super().__init__(system, device)
        
        if not url.startswith("http"):
            self.url  = "http://" + url
        else:
            self.url = url
        
    def start_content(self, screen: device_manager_screen.Screen):
        pass
        
    def stop_display(self):
        pass
        
    def get_status(self):
        return {"type": "url", "url": self.url}
        
    def update_content(self, content_data: dict):
        if "url" in content_data:
            self.url = content_data["url"]
            
    def preview(self):
        return f"Previewing URL Content: {self.url}"
    
class ContentPublishedGoogleSlide(Content):
    def __init__(self, system: system.system, device: device.Device, slide_id: str):
        super().__init__(system, device)
        self.slide_id = slide_id
        
        # Old Implementation for reference
        # data = json.loads(event["data"])
        #     url_split = data["url"].split("/")
        #     self.browser_manager.open_url(
        #         "https://docs.google.com/presentation/d/e/"
        #         + url_split[-2]
        #         + f"/pub?start={data['autoStart']}&loop={data['restart']}&delayms={int(data['delay'])*1000}"
        #     )
        #     self.browser_manager.set_event(event["id"])
        
    def start_content(self, screen: device_manager_screen.Screen):
        pass
        
    def stop_display(self):
        pass
        
    def get_status(self):
        return {"type": "published_google_slide", "slide_id": self.slide_id}
        
    def update_content(self, content_data: dict):
        if "slide_id" in content_data:
            self.slide_id = content_data["slide_id"]
            
    def preview(self):
        return f"Previewing Published Google Slide Content: {self.slide_id}"
    
class ContentViewingGoogleSlide(Content):
    def __init__(self, system: system.system, device: device.Device, slide_id: str):
        super().__init__(system, device)
        self.slide_id = slide_id
        
        # Old Implementation for reference
        # data = json.loads(event["data"])
        # url_split = data["url"].split("/")
        # self.browser_manager.open_url(
        #     "https://docs.google.com/presentation/d/"
        #     + url_split[-2]
        #     + f"/present?start={data['autoStart']}&loop={data['restart']}&delayms={int(data['delay'])*1000}"
        # )
        # self.browser_manager.set_event(event["id"])
        
    def start_content(self, screen: device_manager_screen.Screen):
        pass
        
    def stop_display(self):
        pass
        
    def get_status(self):
        return {"type": "viewing_google_slide", "slide_id": self.slide_id}
        
    def update_content(self, content_data: dict):
        if "slide_id" in content_data:
            self.slide_id = content_data["slide_id"]
            
    def preview(self):
        return f"Previewing Viewing Google Slide Content: {self.slide_id}"
    
    
def register_content_types(content_manager):
    content_manager.register_content_type("url", [])
    content_manager.register_content_type("published_google_slide", [])
    content_manager.register_content_type("viewing_google_slide", [])
    