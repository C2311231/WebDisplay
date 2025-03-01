from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from base import commons


class BrowserManager(commons.BaseClass):
    def __init__(self):
        self.event = 0
        self.awaiting = []
        self.driver = None

    def init_driver(self):
        chrome_options = Options()
        # chrome_options.add_argument("--kiosk")  # Uncomment if needed
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.event = 0

    def open_url(self, url):
        if self.driver:
            try:
                self.driver.get(url)
            except:
                self.initDriver()
                self.driver.get(url)
        else:
            self.initDriver()
            self.driver.get(url)

    def get_screenshot(self):
        if self.driver:
            try:
                self.driver.save_screenshot("./static/images/latestScreenShot.png")

            except:
                self.initDriver()
                self.getScreenShot()

    def close(self):
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_event(self):
        return self.event

    def set_event(self, eventID):
        self.event = eventID
