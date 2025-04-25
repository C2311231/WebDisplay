from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from base import commons


class BrowserManager(commons.BaseClass):
    def __init__(self):
        self.event = 0
        self.awaiting = []
        self.driver = None

    def init_driver(self) -> None:

        try:
            chrome_options = Options()
            chrome_options.add_argument("--kiosk")  # Uncomment if needed
            chrome_options.add_argument("--display=:0")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            service = Service(executable_path=r'/usr/bin/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            chrome_options = Options()
            chrome_options.add_argument("--kiosk")  # Uncomment if needed
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            self.driver = webdriver.Chrome(options=chrome_options)
        self.event = 0
        self.driver.command_executor.set_timeout(1000)

    def open_url(self, url: commons.url) -> None:
        if self.driver:
            try:
                self.driver.get(url)
            except:
                self.init_driver()
                self.driver.get(url)
        else:
            self.init_driver()
            self.driver.get(url)

    def get_screenshot(self) -> None:
        if self.driver:
            try:
                self.driver.save_screenshot("./static/images/latestScreenShot.png")

            except:
                print("Failed to get Screenshot")

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_event(self) -> int:
        return self.event

    def set_event(self, eventID: int) -> None:
        self.event = eventID

    def __del__(self):
        self.close()