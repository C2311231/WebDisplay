from ics import Calendar as ics_cal
from ics import Event
from base import commons, database
import requests
import arrow
import uuid
from ics.timeline import Timeline

class Calender:
    def __init__(self, name, url):
        self.id = uuid.uuid4()
        self.url = url
        self.name = name
        self.date_range_after = 7
        self.date_range_before = 0
        self.update()
        
    def get_events(self):
        return self.ics.events
    
    def get_timeline(self) -> Timeline:
        return self.ics.timeline

    def events_on(self, day: int, month: int, year: int) -> list[Event]:
        events = []
        for event in self.get_timeline().on(arrow.Arrow(year, month, day), strict=True):
            events.append(event)
        return events

    def set_date_range(self, before, after):
        self.date_range_before = before
        self.date_range_after = after

    def update(self) -> None:
        data = requests.get(self.url)
        if not data.ok:
            raise Exception("Unable to get Calender")
        
        else:
            self.ics = ics_cal(data.text)
            
    def get_dict(self) -> dict:
        return {"id": str(self.id), "name": self.name, "date_range_before": self.date_range_before, "date_range_after": self.date_range_after}
        
        
class MergedCalender(Calender):
    def __init__(self, name: str, urls: list[str]):
        self.urls = urls
        super(name, "")
        self.update()
        
    def update(self) -> None:
        cal = ics_cal()
        for url in self.urls:
            data = requests.get(url)
            if not data.ok:
                print(f"Unable to get calender: {url}")
            else:
                events = ics_cal(data.text).events
                for event in events:
                    cal.events.add(event)
        self.ics = cal 
        
class CalenderManager(commons.BaseClass):
    def __init__(self, db: database.Database):
        self.db = db
        self.calenders = []
        self.merged_calenders = []
        
    def add_calender(self, name: str, url: str):
        self.calenders.append(Calender(name, url))

    def create_merged_calender(self, name, urls: list[str]):
        self.merged_calenders.append(MergedCalender(name, urls))
        
    def remove_calender(self, name):
        for calender in self.calenders:
            if calender.name == name:
                self.calenders.remove(calender)
                return
             
    def remove_merged_calender(self, name):
        for calender in self.merged_calenders:
            if calender.name == name:
                self.merged_calenders.remove(calender)
                return
    
    def get_calender(self, name) -> Calender:
        for calender in self.calenders:
            if calender.name == name:
                return calender
            
    def get_calender_by_id(self, id) -> Calender:
        for calender in self.calenders:
            if calender.id == id:
                return calender
        
        for calender in self.merged_calenders:
            if calender.id == id:
                return calender
        
    def get_merged_calender(self, name) -> Calender:
        for calender in self.merged_calenders:
            if calender.name == name:
                return calender
    
    def update_all(self):
        for calender in self.calenders:
            calender.update()
            
        for calender in self.merged_calenders:
            calender.update()    