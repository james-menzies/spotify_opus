from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject


class Composer(ContextObject):
    __tablename__ = "composers"
    composer_id = db.Column(db.Integer, db.ForeignKey(
        "context_objects.context_id"), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "artists.artist_id"), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    death_year = db.Column(db.Integer, nullable=True)
    biography = db.Column(db.String(), nullable=True)
    country = db.Column(db.String(), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "composer"
    }
