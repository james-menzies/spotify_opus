from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject


class Track(ContextObject):

    __tablename__ = "tracks"

    track_id = db.Column(db.Integer, db.ForeignKey(
        "context_objects.context_id"), primary_key=True)

    album_id = db.Column(db.Integer, db.ForeignKey("albums.album_id"), nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    disc_no = db.Column(db.Integer, nullable=False)
    explicit = db.Column(db.Boolean, nullable=False)

