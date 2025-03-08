from ics import Calendar as ics_cal
from base import commons, database
import requests
import arrow
from ics.timeline import Timeline

class CalenderManager(commons.BaseClass):
    def __init__(self, db: database.Database):
        self.db = db
        self.calenders = []

class Calender:
    def __init__(self, url):
        self.url = url
        data = requests.get(url)
        if not data.ok:
            raise Exception("Unable to get Calender")
        
        else:
            self.ics = ics_cal(data.text)
            
    def get_events(self):
        return self.ics.events
    
    def get_timeline(self) -> Timeline:
        return self.ics.timeline
    
    def update(self) -> None:
        self.__init__(self.url)