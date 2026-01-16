"""
Database Module Setting Model

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
- Represents a setting stored in the database.
- Validation and other features added in BaseSetting.
"""

from core.system_modules.database.extentions import db
import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime

class dbSetting(db):
    __tablename__ = "setting"
    id = mapped_column(Integer, primary_key=True)
    setting_name = mapped_column(String(100), nullable=False)
    domain = mapped_column(String(300), nullable=False, index=True)
    value = mapped_column(String(255), nullable=False)
    version = mapped_column(String(5), nullable=False)
    lastchanged = mapped_column(DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    created_at = mapped_column(DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))