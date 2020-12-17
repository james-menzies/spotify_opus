from sqlalchemy import ForeignKey

from spotify_opus import db
from spotify_opus.models.Composer import Composer
from spotify_opus.models.ContextObject import ContextObject


class Artist(ContextObject):
    __tablename__ = "artists"
    artist_id = db.Column(db.Integer(), ForeignKey(
        "context_objects.context_id"), primary_key=True)
    external_id = db.Column(db.String(), nullable=False, unique=True)
    composer = db.relationship(
        Composer, backref="artist", uselist=False,
        foreign_keys=[Composer.artist_id],
        lazy="raise")

    __mapper_args__ = {
        "polymorphic_identity": "artist"
    }

    def __repr__(self) -> str:
        return f"<Artist: {self.name}>"

    def __eq__(self, other) -> bool:

        if not isinstance(other, Artist):
            return False

        return self.external_id == other.external_id
