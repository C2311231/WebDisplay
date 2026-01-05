from core.system_modules.database.setting import Setting
from .extentions import db

class DBManager:
    def __init__(self):
        self.db = db