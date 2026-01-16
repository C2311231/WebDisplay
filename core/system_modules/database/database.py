"""
Database Module Manager

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
"""

from core.system_modules.database.setting import Setting
from .extentions import db, BaseModel
from core.module import module
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

class DBManager(module):
    def __init__(self):
        self.db = db
        
        ## TODO load this from config, environment variable or argument
        self.DATABASE_URL = "sqlite:///webdisplay.db"

        self.engine = create_engine(
            self.DATABASE_URL,
            future=True,
            echo=False,
        )

        self.SessionFactory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

        self.Session = scoped_session(self.SessionFactory)
        
    def get_database(self):
        return self.db
    
    def get_session(self):
        return self.Session

    def preload(self):
        BaseModel.metadata.create_all(self.engine)