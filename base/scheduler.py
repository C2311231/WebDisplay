import threading
import time
from datetime import datetime
import json
from base import commons, database, browser, cec


class Scheduler(commons.BaseClass):
    def __init__(self, db: database.Database, browser_manager: browser.BrowserManager, cec: cec.CecManager):
        self.db = db
        self.run = False
        self.browser_manager = browser_manager
        self.cec = cec
        self.turned_screen_off = False
        self.last_reload_time = 9999999999999999999999999999999999999999999999999999999999999999

    def running(self) -> None:
        while self.run:
            try:
                t = (
                    float(datetime.now().strftime("%H"))
                    + float(datetime.now().strftime("%M")) / 60
                )

                wk_day = datetime.now().strftime("%A")
                events = self.db.get_events()
                current_event = False
                # print(f"Event ID: {self.browser_manager.get_event()}")
                for event in events:
                    if event["wk_day"] == wk_day:
                        if (float(event["start_time"]) <= t) and (
                            float(event["end_time"]) > t
                        ):
                            current_event = True
                            reload_time = 60*float(self.db.config()["reload_time"])
                            if time.time() - self.last_reload_time >= reload_time and reload_time != 0:
                                self.last_reload_time = time.time()
                                self.start_event(event)
                                                            
                            if (self.browser_manager.get_event() != event["id"]) and self.browser_manager.get_event() >= 0:
                                print(f"Event id is: {self.browser_manager.get_event()}, Should be: {event['id']}")
                                self.last_reload_time = time.time()
                                self.start_event(event)
                        continue
                if not current_event:
                    self.browser_manager.set_event(0)
                    self.last_reload_time = 9999999999999999999999999999999999999999999999999999999999999999
                    if self.browser_manager.driver != None:
                        self.browser_manager.close()
                        
                    if not self.turned_screen_off:
                        self.cec.tv_off()
                        self.turned_screen_off = True
            except Exception as e:
                print(e)
            time.sleep(2)

    def start(self) -> None:
        self.run = True
        self.thread = threading.Thread(target=self.running, args=(), daemon=True)
        self.thread.start()

    def stop(self) -> None:
        self.run = False

    def start_event(self, event: dict) -> None:
        print("Starting Event")
        if not self.cec.get_tv_power():
            self.cec.tv_on()
        self.turned_screen_off = False

        self.cec.set_active()

        if event["type"] == "URL":
            data = json.loads(event["data"])
            if not data["url"].startswith("http"):
                self.browser_manager.open_url("http://" + data["url"])
            else:
                self.browser_manager.open_url(data["url"])
            self.browser_manager.set_event(event["id"])

        elif event["type"] == "idle":
            config = self.db.config()
            self.browser_manager.open_url(config["url"] + "/idle")
            self.browser_manager.set_event(event["id"])

        elif event["type"] == "publishedSlide":
            data = json.loads(event["data"])
            url_split = data["url"].split("/")
            self.browser_manager.open_url(
                "https://docs.google.com/presentation/d/e/"
                + url_split[-2]
                + f"/pub?start={data['autoStart']}&loop={data['restart']}&delayms={int(data['delay'])*1000}"
            )
            self.browser_manager.set_event(event["id"])

        elif event["type"] == "viewingSlide":
            data = json.loads(event["data"])
            url_split = data["url"].split("/")
            self.browser_manager.open_url(
                "https://docs.google.com/presentation/d/"
                + url_split[-2]
                + f"/present?start={data['autoStart']}&loop={data['restart']}&delayms={int(data['delay'])*1000}"
            )
            self.browser_manager.set_event(event["id"])

    def required_config() -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        data = {
            "reload_time": 0,
            "url": None,
        }
        return data