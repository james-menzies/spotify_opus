from enum import Enum

from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject


class AlbumType(Enum):
    single = 1
    album = 2
    compilation = 3


class Album(ContextObject):
    __tablename__ = "albums"
    album_id = db.Column(db.Integer(), db.ForeignKey(
        "context_objects.context_id"), primary_key=True)
    album_type = db.Column(db.Enum(AlbumType), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "album"
    }
