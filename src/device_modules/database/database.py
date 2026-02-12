"""
Database Module Manager

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
"""

from src.device_modules.database.setting import Setting
from .extentions import db, BaseModel
from src.module import module
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import argparse

class DBManager(module):
    def __init__(self):
        self.db = db
        parser = argparse.ArgumentParser()
        parser.add_argument("--db_path", type=str, help="Path to the sqlite DB file")
        args = parser.parse_args()
        
        if args.db_path is not None:
            self.DATABASE_URL = f"sqlite:///{args.db_path}"
        
        else:
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