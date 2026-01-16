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
import core.system_modules.device_manager.local_device as local_device
import core.system_modules.device_manager.device_modules.screens as device_manager_screen
from core.system_modules.device_manager.device_modules.browsers import BrowserManager
# TODO Store Content in Database

class ContentContext:
    def __init__(self, screen: device_manager_screen.Screen, context: dict = {}) -> None:
        self.screen = screen
        self.context = context
        
    def get_screen(self):
        return self.screen
    
    def get_context(self):
        return self.context
    
    def add_context(self, key, value):
        self.context[key] = value

class Content:
    def __init__(self, system: system.system, device: local_device.LocalDevice):
        self.device = device
        self.system = system
        
    def start_content(self, screen: device_manager_screen.Screen) -> ContentContext:
        return ContentContext(screen)
    
    def stop_display(self, content_context: ContentContext):
        pass
    
    def get_status(self, content_context: ContentContext) -> dict:
        return {}
    
    def update_content(self, content_data: dict, content_context: ContentContext):
        pass
    
    def preview(self, content_context: ContentContext) -> str:
        return ""
    
class ContentURL(Content):
    def __init__(self, system: system.system, device: local_device.LocalDevice, url: str):
        super().__init__(system, device)
        self.browser_manager: BrowserManager = self.device.get_module("browser_manager") # type: ignore
        
        if not url.startswith("http"):
            self.url  = "http://" + url
        else:
            self.url = url
        
    def start_content(self, screen: device_manager_screen.Screen):
        context = ContentContext(screen)
        browser = self.browser_manager.requestBrowser()
        context.add_context("browser", browser)
        browser.init_driver()
        browser.set_position(screen.x, screen.y)
        screen.lock()
        browser.open_url(self.url)
        return context
        
    def stop_display(self, content_context: ContentContext):
        browser = content_context.get_context()["browser"]
        self.browser_manager.returnBrowser(browser)
        content_context.get_screen().release()
        
    def get_status(self, content_context: ContentContext):
        return {"type": "url", "url": self.url}
        
    def update_content(self, content_data: dict, content_context: ContentContext):
        if "url" in content_data:
            self.url = content_data["url"]
            content_context.get_context()["browser"].open_url(self.url)
            
    def preview(self, content_context: ContentContext):
        return f"Previewing URL Content: {self.url}"
    
class ContentPublishedGoogleSlide(Content):
    def __init__(self, system: system.system, device: local_device.LocalDevice, slide_id: str, autostart: bool, loop: bool, delay: float):
        super().__init__(system, device)
        self.slide_id = slide_id
        self.autostart = autostart
        self.loop = loop
        self.delay = delay
        self.browser_manager: BrowserManager = self.device.get_module("browser_manager") # type: ignore
        
        self.url = "https://docs.google.com/presentation/d/e/" + slide_id +  f"/pub?start={autostart}&loop={loop}&delayms={delay * 1000}"
        
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
        context = ContentContext(screen)
        browser = self.browser_manager.requestBrowser()
        context.add_context("browser", browser)
        browser.init_driver()
        browser.set_position(screen.x, screen.y)
        screen.lock()
        browser.open_url(self.url)
        return context
        
    def stop_display(self, content_context: ContentContext):
        browser = content_context.get_context()["browser"]
        self.browser_manager.returnBrowser(browser)
        content_context.get_screen().release()
        
    def get_status(self, content_context: ContentContext):
        return {"type": "published_google_slide", "slide_id": self.slide_id}
        
    def update_content(self, content_data: dict, content_context: ContentContext):
        if "slide_id" in content_data:
            self.slide_id = content_data["slide_id"]
            self.url = "https://docs.google.com/presentation/d/e/" + self.slide_id +  f"/pub?start={self.autostart}&loop={self.loop}&delayms={self.delay * 1000}"
            content_context.get_context()["browser"].open_url(self.url)
            
    def preview(self, content_context: ContentContext):
        return f"Previewing Published Google Slide Content: {self.slide_id}"
    
class ContentViewingGoogleSlide(Content):
    def __init__(self, system: system.system, device: local_device.LocalDevice, slide_id: str, autostart: bool, loop: bool, delay: float):
        super().__init__(system, device)
        self.slide_id = slide_id
        self.autostart = autostart
        self.loop = loop
        self.delay = delay
        self.browser_manager: BrowserManager = self.device.get_module("browser_manager") # type: ignore

        self.url = "https://docs.google.com/presentation/d/" + slide_id + f"/present?start={self.autostart}&loop={self.loop}&delayms={self.delay * 1000}"
        
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
        context = ContentContext(screen)
        browser = self.browser_manager.requestBrowser()
        context.add_context("browser", browser)
        browser.init_driver()
        browser.set_position(screen.x, screen.y)
        screen.lock()
        browser.open_url(self.url)
        return context
        
    def stop_display(self, content_context: ContentContext):
        browser = content_context.get_context()["browser"]
        self.browser_manager.returnBrowser(browser)
        content_context.get_screen().release()
        
    def get_status(self, content_context: ContentContext):
        return {"type": "viewing_google_slide", "slide_id": self.slide_id}
        
    def update_content(self, content_data: dict, content_context: ContentContext):
        if "slide_id" in content_data:
            self.slide_id = content_data["slide_id"]
            self.url = "https://docs.google.com/presentation/d/" + self.slide_id +  f"/present?start={self.autostart}&loop={self.loop}&delayms={self.delay * 1000}"
            content_context.get_context()["browser"].open_url(self.url)
            
    def preview(self, content_context: ContentContext):
        return f"Previewing Viewing Google Slide Content: {self.slide_id}"
    
    
def register_content_types(content_manager):
    content_manager.register_content_type("url", [])
    content_manager.register_content_type("published_google_slide", [])
    content_manager.register_content_type("viewing_google_slide", [])
    