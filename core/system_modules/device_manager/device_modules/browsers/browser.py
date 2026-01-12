"""
Browser Module Class

Part of WebDisplay
Device Browser Module

License: MIT license

Author: C2311231

Notes:
- Manages and represents a web browser instance for a device.
"""

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import core.commons as commons
import time

class Browser:
    def __init__(self, config: dict):
        self.driver = None
        self.config = config
        self.in_use = False
        self.cleanup_timer = time.time()
        
    def is_in_use(self) -> bool:
        return self.in_use

    def set_in_use(self, in_use: bool) -> None:
        self.in_use = in_use
        if not in_use:
            self.cleanup_timer = time.time()

    # TODO Add propererror handling and recovery for driver issues
    # TODO Load browser on desired screen
    # TODO Add audio desitination handling
    def init_driver(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--kiosk")  # Uncomment if needed
        chrome_options.add_argument("--display=:0")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--v=1')
        chrome_options.add_argument('--disable-dev-shm-usage')  # helpful on small RAM devices
        chrome_options.add_experimental_option('extensionLoadTimeout', 60000)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # TODO improve handling of chromedriver path
        try:
            service = Service(executable_path=r'/usr/bin/chromedriver', log_output='/tmp/chromedriver.log')
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            self.driver = webdriver.Chrome(options=chrome_options)
        if self.event != -1:
            self.event = 0
        self.driver.command_executor.set_timeout(10000) # type: ignore
        self.driver.set_page_load_timeout(60)


    def open_url(self, url: commons.Url) -> None:
        if self.driver:
            try:
                self.driver.get(str(url))
            except TimeoutException:
                print(f"Timeout loading {url}")
    
            except:
                self.init_driver()
                self.driver.get(str(url))
        else:
            self.init_driver()
            self.driver.get(str(url)) # type: ignore

    def get_screenshot(self) -> str | None:
        if self.driver:
            try:
                return self.driver.get_screenshot_as_base64()

            except:
                self.init_driver()
                self.get_screenshot()

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None