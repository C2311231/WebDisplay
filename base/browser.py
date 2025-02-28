# from selenium import webdriver
# import time
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# import os
# ## https://www.youtube.com/watch?v=qQOgqeRteJA
# chrome_options = Options()
# #chrome_options.add_argument("--kiosk")  # Example of adding an argument (adjust as needed)
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option("useAutomationExtension", False)
# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.google.com")
# time.sleep(10)
# driver.get("https://www.youtube.com")
# time.sleep(20)

# driver.close()

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import commons
class BrowserManager(commons.BaseClass):
    def __init__(self):
        self.event = 0
        self.awaiting = []
        self.driver = None

    def initDriver(self):
        chrome_options = Options()
        #chrome_options.add_argument("--kiosk")  # Uncomment if needed
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.event = 0

    def openURL(self, url):
        if self.driver:
            try:
                self.driver.get(url)
            except:
                self.initDriver()
                self.driver.get(url)
        else:
            self.initDriver()
            self.driver.get(url)

    def getScreenShot(self):
        if self.driver:
            try:
                self.driver.save_screenshot("./static/images/latestScreenShot.png")
                
            except:
                self.initDriver()
                self.getScreenShot()
                

    def close(self):
        if self.driver:
            self.driver.quit()  # Use `quit()` to close all windows and processes
            self.driver = None

    def getEvent(self):
        return self.event
    
    def setEvent(self, eventID):
        self.event = eventID