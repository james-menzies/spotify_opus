from spotify_opus import db
from spotify_opus.models.Artist import Artist
from spotify_opus.models.ContextObject import ContextObject

association_table = db.Table(
    'tracks_artists',
    db.Column('track_id', db.Integer, db.ForeignKey('tracks.track_id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.artist_id'))
)


class Track(ContextObject):
    __tablename__ = "tracks"

    track_id = db.Column(db.Integer, db.ForeignKey(
        "context_objects.context_id"), primary_key=True)
    external_id = db.Column(db.String(), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.album_id"), nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    disc_no = db.Column(db.Integer, nullable=False)
    explicit = db.Column(db.Boolean, nullable=False)
    track_number = db.Column(db.Integer, nullable=False)

    artists = db.relationship(
        Artist, secondary=association_table, backref="tracks")


