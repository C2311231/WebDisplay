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

class dbSetting(db.Model):
    __tablename__ = "setting"
    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(300), nullable=False, index=True)
    value = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(5), nullable=False)
    lastchanged = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))