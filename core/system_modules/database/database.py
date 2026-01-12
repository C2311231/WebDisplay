"""
Database Module Manager

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
"""

from core.system_modules.database.setting import Setting
from .extentions import db

class DBManager:
    def __init__(self):
        self.db = db