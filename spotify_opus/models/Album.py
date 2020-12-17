from enum import Enum

from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject
from spotify_opus.models.Track import Track


class AlbumType(Enum):
    single = 1
    album = 2
    compilation = 3


class Album(ContextObject):
    __tablename__ = "albums"
    album_id = db.Column(db.Integer(), db.ForeignKey(
        "context_objects.context_id"), primary_key=True)
    external_id = db.Column(db.String(), nullable=False, unique=True)
    album_type = db.Column(db.Enum(AlbumType), nullable=False)
    image_url = db.Column(db.String(), nullable=True)

    release_date = db.Column(db.Date, nullable=False)
    tracks = db.relationship(
        Track, backref="album", foreign_keys=[Track.album_id])

    __mapper_args__ = {
        "polymorphic_identity": "album"
    }

    def __repr__(self):
        return f"<Album: {self.name}>"
