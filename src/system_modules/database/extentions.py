"""
Database Module Constants and Extensions

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
- Creates db object for model classes to inherit from.
"""

from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine


class BaseModel(DeclarativeBase):
    pass

db = BaseModel

