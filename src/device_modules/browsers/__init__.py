"""
Browser Module Manager

Part of WebDisplay
Device Browser Module

License: MIT license

Author: C2311231

Notes:
"""

import src.module as device_module
from src.device_modules.browsers.browser import Browser
import time


class BrowserManager(device_module.module):
    def __init__(self, device_module: device_module.module):
        self.device_module = device_module
        self.browsers: list[Browser] = []
        
    def getBrowsers(self) -> list[Browser]:
        return self.browsers
    
    def requestBrowser(self) -> Browser:
        for browser in self.browsers:
            if not browser.is_in_use():
                browser.set_in_use(True)
                return browser
            
        browser = Browser()
        self.browsers.append(browser)
        browser.set_in_use(True)
        browser.init_driver()
        return browser
    
    def returnBrowser(self, browser: Browser) -> None:
        browser.set_in_use(False)
        
    def update(self, delta_time: float):
        for browser in list(self.browsers):
            if not browser.is_in_use():
                # If browser has been disabled for more than 5 seconds, close it
                if time.time() - browser.cleanup_timer > 5:
                    browser.close()
                    self.browsers.remove(browser)
                    
def register(device):
    return "browser_manager", BrowserManager(device)