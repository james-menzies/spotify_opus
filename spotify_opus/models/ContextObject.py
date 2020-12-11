import enum

from marshmallow.fields import Integer
from sqlalchemy import Column, String

from spotify_opus import db


class ContextObject(db.Model):
    __tablename__ = "context_objects"
    context_id = Column(Integer, primary_key=True)
    uri = Column(String, unique=True, nullable=False)
    external_uri = Column(String, unique=True, nullable=False)


class ContextType(enum.Enum):
    artist = 1
    album = 2
    composer = 3
    conductor = 4
    ensemble = 5
    playlist = 6
    track = 7
    performance = 8
    work = 9
