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

    def running(self):
        while self.run:
            t = (
                float(datetime.now().strftime("%H"))
                + float(datetime.now().strftime("%M")) / 60
            )

            wk_day = datetime.now().strftime("%A")
            events = self.db.get_events()
            current_event = False
            for event in events:
                if event["wkDay"] == wk_day:
                    if (float(event["startTime"]) <= t) and (
                        float(event["endTime"]) > t
                    ):
                        current_event = True
                        if self.browser_manager.get_event() != event["id"]:
                            self.start_event(event)
            if not current_event:
                if self.browser_manager.driver != None:
                    self.browser_manager.close()
                    
                if not self.turned_screen_off:
                    self.cec.tv_off()
                    self.turned_screen_off = True
            time.sleep(2)

    def start(self):
        self.run = True
        self.thread = threading.Thread(target=self.running, args=(), daemon=True)
        self.thread.start()

    def stop(self):
        self.run = False

    def start_event(self, event):
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
