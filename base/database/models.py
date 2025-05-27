from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import uuid
db = SQLAlchemy()


class Config(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    device: Mapped[list[str]]
    parameter: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str]
    lastchanged: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    check_data: Mapped[str] = mapped_column(default=lambda: uuid.uuid4().hex, onupdate=lambda: uuid.uuid4().hex)

class Events(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    groups: Mapped[list[str]]
    criteria: Mapped[str]
    action: Mapped[str]
    color: Mapped[str]
    lastchanged: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    check_data: Mapped[str] = mapped_column(default=lambda: uuid.uuid4().hex, onupdate=lambda: uuid.uuid4().hex)


class Peers(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    device_name: Mapped[str]
    device_id: Mapped[str] = mapped_column(unique=True)
    device_ip: Mapped[str]
    groups: Mapped[list[str]]
    lastchanged: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    check_data: Mapped[str] = mapped_column(default=lambda: uuid.uuid4().hex, onupdate=lambda: uuid.uuid4().hex)
