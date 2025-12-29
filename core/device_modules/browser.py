from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from base import commons
from selenium.common.exceptions import TimeoutException

class BrowserManager(commons.BaseClass):
    def __init__(self, config: dict):
        self.event = 0
        self.awaiting = []
        self.driver = None
        self.config = config

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

    def get_screenshot(self) -> None:
        if self.driver:
            try:
                self.driver.save_screenshot("./static/images/latestScreenShot.png")

            except:
                self.init_driver()
                self.get_screenshot()

    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def get_event(self) -> int:
        return self.event

    def set_event(self, eventID: int) -> None:
        self.event = eventID
        
    def required_config(self) -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        data = {}
        return data
