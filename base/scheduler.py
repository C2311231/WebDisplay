import threading
import time
from datetime import datetime
import json
import commons


class scheduler(commons.BaseClass):
    def __init__(self, db, browser_manager, cec):
        self.db = db
        self.run = False
        self.browser_manager = browser_manager
        self.cec = cec
        self.turnedScreenOff = False

    def running(self):
        while self.run:
            t = (
                float(datetime.now().strftime("%H"))
                + float(datetime.now().strftime("%M")) / 60
            )

            wk_day = datetime.now().strftime("%A")
            events = self.db.getEvents()
            currentEvent = False
            for event in events:
                if event["wkDay"] == wk_day:
                    if (float(event["startTime"]) <= t) and (
                        float(event["endTime"]) > t
                    ):
                        currentEvent = True
                        if self.browser_manager.getEvent() != event["id"]:
                            self.startEvent(event)
            if not currentEvent:
                if self.browser_manager.driver != None:
                    self.browser_manager.close()
                if not self.turnedScreenOff:
                    self.cec.tv_off()
                    self.turnedScreenOff = True
            time.sleep(2)

    def start(self):
        self.run = True
        self.thread = threading.Thread(target=self.running, args=(), daemon=True)
        self.thread.start()

    def stop(self):
        self.run = False

    def startEvent(self, event):
        print("Starting Event")
        if not self.cec.get_tv_power():
            self.cec.tv_on()
        self.turnedScreenOff = False

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
            urlSplit = data["url"].split("/")
            self.browser_manager.open_url(
                "https://docs.google.com/presentation/d/e/"
                + urlSplit[-2]
                + f"/pub?start={data['autoStart']}&loop={data['restart']}&delayms={int(data['delay'])*1000}"
            )
            self.browser_manager.set_event(event["id"])

        elif event["type"] == "viewingSlide":
            data = json.loads(event["data"])
            urlSplit = data["url"].split("/")
            self.browser_manager.open_url(
                "https://docs.google.com/presentation/d/"
                + urlSplit[-2]
                + f"/present?start={data['autoStart']}&loop={data['restart']}&delayms={int(data['delay'])*1000}"
            )
            self.browser_manager.set_event(event["id"])
