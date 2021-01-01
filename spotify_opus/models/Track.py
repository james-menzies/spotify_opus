from spotify_opus import db
from spotify_opus.models.Artist import Artist

association_table = db.Table(
    'tracks_artists',
    db.Column('track_id', db.String, db.ForeignKey('tracks.track_id')),
    db.Column('artist_id', db.String, db.ForeignKey('artists.artist_id'))
)


class Track(db.Model):
    __tablename__ = "tracks"

    track_id = db.Column(db.String, primary_key=True, autoincrement=False)
    name = db.Column(db.String, nullable=False)
    sanitized_name = db.Column(db.String, nullable=True)
    album_id = db.Column(
        db.String, db.ForeignKey("albums.album_id"), nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    disc_no = db.Column(db.Integer, nullable=False)
    explicit = db.Column(db.Boolean, nullable=False)
    track_number = db.Column(db.Integer, nullable=True)

    artists = db.relationship(Artist, secondary=association_table,
                              backref="tracks", lazy="joined")

    performance_id = db.Column(
        db.Integer, db.ForeignKey(
            "performances.performance_id"), nullable=True)

    def __repr__(self):
        return f"<Track: {self.name}>"

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False

        return self.track_id == other.track_id
