from spotify_opus import db
from spotify_opus.models.Track import Track


class Performance(db.Model):
    __tablename__ = "performances"

    performance_id = db.Column(db.Integer, primary_key=True)
    tracks = db.relationship(Track, backref="performance", lazy="joined")
    work_id = db.Column(
        db.Integer, db.ForeignKey("works.work_id"), nullable=False)
    album_id = db.Column(db.String, db.ForeignKey(
        "albums.album_id"), nullable=False)

    def __eq__(self, other):
        if not isinstance(other, Performance):
            return False

        return self.work == other.work and \
            self.album_id == other.album_id

    def __repr__(self):
        return f"<Performance: Work - {self.work_id}, Album - {self.album_id}>"
