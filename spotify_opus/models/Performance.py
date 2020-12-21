from spotify_opus import db
from spotify_opus.models.Track import Track


class Performance(db.Model):
    __tablename__ = "performances"

    performance_id = db.Column(db.Integer, primary_key=True)
    tracks = db.relationship(Track, backref="performance", lazy="joined")
    work_id = db.Column(db.Integer, db.ForeignKey("works.work_id"), nullable=False)


