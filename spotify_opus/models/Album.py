from spotify_opus import db
from spotify_opus.models.Track import Track


class Album(db.Model):
    __tablename__ = "albums"
    album_id = db.Column(db.String(), primary_key=True, autoincrement=False)
    album_type = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=False)

    release_date = db.Column(db.Date, nullable=False)
    tracks = db.relationship(
        Track, backref="album", foreign_keys=[Track.album_id])

    def __repr__(self):
        return f"<Album: {self.name}>"

    def __eq__(self, other):
        if not isinstance(other, Album):
            return False

        return self.external_id == other.external_id
