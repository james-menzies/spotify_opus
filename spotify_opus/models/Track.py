from spotify_opus import db
from spotify_opus.models.Artist import Artist

association_table = db.Table(
    'tracks_artists',
    db.Column('track_id', db.Integer, db.ForeignKey('tracks.track_id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.artist_id'))
)


class Track(db.Model):
    __tablename__ = "tracks"

    track_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sanitized_name = db.Column(db.String, nullable=True)
    external_id = db.Column(db.String(), nullable=False, unique=True)
    album_id = db.Column(
        db.Integer, db.ForeignKey("albums.album_id"), nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    disc_no = db.Column(db.Integer, nullable=False)
    explicit = db.Column(db.Boolean, nullable=False)
    track_number = db.Column(db.Integer, nullable=True)

    artists = db.relationship(
        Artist, secondary=association_table, backref="tracks")

